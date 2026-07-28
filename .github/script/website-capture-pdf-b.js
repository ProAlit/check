const { chromium } = require('playwright');
const fs = require('fs').promises;
const path = require('path');
const { execSync } = require('child_process');

// ── helpers ──────────────────────────────────────────────
function randomFiveLetters() {
  return Array.from({ length: 5 }, () =>
    String.fromCharCode(97 + Math.floor(Math.random() * 26))
  ).join('');
}

async function waitForStable(page) {
  await page.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {
    console.warn('Network idle timeout – continuing…');
  });
  await page.waitForTimeout(3000);
}

async function scrollToLoad(page) {
  await page.evaluate(async () => {
    await new Promise(resolve => {
      let totalHeight = 0;
      const distance = 300;
      const timer = setInterval(() => {
        window.scrollBy(0, distance);
        totalHeight += distance;
        if (totalHeight >= document.body.scrollHeight) {
          clearInterval(timer);
          resolve();
        }
      }, 200);
    });
  });
  await page.waitForTimeout(2000);
}

async function extractLinks(page) {
  return page.evaluate(() => {
    const links = Array.from(document.querySelectorAll('a[href]'))
      .map(a => a.href)
      .filter(href => href.startsWith('http'));
    const seen = new Set();
    return links
      .map(link => link.split('#')[0])
      .filter(link => {
        if (seen.has(link)) return false;
        seen.add(link);
        return true;
      });
  });
}

// ── argument parsing ─────────────────────────────────────
const args = process.argv.slice(2);
let inputUrl = null;
let bundle = false;                 // default false (per‑URL zip)

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--bundle' && i + 1 < args.length) {
    bundle = args[i + 1] === 'true';
    i++;                            // skip the value
  } else if (!inputUrl) {
    inputUrl = args[i];
  }
}

if (!inputUrl) {
  console.error('Usage: node script.js <URL> [--bundle true|false]');
  process.exit(1);
}

// ── main ─────────────────────────────────────────────────
(async () => {
  const MAX_LINKS = 500;
  const VIEWPORT = { width: 1280, height: 720 };
  const OUTPUT_DIR = 'website';                 // final destination
  await fs.mkdir(OUTPUT_DIR, { recursive: true });

  // Temporary working directory for intermediate files
  const TMP_DIR = 'tmp_pdf';
  await fs.mkdir(TMP_DIR, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: VIEWPORT,
    userAgent:
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  });

  let page; // Declared outside try so finally can access it

  try {
    page = await context.newPage();

    // 1. Capture main page
    await page.goto(inputUrl, { waitUntil: 'load', timeout: 30000 });
    await waitForStable(page);
    await scrollToLoad(page);

    const mainPdfPath = path.join(TMP_DIR, 'main.pdf');
    await page.pdf({
      path: mainPdfPath,
      fullPage: true,
      printBackground: true,
      margin: { top: '0px', bottom: '0px', left: '0px', right: '0px' }
    });

    // 2. Extract links
    const allLinks = await extractLinks(page);
    console.log(`Found ${allLinks.length} unique links.`);

    const limitedLinks = allLinks.slice(0, MAX_LINKS);
    if (allLinks.length > MAX_LINKS) {
      console.log(`(Trimmed to ${MAX_LINKS} for the list.)`);
    }

    // 3. Build link list HTML → PDF
    const listHtml = `<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Extracted URLs</title>
<style>
  body { font-family: monospace; margin: 50px; }
  a   { display: block; word-break: break-all; margin-bottom: 8px; }
</style></head>
<body>
<h1>Extracted URLs from ${inputUrl}</h1>
<ol>
${limitedLinks.map(link => `<li><a href="${link}">${link}</a></li>`).join('\n')}
</ol>
</body></html>`;

    const listPage = await context.newPage();
    await listPage.setContent(listHtml, { waitUntil: 'load' });
    await listPage.waitForTimeout(1000);
    const listPdfPath = path.join(TMP_DIR, 'list.pdf');
    await listPage.pdf({
      path: listPdfPath,
      fullPage: true,
      printBackground: true,
      margin: { top: '20px', bottom: '20px', left: '20px', right: '20px' }
    });
    await listPage.close();

    // 4. Merge with Ghostscript
    const mergedPdfPath = path.join(TMP_DIR, 'merged.pdf');
    execSync(
      `gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=${mergedPdfPath} ${mainPdfPath} ${listPdfPath}`,
      { stdio: 'inherit' }
    );

    // 5. Build final filename
    const hostname = new URL(inputUrl).hostname.replace(/^www\./, '');
    const randomPart = randomFiveLetters();
    const pdfFilename = `${hostname}-${randomPart}.pdf`;

    if (bundle) {
      // Bundle mode: place PDF directly into website/
      const destPath = path.join(OUTPUT_DIR, pdfFilename);
      await fs.rename(mergedPdfPath, destPath);
      console.log(`✅ Bundle mode – PDF saved to ${destPath}`);
    } else {
      // Non‑bundle mode: create a zip containing the PDF
      const finalPdfPath = path.join(TMP_DIR, pdfFilename);
      await fs.rename(mergedPdfPath, finalPdfPath);
      const zipFilename = `${hostname}-${randomPart}.zip`;
      const zipPath = path.join(OUTPUT_DIR, zipFilename);
      const zip = require('child_process').spawnSync('zip', [
        '-j', zipPath, finalPdfPath
      ]);
      if (zip.status !== 0) {
        console.error('Failed to create zip');
        process.exit(1);
      }
      // clean up the temporary renamed PDF
      await fs.unlink(finalPdfPath);
      console.log(`✅ Non‑bundle mode – per‑URL zip saved to ${zipPath}`);
    }

    // Clean up remaining temporary files
    const files = await fs.readdir(TMP_DIR);
    for (const file of files) {
      await fs.unlink(path.join(TMP_DIR, file));
    }
    await fs.rmdir(TMP_DIR);

  } catch (err) {
    console.error('❌ Error during PDF capture:', err);
    process.exit(1);
  } finally {
    if (page) await page.close().catch(() => {});  // Safe close
    await context.close();
    await browser.close();
  }
})();