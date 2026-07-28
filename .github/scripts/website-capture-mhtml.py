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

async def save_mhtml(url: str, output_path: str):
    browser = await launch(headless=True, args=['--no-sandbox'])
    try:
        page = await browser.newPage()
        # Use 'load' instead of 'networkidle0' to avoid Prezi timeout
        await page.goto(url, waitUntil='load', timeout=120000)
        # Extra wait for lazy content
        await page.waitForTimeout(5000)
        mhtml_data = await page._client.send('Page.captureSnapshot', {})
        with open(output_path, 'wb') as f:
            f.write(mhtml_data['data'].encode())
    finally:
        await browser.close()

def main():
    parser = argparse.ArgumentParser(description="Download a webpage as MHTML.")
    parser.add_argument("--url", required=True, help="URL of the page to download")
    parser.add_argument("--bundle", type=lambda x: (str(x).lower() == 'true'), default=False,
                        help="If true, save MHTML directly into website/ without per-URL zip")
    args = parser.parse_args()

    # Build a safe base name
    parsed = urlparse(args.url)
    path = parsed.path.strip('/').replace('/', '_')
    base_name = sanitize_filename(path or parsed.netloc) or "webpage"
    suffix = random_suffix()
    mhtml_filename = f"{base_name}-{suffix}.mhtml"

    output_dir = "website"
    os.makedirs(output_dir, exist_ok=True)

    # Temporary working dir (for zip creation if not bundle)
    temp_dir = "temp_mhtml"
    os.makedirs(temp_dir, exist_ok=True)
    mhtml_temp_path = os.path.join(temp_dir, mhtml_filename)

    print(f"Downloading {args.url} → {mhtml_filename}")
    try:
        asyncio.run(save_mhtml(args.url, mhtml_temp_path))
    except Exception as e:
        print(f"❌ Failed to capture {args.url}: {e}", file=sys.stderr)
        if os.path.exists(mhtml_temp_path):
            os.remove(mhtml_temp_path)
        return

    if args.bundle:
        # Move MHTML directly to website/
        final_path = os.path.join(output_dir, mhtml_filename)
        os.rename(mhtml_temp_path, final_path)
        print(f"✅ Saved MHTML to {final_path}")
    else:
        # Create a per‑URL ZIP
        zip_filename = f"{base_name}-{suffix}.zip"
        zip_path = os.path.join(output_dir, zip_filename)
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.write(mhtml_temp_path, arcname=mhtml_filename)
        os.remove(mhtml_temp_path)
        print(f"✅ Created {zip_path}")

if __name__ == "__main__":
    main()