// My O! Service Worker — network-first for pages, stale-while-revalidate for assets
const CACHE_NAME = 'myo-cache-v2';
const STATIC_ASSETS = [
  '/',
  '/v2.html',
  '/poster.html',
  '/llms.txt',
  '/pricing.md',
  '/blog/index.html',
  '/image/01_company_logo.png',
  '/image/icon-192x192.png',
  '/image/icon-512x512.png',
  '/manifest.json',
  '/privacy.html',
  '/terms.html'
];

// Cloudflare Pages answers every `.html` request with a 308 to the extensionless
// URL. A response captured through such a redirect (response.redirected) is
// rejected by the browser when replayed for a navigation request, so those
// responses are never written to the cache.
function isCacheable(response) {
  return Boolean(response) && response.status === 200 && response.type === 'basic' && !response.redirected;
}

function cacheResponse(request, response) {
  if (!isCacheable(response)) return;
  const copy = response.clone();
  caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
}

async function purgeRedirectEntries() {
  const cache = await caches.open(CACHE_NAME);
  const keys = await cache.keys();
  await Promise.all(
    keys.map(async (request) => {
      const cached = await cache.match(request);
      if (cached && cached.redirected) await cache.delete(request);
    })
  );
}

// Install: pre-cache critical assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) =>
        Promise.allSettled(
          STATIC_ASSETS.map((url) => cache.add(url).catch(() => console.warn('Failed to cache: ' + url)))
        )
      )
      .then(purgeRedirectEntries)
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

// Fetch: stale-while-revalidate
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  if (!event.request.url.startsWith('http')) return;

  // Pages: network-first, so redirects resolve normally and the cache is only an
  // offline fallback. Serving a cached response here is what made `.html` links
  // fail with ERR_FAILED.
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          cacheResponse(event.request, response);
          return response;
        })
        .catch(() => caches.match(event.request).then((cached) => cached || caches.match('/')))
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cached) => {
      const fetchPromise = fetch(event.request)
        .then((response) => {
          cacheResponse(event.request, response);
          return response;
        })
        .catch(() => cached || new Response('Offline', { status: 503 }));

      return cached || fetchPromise;
    })
  );
});