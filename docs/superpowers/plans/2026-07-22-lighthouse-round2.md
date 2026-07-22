# Lighthouse Performance Optimization — Round 2 (CLS 0.037 → LCP reduction)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce LCP time by ~0.5s via image sizing, eliminate unused Swiper JS (25 KiB), and push CLS from 0.037 to near-zero.

**Architecture:** Single-page static HTML file (`index.html`) with inline `<script>` and `<style>`. All changes are surgical edits to one file plus one new image asset. No framework. No bundler.

**Tech Stack:** Vanilla HTML/JS/CSS, `cwebp` (or `sips`/`ffmpeg` macOS built-in) for image resizing.

**Files affected:**
- `index.html` — hero image `<picture>` srcset, Swiper init script, hero section CSS
- `image/cert_hero_680.webp` — new 680×561 WebP (filling the 600→900 gap)

---

### Task 1: Add 680w hero image variant and fix srcset

**Files:**
- Create: `image/cert_hero_680.webp` (680×561, ~20 KiB, quality 82)
- Modify: `index.html:416-418` (hero picture srcset)

**Why:** Lighthouse reports `cert_hero_900.webp` (900×743, 35.5 KiB) being downloaded but displayed at 679×561. The gap between 600w (600×495, 9.8 KiB) and 900w (900×743, 35.5 KiB) is too wide — the browser picks 900w when 600w doesn't cover 1.5x+ DPR or when viewport is between 600-900px. Adding a 680w variant at ~20 KiB saves ~15 KiB on this critical LCP image.

- [ ] **Step 1: Generate the 680w WebP variant**

Run this command to create a 680px-wide WebP from the source JPG:

```bash
cd image
# Use cwebp if available (produces best quality/size ratio)
cwebp -q 82 -resize 680 0 cert_hero.jpg -o cert_hero_680.webp
# Fallback: ffmpeg
# ffmpeg -i cert_hero.jpg -vf "scale=680:-1" -q:v 82 cert_hero_680.webp
# Fallback: sips (macOS built-in, less efficient)
# sips -Z 680 cert_hero.jpg --out cert_hero_680.webp
```

Expected output: `image/cert_hero_680.webp` at ~20 KiB, 680×561.

- [ ] **Step 2: Update the `<picture>` srcset and sizes**

Modify lines 416-418 in `index.html` from:

```html
                    <picture>
                        <source srcset="image/cert_hero_600.webp 600w, image/cert_hero_900.webp 900w, image/cert_hero.webp 1200w" sizes="(max-width: 768px) 100vw, 600px" type="image/webp">
                        <img src="image/cert_hero.webp" alt="結婚證書套示意圖" class="rounded-2xl shadow-lg product-image" style="width:600px;aspect-ratio:1200/991;" loading="eager" fetchpriority="high">
```

To:

```html
                    <picture>
                        <source srcset="image/cert_hero_600.webp 600w, image/cert_hero_680.webp 680w, image/cert_hero_900.webp 900w, image/cert_hero.webp 1200w" sizes="(max-width: 640px) calc(100vw - 2rem), (max-width: 1024px) 50vw, 600px" type="image/webp">
                        <img src="image/cert_hero.webp" alt="結婚證書套示意圖" class="rounded-2xl shadow-lg product-image" style="width:600px;aspect-ratio:1200/991;" loading="eager" fetchpriority="high">
```

Changes:
- Added `image/cert_hero_680.webp 680w` to fill the 600→900 gap
- `sizes` updated to account for container padding (`calc(100vw - 2rem)` instead of `100vw`) and grid column (`50vw` on tablet instead of hardcoded `600px`)
- Breakpoints tuned to match Tailwind `md` (768px) breakpoint more precisely

- [ ] **Step 3: Verify the image loads correctly**

```bash
# Check file exists and size
ls -la image/cert_hero_680.webp
# Should show ~20 KiB
```

Open `index.html` in browser and inspect the hero image in DevTools Network tab → confirm `cert_hero_680.webp` is served on viewports >600px.

- [ ] **Step 4: Commit**

```bash
git add image/cert_hero_680.webp index.html
git commit -m "perf: add 680w hero image variant, fix srcset sizes for LCP"
```

---

### Task 2: Defer Swiper load to IntersectionObserver

**Files:**
- Modify: `index.html:574` (Swiper script tag)
- Modify: `index.html:574-748` (Swiper script + init logic)

**Why:** Swiper bundle (42 KiB, ~25 KiB unused) loads via `<script defer>` on all pages regardless of whether the carousel section is visible. This consumes bandwidth and adds forced reflow on init (100ms reported). Using IntersectionObserver delays load + init until the user scrolls near the "選擇款式" section.

