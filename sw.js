let statics = [
    "/",
    "/app.js",
    "/qrcode.min.js",
    "/sw.js",
    "/index.html",
    "/icon.png",
    "/hub.png"
]

self.addEventListener("install", function (event) {
    event.waitUntil(
        caches.open("feather-v1").then(function (cache) {
            return cache.addAll(statics);
        })
    );
});

self.addEventListener("fetch", function (event) {
    event.respondWith(
        caches.match(event.request).then(function (response) {
            return response || fetch(event.request);
        })
    );
});
