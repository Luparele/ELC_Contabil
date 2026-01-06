from django.db import models
from django.contrib.auth.models import User

class PerfilEmpresa(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cnpj = models.CharField(max_length=18, unique=True, blank=True, null=True)
    razao_social = models.CharField(max_length=255, blank=True, null=True)
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True)
    ramo_atividade = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ramo de Atividade")
    logradouro = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=30, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)

    def __str__(self):
        return self.razao_social or self.usuario.username

# --- NOVO MODELO ADICIONADO ---
class ContaBancaria(models.Model):
    # Link para o perfil da empresa (um perfil pode ter várias contas)
    perfil_empresa = models.ForeignKey(PerfilEmpresa, on_delete=models.CASCADE, related_name='contas')
    
    # Campos da conta
    nome_banco = models.CharField(max_length=100, verbose_name="Nome do Banco")
    codigo_banco = models.CharField(max_length=10, verbose_name="Número da Instituição")
    agencia = models.CharField(max_length=10)
    conta_corrente = models.CharField(max_length=20, verbose_name="Conta Corrente")
    preferencial = models.BooleanField(default=False, verbose_name="Conta Preferencial")

    def __str__(self):
        return f"{self.nome_banco} - Ag: {self.agencia} / CC: {self.conta_corrente}"

    def save(self, *args, **kwargs):
        # Garante que apenas uma conta seja a preferencial
        if self.preferencial:
            # Desmarca todas as outras contas do mesmo perfil como não preferenciais
            ContaBancaria.objects.filter(perfil_empresa=self.perfil_empresa).update(preferencial=False)
        super(ContaBancaria, self).save(*args, **kwargs)


class Categoria(models.Model):
    TIPO_CHOICES = [
        ('R', 'Receita'),
        ('D', 'Despesa'),
    ]
    
    # Vinculação ao usuário - cada usuário tem suas categorias
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categorias', null=True, blank=True)
    
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default='D')
    
    # Novos campos
    cor = models.CharField(max_length=7, default='#6c757d', help_text='Cor em hexadecimal (ex: #FF5733)')
    icone = models.CharField(max_length=50, default='bi-tag', help_text='Classe do ícone Bootstrap (ex: bi-cart)')
    ativo = models.BooleanField(default=True)
    
    # Para categorias padrão do sistema
    is_padrao = models.BooleanField(default=False, help_text='Categoria padrão do sistema')

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"
    
    class Meta:
        unique_together = ('nome', 'tipo', 'usuario')
        ordering = ['tipo', 'nome']


# --- MODELO FORNECEDOR ---
class Fornecedor(models.Model):
    TIPO_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    ]
    
    # Vinculação ao usuário (cada usuário tem seus fornecedores)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fornecedores')
    
    # Identificação
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default='PJ', verbose_name='Tipo')
    
    # Nome/Razão Social (campo principal)
    nome = models.CharField(max_length=255, verbose_name='Nome/Razão Social')
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nome Fantasia')
    
    # Documentos
    cpf_cnpj = models.CharField(max_length=18, blank=True, null=True, verbose_name='CPF/CNPJ')
    
    # Contato
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    # Endereço (opcional)
    logradouro = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=30, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)
    
    # Observações
    observacoes = models.TextField(blank=True, null=True)
    
    # Controle
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nome']
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"


class Receita(models.Model):
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    comprovante = models.FileField(upload_to='comprovantes_receitas/', null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # NOVO CAMPO - NULLABLE para compatibilidade com dados existentes
    fornecedor = models.ForeignKey(
        'Fornecedor', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='receitas',
        verbose_name='Cliente/Fornecedor'
    )
    
    # Campos de controle
    data_cadastro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    data_atualizacao = models.DateTimeField(auto_now=True, null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.descricao
    
    class Meta:
        ordering = ['-data', '-data_cadastro']


class Despesa(models.Model):
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    comprovante = models.FileField(upload_to='comprovantes_despesas/', null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # NOVO CAMPO - NULLABLE para compatibilidade com dados existentes
    fornecedor = models.ForeignKey(
        'Fornecedor', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='despesas',
        verbose_name='Fornecedor'
    )
    
    # Campos de controle
    data_cadastro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    data_atualizacao = models.DateTimeField(auto_now=True, null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.descricao
    
    class Meta:
        ordering = ['-data', '-data_cadastro']
    
class DeclaracaoAnual(models.Model):
    # Link para o perfil da empresa
    perfil_empresa = models.ForeignKey(PerfilEmpresa, on_delete=models.CASCADE)
    # O ano para o qual a declaração foi confirmada
    ano = models.IntegerField()
    # Data e hora em que a confirmação foi feita
    data_confirmacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Garante que só exista uma confirmação por perfil e por ano
        unique_together = ('perfil_empresa', 'ano')

    def __str__(self):
        return f"Declaração de {self.ano} confirmada para {self.perfil_empresa.razao_social}"


class PreferenciaUsuario(models.Model):
    """Preferências do usuário (tema, configurações de interface, etc)"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferencias')
    
    # Tema
    tema_escuro = models.BooleanField(default=False, verbose_name='Tema Escuro')
    
    # Páginação
    itens_por_pagina = models.IntegerField(default=25, verbose_name='Itens por página')
    
    # Notificações
    alertas_ativos = models.BooleanField(default=True, verbose_name='Alertas Ativos')
    alerta_percentual_despesas = models.IntegerField(default=80, verbose_name='Alerta quando despesas atingirem (%)') 
    
    def __str__(self):
        return f"Preferências de {self.usuario.username}"


class DASN_SIMEI(models.Model):
    """Declaração Anual do Simples Nacional - SIMEI"""
    
    # Vinculação ao perfil da empresa
    perfil_empresa = models.ForeignKey(
        PerfilEmpresa, 
        on_delete=models.CASCADE, 
        related_name='declaracoes_simei',
        verbose_name='Perfil da Empresa'
    )
    
    # Ano da declaração
    ano_calendario = models.IntegerField(verbose_name='Ano Calendário')
    
    # Valor bruto anual
    valor_bruto_anual = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        verbose_name='Valor Bruto Anual (R$)',
        help_text='Total de receitas brutas do ano'
    )
    
    # Status da declaração
    declarada = models.BooleanField(
        default=False,
        verbose_name='Declaração Enviada?',
        help_text='Marque se a DASN-SIMEI foi enviada à Receita Federal'
    )
    
    # Data de envio (quando for declarada)
    data_envio = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Envio',
        help_text='Data em que a declaração foi enviada'
    )
    
    # Comprovante em PDF
    comprovante_pdf = models.FileField(
        upload_to='dasn_simei/',
        null=True,
        blank=True,
        verbose_name='Comprovante (PDF)',
        help_text='Upload do comprovante de envio da DASN-SIMEI'
    )
    
    # Observações
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações'
    )
    
    # Controle
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-ano_calendario']
        verbose_name = 'DASN-SIMEI'
        verbose_name_plural = 'DASN-SIMEI'
        unique_together = ('perfil_empresa', 'ano_calendario')
    
    def __str__(self):
        status = "Declarada" if self.declarada else "Pendente"
        return f"DASN-SIMEI {self.ano_calendario} - {status}"
