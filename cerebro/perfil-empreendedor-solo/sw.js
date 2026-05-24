const CACHE = "opb-studio-v3";
const ASSETS = [
  "/dashboard.html",
  "/plataforma.html",
  "/manifest.json"
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (e) => {
  if (e.request.url.includes("/api/")) {
    e.respondWith(fetch(e.request).catch(() => new Response(JSON.stringify({ error: "offline" }), { status: 503, headers: { "Content-Type": "application/json" } })));
    return;
  }
  e.respondWith(
    caches.match(e.request).then((r) => r || fetch(e.request).catch(() => {
      if (e.request.mode === "navigate") {
        return caches.match("/plataforma.html");
      }
      return new Response('<html><body><h1>Offline</h1><p>Conteúdo não disponível sem internet.</p></body></html>', { status: 503, headers: { "Content-Type": "text/html;charset=UTF-8" } });
    }))
  );
});