- [ ] **Step 1: Replace the static Swiper script with deferred dynamic load**

Remove the static `<script defer>` tag at line 574:

```html
    <script defer src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>
```

Replace with a dynamic loader inside the DOMContentLoaded handler (around line 577). The loader watches for the `#designs` section to enter the viewport, then injects the Swiper script and initializes the carousel.

```html
    <script>
    document.addEventListener('DOMContentLoaded', function () {
        // ... existing code (mobile menu, select options, modal) remains unchanged ...

        // 3. 輪播初始化 (Swiper Carousel) — lazy load on viewport enter
        var swiperLoaded = false;
        var swiperScript = document.createElement('script');
        swiperScript.src = 'https://unpkg.com/swiper/swiper-bundle.min.js';

        function initSwiper() {
            if (swiperLoaded) return;
            swiperLoaded = true;
            if (observer) observer.disconnect();

            // Inject Swiper CSS if not already loaded
            if (!document.querySelector('link[href*="swiper-bundle.min.css"]')) {
                var link = document.createElement('link');
                link.rel = 'stylesheet';
                link.href = 'https://unpkg.com/swiper/swiper-bundle.min.css';
                document.head.appendChild(link);
            }

            // Inject Swiper JS
            swiperScript.onload = function () {
                new Swiper('.mySwiper', {
                    slidesPerView: 'auto',
                    centeredSlides: true,
                    spaceBetween: 20,
                    simulateTouch: true,
                    touchRatio: 1,
                    touchAngle: 45,
                    shortSwipes: true,
                    longSwipesRatio: 0.5,
                    allowTouchMove: true,
                    threshold: 5,
                    breakpoints: {
                        0: { slidesPerView: 1.2, spaceBetween: 10 },
                        640: { slidesPerView: 2.2, spaceBetween: 15 },
                        768: { slidesPerView: 3.2, spaceBetween: 20 },
                        1024: { slidesPerView: 4.2, spaceBetween: 20 },
                        1280: { slidesPerView: 5.2, spaceBetween: 20 }
                    },
                    loop: true,
                    pagination: { el: '.swiper-pagination', clickable: true },
                    navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' },
                    autoplay: { delay: 2500, disableOnInteraction: false }
                });
            };
            document.body.appendChild(swiperScript);
        }

        var observer;
        var designSection = document.getElementById('designs');
        if (designSection && 'IntersectionObserver' in window) {
            observer = new IntersectionObserver(function(entries) {
                if (entries[0].isIntersecting) {
                    initSwiper();
                }
            }, { rootMargin: '200px' });
            observer.observe(designSection);
        } else if (designSection) {
            // Fallback: load on idle if IntersectionObserver not available
            if ('requestIdleCallback' in window) {
                requestIdleCallback(initSwiper, { timeout: 3000 });
            } else {
                setTimeout(initSwiper, 2000);
            }
        }

        // 4. Mobile Sticky Conversion Bar - 保持始終顯示（無需額外 JS）
    });
    </script>
```

The full replacement block spans from the Swiper `<script defer>` at line 574 through the end of the DOMContentLoaded handler (line 747). See the exact diff below.

**Exact edit — replace lines 574-748:**

Replace this block:
```html
    <script defer src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>

    <script>
        document.addEventListener('DOMContentLoaded', function () {
            // 1. 手機選單開關功能 (Mobile Menu Toggle)
            ... (lines 579-747)
        });
    </script>
```

With the code above (the full DOMContentLoaded handler with IntersectionObserver-based Swiper loading instead of `requestAnimationFrame(initSwiper)`).

- [ ] **Step 2: Verify Swiper loads on scroll**

Open `index.html` in browser DevTools:
1. Clear cache, reload
2. Confirm Swiper JS is NOT loaded on initial page load (check Network tab)
3. Scroll down to the "選擇您的專屬款式與設計" section
4. Confirm Swiper JS loads dynamically and carousel initializes

- [ ] **Step 3: Remove unused Swiper CSS preload**

Remove line 66-67 (Swiper CSS preload + noscript), since the CSS is now injected alongside the JS:

```html
    <link rel="preload" href="https://unpkg.com/swiper/swiper-bundle.min.css" as="style" fetchpriority="low" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://unpkg.com/swiper/swiper-bundle.min.css"></noscript>
```

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "perf: lazy load Swiper via IntersectionObserver, save 25 KiB unused JS"
```

---

### Task 3: Eliminate residual CLS (0.037 → ~0)

**Files:**
- Modify: `index.html:278` (hero section min-height or inline style)

**Why:** The remaining 0.037 CLS is attributed to `<main>`, likely from subtle shifts in hero section text height after the Inter font swap. Even with improved font-fallback metrics, the multi-line H1 (with `<br>`) can shift by 1-2px when Inter replaces Arial. Adding an explicit `min-height` to the hero section container locks its dimensions regardless of font rendering.

- [ ] **Step 1: Add explicit height anchoring to the hero section**

Find the `<header class="hero-section">` at line 278 and add a `min-height` that accommodates both font renders. The hero currently has `min-height: 400px` defined in CSS. The shift is within that range but the content inside shifts relative to other elements.

Add the following inline style to the `<header>` tag:

```html
    <header class="hero-section" style="min-height:400px">
