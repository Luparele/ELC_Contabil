# settings_local.py - Configurações para desenvolvimento local
from .settings import *

# Sobrescrever configurações para desenvolvimento
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '*']

# Configurações de static files para desenvolvimento local
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Opcional: Usar console email backend para desenvolvimento
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Desabilitar algumas checagens de segurança em desenvolvimento
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
