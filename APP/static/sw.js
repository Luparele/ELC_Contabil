const CACHE_NAME = 'elc-contabil-v3';
const RUNTIME_CACHE = 'elc-runtime-v3';

const urlsToCache = [
  '/',
  '/static/manifest.json',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js',
];

// Install - cache recursos estáticos
self.addEventListener('install', event => {
  console.log('[SW] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[SW] Caching static resources');
        return cache.addAll(urlsToCache);
      })
      .then(() => {
        console.log('[SW] Skip waiting');
        return self.skipWaiting();
      })
      .catch(err => {
        console.error('[SW] Cache failed:', err);
      })
  );
});

// Activate - limpa caches antigos
self.addEventListener('activate', event => {
  console.log('[SW] Activating...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE) {
            console.log('[SW] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('[SW] Claiming clients');
      return self.clients.claim();
    })
  );
});

// Fetch - estratégia de cache
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Ignora requisições não-GET
  if (request.method !== 'GET') {
    return;
  }

  // Ignora requisições de API (Django admin, uploads, etc)
  if (url.pathname.startsWith('/admin/') || 
      url.pathname.startsWith('/api/') ||
      url.pathname.includes('/media/')) {
    return;
  }

  // Network First para páginas HTML (sempre busca a versão mais recente)
  if (request.headers.get('accept').includes('text/html')) {
    event.respondWith(
      fetch(request)
        .then(response => {
          // Clone a resposta antes de cachear
          const responseClone = response.clone();
          caches.open(RUNTIME_CACHE)
            .then(cache => cache.put(request, responseClone));
          return response;
        })
        .catch(() => {
          // Se offline, tenta buscar do cache
          return caches.match(request)
            .then(cached => {
              if (cached) {
                return cached;
              }
              // Página offline genérica (pode criar depois)
              return new Response(
                '<h1>Offline</h1><p>Você está offline. Algumas funcionalidades podem não estar disponíveis.</p>',
                { headers: { 'Content-Type': 'text/html' } }
              );
            });
        })
    );
    return;
  }

  // Cache First para recursos estáticos (CSS, JS, imagens, ícones)
  event.respondWith(
    caches.match(request)
      .then(cached => {
        if (cached) {
          console.log('[SW] Cache hit:', request.url);
          return cached;
        }

        console.log('[SW] Fetching:', request.url);
        return fetch(request)
          .then(response => {
            // Não cacheia se não for uma resposta OK
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Clone a resposta para cachear
            const responseClone = response.clone();
            
            caches.open(RUNTIME_CACHE)
              .then(cache => {
                cache.put(request, responseClone);
              });

            return response;
          })
          .catch(err => {
            console.error('[SW] Fetch failed:', err);
            // Retorna do cache se houver erro na rede
            return caches.match(request);
          });
      })
  );
});

// Mensagens do cliente
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    console.log('[SW] Skip waiting requested');
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CLEAR_CACHE') {
    console.log('[SW] Clearing all caches');
    event.waitUntil(
      caches.keys().then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => caches.delete(cacheName))
        );
      })
    );
  }
});

console.log('[SW] Service Worker loaded');
