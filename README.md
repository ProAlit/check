<p align="center">
  <h1 align="center">🌐 aio‑downloader</h1>
  <p align="center"><strong>All‑in‑One GitHub Actions Downloader — بدون فیلتر · بدون تحریم</strong></p>
</p>

<p align="center">
  ⭐ <strong>اگر این پروژه برایتان مفید است، لطفاً ستاره بدهید — به دیگران کمک می‌کند پیدایش کنند!</strong> ⭐
</p>

---

## ⚠️ اعلامیه مهم برای کاربرانی که قبلاً فورک کرده‌اند (حتماً بخوانید)

> **مخزن اصلی** (`ProAlit/aio-downloader`) به‌طور مداوم به‌روزرسانی می‌شود — رفع باگ‌ها، ویژگی‌های جدید، و بهبود امنیت. **فورک شما به‌صورت خودکار این به‌روزرسانی‌ها را دریافت نمی‌کند!**

### ✅ مشکل push و پوشه — کاملاً برطرف شد
در نسخه‌های قدیمی‌تر، برخی workflowها هنگام push با خطا مواجه می‌شدند یا فایل‌ها در مسیر اشتباه قرار می‌گرفتند. این مشکل اکنون به‌طور کامل حل شده است:
- تمام workflowها از `persist-credentials: true` استفاده می‌کنند
- قبل از هر push، یک `git pull --rebase --autostash` اجرا می‌شود تا تداخلی پیش نیاید
- حلقه‌ی تلاش مجدد ۵ مرحله‌ای برای push وجود دارد
- پوشه‌های خروجی با `mkdir -p` ساخته می‌شوند
- حجم بافر git به ۵۰۰ مگابایت افزایش یافته (`http.postBuffer`)

> **اگر همچنان مشکلی دیدید، ابتدا فورک خود را به‌روز کنید (پایین را ببینید) — به احتمال زیاد فورک‌تان قدیمی است.**

---

### 🔄 همگام‌سازی فورک — فقط با خودِ وبسایت GitHub (بدون گیت)

> ❗ **این کار را انجام دهید تا آخرین اصلاحات و امکانات را دریافت کنید.**

#### ⚠️ نکته بسیار مهم: نمی‌توانید Pull Request باز کنید
اگر در فورک خود تغییری commit کرده باشید (حتی ویرایش `channels.json`)، فورک شما از مخزن اصلی «جلوتر» می‌افتد و دیگر به‌روزرسانی دریافت نمی‌کند. **تنها راه، دور انداختن commitهای خودتان و همگام‌سازی کامل است.**

#### روش (فقط در وبسایت GitHub):

1. به صفحه فورک خود بروید (مثلاً `github.com/your-username/aio-downloader`)
2. بالای لیست فایل‌ها، روی دکمه‌ای که نوشته **«Sync fork»** کلیک کنید.
3. در منوی بازشده، اگر commit اضافی ندارید، گزینه **«Update branch»** را بزنید.
4. **اگر commit اضافی دارید** (مثلاً فایل‌ها را ویرایش کرده‌اید)، به جای Update branch، گزینه **«Discard commits»** (دور انداختن commitها) را انتخاب کنید. این کار فورک شما را دقیقاً با مخزن اصلی یکسان می‌کند.

> ⚠️ با Discard commits تمام تغییرات خود را از دست می‌دهید. اگر فایل مهمی دارید، اول دانلودش کنید.

**پس از آن، فورک شما کاملاً به‌روز شده و آخرین رفع‌ها و قابلیت‌ها را دارد.** توصیه می‌کنیم حداقل هفته‌ای یک‌بار این کار را انجام دهید.

---

## 📚 فهرست مطالب

