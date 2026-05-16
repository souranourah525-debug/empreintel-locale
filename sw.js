const CACHE_NAME = 'empreinte-v2';
const ASSETS = [
  'index.html',
  'style.css',
  'app.js',
  'mockData.js',
  'icon.png'
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
