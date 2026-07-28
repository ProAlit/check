#!/usr/bin/env python3
"""
Python exit node — compatible with the TypeScript version.
Listens on 127.0.0.1:8181 and relays HTTP requests.
Authentication via pre‑shared key (PSK) passed as EXIT_NODE_PSK.
"""

import argparse
import base64
import http.server
import json
import logging
import os
import re
import socketserver
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("exit-node")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Headers that MUST be stripped before forwarding (match TypeScript version)
STRIP_HEADERS = frozenset(
    [
        "host",
        "connection",
        "content-length",
        "transfer-encoding",
        "proxy-connection",
        "proxy-authorization",
        "x-forwarded-for",
        "x-forwarded-host",
        "x-forwarded-proto",
        "x-forwarded-port",
        "x-real-ip",
        "forwarded",
        "via",
    ]
)

MAX_REQUEST_BODY = 32 * 1024 * 1024  # 32 MiB
MAX_RESPONSE_BODY = 64 * 1024 * 1024  # 64 MiB
OUTBOUND_TIMEOUT = 30

# Pre‑shared key – set at startup from environment or CLI
PSK = ""

# ---------------------------------------------------------------------------
# HTTP client – no redirects (matching `redirect: "manual"`)
# ---------------------------------------------------------------------------
_NO_REDIRECT_OPENER = urllib.request.OpenerDirector()
for _handler in (
    urllib.request.UnknownHandler(),
    urllib.request.HTTPDefaultErrorHandler(),
    urllib.request.HTTPErrorProcessor(),
    urllib.request.HTTPHandler(),
    urllib.request.HTTPSHandler(),
):
    _NO_REDIRECT_OPENER.add_handler(_handler)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def sanitize_headers(raw: object) -> dict[str, str]:
    """Return a clean header dict, removing hop‑by‑hop and proxy headers."""
    if not isinstance(raw, dict):
        return {}
    out: dict[str, str] = {}
    for k, v in raw.items():
        if not k or not isinstance(k, str):
            continue
        if k.lower() in STRIP_HEADERS:
            continue
        out[k] = str(v) if v is not None else ""
    return out


def is_loop(own_host: str, target_url: str) -> bool:
    """Return True if target_url points back at this exit node."""
    try:
        own = urlparse(f"//{own_host}")
        dst = urlparse(target_url)
        return own.hostname == dst.hostname
    except Exception:
        return False


def collect_headers(raw_headers) -> dict:
    """Collect response headers, preserving duplicates (e.g. Set‑Cookie)."""
    out: dict = {}
    key_map: dict[str, str] = {}  # lowercase → canonical case
    for k, v in raw_headers.items():
        kl = k.lower()
        if kl not in key_map:
            key_map[kl] = k
            out[k] = v
        else:
            canonical = key_map[kl]
            cur = out[canonical]
            if isinstance(cur, list):
                cur.append(v)
            else:
                out[canonical] = [cur, v]
    return out


def relay_request(url: str, method: str, headers: dict, body: bytes) -> dict:
    """Perform the outbound HTTP request and return a relay JSON dict."""
    req = urllib.request.Request(url, method=method, headers=headers)
    if body:
        req.data = body

    try:
        with _NO_REDIRECT_OPENER.open(req, timeout=OUTBOUND_TIMEOUT) as resp:
            data = resp.read(MAX_RESPONSE_BODY)
            return {
                "s": resp.status,
                "h": collect_headers(resp.headers),
                "b": base64.b64encode(data).decode(),
            }
    except urllib.error.HTTPError as exc:
        data = exc.read(MAX_RESPONSE_BODY) if exc.fp else b""
        return {
            "s": exc.code,
            "h": collect_headers(exc.headers) if exc.headers else {},
            "b": base64.b64encode(data).decode(),
        }


# ---------------------------------------------------------------------------
# HTTP Request Handler
# ---------------------------------------------------------------------------
class ExitNodeHandler(http.server.BaseHTTPRequestHandler):
    """Handles incoming relay requests and the health‑check endpoint."""

    # Suppress default access logs – we log ourselves
    def log_message(self, fmt, *args):
        pass

    def _send_json(self, status: int, obj: dict) -> None:
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        """Health‑check endpoint."""
        self._send_json(
            200,
            {
                "ok": True,
                "status": "healthy",
                "message": "VPS exit node is running (Python).",
                "usage": "Send POST with relay payload to proxy requests.",
            },
        )

    def do_POST(self):
        """Relay endpoint."""
        content_length = int(self.headers.get("Content-Length") or 0)
        if content_length <= 0:
            self._send_json(400, {"e": "empty_body"})
            return
        if content_length > MAX_REQUEST_BODY:
            self._send_json(413, {"e": "request_too_large"})
            return

        raw = self.rfile.read(content_length)
        try:
            body = json.loads(raw)
        except Exception:
            self._send_json(400, {"e": "bad_json"})
            return

        if not isinstance(body, dict):
            self._send_json(400, {"e": "bad_json"})
            return

        # Extract parameters
        k = str(body.get("k") or "")
        u = str(body.get("u") or "")
        m = str(body.get("m") or "GET").upper()
        h = sanitize_headers(body.get("h"))
        b64 = body.get("b")

        # PSK check
        if not PSK:
            self._send_json(500, {"e": "server_psk_missing"})
            return
        if k != PSK:
            log.warning("Rejected unauthorized request from %s", self.client_address[0])
            self._send_json(401, {"e": "unauthorized"})
            return

        # URL validation
        if not re.match(r"^https?://", u, re.IGNORECASE):
            self._send_json(400, {"e": "bad_url"})
            return

        # Loop guard
        own_host = self.headers.get("Host") or ""
        if is_loop(own_host, u):
            log.warning("Loop refused: target %s is this exit node", u)
            self._send_json(400, {"e": "exit-node loop refused"})
            return

        # Decode body
        payload_bytes = b""
        if isinstance(b64, str) and b64:
            try:
                payload_bytes = base64.b64decode(b64)
            except Exception:
                self._send_json(400, {"e": "bad_base64"})
                return

        # Relay the request
        log.info("Relaying %s %s", m, u[:100])
        try:
            result = relay_request(u, m, h, payload_bytes)
        except Exception as exc:
            log.warning("Relay error for %s: %s", u[:80], exc)
            self._send_json(500, {"e": str(exc) or type(exc).__name__})
            return

        log.info(
            "Relay OK %s → HTTP %d (%d B)",
            u[:80],
            result["s"],
            len(result.get("b", "")),
        )
        self._send_json(200, result)


# ---------------------------------------------------------------------------
# Threaded HTTP server
# ---------------------------------------------------------------------------
class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Python exit node (TypeScript compatible)")
    parser.add_argument("--host", default="127.0.0.1", help="Listen IP (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8181, help="Listen port (default: 8181)")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity",
    )
    parser.add_argument("--psk", default="", help="Pre‑shared key (overrides env)")
    args = parser.parse_args()

    logging.getLogger().setLevel(args.log_level)

    global PSK
    # PSK can come from --psk flag or EXIT_NODE_PSK environment variable
    PSK = args.psk.strip() or os.environ.get("EXIT_NODE_PSK", "").strip()
    if not PSK:
        log.error(
            "No PSK configured. Set EXIT_NODE_PSK environment variable or pass --psk."
        )
        sys.exit(1)

    server = ThreadedHTTPServer((args.host, args.port), ExitNodeHandler)
    log.info("VPS exit node listening on http://%s:%d", args.host, args.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("Shutting down.")
        server.shutdown()


if __name__ == "__main__":
    main()