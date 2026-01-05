"""
Serializers para a API REST do ELC_Contabil
Converte modelos Django em JSON e vice-versa
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    PerfilEmpresa, 
    ContaBancaria, 
    Categoria, 
    Fornecedor, 
    Receita, 
    Despesa,
    DeclaracaoAnual,
    PreferenciaUsuario
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer para o modelo User"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
        read_only_fields = ['id', 'is_staff', 'date_joined']


class PerfilEmpresaSerializer(serializers.ModelSerializer):
    """Serializer para o Perfil da Empresa"""
    usuario = UserSerializer(read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='usuario', 
        write_only=True
    )
    
    class Meta:
        model = PerfilEmpresa
        fields = [
            'id', 'usuario', 'usuario_id', 'cnpj', 'razao_social', 
            'nome_fantasia', 'ramo_atividade', 'logradouro', 'numero',
            'complemento', 'bairro', 'municipio', 'uf', 'cep'
        ]
        read_only_fields = ['id']


class ContaBancariaSerializer(serializers.ModelSerializer):
    """Serializer para Contas Bancárias"""
    perfil_empresa_nome = serializers.CharField(source='perfil_empresa.razao_social', read_only=True)
    
    class Meta:
        model = ContaBancaria
        fields = [
            'id', 'perfil_empresa', 'perfil_empresa_nome', 'nome_banco', 
            'codigo_banco', 'agencia', 'conta_corrente', 'preferencial'
        ]
        read_only_fields = ['id']


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para Categorias"""
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = Categoria
        fields = [
            'id', 'usuario', 'usuario_username', 'nome', 'tipo', 
            'tipo_display', 'cor', 'icone', 'ativo', 'is_padrao'
        ]
        read_only_fields = ['id', 'is_padrao']


class FornecedorSerializer(serializers.ModelSerializer):
    """Serializer para Fornecedores"""
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = Fornecedor
        fields = [
            'id', 'usuario', 'usuario_username', 'tipo', 'tipo_display',
            'nome', 'nome_fantasia', 'cpf_cnpj', 'telefone', 'email',
            'logradouro', 'numero', 'complemento', 'bairro', 'municipio',
            'uf', 'cep', 'observacoes', 'ativo', 'data_cadastro', 'data_atualizacao'
        ]
        read_only_fields = ['id', 'data_cadastro', 'data_atualizacao']


class ReceitaSerializer(serializers.ModelSerializer):
    """Serializer para Receitas"""
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    fornecedor_nome = serializers.CharField(source='fornecedor.nome', read_only=True)
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
    comprovante_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Receita
        fields = [
            'id', 'descricao', 'valor', 'data', 'categoria', 'categoria_nome',
            'fornecedor', 'fornecedor_nome', 'comprovante', 'comprovante_url',
            'usuario', 'usuario_username', 'observacoes', 
            'data_cadastro', 'data_atualizacao'
        ]
        read_only_fields = ['id', 'data_cadastro', 'data_atualizacao']
    
    def get_comprovante_url(self, obj):
        """Retorna a URL completa do comprovante se existir"""
        if obj.comprovante:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.comprovante.url)
        return None


class DespesaSerializer(serializers.ModelSerializer):
    """Serializer para Despesas"""
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    fornecedor_nome = serializers.CharField(source='fornecedor.nome', read_only=True)
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
    comprovante_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Despesa
        fields = [
            'id', 'descricao', 'valor', 'data', 'categoria', 'categoria_nome',
            'fornecedor', 'fornecedor_nome', 'comprovante', 'comprovante_url',
            'usuario', 'usuario_username', 'observacoes',
            'data_cadastro', 'data_atualizacao'
        ]
        read_only_fields = ['id', 'data_cadastro', 'data_atualizacao']
    
    def get_comprovante_url(self, obj):
        """Retorna a URL completa do comprovante se existir"""
        if obj.comprovante:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.comprovante.url)
        return None


class DeclaracaoAnualSerializer(serializers.ModelSerializer):
    """Serializer para Declarações Anuais"""
    perfil_empresa_nome = serializers.CharField(source='perfil_empresa.razao_social', read_only=True)
    
    class Meta:
        model = DeclaracaoAnual
        fields = [
            'id', 'perfil_empresa', 'perfil_empresa_nome', 
            'ano', 'data_confirmacao'
        ]
        read_only_fields = ['id', 'data_confirmacao']


class PreferenciaUsuarioSerializer(serializers.ModelSerializer):
    """Serializer para Preferências do Usuário"""
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = PreferenciaUsuario
        fields = [
            'id', 'usuario', 'usuario_username', 'tema_escuro', 
            'itens_por_pagina', 'alertas_ativos', 'alerta_percentual_despesas'
        ]
        read_only_fields = ['id']


# Serializers para relatórios e estatísticas
class RelatorioMensalSerializer(serializers.Serializer):
    """Serializer para relatório mensal consolidado"""
    mes = serializers.IntegerField()
    ano = serializers.IntegerField()
    total_receitas = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_despesas = serializers.DecimalField(max_digits=10, decimal_places=2)
    saldo = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantidade_receitas = serializers.IntegerField()
    quantidade_despesas = serializers.IntegerField()


class EstatisticasCategoriaSerializer(serializers.Serializer):
    """Serializer para estatísticas por categoria"""
    categoria_id = serializers.IntegerField()
    categoria_nome = serializers.CharField()
    categoria_tipo = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantidade = serializers.IntegerField()
    percentual = serializers.DecimalField(max_digits=5, decimal_places=2)
