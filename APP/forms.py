from django import forms
from .models import Despesa, Receita, Categoria, PerfilEmpresa, ContaBancaria, Fornecedor, DASN_SIMEI

class DespesaForm(forms.ModelForm):
    # Campo adicional para cadastro rápido de fornecedor
    novo_fornecedor = forms.CharField(
        max_length=255, 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o nome para criar novo fornecedor'
        }),
        label='Ou criar novo fornecedor'
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(tipo='D').order_by('nome')
        
        # Filtrar fornecedores do usuário logado
        if user:
            self.fields['fornecedor'].queryset = Fornecedor.objects.filter(
                usuario=user, 
                ativo=True
            ).order_by('nome')
            self.fields['fornecedor'].required = False

    class Meta:
        model = Despesa
        fields = ['descricao', 'valor', 'data', 'categoria', 'fornecedor', 'comprovante']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'fornecedor': forms.Select(attrs={'class': 'form-select'}),
            'comprovante': forms.FileInput(attrs={'class': 'form-control'}),
        }


# --- FORMULÁRIO DE RECEITA ATUALIZADO ---
class ReceitaForm(forms.ModelForm):
    # Campo adicional para cadastro rápido de cliente/fornecedor
    novo_fornecedor = forms.CharField(
        max_length=255, 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o nome para criar novo cliente'
        }),
        label='Ou criar novo cliente'
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(tipo='R').order_by('nome')
        
        # Filtrar fornecedores do usuário logado
        if user:
            self.fields['fornecedor'].queryset = Fornecedor.objects.filter(
                usuario=user, 
                ativo=True
            ).order_by('nome')
            self.fields['fornecedor'].required = False

    class Meta:
        model = Receita
        fields = ['descricao', 'valor', 'data', 'categoria', 'fornecedor', 'comprovante']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'fornecedor': forms.Select(attrs={'class': 'form-select'}),
            'comprovante': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'tipo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }

class PerfilEmpresaForm(forms.ModelForm):
    class Meta:
        model = PerfilEmpresa
        # Lista de todos os campos que aparecerão no formulário
        fields = [
            'cnpj', 'razao_social', 'nome_fantasia', 'ramo_atividade',
            'logradouro', 'numero', 'complemento', 'bairro', 'municipio',
            'uf', 'cep'
        ]
        # Aplica classes do Bootstrap para estilização
        widgets = {
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-control'}),
            'ramo_atividade': forms.TextInput(attrs={'class': 'form-control'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control'}),
            'uf': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ContaBancariaForm(forms.ModelForm):
    class Meta:
        model = ContaBancaria
        fields = ['nome_banco', 'codigo_banco', 'agencia', 'conta_corrente', 'preferencial']
        widgets = {
            'nome_banco': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_banco': forms.TextInput(attrs={'class': 'form-control'}),
            'agencia': forms.TextInput(attrs={'class': 'form-control'}),
            'conta_corrente': forms.TextInput(attrs={'class': 'form-control'}),
            'preferencial': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        # CNPJ em primeiro para facilitar autocomplete
        fields = [
            'cpf_cnpj', 'tipo', 'nome', 'nome_fantasia',
            'telefone', 'email', 'cep', 'logradouro', 'numero',
            'complemento', 'bairro', 'municipio', 'uf',
            'observacoes', 'ativo'
        ]
        widgets = {
            'cpf_cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o CNPJ para buscar automaticamente',
                'id': 'id_cpf_cnpj'
            }),
            'tipo': forms.Select(attrs={'class': 'form-select', 'id': 'id_tipo'}),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo ou Razão Social',
                'id': 'id_nome'
            }),
            'nome_fantasia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome Fantasia (opcional)',
                'id': 'id_nome_fantasia'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000',
                'id': 'id_telefone'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com',
                'id': 'id_email'
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-000',
                'id': 'id_cep'
            }),
            'logradouro': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_logradouro'
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_numero'
            }),
            'complemento': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_complemento'
            }),
            'bairro': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_bairro'
            }),
            'municipio': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_municipio'
            }),
            'uf': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '2',
                'style': 'text-transform: uppercase;',
                'id': 'id_uf'
            }),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DASN_SIMEIForm(forms.ModelForm):
    """Formulário para DASN-SIMEI"""
    
    class Meta:
        model = DASN_SIMEI
        fields = [
            'ano_calendario',
            'valor_bruto_anual',
            'declarada',
            'data_envio',
            'comprovante_pdf',
            'observacoes'
        ]
        widgets = {
            'ano_calendario': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 2024',
                'min': '2008',
                'max': '2099'
            }),
            'valor_bruto_anual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'R$ 0,00'
            }),
            'declarada': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'data_envio': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'comprovante_pdf': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Informações adicionais sobre a declaração...'
            })
        }
        labels = {
            'ano_calendario': 'Ano Calendário',
            'valor_bruto_anual': 'Valor Bruto Anual (R$)',
            'declarada': 'Declaração Enviada?',
            'data_envio': 'Data de Envio',
            'comprovante_pdf': 'Comprovante (PDF)',
            'observacoes': 'Observações'
        }
    
    def clean_comprovante_pdf(self):
        """Valida se o arquivo é PDF"""
        arquivo = self.cleaned_data.get('comprovante_pdf')
        if arquivo:
            if not arquivo.name.endswith('.pdf'):
                raise forms.ValidationError('Apenas arquivos PDF são permitidos.')
            if arquivo.size > 5 * 1024 * 1024:
                raise forms.ValidationError('O arquivo não pode exceder 5MB.')
        return arquivo
    
    def clean(self):
        """Validação customizada"""
        cleaned_data = super().clean()
        declarada = cleaned_data.get('declarada')
        data_envio = cleaned_data.get('data_envio')
        
        if declarada and not data_envio:
            self.add_error('data_envio', 'Informe a data de envio da declaração.')
        
        return cleaned_data