1. [پیشنیازها](#-پیشنیازها)
2. [فورک و راهاندازی اولیه](#-فورک-و-راهاندازی-اولیه)
3. [راهنمای جامع تمام Secretها و Tokenهای مورد نیاز](#-راهنمای-جامع-تمام-secretها-و-tokenهای-مورد-نیاز)
   - [نحوه استخراج کوکی (Cookie) با روش robots.txt](#۱-نحوه-استخراج-کوکی-cookie-با-روش-robotstxt-توصیه-اصلی)
   - [کوکی یوتیوب (YOUTUBE_COOKIES)](#۲-کوکی-یوتیوب-youtube_cookies)
   - [کوکی اینستاگرام (INSTAGRAM_COOKIES)](#۳-کوکی-اینستاگرام-instagram_cookies)
   - [کوکی X/توییتر (X_COOKIES)](#۴-کوکی-xتوییتر-x_cookies)
   - [کلید احراز هویت تونل (TUNNEL_AUTH_KEY)](#۵-کلید-احراز-هویت-تونل-tunnel_auth_key)
   - [توکن استاتیک Cloudflare (CF_TUNNEL_TOKEN)](#۶-توکن-استاتیک-cloudflare-cf_tunnel_token)
   - [آپلود در Google Drive (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN)](#۷-آپلود-در-google-drive-google_client_id-google_client_secret-google_refresh_token)
   - [کانفیگ خروجی Skirk (SKIRK_EXIT_CONFIG)](#۸-کانفیگ-خروجی-skirk-skirk_exit_config)
   - [کانفیگ WireGuard (WG_CONFIG)](#۹-کانفیگ-wireguard-wg_config)
4. [راهنمای کامل هر گردش کار (Workflow)](#-راهنمای-کامل-هر-گردش-کار-workflow)
   - [۱. دانلودر یوتیوب (downloader-youtube)](#۱-دانلودر-یوتیوب-downloader-youtube)
   - [۲. دانلودر اینستاگرام (downloader-instagram)](#۲-دانلودر-اینستاگرام-downloader-instagram)
   - [۳. دانلودر X/توییتر (downloader-x)](#۳-دانلودر-xتوییتر-downloader-x)
   - [۴. دانلودر مستقیم (downloader-direct)](#۴-دانلودر-مستقیم-downloader-direct)
   - [۵. آرشیو کانال تلگرام (fetcher-telegram)](#۵-آرشیو-کانال-تلگرام-fetcher-telegram)
   - [۶. دانلودر تلگرام بتا (downloader-telegram-beta)](#۶-دانلودر-تلگرام-بتا-downloader-telegram-beta)
   - [۷. ضبط وبسایت - PDF و MHTML (fetcher-website)](#۷-ضبط-وبسایت---pdf-و-mhtml-fetcher-website)
   - [۸. لیچر قدرتمند (aio-leecher)](#۸-لیچر-قدرتمند-aio-leecher)
   - [۹. دانلودر ساندکلود (downloader-soundcloud)](#۹-دانلودر-ساندکلود-downloader-soundcloud)
   - [۱۰. دانلودر اسپاتیفای (downloader-spotify)](#۱۰-دانلودر-اسپاتیفای-downloader-spotify)
   - [۱۱. پاککننده جامع (aio-cleaner)](#۱۱-پاککننده-جامع-aio-cleaner)
   - [۱۲. دانلودر گوگل پلی (downloader-google-play)](#۱۲-دانلودر-گوگل-پلی-downloader-google-play)
   - [۱۳. دانلودر MEGA.nz (downloader-mega-nz)](#۱۳-دانلودر-meganz-downloader-mega-nz)
   - [۱۴. Exit Node پایتون - داینامیک (python-mhrv-dynamic-exit-node)](#۱۴-exit-node-پایتون---داینامیک-python-mhrv-dynamic-exit-node)
   - [۱۵. Exit Node پایتون - استاتیک (python-mhrv-static-exit-node)](#۱۵-exit-node-پایتون---استاتیک-python-mhrv-static-exit-node)
   - [۱۶. Exit Node Zyrln - داینامیک (zyrln-cloudflare-dynamic-exit-node)](#۱۶-exit-node-zyrln---داینامیک-zyrln-cloudflare-dynamic-exit-node)
   - [۱۷. Exit Node Zyrln - استاتیک (zyrln-cloudflare-static-exit-node)](#۱۷-exit-node-zyrln---استاتیک-zyrln-cloudflare-static-exit-node)
   - [۱۸. Exit Node Rust - استاتیک (mhrv-rust-static-exit-node)](#۱۸-exit-node-rust---استاتیک-mhrv-rust-static-exit-node)
   - [۱۹. Skirk Exit Node (skirk-vps)](#۱۹-skirk-exit-node-skirk-vps)
5. [🌐 راهنمای تانل WireGuard (اختیاری برای تمام Workflowها)](#-راهنمای-تانل-wireguard-اختیاری-برای-تمام-workflowها)
6. [ویژگیهای جدید (که در README قبلی نیستند)](#-ویژگیهای-جدید-که-در-readme-قبلی-نیستند)
7. [مشکل کندی checkout و راهحل آن](#-مشکل-کندی-checkout-و-راهحل-آن)
8. [محدودیتها و هشدارهای مهم](#-محدودیتها-و-هشدارهای-مهم)
9. [پشتیبانی](#-پشتیبانی)
10. [فایل zoomusers.md چیست](#فایل-zoomusers.md-چیست)

---

## ⚠️ پیشنیازها

| نیاز | توضیح |
|---|---|
| **حساب GitHub** | رایگان — همین کافیست |
| **مرورگر + افزونه Get cookies.txt LOCALLY** | Chrome / Firefox / Edge |
| **حساب اینستاگرام** | (اختیاری) برای استوری و محتوای خصوصی |
| **حساب X (توییتر)** | **الزامی** برای دانلودر X |
| **حساب Google Cloud** | (اختیاری) برای آپلود خودکار در Google Drive و Skirk Exit Node |
| **حساب Cloudflare** | (اختیاری) برای Exit Nodeهای استاتیک |
| **حساب ProtonVPN (رایگان)** | (اختیاری) برای تغییر IP خروجی با WireGuard |
| **تلگرام، ضبط وبسایت، گوگل پلی، MEGA** | هیچ چیز اضافی نیاز ندارند |

---

## 🚀 فورک و راهاندازی اولیه

### مرحله ۱: فورک کردن
روی دکمه **Fork** در بالای صفحه کلیک کنید.

### مرحله ۲: فعالسازی Actions
1. به تنظیمات بروید: **Settings** → **Actions** → **General**
2. **Actions permissions**: گزینه **Allow all actions and reusable workflows**
3. **Workflow permissions**: گزینه **Read and write permissions**
4. ذخیره کنید.

> ⚠️ **اگر دسترسی نوشتن ندهید، آپلود فایلها با خطا مواجه میشود!**

### مرحله ۳: پاکسازی اولیه (اکیداً توصیه میشود)
مخزن فورکشده شامل فایلهای رسانهای از مخزن اصلی است. برای شروع تمیز، به **Actions** → **aio-cleaner** بروید، **Clean ALL platforms** را تیک بزنید و اجرا کنید.

### مرحله ۴: تنظیم Secretها
با توجه به نیاز خود، Secretهای مورد نظر را تنظیم کنید (راهنمای کامل در بخش بعدی).

---

## 🔐 راهنمای جامع تمام Secretها و Tokenهای مورد نیاز

در این بخش، **تکتک Secretهایی که هر Workflow نیاز دارد** به همراه **آموزش گامبهگام و تصویری** برای دریافت آنها توضیح داده شده است. هر Secret در بخش Workflow مربوطه نیز ذکر شده است.

---

### ۱. نحوه استخراج کوکی (Cookie) با روش robots.txt (توصیه اصلی)

> ⭐ **روش جدید و بهتر:** به جای رفتن به صفحه اصلی سایت، از آدرس `https://website.com/robots.txt` کوکی导出 کنید. این روش **نرخ موفقیت بالاتری** دارد زیرا robots.txt یک فایل ساده و سبک است و درخواستهای مشکوک کمتری روی آن اعمال میشود.

<div dir="ltr" markdown="1">

#### 📝 مراحل استخراج کوکی:

</div>

1. یک پنجره **Private/Incognito** در مرورگر خود باز کنید.
2. افزونه **Get cookies.txt LOCALLY** را نصب کنید (از فروشگاه افزونه مرورگرتان).
3. به آدرس زیر بروید (بسته به سرویس مورد نظر):

<div dir="ltr" markdown="1">

+++
https://www.youtube.com/robots.txt
https://www.instagram.com/robots.txt
https://x.com/robots.txt
+++

</div>

4. روی آیکون افزونه کلیک کنید → **Export** (فرمت Netscape) → فایل txt را ذخیره کنید.
5. **پنجره خصوصی را کاملاً ببندید** (این کار نشست را میبندد ولی کوکی معتبر میماند).

> **چرا robots.txt بهتر است؟** robots.txt یک فایل متنی ساده است که هیچ محتوای سنگین یا اسکریپتهای امنیتی ندارد. در نتیجه:
> - کوکیهای دریافتی «تمیزتر» هستند
> - احتمال trigger شدن سیستمهای ضد-ربات کمتر است
> - نشست شما معتبرتر باقی میماند

> **چرا پنجره ناشناس؟** اگر در پنجره عادی لاگاوت کنید، کوکیها بیاعتبار میشوند. با بستن پنجره ناشناس، نشست بسته میشود ولی کوکی معتبر میماند.

> ⚠️ **نشانههای خرابی کوکی:** خطای `Sign in to confirm you're not a bot` (یوتیوب)، خطای `429 Too Many Requests` (اینستاگرام)، یا دانلود موفق ولی بدون فایل خروجی. راه حل: کوکی جدید از پنجره ناشناس بگیرید و Secret را بهروز کنید.

---

### ۲. کوکی یوتیوب (YOUTUBE_COOKIES)

<div dir="ltr" markdown="1">

**Secret Name:** `YOUTUBE_COOKIES`
**وضعیت:** اختیاری (اما بهشدت توصیه میشود)
**مورد استفاده در:** downloader-youtube, aio-leecher

</div>

#### 📝 مراحل:
1. پنجره Private باز کنید.
2. به `https://www.youtube.com/robots.txt` بروید.
3. **وارد اکانت گوگل خود شوید** (حتماً در همان پنجره ناشناس).
4. افزونه Get cookies.txt LOCALLY را باز کرده و Export بزنید.
5. محتوای فایل txt را کپی کنید.
6. به **Settings** → **Secrets and variables** → **Actions** بروید.
7. **New repository secret** بزنید.
8. نام: `YOUTUBE_COOKIES` | مقدار: محتوای فایل txt را بچسبانید.
9. پنجره ناشناس را ببندید.

---

### ۳. کوکی اینستاگرام (INSTAGRAM_COOKIES)

<div dir="ltr" markdown="1">

**Secret Name:** `INSTAGRAM_COOKIES`
**وضعیت:** اختیاری (برای استوری و محتوای خصوصی الزامی)
**مورد استفاده در:** downloader-instagram, aio-leecher

</div>

#### 📝 مراحل:
1. پنجره Private باز کنید.
2. به `https://www.instagram.com/robots.txt` بروید.
3. **وارد اکانت اینستاگرام خود شوید** (حتماً در همان پنجره ناشناس).
4. افزونه را باز کرده و Export بزنید.
5. Secret با نام `INSTAGRAM_COOKIES` بسازید و محتوای فایل را بچسبانید.
6. پنجره ناشناس را ببندید.

---

### ۴. کوکی X/توییتر (X_COOKIES)

<div dir="ltr" markdown="1">

**Secret Name:** `X_COOKIES`
**وضعیت:** **الزامی** ⚠️
**مورد استفاده در:** downloader-x, aio-leecher

</div>

#### 📝 مراحل:
1. پنجره Private باز کنید.
2. به `https://x.com/robots.txt` بروید.
3. **وارد اکانت X شوید** (حتماً در همان پنجره ناشناس).
4. افزونه را باز کرده و Export بزنید.
5. Secret با نام `X_COOKIES` بسازید.
6. پنجره ناشناس را ببندید.

> ⚠️ بدون کوکی X، دانلودر X اصلاً کار نمیکند!

---

### ۵. کلید احراز هویت تونل (TUNNEL_AUTH_KEY)

<div dir="ltr" markdown="1">

**Secret Name:** `TUNNEL_AUTH_KEY`
**وضعیت:** اختیاری
**مورد استفاده در:** python-mhrv-dynamic-exit-node, python-mhrv-static-exit-node, zyrln-cloudflare-dynamic-exit-node, zyrln-cloudflare-static-exit-node, mhrv-rust-static-exit-node

</div>

#### 📝 مراحل:
1. یک رمز عبور قوی (Pre-Shared Key) انتخاب کنید (مثلاً ترکیبی از حروف و اعداد حداقل ۱۶ کاراکتری).
2. به **Settings** → **Secrets and variables** → **Actions** بروید.
3. Secret با نام `TUNNEL_AUTH_KEY` بسازید و رمز خود را وارد کنید.
4. همین رمز را در کانفیگ VPN خود (فیلد `psk`) نیز قرار دهید.

> ⚠️ این رمز باید دقیقاً با `psk` در `config.json` پروژه VPN شما یکی باشد. URL و PSK را کنار هم منتشر نکنید.

---

### ۶. توکن استاتیک Cloudflare (CF_TUNNEL_TOKEN)

<div dir="ltr" markdown="1">

**Secret Name:** `CF_TUNNEL_TOKEN`
**وضعیت:** اختیاری (فقط برای Exit Nodeهای استاتیک)
**مورد استفاده در:** python-mhrv-static-exit-node, zyrln-cloudflare-static-exit-node, mhrv-rust-static-exit-node

</div>

#### 📝 مراحل:
1. به [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/) بروید.
2. **Access** → **Tunnels** → **Create a tunnel**.
3. نام دلخواه بدهید و **Save** کنید.
4. نوع اتصال را **Cloudflared** انتخاب کنید.
5. دستور نمایش داده شده شامل توکن است. توکن را کپی کنید.
6. Secret با نام `CF_TUNNEL_TOKEN` بسازید و توکن را بچسبانید.

> ℹ️ این Secret فقط برای Exit Nodeهای **استاتیک** (با دامنه ثابت) نیاز است. برای Exit Nodeهای داینامیک (با آدرس trycloudflare.com موقت)، نیازی به این توکن نیست.

---

### ۷. آپلود در Google Drive (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN)

<div dir="ltr" markdown="1">

**Secret Names:** `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`
**وضعیت:** کاملاً اختیاری
**مورد استفاده در:** تمام workflowهایی که گزینه `upload_to_drive` دارند (downloader-youtube, downloader-instagram, downloader-direct, fetcher-website, aio-leecher, downloader-soundcloud, downloader-spotify, downloader-google-play, downloader-mega-nz)

</div>

این ویژگی جدید به شما امکان میدهد فایلهای دانلودی را **مستقیماً در Google Drive خود** (در پوشه `github-actions`) ذخیره کنید، بدون اینکه فضای مخزن GitHub را اشغال کنید!

#### 📝 مراحل گام به گام:
> با تشکر از کاربران و زحماتشون اگه مشکلی داشتید میتونید از این لینک راهنمای نوشته شده توسط یکی از کاربران رو بخونید و انجام بدید و سوالی بود در اون قسمت مطرح کنید برای این موضوع - [کلیک کنید](https://github.com/ProAlit/aio-downloader/discussions/79)

<div dir="ltr" markdown="1">

**قسمت اول: ایجاد پروژه در Google Cloud Console**

</div>

1. به [Google Cloud Console](https://console.cloud.google.com/) بروید.
2. یک پروژه جدید بسازید (یا پروژه موجود را انتخاب کنید).
3. **APIs & Services** → **Library**.
4. **Google Drive API** را جستجو و **Enable** کنید.

<div dir="ltr" markdown="1">

**قسمت دوم: ایجاد OAuth Client ID**

</div>

5. **APIs & Services** → **Credentials**.
6. **Create Credentials** → **OAuth client ID**.
7. نوع اپلیکیشن را **Web application** انتخاب کنید (حتی اگر برای استفاده شخصی است).
8. نام دلخواه بدهید.
9. در بخش **Authorized redirect URIs**، روی **ADD URI** کلیک کنید و آدرس زیر را وارد کنید:

<div dir="ltr" markdown="1">

+++
https://developers.google.com/oauthplayground
+++

</div>

10. روی **Create** کلیک کنید.
11. **Client ID** و **Client Secret** نمایش داده میشود. آنها را کپی کنید.
12. Secretهای زیر را در GitHub بسازید:

<div dir="ltr" markdown="1">

+++
GOOGLE_CLIENT_ID → Client ID خود را بچسبانید
GOOGLE_CLIENT_SECRET → Client Secret خود را بچسبانید
+++

</div>

<div dir="ltr" markdown="1">

**⚠️  قسمت دوم-الف: انتشار برنامه (Publish) — حیاتی!**

</div>

اگر این مرحله را انجام ندهید، در قسمت سوم (مرحله ۱۶) با خطای **403** یا **400** مواجه میشوید.

13. به صفحه [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent) بروید.
14. اگر برنامه شما در حالت **Testing** قرار دارد (با نوار زرد رنگ)، روی دکمه‌ای که زیر **"In production"** نیست کلیک کنید (معمولاً **PUBLISH APP**). در تأییدیه، **Confirm** را بزنید.
15. وضعیت باید به **"In production"** تغییر کند. (لازم نیست برنامه توسط گوگل تأیید شود؛ برای استفاده شخصی کافیست.)

<div dir="ltr" markdown="1">

**قسمت سوم: دریافت Refresh Token با OAuth Playground**

</div>

16. به [Google OAuth Playground](https://developers.google.com/oauthplayground/) بروید.
17. روی آیکون ⚙️ (تنظیمات) کلیک کنید.
18. تیک **Use your own OAuth credentials** را بزنید.
19. Client ID و Client Secret خود را وارد کنید و **Close** کنید.
20. در **Step 1**، در بخش **Drive API v3**، scope زیر را انتخاب کنید:

<div dir="ltr" markdown="1">

+++
https://www.googleapis.com/auth/drive
+++

</div>

21. روی **Authorize APIs** کلیک کنید و اجازه دسترسی بدهید. (اگر خطای redirect_uri_mismatch گرفتید، مطمئن شوید Authorized redirect URIs شامل آدرس Playground است.)
22. در **Step 2**، تیک **Auto-refresh the token before it expires** را بزنید.
23. روی **Exchange authorization code for tokens** کلیک کنید.
24. **Refresh token** نمایش داده میشود. آن را کپی کنید.
25. Secret زیر را در GitHub بسازید:

<div dir="ltr" markdown="1">

+++
GOOGLE_REFRESH_TOKEN → Refresh Token خود را بچسبانید
+++

</div>

> ⚠️ **نکته مهم:** Refresh Token فقط **یک بار** نمایش داده میشود. اگر آن را گم کنید، باید دوباره از اول مراحل را طی کنید. همچنین اگر از OAuth Playground استفاده میکنید، حتماً تیک Auto-refresh را بزنید.

> ℹ️ پس از تنظیم هر سه Secret، در هر workflow که اجرا میکنید، کافیست گزینه **upload_to_drive** را تیک بزنید تا فایلها به جای مخزن GitHub، در Google Drive شما (پوشه `github-actions`) ذخیره شوند.

---

<div dir="rtl" markdown="1">

### ۸. کانفیگ خروجی Skirk (SKIRK_EXIT_CONFIG)

<div dir="ltr" markdown="1">

**Secret Name:** `SKIRK_EXIT_CONFIG`
**وضعیت:** **الزامی** برای Skirk Exit Node
**مورد استفاده در:** skirk-vps

</div>

این Secret قلب گردش‌کار `skirk-vps` است. محتوای آن **تمام اطلاعات موجود در فایل `exit.json`** می‌باشد که یک بار برای همیشه تولید می‌شود.  
فایل `exit.json` حاوی یک Refresh Token دائمی گوگل و شناسه صندوق دریافتی Drive است و تا زمانی که اپلیکیشن OAuth شما در وضعیت **In production** باشد، هرگز منقضی نمی‌شود.

این راهنما تمام مراحل را از **صفر** و بدون ارجاع به بخش‌های دیگر توضیح می‌دهد. برای راحتی شما، تمام گام‌ها به‌صورت مرحله‌بهمرحله و مستقل نوشته شده‌اند.

---

#### 🛠️ گام صفر – پیش‌نیازها

- یک **حساب Google** (جیمیل معمولی کافی است)
- یک **مخزن GitHub** (همان که گردش‌کارهای aio‑downloader را در آن فعال کرده‌اید)
- یک **مرورگر وب** روی سیستم خودتان

---

#### 🧩 گام اول – ساخت پروژه و فعال‌سازی Google Drive API

1. به [کنسول Google Cloud](https://console.cloud.google.com/) بروید.
2. یک پروژه جدید بسازید (در صورت نداشتن پروژه، روی منوی کشویی بالای صفحه کلیک کرده و **New Project** را انتخاب کنید).
3. پس از ورود به پروژه، از منوی سمت چپ به **APIs & Services** → **Library** بروید.
4. عبارت «Google Drive API» را جستجو کنید.
5. وارد صفحه آن شده و روی دکمه **Enable** کلیک کنید. (اگر از قبل فعال است، چیزی تغییر ندهید.)

---

#### ⚖️ گام دوم – تنظیم صفحه رضایت OAuth و انتشار برنامه (Publish)

این مرحله تضمین می‌کند که Refresh Token شما پس از ۷ روز منقضی نشود و برای همیشه معتبر بماند.

1. در کنسول Google Cloud، از منوی سمت چپ به **APIs & Services** → **OAuth consent screen** بروید.
2. نوع کاربر (User Type) را **External** انتخاب کنید و روی **Create** کلیک کنید.
3. در صفحه اطلاعات برنامه، فقط این فیلدها را پر کنید:
   - **App name**: `Skirk Exit` (هر نام دلخواه)
   - **User support email**: ایمیل خودتان
   - **Developer contact email**: ایمیل خودتان  
   (بقیه فیلدها را خالی بگذارید)
4. روی **Save and Continue** کلیک کنید.
5. در بخش **Scopes** چیزی اضافه نکنید و فقط **Save and Continue** را بزنید.
6. در بخش **Test users**، روی **Add Users** کلیک کنید و ایمیل خود را وارد کنید. سپس **Save and Continue** را بزنید.
7. **اکنون در همان صفحه OAuth consent screen**، به دنبال بخش **Publishing status** بگردید. اگر دکمه **PUBLISH APP** را می‌بینید (معمولاً زیر نوار زرد رنگ Testing)، روی آن کلیک کنید و در پنجره تأیید، **Confirm** را بزنید.
8. وضعیت باید به **In production** تغییر کند. (نگران هشدار "Verification" نباشید – برنامه شما فقط برای استفاده شخصی است.)

---

#### 🧬 گام سوم – ساخت OAuth Client ID از نوع Desktop

1. در کنسول Google Cloud، از منوی سمت چپ به **Credentials** بروید.
2. روی **Create Credentials** کلیک کرده و **OAuth client ID** را انتخاب کنید.
3. **Application type** را **Desktop app** قرار دهید.
4. **Name**: یک نام ساده مثل `Skirk Exit Desktop` بدهید.
5. **مهم:** در قسمت **Authorized redirect URIs**، مقدار `http://localhost` را وارد کنید و روی **Add URI** کلیک کنید. (اگر یک پورت هم خواست، مثلاً `http://localhost:8080` مشکلی ندارد، اما `http://localhost` کافیست.)
6. روی **Create** کلیک کنید.
7. یک پنجره باز می‌شود که **Client ID** و **Client Secret** را نمایش می‌دهد. هر دو را در یک جای امن کپی کنید (مثلاً یک فایل متنی موقت). در گام‌های بعدی به آنها نیاز دارید.

---

#### 💻 گام چهارم – ورود به GitHub Codespaces

1. به صفحه مخزن فورک‌شده خود در GitHub بروید.
2. روی دکمه سبز **Code** کلیک کنید، سپس تب **Codespaces** را باز کنید.
3. روی **Create codespace on main** کلیک کنید.
4. صبر کنید تا محیط بارگذاری شود (حدود ۱ دقیقه). شما یک ترمینال لینوکسی آنلاین در مرورگر خود خواهید داشت.

---

#### ⚙️ گام پنجم – نصب Skirk در ترمینال Codespaces

در ترمینال Codespaces (اگر باز نشد، کلیدهای **Ctrl+Shift+`** را فشار دهید)، دستور زیر را اجرا کنید:

<div dir="ltr" markdown="1">

+++
curl -fsSL https://raw.githubusercontent.com/ShahabSL/Skirk/main/install.sh | sh
+++

</div>

پس از پایان نصب، با زدن دستور `skirk --version` می‌توانید از نصب موفق مطمئن شوید.

---

#### 🧪 گام ششم – اجرای دستور راه‌اندازی OAuth و ورود به حساب گوگل

حال باید دستور راه‌اندازی را با Client ID و Client Secret خود اجرا کنید. در ترمینال Codespaces دستور زیر را عیناً کپی کنید و **فقط بخش‌های `CLIENT_ID` و `CLIENT_SECRET` را با مقادیر واقعی خود جایگزین کنید** (به‌دقت، بدون تغییر گیومه‌ها):

<div dir="ltr" markdown="1">

+++
skirk setup init \
  --out skirk-kit \
  --reset-google-login \
  --oauth-mode personal \
  --oauth-client-id "CLIENT_ID" \
  --oauth-client-secret "CLIENT_SECRET"
+++

</div>

پس از اجرا، دستور یک URL طولانی چاپ می‌کند.  
**Ctrl+Click** روی این URL کنید تا در مرورگر عادی سیستم خودتان باز شود.

- مرورگر شما صفحه ورود گوگل را نشان می‌دهد. **حتماً همان اکانتی را انتخاب کنید که در Test users اضافه کرده‌اید**.
- پس از اجازه دادن، گوگل شما را به آدرسی مثل `http://localhost/?code=4/0AanRRr...` هدایت می‌کند.  
  (ممکن است مرورگر خطای «اتصال برقرار نشد» نشان دهد – این طبیعی است، چون هیچ سروری روی لوکال‌هاست شما اجرا نمی‌شود.)

**کاری که باید انجام دهید:**
- نوار آدرس مرورگر را کامل **کپی** کنید.  
- به ترمینال Codespaces برگردید و این آدرس را به‌صورت کامل **پیست** کنید (دقت کنید که تمام آن، شامل `code=...` را کپی کرده باشید).  
- سپس **Enter** بزنید.

دستور راه‌اندازی به‌طور خودکار کد را از آدرس استخراج کرده و کار را ادامه می‌دهد.

پس از چند ثانیه، در ترمینال پیام «Setup completed» و نمایش فایل‌های تولید شده را می‌بینید.

---

#### 📥 گام هفتم – دانلود فایل‌های مورد نیاز

در پنل سمت چپ Codespaces، یک فایل‌اکسپلورر وجود دارد. وارد پوشه `skirk-kit` شوید.  
دو فایل حیاتی در اینجا قرار دارند:

- **`exit.json`** → برای Secret `SKIRK_EXIT_CONFIG` لازم است.
- **`client.skirk`** → برای استفاده از پروکسی روی سیستم شخصی شما (اختیاری اما مهم).

**روش دانلود:**
- روی `exit.json` راست‌کلیک کنید و **Download** را انتخاب کنید. فایل روی سیستم شما ذخیره می‌شود.
- همین کار را برای `client.skirk` نیز انجام دهید.

> ⚠️ این دو فایل، **کلید ورود به حساب گوگل و سرویس خروجی شما هستند**. آنها را در جای امن نگه دارید و هرگز به‌صورت عمومی به اشتراک نگذارید.

---

#### ☁️ گام هشتم – ذخیره Secret در GitHub

1. فایل `exit.json` را با یک ویرایشگر متن (مثل Notepad) باز کنید.
2. **همه** محتوای آن (شامل آکولادهای `{` و `}`) را کپی کنید.
3. در مرورگر، به مخزن GitHub خود بروید: **Settings** → **Secrets and variables** → **Actions**.
4. روی **New repository secret** کلیک کنید.
5. **Name** را `SKIRK_EXIT_CONFIG` و **Value** را محتوای کپی‌شده قرار دهید.
6. روی **Add secret** کلیک کنید.

> ℹ️ فایل `client.skirk` را فعلاً جایی امن نگه دارید. بعداً برای اتصال از سیستم شخصی (با `skirk serve-client`) از آن استفاده خواهید کرد.

---

#### 🧹 گام نهم – پاکسازی و ایمن‌سازی مخزن

**این مرحله فوق‌العاده مهم است!** از آنجایی که شما فایل‌های حساس را در محیط Codespaces تولید کرده‌اید، نباید هیچ ردپایی از آنها در مخزن باقی بماند. برای این کار:

1. در ترمینال Codespaces، دستورهای زیر را به ترتیب اجرا کنید:

<div dir="ltr" markdown="1">

+++
cd ~/workspace/your-repo-name   # مسیر دقیق با توجه به نام مخزن‌تان (معمولاً به‌طور خودکار آنجا هستید)
rm -rf skirk-kit
git add -A
git commit -m "Remove temporary Skirk configuration files"
git push
+++

</div>

(اگر نام مخزن یا مسیر دقیق را نمی‌دانید، با دستور `pwd` بررسی کنید. معمولاً پیش‌فرض Codespaces شما را در `/workspaces/نام-مخزن` قرار می‌دهد.)

این کار پوشه `skirk-kit` را به‌طور کامل از مخزن حذف کرده و تغییر را ثبت (push) می‌کند.

2. اکنون می‌توانید Codespace را ببندید و حذف کنید:  
   از گوشه پایین–چپ روی نام Codespace کلیک کنید و **Delete Codespace** را انتخاب کنید.

اکنون مخزن شما کاملاً تمیز است و هیچ فایل حساسی در آن وجود ندارد. تنها یک Secret رمزنگاری‌شده با نام `SKIRK_EXIT_CONFIG` دارید که برای اجرای `skirk-vps` کافیست.

---

#### 🧠 نکات تکمیلی

- **Refresh Token دائمی است**، مگر اینکه OAuth App را دوباره به حالت Testing برگردانید یا دسترسی برنامه را از حساب گوگل لغو کنید.
- **اگر نیاز به ساخت مجدد `exit.json` دارید**، کافیست گام‌های ۴ تا ۹ را دوباره انجام دهید و Secret را با فایل جدید به‌روز کنید.
- **فایل `client.skirk`** را می‌توانید روی لپ‌تاپ یا گوشی خود نگه دارید. با نصب Skirk روی سیستم شخصی و اجرای `skirk serve-client --config client.skirk` یک پروکسی SOCKS5 روی `127.0.0.1:1080` خواهید داشت که تمام ترافیک را از طریق Exit Node گیت‌هاب (و در صورت تمایل VPN) عبور می‌دهد.

</div>

#### 🛠️ مراحل یکباره تولید `exit.json` و افزودن به Secret

**پیش‌نیاز:** یک پروژه Google Cloud با **Google Drive API** فعال و یک OAuth Client ID از نوع **Desktop app** (مراحل ۱ تا ۷ از بخش Google Drive را انجام دهید، اما نیازی به Web application و redirect URI نیست — **Desktop app** کافیست). همچنین برنامه را **Publish** کنید (مرحله ۱۳ تا ۱۵ بالا).

**مرحله ۱: باز کردن GitHub Codespaces**
1. به مخزن خود بروید.
2. روی دکمه سبز **Code** کلیک کنید → تب **Codespaces** → **Create codespace on main**.
3. صبر کنید تا محیط آماده شود (حدود ۱ دقیقه).

**مرحله ۲: نصب Skirk در ترمینال Codespaces**
در ترمینال (اگر باز نیست، Ctrl+Shift+` را بفشارید) دستور زیر را اجرا کنید:

<div dir="ltr" markdown="1">

+++
curl -fsSL https://raw.githubusercontent.com/ShahabSL/Skirk/main/install.sh | sh
+++

</div>

**مرحله ۳: اجرای تنظیمات OAuth**
دستور زیر را با جایگزین کردن `CLIENT_ID` و `CLIENT_SECRET` خود (از Google Cloud) اجرا کنید:

<div dir="ltr" markdown="1">

+++
skirk setup init \
  --out skirk-kit \
  --reset-google-login \
  --oauth-mode personal \
  --oauth-client-id "CLIENT_ID" \
  --oauth-client-secret "CLIENT_SECRET"
+++

</div>

**مرحله ۴: ورود به حساب Google**
- دستور یک URL چاپ می‌کند. روی آن Ctrl+Click کنید (در مرورگر عادی باز می‌شود).
- وارد حساب Google خود شوید و اجازه دسترسی بدهید.
- کد Authorization نمایش داده شده را **کپی** کنید و در ترمینال Codespaces بچسبانید (Enter بزنید).
- پس از پایان، پوشه `skirk-kit` با فایل `exit.json` ایجاد می‌شود.

**مرحله ۵: دانلود فایل `exit.json`**
- در پنل فایل‌ها (سمت چپ Codespaces) وارد پوشه `skirk-kit` شوید.
- روی `exit.json` راست‌کلیک کرده و **Download** را بزنید.
- فایل را در جای امن ذخیره کنید. ⚠️ این فایل را **هرگز** در مخزن Commit نکنید!

**مرحله ۶: ذخیره در Secret**
- فایل `exit.json` را با یک ویرایشگر متن باز کنید و **همه محتویات آن را کپی** کنید.
- در مخزن GitHub به **Settings** → **Secrets and variables** → **Actions** بروید.
- **New repository secret** با نام `SKIRK_EXIT_CONFIG` بسازید و محتوا را بچسبانید.
- پس از اطمینان از ذخیره، Codespace را حذف کنید (گوشه پایین-چپ **Codespaces** → **Delete Codespace**).

> ℹ️ این عملیات فقط **یک بار** نیاز است. فایل `exit.json` یک Refresh Token دائمی دارد (به شرطی که OAuth App را Publish کرده باشید) و نیازی به تمدید ندارد.

---

### ۹. کانفیگ WireGuard (WG_CONFIG)

<div dir="ltr" markdown="1">

**Secret Name:** `WG_CONFIG`
**وضعیت:** کاملاً اختیاری (فقط در صورت تمایل به تغییر IP خروجی)
**مورد استفاده در:** تمام workflowهای دارای گزینه `vpn_enabled` (aio-leecher، تمام Exit Nodeها، skirk-vps)

</div>

این Secret شامل **کل محتوای فایل کانفیگ WireGuard** (از ProtonVPN یا هر سرویس‌دهنده دیگر) به صورت متن ساده است.

#### 📝 مراحل دریافت کانفیگ رایگان از ProtonVPN:

1. یک حساب رایگان در [ProtonVPN](https://protonvpn.com) بسازید (بدون کارت اعتباری).
2. پس از ورود، به [Account → OpenVPN / IKEv2 username](https://account.protonvpn.com/) بروید (بله، بخش WireGuard هم همانجاست).
3. زیر **WireGuard configuration**، یک کلید جدید بسازید و **سرور رایگان** (مثلاً Netherlands, Japan, US) و پروتکل WireGuard را انتخاب کنید.
4. فایل `.conf` را دانلود کنید. محتوای آن شبیه زیر است:

<div dir="ltr" markdown="1">

+++
[Interface]
PrivateKey = ...
Address = 10.2.0.2/32
DNS = 10.2.0.1

[Peer]
PublicKey = ...
AllowedIPs = 0.0.0.0/0
Endpoint = 185.159.158.146:51820
+++

</div>

5. **همه خطوط را کپی** کرده و به عنوان یک Secret جدید با نام `WG_CONFIG` در مخزن ذخیره کنید (Settings → Secrets → Actions → New secret).

> ⚠️ کانفیگ را دقیقاً همانطور که هست (با Line Break) بچسبانید. DNS داخل آن برای جلوگیری از نشت DNS ضروری است.

> ℹ️ اگر می‌خواهید IP خروجی آلمان یا کشور دیگری باشد، می‌توانید با نسخه پولی ProtonVPN یا هر سرویس WireGuard دیگر این کار را انجام دهید. در صورت عدم نیاز، این Secret را ایجاد نکنید.

---

## 📋 راهنمای کامل هر گردش کار (Workflow)

در این بخش، **تمامی ۱۹ گردش کار** به همراه **Secretهای مورد نیاز هر کدام**، **نحوه استفاده**، و **نکات مهم** توضیح داده شده است.

---

### ۱. دانلودر یوتیوب (downloader-youtube)

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** `YOUTUBE_COOKIES` (اختیاری، توصیه میشود)
**Secretهای Google Drive:** `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` (اختیاری)
**زمان اجرا:** حداکثر ۷۰۰ دقیقه

</div>

#### ✨ ویژگیها:
- تلاش با شبیهسازی کلاینت اندروید، iOS، و بدون کوکی
- در صورت شکست، از ابزارهای جایگزین مانند pytube، سرویسهای API خارجی و youtube‑dl استفاده میکند
- پشتیبانی از لینکهای غیر یوتیوب (دانلود مستقیم با wget)
- انتخاب هوشمند نزدیکترین کیفیت موجود
- Remux خودکار با ffmpeg برای سازگاری کامل
- تقسیم خودکار فایلهای >۹۹MB به ZIP چندبخشی
- **🆕 آپلود خودکار در Google Drive**

#### 📝 نحوه استفاده:
1. **Actions** → **downloader-youtube** → **Run workflow**
2. ورودی: `URL v/a رزولوشن fps` (fps اختیاری)

<div dir="ltr" markdown="1">

+++
https://www.youtube.com/watch?v=dfdXGw1xY9A v 480
https://www.youtube.com/watch?v=dfdXGw1xY9A v 1080 60
https://www.youtube.com/watch?v=VIDEO_ID a max
https://www.youtube.com/watch?v=VIDEO_ID v 4k
+++

</div>

- `v` = ویدیو، `a` = صدا
- رزولوشن: `max`, `min`, `1080`, `2k`, `4k` و …
- FPS: اختیاری (مثلاً `60`)
- اگر `v/a` ندهید، پیشفرض **حداکثر کیفیت ویدیو** انتخاب میشود.
- برای صدا (`a max`) خروجی به صورت `.opus` است.

3. **🆕 گزینههای جدید:**
   - `output_format`: انتخاب فرمت خروجی (mp4 یا mp3)
   - `video_quality`: حداکثر رزولوشن (4K, 1080, 720, 480, 360, best)
   - `audio_quality`: بیتریت صدا (320, 192, 128, 64)
   - `bundle_all`: تجمیع همه فایلها در یک ZIP
   - `upload_as_release`: آپلود به عنوان GitHub Release
   - `upload_to_drive`: **🆕 آپلود در Google Drive** (به جای مخزن)

4. خروجی در پوشه `youtube/` (فایلهای بزرگ به ZIP چندبخشی تبدیل میشوند)

---

### ۲. دانلودر اینستاگرام (downloader-instagram)

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** `INSTAGRAM_COOKIES` (اختیاری)
**Secretهای Google Drive:** `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` (اختیاری)

</div>

#### 📝 نحوه استفاده:
1. **Actions** → **downloader-instagram** → **Run workflow**
2. لینکها را با کاما، فاصله یا خط جدید جدا کنید.

<div dir="ltr" markdown="1">

+++
https://www.instagram.com/p/DX2y7oLDFOb/,
https://www.instagram.com/reel/DVRXhn0gjL3/,
https://www.instagram.com/p/DX6US4uCNGb/
+++

</div>

3. **🆕 گزینههای جدید:**
   - `upload_as_release`: آپلود به عنوان GitHub Release
   - `upload_to_drive`: **🆕 آپلود در Google Drive**

4. خروجی ZIP در پوشه `instagram/`.

> ⚠️ خطای ۴۲۹ یعنی کوکی اینستاگرام منقضی یا محدود شده — کوکی جدید بگیرید.

---

### ۳. دانلودر X/توییتر (downloader-x)

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** `X_COOKIES` (**الزامی** ⚠️)

</div>

#### 📝 نحوه استفاده:
1. **Actions** → **downloader-x** → **Run workflow**
2. لینکها را با کاما، فاصله یا خط جدید وارد کنید.

<div dir="ltr" markdown="1">

+++
https://x.com/username/status/123456789,
https://x.com/otheruser/status/987654321
+++

</div>

3. خروجی ZIP در پوشه `x/`.

---

### ۴. دانلودر مستقیم (downloader-direct)

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** هیچکدام الزامی نیست
**Secretهای Google Drive:** `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` (اختیاری)

</div>

#### ✨ ویژگیها:
- دانلود با `aria2c` (۱۶ اتصال همزمان — بسیار سریع)
- پشتیبانی از تمام لینکهای مستقیم (`.zip`, `.mp4`, `.apk`, `.pdf` و …)

#### 📝 نحوه استفاده:
1. **Actions** → **downloader-direct** → **Run workflow**
2. لینکهای مستقیم را بچسبانید.

<div dir="ltr" markdown="1">

+++
https://example.com/file.zip, https://example.com/video.mp4
+++

</div>

3. **🆕 گزینههای جدید:**
   - `bundle_all`: تجمیع همه فایلها در یک ZIP
   - `upload_as_release`: آپلود به عنوان GitHub Release
   - `upload_to_drive`: **🆕 آپلود در Google Drive**

4. فایلها در `direct/` ذخیره میشوند (بزرگتر از ۹۹MB به ZIP چندبخشی تقسیم میشوند).

---

### ۵. آرشیو کانال تلگرام (fetcher-telegram)

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** هیچکدام
**اجرای خودکار:** هر ۳۰ دقیقه یکبار (cron)

</div>

#### 📝 نحوه استفاده:
1. فایل `telegram/channels.json` را ویرایش کنید. **نام کانال را بدون @ وارد کنید.**

<div dir="ltr" markdown="1">

+++
["VahidOOnLine", "mwarmonitor", "channelname"]
+++

</div>

2. **Actions** → **fetcher-telegram** → **Run workflow** (یا منتظر اجرای خودکار بمانید).

> ⚠️ فقط کانالهای عمومی. زمانبندی خودکار ممکن است با تأخیر ۱ تا ۶ ساعت اجرا شود.

---

### ۶. دانلودر تلگرام بتا (downloader-telegram-beta)

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** هیچکدام
**محدودیت:** حداکثر ۱۰۰۰ لینک

</div>

#### 📝 نحوه استفاده:
1. **Actions** → **downloader-telegram-beta** → **Run workflow**
2. لینک پستهای تلگرام را وارد کنید.

<div dir="ltr" markdown="1">

+++
https://t.me/channelname/123, https://t.me/channelname/456
+++

</div>

3. فایلها در `telegram/downloader/` ذخیره میشوند.

---

### ۷. ضبط وبسایت — PDF و MHTML (fetcher-website)

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** هیچکدام
**Secretهای Google Drive:** `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` (اختیاری)
**محدودیت:** حداکثر ۵۰۰ لینک داخلی، مهلت ۳۰ دقیقه

</div>

#### ✨ ویژگیها:
- **PDF** با کیفیت بالا (مناسب برای چاپ و آرشیو)
- **MHTML** (بایگانی کامل صفحه شامل تصاویر، CSS و فونتها — قابل باز شدن در مرورگر)
- رندر با **Playwright + Chromium** برای صفحات داینامیک

#### 📝 نحوه استفاده:
1. **Actions** → **fetcher-website** → **Run workflow**
2. آدرس کامل با `https://` را وارد کنید.

<div dir="ltr" markdown="1">

+++
https://example.com/article
https://github.com/ProAlit/aio-downloader
+++

</div>

3. **🆕 گزینههای جدید:**
   - `capture_mhtml`: ذخیره به صورت MHTML (پیشفرض: فعال)
   - `capture_pdf`: ذخیره به صورت PDF (پیشفرض: فعال)
   - `upload_as_release`: آپلود به عنوان GitHub Release
   - `upload_to_drive`: **🆕 آپلود در Google Drive**

4. خروجیها در پوشه `website/` — هم فایل PDF و هم فایل MHTML.

> ⚠️ فقط سایتهای عمومی. صفحات SPA سنگین ممکن است کامل رندر نشوند.

---

### ۸. لیچر قدرتمند (aio-leecher)

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** `YOUTUBE_COOKIES`, `INSTAGRAM_COOKIES`, `X_COOKIES` (همگی اختیاری، خودکار تشخیص داده میشوند)
**Secretهای Google Drive:** `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` (اختیاری)
**زمان اجرا:** حداکثر ۷۰۰ دقیقه
**قابلیت تانل WireGuard:** دارد (گزینه `vpn_enabled`)

</div>

**قدرتمندترین بخش!** از یوتیوب و اینستاگرام تا تیکتاک، ساندکلاد، اسپاتیفای و بیش از ۱۸۰۰ سایت دیگر.

#### ⚡ حالت خام (Raw) — توصیه اصلی
برای بهترین نتیجه، **حتماً از حالت خام استفاده کنید.** کافیست بعد از لینک، دو خط فاصله `--` بگذارید و سپس هر آرگومان معتبر `yt-dlp` را بنویسید.

<div dir="ltr" markdown="1">

+++
https://www.youtube.com/watch?v=VIDEO_ID -- --format "bestvideo[height<=1080]+bestaudio/best[height<=1080]" --merge-output-format mkv
https://www.tiktok.com/@user/video/ID -- --write-subs --sub-lang en
# یوتیوب با زیرنویس
https://www.youtube.com/watch?v=ID -- -f "bestvideo[height<=1080]+bestaudio" --write-subs --sub-lang en --merge-output-format mp4
# اینستاگرام
https://www.instagram.com/p/CODE -- --format best
# توییتر
https://x.com/user/status/ID -- --format best
# پینترست
https://www.pinterest.com/pin/ID -- --format best
# ساندکلاد
https://soundcloud.com/artist/track -- --format bestaudio
+++

</div>

#### حالت میانبر
هنوز هم میتوانید از `v` (ویدیو) و `a` (صدا) استفاده کنید، ولی برای محتوایی که ویدیو/صدا/موسیقی نیست، نرخ شکست بالایی دارد.

<div dir="ltr" markdown="1">

+++
https://www.youtube.com/watch?v=dfdXGw1xY9A v 1080
https://soundcloud.com/artist/track a 320
+++

</div>

#### ❓ اگر دستور بلد نیستید
از چتباتهای هوش مصنوعی مثل **[chat.deepseek.com](https://chat.deepseek.com)** (بدون فیلتر) بپرسید: *"یک دستور yt‑dlp برای دانلود این لینک با بهترین کیفیت بنویس"* — دستور تولید شده را در حالت خام استفاده کنید.

#### 🆕 گزینههای جدید:
- `bundle_all`: تجمیع همه فایلها در یک ZIP
- `upload_as_release`: آپلود به عنوان GitHub Release
- `upload_to_drive`: **🆕 آپلود در Google Drive**
- **`vpn_enabled`**: فعال‌سازی WireGuard VPN برای عبور از محدودیت‌های جغرافیایی (نیاز به Secret `WG_CONFIG`)

---

### ۹. دانلودر ساندکلود (downloader-soundcloud)

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** هیچکدام
**Secretهای Google Drive:** `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` (اختیاری)

</div>

#### 📝 نحوه استفاده:
1. **Actions** → **downloader-soundcloud** → **Run workflow**
2. لینکها را وارد کنید.

<div dir="ltr" markdown="1">

+++
https://soundcloud.com/artist/track,
https://soundcloud.com/artist/track
+++

</div>

3. **🆕 گزینههای جدید:**
   - `output_format`: فرمت خروجی (mp3, flac, ogg, opus, m4a, wav)
   - `audio_quality`: کیفیت صدا (128k, 192k, 256k, 320k)
   - `upload_as_release`: آپلود به عنوان GitHub Release
   - `upload_to_drive`: **🆕 آپلود در Google Drive**

4. فایلها در `music/` (تبدیل خودکار با ffmpeg).

---

### ۱۰. دانلودر اسپاتیفای (downloader-spotify) 🆕

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** هیچکدام (SpotiFLAC بدون نیاز به اکانت کار میکند)
**Secretهای Google Drive:** `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` (اختیاری)
**سرویسهای پشتیبانیشده:** Spotify, Tidal, Apple Music, SoundCloud, YouTube, Pandora

</div>

> ℹ️ این دانلودر از **SpotiFLAC** استفاده میکند که بدون نیاز به هیچ اکانتی، موسیقی را با بهترین کیفیت ممکن (از جمله FLAC بدون اتلاف) دانلود میکند.

#### 📝 نحوه استفاده:
1. **Actions** → **downloader-spotify** → **Run workflow**
2. لینکها را وارد کنید (ترک، آلبوم، پلیلیست، آرتیست).

<div dir="ltr" markdown="1">

+++
https://open.spotify.com/track/xxxxx,
https://open.spotify.com/album/xxxxx,
https://open.spotify.com/playlist/xxxxx
+++

</div>

3. **گزینهها:**
   - `output_format`: فرمت خروجی (flac, mp3, m4a, ogg, opus, wav) — پیشفرض: flac
   - `audio_quality`: کیفیت (LOSSLESS, HI_RES_LOSSLESS, DOLBY_ATMOS, HIGH, LOW, 320k, 256k, 192k, 128k) — پیشفرض: LOSSLESS
   - `upload_as_release`: آپلود به عنوان GitHub Release
   - `upload_to_drive`: **🆕 آپلود در Google Drive**

4. فایلها در `music/` ذخیره میشوند.

---

### ۱۱. پاککننده جامع (aio-cleaner)

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** هیچکدام

</div>

> ⚠️ فضای مخزن رایگان GitHub حدود ۵ گیگابایت است. فایلهای حجیم فضا را پر میکنند — **مرتب پاکسازی کنید.**

#### 📝 پلتفرمهای قابل پاک شدن:

| پلتفرم | چه چیزهایی حذف میشود |
|---|---|
| تلگرام | `telegram/content/`، `telegram.md`، `last_ids.json` |
| تلگرام دانلودر | `telegram/downloader/` |
| یوتیوب | کل `youtube/` |
| اینستاگرام | کل `instagram/` |
| X | کل `x/` |
| وبسایت | کل `website/` |
| لیچر | کل `leecher/` |
| گوگل پلی | کل `google-play/` |
| موسیقی | کل `music/` |
| مستقیم | کل `direct/` |
| MEGA | کل `mega-nz/` 🆕 |

#### 📝 نحوه اجرا:
1. **Actions** → **aio-cleaner** → **Run workflow**
2. چکباکسهای دلخواه را تیک بزنید (یا **Clean ALL platforms**)
3. اجرا کنید.

> ❗ حذف دائمی است — ابتدا فایلهای مهم را دانلود کنید. **حتما بعد هر آپدیت مرحله کلینر رو برای همه اجرا کنید وگرنه دانلودهاتون به شدت کند انجام میشه!!**

---

### ۱۲. دانلودر گوگل پلی (downloader-google-play)

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** هیچکدام (احراز هویت خودکار)
**Secretهای Google Drive:** `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` (اختیاری)

</div>

#### 📝 نحوه استفاده:
1. **Actions** → **downloader-google-play** → **Run workflow**
2. **app**: نام پکیج (مثلاً `com.google.android.youtube`) یا لینک گوگل پلی.
3. **architecture**: `arm64` (پیشفرض) یا `armv7`.
4. **merge_splits**: ادغام APKهای چندبخشی (پیشفرض فعال).

<div dir="ltr" markdown="1">

+++
app: com.spotify.music
architecture: arm64
merge_splits: true
+++

</div>

5. **🆕 گزینههای جدید:**
   - `bundle_all`: تجمیع همه APKها در یک ZIP
   - `upload_as_release`: آپلود به عنوان GitHub Release
   - `upload_to_drive`: **🆕 آپلود در Google Drive**

6. فایل APK (زیپشده) در `google-play/`.

> ℹ️ برای پیدا کردن نام پکیج، به لینک برنامه در گوگل پلی دقت کنید: `id=com.example.app`.

---

### ۱۳. دانلودر MEGA.nz (downloader-mega-nz) 🆕

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** هیچکدام (بدون نیاز به اکانت MEGA)
**Secretهای Google Drive:** `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` (اختیاری)

</div>

#### ✨ ویژگیها:
- دانلود فایل و فولدر از MEGA.nz بدون نیاز به اکانت
- استفاده از megatools برای دانلود مطمئن
- پشتیبانی از لینکهای فایل و فولدر

#### 📝 نحوه استفاده:
1. **Actions** → **downloader-mega-nz** → **Run workflow**
2. لینکهای MEGA را وارد کنید.

<div dir="ltr" markdown="1">

+++
https://mega.nz/file/xxxxx,
https://mega.nz/folder/xxxxx
+++

</div>

3. **گزینهها:**
   - `bundle_all`: تجمیع همه فایلها در یک ZIP
   - `upload_method`: روش آپلود (`split_push` یا `release`)
   - `upload_to_drive`: **🆕 آپلود در Google Drive**

4. فایلها در `mega-nz/` ذخیره میشوند.

---

### ۱۴. Exit Node پایتون — داینامیک (python-mhrv-dynamic-exit-node)

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** `TUNNEL_AUTH_KEY` (اختیاری)
**Secretهای WireGuard:** `WG_CONFIG` (اختیاری)
**خروجی:** URL موقت trycloudflare.com (اعتبار ۶ ساعت)
**قابلیت تانل WireGuard:** دارد (گزینه `vpn_enabled`)

</div>

#### 📝 نحوه استفاده:
1. **Actions** → **python-mhrv-dynamic-exit-node** → **Run workflow**
2. پس از ۲۰-۳۰ ثانیه در لاگ، خطی شبیه زیر میبینید:

<div dir="ltr" markdown="1">

+++
https://random-name.trycloudflare.com
+++

</div>

3. این URL را کپی و در بخش `exit_node` کانفیگ VPN خود قرار دهید:

<div dir="ltr" markdown="1">

+++
"exit_node": {
  "enabled": true,
  "provider": "vps",
  "url": "https://random-name.trycloudflare.com",
  "psk": "همان_رمز_مخفی"
}
+++

</div>

> ⏱️ اعتبار هر URL تا ۶ ساعت است. بعداً باید دوباره اجرا کنید.

---

### ۱۵. Exit Node پایتون — استاتیک (python-mhrv-static-exit-node) 🆕

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** `TUNNEL_AUTH_KEY` (اختیاری), `CF_TUNNEL_TOKEN` (الزامی ⚠️)
**Secretهای WireGuard:** `WG_CONFIG` (اختیاری)
**خروجی:** دامنه ثابت Cloudflare (مثلاً `exit.yourdomain.com`)
**قابلیت تانل WireGuard:** دارد (گزینه `vpn_enabled`)

</div>

#### 📝 نحوه استفاده:
1. ابتدا `CF_TUNNEL_TOKEN` را تنظیم کنید (راهنما در بخش Secretها).
2. **Actions** → **python-mhrv-static-exit-node** → **Run workflow**
3. تونل روی دامنه ثابت شما فعال میشود.

> ℹ️ مزیت این روش نسبت به داینامیک: URL ثابت است و نیازی به بهروزرسانی مداوم کانفیگ نیست.

---

### ۱۶. Exit Node Zyrln — داینامیک (zyrln-cloudflare-dynamic-exit-node) 🆕

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** `TUNNEL_AUTH_KEY` (اختیاری)
**Secretهای WireGuard:** `WG_CONFIG` (اختیاری)
**زبان برنامهنویسی:** Go (عملکرد سریعتر)
**خروجی:** URL موقت trycloudflare.com (اعتبار ۶ ساعت)
**قابلیت تانل WireGuard:** دارد (گزینه `vpn_enabled`)

</div>

#### 📝 نحوه استفاده:
1. **Actions** → **zyrln-cloudflare-dynamic-exit-node** → **Run workflow**
2. URL موقت در لاگ نمایش داده میشود.
3. مانند روش پایتون، URL را در کانفیگ VPN خود قرار دهید.

> ℹ️ این نسخه با زبان Go نوشته شده و برای کاربرانی که به دنبال عملکرد سریعتر و مصرف کمتر هستند مناسب است.

---

### ۱۷. Exit Node Zyrln — استاتیک (zyrln-cloudflare-static-exit-node) 🆕

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** `TUNNEL_AUTH_KEY` (اختیاری), `CF_TUNNEL_TOKEN` (الزامی ⚠️)
**Secretهای WireGuard:** `WG_CONFIG` (اختیاری)
**زبان برنامهنویسی:** Go
**قابلیت تانل WireGuard:** دارد (گزینه `vpn_enabled`)

</div>

#### 📝 نحوه استفاده:
1. `CF_TUNNEL_TOKEN` را تنظیم کنید.
2. **Actions** → **zyrln-cloudflare-static-exit-node** → **Run workflow**
3. تونل روی دامنه ثابت Cloudflare شما فعال میشود.

---

### ۱۸. Exit Node Rust — استاتیک (mhrv-rust-static-exit-node) 🆕

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** `TUNNEL_AUTH_KEY` (اختیاری), `CF_TUNNEL_TOKEN` (الزامی ⚠️)
**Secretهای WireGuard:** `WG_CONFIG` (اختیاری)
**زبان برنامهنویسی:** Rust (بسیار سریع و کم‌حجم)
**خروجی:** دامنه ثابت Cloudflare
**قابلیت تانل WireGuard:** دارد (گزینه `vpn_enabled`)

</div>

#### 📝 نحوه استفاده:
1. توکن `CF_TUNNEL_TOKEN` را تنظیم کنید.
2. **Actions** → **mhrv-rust-static-exit-node** → **Run workflow**
3. تونل روی دامنه ثابت فعال می‌شود.

> ℹ️ نسخه Rust برای کسانی که به حداکثر سرعت و پایداری نیاز دارند ایده‌آل است.

---

### ۱۹. Skirk Exit Node (skirk-vps) 🆕

<div dir="ltr" markdown="1">

**Secretهای مورد نیاز:** `SKIRK_EXIT_CONFIG` (**الزامی** ⚠️)
**Secretهای WireGuard:** `WG_CONFIG` (اختیاری)
**مدت زمان اجرا:** حداکثر ۶ ساعت
**قابلیت تانل WireGuard:** دارد (گزینه `vpn_enabled`)

</div>

این گردش کار یک **سرویس خروجی Skirk** مبتنی بر Google Drive راه‌اندازی می‌کند که به‌عنوان رله ترافیک عمل می‌کند. برخلاف Exit Nodeهای دیگر، نیازی به Cloudflare Tunnel ندارد و از زیرساخت گوگل برای انتقال داده استفاده می‌کند.

#### ✨ ویژگی‌ها:
- احراز هویت خودکار از طریق Google OAuth (بدون نیاز به دخالت دستی پس از تنظیم اولیه)
- Refresh Token دائمی (به شرط Publish بودن OAuth App)
- امکان تانل WireGuard برای تغییر IP خروجی
- اجرای خودکار یا دستی

#### 📝 نحوه استفاده:
1. مطمئن شوید Secret **`SKIRK_EXIT_CONFIG`** طبق راهنمای بخش [۸. کانفیگ خروجی Skirk](#۸-کانفیگ-خروجی-skirk-skirk_exit_config) تنظیم شده باشد.
2. **Actions** → **skirk-vps** → **Run workflow**
3. در صورت تمایل، گزینه `vpn_enabled` را فعال کنید (نیاز به `WG_CONFIG`).
4. پس از شروع، Skirk به‌طور خودکار سرویس خروجی را اجرا می‌کند و توکن‌ها را تمدید می‌کند.

#### دریافت فایل Client:
هنگام تنظیم اولیه (بخش ۸)، علاوه بر `exit.json`، یک فایل `client.skirk` نیز در پوشه `skirk-kit` ایجاد می‌شود. برای استفاده از این Exit Node روی سیستم شخصی:
- فایل `client.skirk` را به ماشین محلی منتقل کنید.
- با دستور `skirk serve-client --config client.skirk` یک پروکسی SOCKS5 روی `127.0.0.1:1080` راه‌اندازی کنید.
- مرورگر یا برنامه خود را برای استفاده از این پروکسی تنظیم کنید.

> ⚠️ برای عملکرد ۲۴/۷، می‌توانید این workflow را با یک زمان‌بندی (cron) هر ۵.۵ ساعت یکبار اجرا کنید تا وقفه‌ها به حداقل برسد.

---

## 🌐 راهنمای تانل WireGuard (اختیاری برای تمام Workflowها)

از این پس **بسیاری از گردش‌کارها** (لیچر، تمام Exit Nodeها، Skirk) دارای یک گزینه **`vpn_enabled`** هستند. با فعال کردن آن، تمام ترافیک خروجی رانر از یک تانل WireGuard عبور کرده و IP شما به IP سرور VPN تغییر می‌کند. این قابلیت برای موارد زیر بی‌نظیر است:

- دور زدن تحریم‌ها و محدودیت‌های جغرافیایی
- دانلود از سایت‌هایی که IP دیتاسنتر GitHub را بلاک کرده‌اند
- تست سرویس‌ها از لوکیشن‌های مختلف

### نحوه فعال‌سازی:

1. یک کانفیگ WireGuard معتبر دریافت کنید (پیشنهاد: ProtonVPN رایگان).  
2. محتوای فایل `.conf` را **دقیقاً** به عنوان Secret با نام `WG_CONFIG` ذخیره کنید.  
3. هنگام اجرای دستی هر Workflow، چک‌باکس **`vpn_enabled`** را تیک بزنید.  
4. اگر اتصال موفق باشد، در لاگ پیام `✅ WireGuard VPN connected.` را می‌بینید.  
5. در صورت شکست (مثلاً عدم وجود Secret یا مشکل کانفیگ)، Workflow **بدون VPN ادامه می‌یابد** — هیچ خطایی رخ نمی‌دهد.

### نکات فنی:
- کانفیگ WireGuard باید دارای `DNS` مناسب باشد تا از نشت DNS جلوگیری شود.  
- برای تغییر کشور خروجی، کافیست کانفیگ مربوط به آن سرور را جایگزین Secret کنید.  
- اگر از ProtonVPN استفاده می‌کنید، سرورهای رایگان شامل **هلند، ژاپن و آمریکا** هستند.  
- این Secret به صورت رمزنگاری شده ذخیره می‌شود و فقط در طول اجرای Job در دسترس است.

---

## 🆕 ویژگیهای جدید (که در README قبلی نیستند)

### ۱. آپلود خودکار در Google Drive
...

### ۸. Skirk Exit Node و تانل WireGuard برای تمام گردش‌کارها
- **Skirk Exit Node**: یک سرویس خروجی قدرتمند مبتنی بر Google Drive با Refresh Token دائمی.  
- **WireGuard Toggle**: اکنون لیچر و تمام Exit Nodeها (Python, Zyrln, Rust, Skirk) دارای سوئیچ `vpn_enabled` هستند که با یک Secret ساده (`WG_CONFIG`) می‌توان IP خروجی را تغییر داد.  
- **پشتیبانی از ProtonVPN رایگان**: با یک حساب رایگان می‌توانید کانفیگ WireGuard دریافت کرده و از IP کشورهای مختلف استفاده کنید.

---

## 🐢 مشکل کندی checkout و راهحل آن

...

---

## ⚠️ محدودیتها و هشدارهای مهم

...

---

## 📞 پشتیبانی

...

---

## 👀 فایل zoomusers.md چیست

...

---

## 📋 خلاصه تمام Secretها

| Secret Name | Workflowها | الزامی؟ | توضیح |
|---|---|---|---|
| `YOUTUBE_COOKIES` | downloader-youtube, aio-leecher | اختیاری | کوکی یوتیوب (با robots.txt بگیرید) |
| `INSTAGRAM_COOKIES` | downloader-instagram, aio-leecher | اختیاری | کوکی اینستاگرام (با robots.txt بگیرید) |
| `X_COOKIES` | downloader-x, aio-leecher | **الزامی** | کوکی X/توییتر (با robots.txt بگیرید) |
| `TUNNEL_AUTH_KEY` | exit-nodeها | اختیاری | رمز PSK دلخواه برای تونل |
| `CF_TUNNEL_TOKEN` | exit-nodeهای استاتیک | اختیاری | توکن تونل Cloudflare |
| `GOOGLE_CLIENT_ID` | تمام workflowها (آپلود در Drive) | اختیاری | OAuth Client ID از Google Cloud |
| `GOOGLE_CLIENT_SECRET` | تمام workflowها (آپلود در Drive) | اختیاری | OAuth Client Secret از Google Cloud |
| `GOOGLE_REFRESH_TOKEN` | تمام workflowها (آپلود در Drive) | اختیاری | Refresh Token از OAuth Playground |
| `SKIRK_EXIT_CONFIG` | skirk-vps | **الزامی** | محتوای کامل فایل `exit.json` |
| `WG_CONFIG` | تمام workflowهای دارای `vpn_enabled` | اختیاری | کانفیگ WireGuard (متن کامل) |

---

⭐⭐⭐ **اگر این پروژه برایتان مفید است، لطفاً ستاره بدهید!** ⭐⭐⭐

</div>
