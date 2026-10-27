// ✅ On incrémente la version à CHAQUE mise à jour de l'application
const CACHE_VERSION = 'v2';
const STATIC_CACHE = `agri-static-${CACHE_VERSION}`;
const PAGES_CACHE = `agri-pages-${CACHE_VERSION}`;
const OFFLINE_URL = '/offline/';

// Fichiers indispensables au démarrage (images de base, css)
const ASSETS_TO_CACHE = [
    OFFLINE_URL,
    '/static/vegetables_fruits/images/AgridomCorp.png'
];

// Pages qui ne doivent JAMAIS être servies depuis le cache (argent, formulaires, API)
const NEVER_CACHE = [
    '/tarification/',
    '/api/',
    '/abonnement/',
    '/admin/',
    '/media/'
];

// 1. INSTALLATION
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(STATIC_CACHE).then((cache) => {
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
    self.skipWaiting();
});

// 2. ACTIVATION (Nettoyage des anciennes versions)
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== STATIC_CACHE && cacheName !== PAGES_CACHE) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// 3. INTERCEPTION
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // ⚠️ SÉCURITÉ 1 : On ne touche pas aux POST/PUT/DELETE
    if (event.request.method !== 'GET') return;

    // ⚠️ SÉCURITÉ 2 : On ignore les domaines externes (Stripe, Mapbox, CDN)
    if (url.origin !== self.location.origin) return;

    // ⚠️ SÉCURITÉ 3 : On ne met JAMAIS en cache les pages sensibles
    if (NEVER_CACHE.some(path => url.pathname.startsWith(path))) {
        return; // Laisse le navigateur faire une requête réseau classique
    }

    // A. FICHIERS STATIQUES (Images, CSS) -> Cache First
    if (url.pathname.startsWith('/static/')) {
        event.respondWith(
            caches.match(event.request).then((cachedResponse) => {
                if (cachedResponse) return cachedResponse;

                return fetch(event.request).then((networkResponse) => {
                    return caches.open(STATIC_CACHE).then((cache) => {
                        cache.put(event.request, networkResponse.clone());
                        return networkResponse;
                    });
                });
            })
        );
        return;
    }

    // B. PAGES HTML -> Network First (On va sur internet, et on sauvegarde en cache)
    event.respondWith(
        fetch(event.request)
            .then((networkResponse) => {
                const responseClone = networkResponse.clone();
                caches.open(PAGES_CACHE).then((cache) => {
                    cache.put(event.request, responseClone);
                });
                return networkResponse;
            })
            .catch(() => {
                // En cas de perte de réseau, on cherche dans le cache
                return caches.match(event.request).then((cachedResponse) => {
                    if (cachedResponse) {
                        return cachedResponse;
                    }
                    // Si la page n'est pas en cache, on affiche la page hors-ligne
                    return caches.match(OFFLINE_URL);
                });
            })
    );
});