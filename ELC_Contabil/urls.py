from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuração do Swagger/OpenAPI
schema_view = get_schema_view(
    openapi.Info(
        title="ELC Contabil API",
        default_version='v1',
        description="""API REST completa para o sistema ELC Contabil
        
        Sistema de controle financeiro com gerenciamento de:
        - Receitas e Despesas
        - Categorias
        - Fornecedores
        - Contas Bancárias
        - Relatórios e Estatísticas
        
        Desenvolvido por Eduardo Luparele Coelho
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contato@elc-contabil.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs de autenticação
    path('accounts/', include('django.contrib.auth.urls')),
    
    # API REST
    path('api/v1/', include('APP.api_urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Documentação Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # App principal
    path('', include('APP.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
