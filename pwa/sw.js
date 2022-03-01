self.addEventListener("install", function (event) {
    event.waitUntil(
        caches.open("feather-v1").then(function (cache) {
            return cache.addAll(
                [
                    "/",
                    "/index.html",
                    "/light.css",
                    "/style.css",
                    "/qrcode.min.js",
                    "/app.js",
                ]
            );
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
