const CACHE_NAME = 'empreinte-v1';
const ASSETS = [
  'index.html',
  'style.css',
  'app.js',
  'mockData.js'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((res) => res || fetch(e.request))
  );
});
