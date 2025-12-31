from django.contrib import admin
from .models import Categoria, Receita, Despesa, PerfilEmpresa, ContaBancaria, DeclaracaoAnual, Fornecedor

# Para mostrar as contas bancárias dentro do perfil da empresa
class ContaBancariaInline(admin.TabularInline):
    model = ContaBancaria
    extra = 1  # Mostra um campo extra para adicionar conta diretamente no perfil

@admin.register(PerfilEmpresa)
class PerfilEmpresaAdmin(admin.ModelAdmin):
    list_display = ('razao_social', 'cnpj', 'usuario')
    search_fields = ('razao_social', 'cnpj', 'usuario__username')
    list_filter = ('usuario',)
    inlines = [ContaBancariaInline]

@admin.register(DeclaracaoAnual)
class DeclaracaoAnualAdmin(admin.ModelAdmin):
    list_display = ('perfil_empresa', 'ano', 'data_confirmacao')
    list_filter = ('ano', 'perfil_empresa')
    search_fields = ('perfil_empresa__razao_social', 'ano')


# ==================== RECEITAS ====================
@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('data', 'descricao', 'valor_formatado', 'categoria', 'fornecedor', 'usuario')
    list_filter = ('data', 'categoria', 'usuario', 'fornecedor')
    search_fields = ('descricao', 'usuario__username', 'fornecedor__nome')
    date_hierarchy = 'data'
    ordering = ('-data',)
    
    # Campos que aparecem no formulário de edição
    fieldsets = (
        ('Informações Principais', {
            'fields': ('usuario', 'descricao', 'valor', 'data', 'categoria')
        }),
        ('Fornecedor/Cliente', {
            'fields': ('fornecedor',),
            'classes': ('collapse',)  # Seção colapsável
        }),
        ('Comprovante', {
            'fields': ('comprovante',),
            'classes': ('collapse',)
        }),
    )
    
    def valor_formatado(self, obj):
        """Exibe o valor formatado em reais"""
        return f"R$ {obj.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    valor_formatado.short_description = 'Valor'
    valor_formatado.admin_order_field = 'valor'  # Permite ordenar por esta coluna


# ==================== DESPESAS ====================
@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = ('data', 'descricao', 'valor_formatado', 'categoria', 'fornecedor', 'usuario')
    list_filter = ('data', 'categoria', 'usuario', 'fornecedor')
    search_fields = ('descricao', 'usuario__username', 'fornecedor__nome')
    date_hierarchy = 'data'
    ordering = ('-data',)
    
    # Campos que aparecem no formulário de edição
    fieldsets = (
        ('Informações Principais', {
            'fields': ('usuario', 'descricao', 'valor', 'data', 'categoria')
        }),
        ('Fornecedor', {
            'fields': ('fornecedor',),
            'classes': ('collapse',)  # Seção colapsável
        }),
        ('Comprovante', {
            'fields': ('comprovante',),
            'classes': ('collapse',)
        }),
    )
    
    def valor_formatado(self, obj):
        """Exibe o valor formatado em reais"""
        return f"R$ {obj.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    valor_formatado.short_description = 'Valor'
    valor_formatado.admin_order_field = 'valor'  # Permite ordenar por esta coluna


# ==================== FORNECEDORES ====================
@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_display', 'cpf_cnpj', 'telefone', 'municipio', 'ativo_display', 'usuario')
    list_filter = ('tipo', 'ativo', 'usuario', 'municipio', 'uf')
    search_fields = ('nome', 'nome_fantasia', 'cpf_cnpj', 'email', 'usuario__username')
    ordering = ('nome',)
    
    # Campos que aparecem no formulário de edição
    fieldsets = (
        ('Informações Principais', {
            'fields': ('usuario', 'tipo', 'nome', 'nome_fantasia', 'cpf_cnpj', 'ativo')
        }),
        ('Contato', {
            'fields': ('telefone', 'email')
        }),
        ('Endereço', {
            'fields': ('cep', 'logradouro', 'numero', 'complemento', 'bairro', 'municipio', 'uf'),
            'classes': ('collapse',)
        }),
        ('Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('data_cadastro', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    # Campos somente leitura
    readonly_fields = ('data_cadastro', 'data_atualizacao')
    
    def tipo_display(self, obj):
        """Exibe o tipo de forma mais legível"""
        return "Pessoa Física" if obj.tipo == 'PF' else "Pessoa Jurídica"
    tipo_display.short_description = 'Tipo'
    tipo_display.admin_order_field = 'tipo'
    
    def ativo_display(self, obj):
        """Exibe status com ícone colorido"""
        if obj.ativo:
            return "✅ Ativo"
        return "❌ Inativo"
    ativo_display.short_description = 'Status'
    ativo_display.admin_order_field = 'ativo'


# ==================== CATEGORIAS ====================
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_display')
    list_filter = ('tipo',)
    search_fields = ('nome',)
    ordering = ('nome',)
    
    def tipo_display(self, obj):
        """Exibe o tipo de forma mais legível"""
        return "Receita" if obj.tipo == 'R' else "Despesa"
    tipo_display.short_description = 'Tipo'
    tipo_display.admin_order_field = 'tipo'


# ==================== CONTAS BANCÁRIAS ====================
@admin.register(ContaBancaria)
class ContaBancariaAdmin(admin.ModelAdmin):
    list_display = ('nome_banco', 'agencia', 'conta_corrente', 'preferencial_display', 'perfil_empresa')
    list_filter = ('preferencial', 'perfil_empresa')
    search_fields = ('nome_banco', 'codigo_banco', 'agencia', 'conta_corrente')
    
    def preferencial_display(self, obj):
        """Exibe se é conta preferencial com ícone"""
        if obj.preferencial:
            return "⭐ Sim"
        return "Não"
    preferencial_display.short_description = 'Preferencial'
    preferencial_display.admin_order_field = 'preferencial'
