import asyncio
import zipfile
import os
import re
import sys
import argparse
import random
import string
from pyppeteer import launch
from urllib.parse import urlparse

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def random_suffix(length=5):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

async def save_mhtml(url: str, output_file: str):
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto(url, waitUntil='networkidle0')
    mhtml_data = await page._client.send('Page.captureSnapshot', {})
    with open(output_file, 'wb') as f:
        f.write(mhtml_data['data'].encode())
    await browser.close()

def main():
    parser = argparse.ArgumentParser(description="Download a webpage as MHTML.")
    parser.add_argument("--url", required=True, help="URL of the page to download")
    parser.add_argument("--title", help="Optional title for the output file (without extension)")
    args = parser.parse_args()

    if args.title:
        base_name = sanitize_filename(args.title)
    else:
        parsed = urlparse(args.url)
        path = parsed.path.strip('/').replace('/', '_')
        if path:
            base_name = sanitize_filename(path)
        else:
            base_name = sanitize_filename(parsed.netloc)
        if not base_name:
            base_name = "webpage"

    # Random 5-letter suffix to avoid filename conflicts
    base_name = f"{base_name}-{random_suffix()}"

    mhtml_filename = f"{base_name}.mhtml"
    zip_filename = f"{base_name}.zip"

    # All files go into 'website/' folder now
    output_dir = "website"
    os.makedirs(output_dir, exist_ok=True)

    os.makedirs("temp", exist_ok=True)
    mhtml_path = os.path.join("temp", mhtml_filename)

    print(f"Downloading {args.url} → {mhtml_filename}")
    asyncio.run(save_mhtml(args.url, mhtml_path))

    zip_path = os.path.join(output_dir, zip_filename)
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.write(mhtml_path, arcname=mhtml_filename)

    import shutil
    shutil.rmtree("temp", ignore_errors=True)

    print(f"✅ Created {zip_path} (contains {mhtml_filename})")

if __name__ == "__main__":
    main()