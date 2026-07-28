import os
import sys
import time
import json
import re
import uuid
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

# ─── Configuration ─────────────────────────────
API_URL = "https://telegramdownloader.net/api.php"
# Use the exact headers from the working script to avoid 403 errors
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://telegramdownloader.net/",
    "Origin": "https://telegramdownloader.net",
    "Content-Type": "application/x-www-form-urlencoded",
}
MAX_RETRIES = 5
RETRY_DELAY = 10  # seconds

# ─── Helper Functions ──────────────────────────
def parse_links(raw_text):
    """Parse input string into a list of unique Telegram links."""
    text = raw_text.replace(',', '\n').replace(' ', '\n')
    lines = text.splitlines()
    links = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('http'):
            links.append(line)
        elif 't.me/' in line:
            links.append('https://' + line.lstrip('/'))
    
    # Remove duplicates while preserving order
    seen = set()
    unique_links = []
    for l in links:
        if l not in seen:
            seen.add(l)
            unique_links.append(l)
    
    if len(unique_links) > 1000:
        print(f"⚠️  More than 1000 links detected. Processing only first 1000.")
        unique_links = unique_links[:1000]
    
    print(f"✅ Parsed {len(unique_links)} unique link(s) to process.")
    return unique_links

def resolve_telegram_link(link, session):
    """Resolve a Telegram link via the API with robust retry logic."""
    for attempt in range(MAX_RETRIES):
        try:
            resp = session.post(API_URL, data={"telegram_link": link}, timeout=30)
            
            # Handle 403 Forbidden specifically
            if resp.status_code == 403:
                print(f"  ⚠️  Attempt {attempt+1}/{MAX_RETRIES}: Received 403 Forbidden. The API might be blocking this IP. Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
                continue
            
            # Check for Cloudflare or other non-JSON responses
            if resp.status_code != 200 or 'text/html' in resp.headers.get('content-type', ''):
                print(f"  ⚠️  Attempt {attempt+1}/{MAX_RETRIES}: Non-JSON response (status {resp.status_code}). Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
                continue
            
            result = resp.json()
            data = result.get('data', {}).get('data', {})
            direct_url = data.get('link')
            file_name = data.get('file_name')
            
            if not direct_url or not file_name:
                print(f"  ⚠️  Attempt {attempt+1}/{MAX_RETRIES}: Incomplete data from API. Retrying...")
                time.sleep(RETRY_DELAY)
                continue
            
            return direct_url, file_name
            
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, json.JSONDecodeError) as e:
            print(f"  ⚠️  Attempt {attempt+1}/{MAX_RETRIES}: {type(e).__name__} - {str(e)[:100]}. Retrying...")
            time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"  ⚠️  Unexpected error: {type(e).__name__} - {str(e)[:100]}")
            return None, None
    
    print(f"  ❌ Failed to resolve link after {MAX_RETRIES} attempts.")
    return None, None

def download_file(url, dest_path, session):
    """Download a file from the resolved URL."""
    try:
        # Ensure parent directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        resp = session.get(url, stream=True, timeout=60)
        resp.raise_for_status()
        
        total_size = int(resp.headers.get('content-length', 0))
        downloaded = 0
        
        with open(dest_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = downloaded / total_size * 100
                        bar_len = 40
                        filled = int(bar_len * downloaded / total_size)
                        bar = '█' * filled + '░' * (bar_len - filled)
                        print(f"\r  Progress: |{bar}| {percent:.1f}%", end='', flush=True)
        
        print()  # New line after progress bar
        return True, dest_path.stat().st_size
    except Exception as e:
        print(f"\n  ❌ Download error: {type(e).__name__} - {str(e)[:100]}")
        return False, 0

def sanitize_filename(name):
    """Ensure the filename is safe for all filesystems."""
    # If non-ASCII, generate a random ASCII name preserving extension
    if not name.isascii():
        ext = Path(name).suffix
        if not ext:
            ext = ".bin"
        return f"{uuid.uuid4().hex}{ext}"
    
    # Replace unsafe characters
    clean = re.sub(r'[^a-zA-Z0-9._-]', '_', name)
    clean = re.sub(r'__+', '_', clean)
    return clean

# ─── Main Processing ────────────────────────────
def main():
    # Get input from environment
    input_links = os.environ.get("TEL_LINKS", "").strip()
    if not input_links:
        print("❌ No links provided. Exiting.")
        sys.exit(1)
    
    links = parse_links(input_links)
    if not links:
        print("❌ No valid links found. Exiting.")
        sys.exit(1)
    
    # Prepare working directories
    WORK_DIR = Path("downloads_tmp")
    WORK_DIR.mkdir(exist_ok=True)
    
    failed_links_file = WORK_DIR / "failed_links.txt"
    # Clear previous failed links
    failed_links_file.write_text("")
    
    # Create a requests session with browser-like headers
    session = requests.Session()
    session.headers.update(HEADERS)
    
    # Process links with a thread pool
    results = []
    failed_count = 0
    success_count = 0
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_to_link = {}
        
        for link in links:
            future = executor.submit(resolve_telegram_link, link, session)
            future_to_link[future] = link
        
        for future in as_completed(future_to_link):
            link = future_to_link[future]
            print(f"\n{'='*50}")
            print(f"Processing: {link}")
            
            try:
                direct_url, file_name = future.result()
            except Exception as e:
                print(f"  ❌ Unexpected error resolving link: {e}")
                direct_url, file_name = None, None
            
            if not direct_url or not file_name:
                print(f"  ❌ Skipping link (resolution failed).")
                with open(failed_links_file, "a") as f:
                    f.write(f"{link}\n")
                failed_count += 1
                continue
            
            print(f"  Resolved filename: {file_name}")
            
            # Sanitize filename
            safe_name = sanitize_filename(file_name)
            dest_path = WORK_DIR / safe_name
            
            # Handle duplicate filenames
            counter = 1
            original_stem = dest_path.stem
            original_suffix = dest_path.suffix
            while dest_path.exists():
                dest_path = WORK_DIR / f"{original_stem}_{counter}{original_suffix}"
                counter += 1
            
            print(f"  Downloading to: {dest_path.name}")
            success, size = download_file(direct_url, dest_path, session)
            
            if success:
                print(f"  ✅ Successfully downloaded ({size / 1e6:.2f} MB)")
                results.append((dest_path, size))
                success_count += 1
            else:
                print(f"  ❌ Download failed.")
                with open(failed_links_file, "a") as f:
                    f.write(f"{link}\n")
                failed_count += 1
    
    # ─── Final Summary ──────────────────────────
    print(f"\n{'='*50}")
    print(f"📊 PROCESSING COMPLETE")
    print(f"   Total links processed: {len(links)}")
    print(f"   Successful downloads:  {success_count}")
    print(f"   Failed downloads:      {failed_count}")
    
    if failed_count > 0:
        print(f"   Failed links logged to: {failed_links_file}")
    
    if not results:
        print("❌ No files were downloaded. Exiting with error.")
        sys.exit(1)
    
    print("✅ Download step completed successfully.")

if __name__ == "__main__":
    main()