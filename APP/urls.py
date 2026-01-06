from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('lancamentos/', views.listar_lancamentos, name='listar_lancamentos'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios/exportar_csv/', views.exportar_csv, name='exportar_csv'),
    path('relatorios/exportar_pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('relatorios/exportar_excel/', views.exportar_excel, name='exportar_excel'),
    path('despesa/adicionar/', views.adicionar_despesa, name='adicionar_despesa'),
    path('receita/adicionar/', views.adicionar_receita, name='adicionar_receita'),
    
    # Edição e exclusão de lançamentos
    path('receita/<int:pk>/editar/', views.editar_receita, name='editar_receita'),
    path('receita/<int:pk>/excluir/', views.excluir_receita, name='excluir_receita'),
    path('despesa/<int:pk>/editar/', views.editar_despesa, name='editar_despesa'),
    path('despesa/<int:pk>/excluir/', views.excluir_despesa, name='excluir_despesa'),
    
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/adicionar/', views.adicionar_categoria, name='adicionar_categoria'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:pk>/excluir/', views.excluir_categoria, name='excluir_categoria'),
    path('perfil/', views.ver_perfil, name='ver_perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('consultar-cnpj/', views.consultar_cnpj, name='consultar_cnpj'),

    # Contas Bancárias
    path('contas/adicionar/', views.adicionar_conta, name='adicionar_conta'),
    path('contas/<int:pk>/editar/', views.editar_conta, name='editar_conta'),
    path('contas/<int:pk>/excluir/', views.excluir_conta, name='excluir_conta'),

    path('declaracao/confirmar/<int:ano>/', views.confirmar_declaracao, name='confirmar_declaracao'),
    path('toggle-tema/', views.toggle_tema, name='toggle_tema'),
    
    # URLs de Fornecedores
    path('fornecedores/', views.lista_fornecedores, name='lista_fornecedores'),
    path('fornecedores/novo/', views.criar_fornecedor, name='criar_fornecedor'),
    path('fornecedores/<int:pk>/', views.detalhes_fornecedor, name='detalhes_fornecedor'),
    path('fornecedores/<int:pk>/editar/', views.editar_fornecedor, name='editar_fornecedor'),
    path('fornecedores/<int:pk>/excluir/', views.excluir_fornecedor, name='excluir_fornecedor'),
    
    # URLs de DASN-SIMEI
    path('dasn-simei/adicionar/', views.adicionar_dasn_simei, name='adicionar_dasn_simei'),
    path('dasn-simei/<int:pk>/editar/', views.editar_dasn_simei, name='editar_dasn_simei'),
    path('dasn-simei/<int:pk>/excluir/', views.excluir_dasn_simei, name='excluir_dasn_simei'),
]