```

(If `min-height:400px` is already in the CSS `hero-section` class at line 69, no change is needed there — the issue is the internal content shift. Instead, we need to ensure the H1 container has a fixed height.)

Better approach: Add explicit `height` to the hero content container (the `.container` div inside `.hero-section`). The content is already laid out deterministically, but the font swap changes inter-line spacing. A more precise fix:

Add inline `min-height` to the H1's parent container that encompasses the full text block in either font:

```html
            <div class="container mx-auto px-4" style="min-height:360px">
```

But this is fragile. A better approach: **force `font-display: block`** on the hero heading so text stays invisible until Inter arrives — zero CLS from that element. Add a `specific-font-load` class:

Modify the H1 to use preload + `font-display: block` behavior. This prevents the fallback from rendering:

```html
            <h1 class="text-4xl md:text-5xl font-bold text-rose-600 leading-tight mb-3 md:mb-4" style="font-family:'Inter',sans-serif;visibility:hidden;animation:fadeInText 0.3s 0.1s forwards;"> 珍藏您的愛情，<br>從一份證書套開始。💖
```

And add the keyframe to the inline `<style>` block (line 60):

```css
@keyframes fadeInText{to{visibility:visible}}
```

This way:
1. Text renders with `visibility:hidden` (takes up space, no CLS)
2. Once Inter is loaded (preloaded at top of `<head>` with `fetchpriority="high"`), the `fadeInText` animation makes it visible
3. If Inter fails to load, the fallback renders but without the animation trigger — text stays hidden

Wait, this approach has a UX problem: text is invisible until font loads. On slow connections this could be a few hundred ms.

A simpler, more user-friendly approach: **add a CSS `line-height` lock specific to the H1.** The H1 already has `leading-tight` (line-height: 1.25). The difference between Inter and Arial at `size-adjust: 107%` in line rendering is minimal. The CLS of 0.037 might not even be font-related — it could be from the Swiper carousel items (which will be fixed in Task 2).

Given that Task 2 defers Swiper (which may be the actual source of the 0.037 CLS), let's validate before over-engineering.

**For this task: Add a lightweight line-height lock and min-height guard.**

```html
<h1 class="text-4xl md:text-5xl font-bold text-rose-600 leading-tight mb-3 md:mb-4" style="min-height:4.5rem;line-height:1.25;"> 珍藏您的愛情，<br>從一份證書套開始。💖
</h1>
```

`min-height:4.5rem` = 72px at default 16px root. For `text-4xl` (2.25rem = 36px) × `leading-tight` (1.25) = 45px per line × 2 lines = 90px = ~5.6rem. A 4.5rem min-height provides a safety floor for small font rendering differences while being short enough not to clip any real content.

- [ ] **Step 1: Add min-height to H1**

Modify line 282:

```html
            <h1 class="text-4xl md:text-5xl font-bold text-rose-600 leading-tight mb-3 md:mb-4" style="min-height:5.625rem;"> 珍藏您的愛情，<br>從一份證書套開始。💖
```

`5.625rem` = 90px = 2 lines × 36px × 1.25 line-height. This ensures the H1 container never collapses below the intended two-line height regardless of font metrics.

- [ ] **Step 2: Commit**

```bash
git add index.html
git commit -m "perf: add line-height lock to H1 for sub-pixel CLS guard"
```

---

### Task 4: Playwright regression test for performance metrics

**Files:**
- Create: Not needed (the existing `tests/lighthouse-audits.spec.ts` can be extended)

**Why:** Ensure future changes don't regress CLS below 0.05 or LCP above 4s.

- [ ] **Step 1: Update the existing performance test**

Edit `tests/lighthouse-audits.spec.ts` to add assertions for:
- CLS ≤ 0.05
- TBT ≤ 100ms

(Test structure should match the existing Playwright tests in the project.)

- [ ] **Step 2: Run the test to confirm passes**

```bash
npx playwright test tests/lighthouse-audits.spec.ts
```

Expected: All assertions pass.

- [ ] **Step 3: Commit**

```bash
git add tests/lighthouse-audits.spec.ts
git commit -m "test: add CLS and TBT thresholds to Lighthouse regression test"
```
