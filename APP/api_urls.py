"""
URLs da API REST do ELC_Contabil
Configura todos os endpoints disponíveis
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    PerfilEmpresaViewSet,
    ContaBancariaViewSet,
    CategoriaViewSet,
    FornecedorViewSet,
    ReceitaViewSet,
    DespesaViewSet,
    DeclaracaoAnualViewSet,
    PreferenciaUsuarioViewSet,
    RelatorioViewSet
)

# Cria o roteador da API
router = DefaultRouter()

# Registra os ViewSets
router.register(r'perfis-empresa', PerfilEmpresaViewSet, basename='perfil-empresa')
router.register(r'contas-bancarias', ContaBancariaViewSet, basename='conta-bancaria')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'fornecedores', FornecedorViewSet, basename='fornecedor')
router.register(r'receitas', ReceitaViewSet, basename='receita')
router.register(r'despesas', DespesaViewSet, basename='despesa')
router.register(r'declaracoes-anuais', DeclaracaoAnualViewSet, basename='declaracao-anual')
router.register(r'preferencias', PreferenciaUsuarioViewSet, basename='preferencia')
router.register(r'relatorios', RelatorioViewSet, basename='relatorio')

# URLs da API
urlpatterns = [
    path('', include(router.urls)),
]
