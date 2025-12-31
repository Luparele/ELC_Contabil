from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # ADICIONADO: Inclui as URLs de autenticação padrão do Django
    path('accounts/', include('django.contrib.auth.urls')),
    # Inclui as URLs do nosso APP
    path('', include('APP.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)