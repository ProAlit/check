import os, sys, time, re, requests, json

URL = os.environ.get('FB_URL')
FMT = os.environ.get('FB_FMT')
QUAL = os.environ.get('FB_QUAL')
TMP_INFO = os.environ.get('TMP_INFO')
is_audio = FMT == 'mp3'

VALID_VIDEO_QUAL = ('360p','480p','720p','1080p','1440p','2160p')
VALID_AUDIO_QUAL = ('64kbps','128kbps','192kbps','320kbps')

if is_audio:
    QUAL = QUAL if QUAL in VALID_AUDIO_QUAL else '192kbps'
else:
    QUAL = QUAL if QUAL in VALID_VIDEO_QUAL else '720p'

payload = {
    "url": URL,
    "os": "linux",
    "output": {
        "type": "audio" if is_audio else "video",
        "format": FMT
    }
}
if is_audio:
    payload["audio"] = {"bitrate": QUAL}
else:
    payload["output"]["quality"] = QUAL

s = requests.Session()
# Simple Windows UA – no extra headers that trigger Cloudflare
s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

# Visit media. subdomain first to obtain necessary session cookies
s.get("https://media.ytmp3.gg/")

resp = s.post("https://hub.ytconvert.org/api/download", json=payload, timeout=30)
resp.raise_for_status()

data = resp.json()
status_url = data.get('statusUrl')
title = data.get('title', 'video')
dl_url = None

for _ in range(150):
    time.sleep(2)
    try:
        r = s.get(status_url, timeout=20)
        status = r.json()
        if status.get('status') == 'completed':
            dl_url = status.get('downloadUrl')
            break
        if status.get('status') == 'failed':
            print("::error::Server failed to prepare the video")
            sys.exit(1)
    except Exception:
        continue

if not dl_url:
    print("::error::Could not get download link after 5 minutes")
    sys.exit(1)

vid = re.search(r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})', URL)[1]
clean = re.sub(r'[^a-zA-Z0-9\-_()\[\]]', '_', title.replace(' ', '_'))
clean = re.sub(r'_+', '_', clean).strip('_')[:70] or vid
clean = clean.lstrip('-')
fname = f"{clean}_{vid}_{QUAL}.{FMT}"

with open(TMP_INFO, "w", encoding="utf-8") as f:
    json.dump({"url": dl_url, "filename": fname, "title": title}, f)
print(f"::notice::ytmp3.gg prepared: {fname}")