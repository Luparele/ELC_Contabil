"""
ViewSets da API REST para o ELC_Contabil
Endpoints completos para integração externa
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

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
from .serializers import (
    PerfilEmpresaSerializer,
    ContaBancariaSerializer,
    CategoriaSerializer,
    FornecedorSerializer,
    ReceitaSerializer,
    DespesaSerializer,
    DeclaracaoAnualSerializer,
    PreferenciaUsuarioSerializer,
    RelatorioMensalSerializer,
    EstatisticasCategoriaSerializer
)


class PerfilEmpresaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar Perfis de Empresa
    
    list: Lista todos os perfis
    create: Cria um novo perfil
    retrieve: Retorna um perfil específico
    update: Atualiza um perfil
    partial_update: Atualiza parcialmente um perfil
    destroy: Remove um perfil
    """
    queryset = PerfilEmpresa.objects.all()
    serializer_class = PerfilEmpresaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['cnpj', 'razao_social', 'nome_fantasia']
    ordering_fields = ['razao_social', 'cnpj']
    ordering = ['razao_social']


class ContaBancariaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar Contas Bancárias
    
    list: Lista todas as contas
    create: Cria uma nova conta
    retrieve: Retorna uma conta específica
    update: Atualiza uma conta
    partial_update: Atualiza parcialmente uma conta
    destroy: Remove uma conta
    preferencial: Marca uma conta como preferencial
    """
    queryset = ContaBancaria.objects.all()
    serializer_class = ContaBancariaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['perfil_empresa', 'preferencial']
    search_fields = ['nome_banco', 'agencia', 'conta_corrente']
    ordering_fields = ['nome_banco', 'agencia']
    ordering = ['nome_banco']
    
    @action(detail=True, methods=['post'])
    def preferencial(self, request, pk=None):
        """Marca esta conta como preferencial"""
        conta = self.get_object()
        conta.preferencial = True
        conta.save()
        serializer = self.get_serializer(conta)
        return Response(serializer.data)


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar Categorias
    
    list: Lista todas as categorias
    create: Cria uma nova categoria
    retrieve: Retorna uma categoria específica
    update: Atualiza uma categoria
    partial_update: Atualiza parcialmente uma categoria
    destroy: Remove uma categoria
    receitas: Lista categorias de receita
    despesas: Lista categorias de despesa
    ativar/desativar: Ativa ou desativa uma categoria
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'ativo', 'is_padrao']
    search_fields = ['nome']
    ordering_fields = ['nome', 'tipo']
    ordering = ['tipo', 'nome']
    
    def get_queryset(self):
        """Filtra categorias do usuário logado"""
        return Categoria.objects.filter(
            Q(usuario=self.request.user) | Q(is_padrao=True)
        )
    
    @action(detail=False, methods=['get'])
    def receitas(self, request):
        """Retorna apenas categorias de receita"""
        categorias = self.get_queryset().filter(tipo='R')
        serializer = self.get_serializer(categorias, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def despesas(self, request):
        """Retorna apenas categorias de despesa"""
        categorias = self.get_queryset().filter(tipo='D')
        serializer = self.get_serializer(categorias, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def ativar(self, request, pk=None):
        """Ativa uma categoria"""
        categoria = self.get_object()
        categoria.ativo = True
        categoria.save()
        serializer = self.get_serializer(categoria)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def desativar(self, request, pk=None):
        """Desativa uma categoria"""
        categoria = self.get_object()
        categoria.ativo = False
        categoria.save()
        serializer = self.get_serializer(categoria)
        return Response(serializer.data)


class FornecedorViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar Fornecedores
    
    list: Lista todos os fornecedores
    create: Cria um novo fornecedor
    retrieve: Retorna um fornecedor específico
    update: Atualiza um fornecedor
    partial_update: Atualiza parcialmente um fornecedor
    destroy: Remove um fornecedor
    ativos: Lista apenas fornecedores ativos
    pf: Lista apenas pessoas físicas
    pj: Lista apenas pessoas jurídicas
    """
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'ativo']
    search_fields = ['nome', 'nome_fantasia', 'cpf_cnpj', 'telefone', 'email']
    ordering_fields = ['nome', 'data_cadastro']
    ordering = ['nome']
    
    def get_queryset(self):
        """Filtra fornecedores do usuário logado"""
        return Fornecedor.objects.filter(usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Retorna apenas fornecedores ativos"""
        fornecedores = self.get_queryset().filter(ativo=True)
        serializer = self.get_serializer(fornecedores, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pf(self, request):
        """Retorna apenas pessoas físicas"""
        fornecedores = self.get_queryset().filter(tipo='PF')
        serializer = self.get_serializer(fornecedores, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pj(self, request):
        """Retorna apenas pessoas jurídicas"""
        fornecedores = self.get_queryset().filter(tipo='PJ')
        serializer = self.get_serializer(fornecedores, many=True)
        return Response(serializer.data)


class ReceitaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar Receitas
    
    list: Lista todas as receitas
    create: Cria uma nova receita
    retrieve: Retorna uma receita específica
    update: Atualiza uma receita
    partial_update: Atualiza parcialmente uma receita
    destroy: Remove uma receita
    periodo: Filtra receitas por período
    total: Retorna o total de receitas
    por_categoria: Agrupa receitas por categoria
    """
    queryset = Receita.objects.all()
    serializer_class = ReceitaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'fornecedor', 'data']
    search_fields = ['descricao']
    ordering_fields = ['data', 'valor', 'data_cadastro']
    ordering = ['-data', '-data_cadastro']
    
    def get_queryset(self):
        """Filtra receitas do usuário logado"""
        return Receita.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        """Ao criar, associa ao usuário logado"""
        serializer.save(usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def periodo(self, request):
        """
        Filtra receitas por período
        Query params: data_inicio, data_fim
        """
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        
        queryset = self.get_queryset()
        
        if data_inicio:
            queryset = queryset.filter(data__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data__lte=data_fim)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def total(self, request):
        """
        Retorna o total de receitas
        Query params: data_inicio, data_fim
        """
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        
        queryset = self.get_queryset()
        
        if data_inicio:
            queryset = queryset.filter(data__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data__lte=data_fim)
        
        total = queryset.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        
        return Response({
            'total': total,
            'quantidade': queryset.count(),
            'periodo': {
                'data_inicio': data_inicio,
                'data_fim': data_fim
            }
        })
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        """Agrupa receitas por categoria"""
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        
        queryset = self.get_queryset()
        
        if data_inicio:
            queryset = queryset.filter(data__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data__lte=data_fim)
        
        categorias = queryset.values(
            'categoria__id', 'categoria__nome', 'categoria__tipo'
        ).annotate(
            total=Sum('valor'),
            quantidade=Count('id')
        ).order_by('-total')
        
        return Response(categorias)


class DespesaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar Despesas
    
    list: Lista todas as despesas
    create: Cria uma nova despesa
    retrieve: Retorna uma despesa específica
    update: Atualiza uma despesa
    partial_update: Atualiza parcialmente uma despesa
    destroy: Remove uma despesa
    periodo: Filtra despesas por período
    total: Retorna o total de despesas
    por_categoria: Agrupa despesas por categoria
    """
    queryset = Despesa.objects.all()
    serializer_class = DespesaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'fornecedor', 'data']
    search_fields = ['descricao']
    ordering_fields = ['data', 'valor', 'data_cadastro']
    ordering = ['-data', '-data_cadastro']
    
    def get_queryset(self):
        """Filtra despesas do usuário logado"""
        return Despesa.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        """Ao criar, associa ao usuário logado"""
        serializer.save(usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def periodo(self, request):
        """
        Filtra despesas por período
        Query params: data_inicio, data_fim
        """
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        
        queryset = self.get_queryset()
        
        if data_inicio:
            queryset = queryset.filter(data__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data__lte=data_fim)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def total(self, request):
        """
        Retorna o total de despesas
        Query params: data_inicio, data_fim
        """
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        
        queryset = self.get_queryset()
        
        if data_inicio:
            queryset = queryset.filter(data__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data__lte=data_fim)
        
        total = queryset.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        
        return Response({
            'total': total,
            'quantidade': queryset.count(),
            'periodo': {
                'data_inicio': data_inicio,
                'data_fim': data_fim
            }
        })
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        """Agrupa despesas por categoria"""
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        
        queryset = self.get_queryset()
        
        if data_inicio:
            queryset = queryset.filter(data__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data__lte=data_fim)
        
        categorias = queryset.values(
            'categoria__id', 'categoria__nome', 'categoria__tipo'
        ).annotate(
            total=Sum('valor'),
            quantidade=Count('id')
        ).order_by('-total')
        
        return Response(categorias)


class DeclaracaoAnualViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar Declarações Anuais
    """
    queryset = DeclaracaoAnual.objects.all()
    serializer_class = DeclaracaoAnualSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['perfil_empresa', 'ano']
    ordering_fields = ['ano', 'data_confirmacao']
    ordering = ['-ano']


class PreferenciaUsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar Preferências de Usuário
    """
    queryset = PreferenciaUsuario.objects.all()
    serializer_class = PreferenciaUsuarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas as preferências do usuário logado"""
        return PreferenciaUsuario.objects.filter(usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def minhas(self, request):
        """Retorna as preferências do usuário logado"""
        preferencia, created = PreferenciaUsuario.objects.get_or_create(
            usuario=request.user
        )
        serializer = self.get_serializer(preferencia)
        return Response(serializer.data)


class RelatorioViewSet(viewsets.ViewSet):
    """
    API endpoint para relatórios e estatísticas
    
    dashboard: Dados consolidados do dashboard
    mensal: Relatório mensal detalhado
    anual: Relatório anual consolidado
    fluxo_caixa: Fluxo de caixa período
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """
        Retorna dados consolidados para o dashboard
        Query params: mes, ano
        """
        mes = request.query_params.get('mes', timezone.now().month)
        ano = request.query_params.get('ano', timezone.now().year)
        
        # Total de receitas e despesas do mês
        receitas_mes = Receita.objects.filter(
            usuario=request.user,
            data__month=mes,
            data__year=ano
        ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        
        despesas_mes = Despesa.objects.filter(
            usuario=request.user,
            data__month=mes,
            data__year=ano
        ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        
        # Saldo do mês
        saldo_mes = receitas_mes - despesas_mes
        
        # Total anual
        receitas_ano = Receita.objects.filter(
            usuario=request.user,
            data__year=ano
        ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        
        despesas_ano = Despesa.objects.filter(
            usuario=request.user,
            data__year=ano
        ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        
        return Response({
            'mes_atual': {
                'mes': mes,
                'ano': ano,
                'receitas': receitas_mes,
                'despesas': despesas_mes,
                'saldo': saldo_mes
            },
            'ano_atual': {
                'ano': ano,
                'receitas': receitas_ano,
                'despesas': despesas_ano,
                'saldo': receitas_ano - despesas_ano
            }
        })
    
    @action(detail=False, methods=['get'])
    def mensal(self, request):
        """
        Relatório mensal detalhado com todas as transações
        Query params: mes, ano
        """
        mes = request.query_params.get('mes', timezone.now().month)
        ano = request.query_params.get('ano', timezone.now().year)
        
        receitas = Receita.objects.filter(
            usuario=request.user,
            data__month=mes,
            data__year=ano
        )
        
        despesas = Despesa.objects.filter(
            usuario=request.user,
            data__month=mes,
            data__year=ano
        )
        
        receitas_serializer = ReceitaSerializer(receitas, many=True, context={'request': request})
        despesas_serializer = DespesaSerializer(despesas, many=True, context={'request': request})
        
        return Response({
            'periodo': {
                'mes': mes,
                'ano': ano
            },
            'resumo': {
                'total_receitas': receitas.aggregate(total=Sum('valor'))['total'] or Decimal('0.00'),
                'total_despesas': despesas.aggregate(total=Sum('valor'))['total'] or Decimal('0.00'),
                'quantidade_receitas': receitas.count(),
                'quantidade_despesas': despesas.count()
            },
            'receitas': receitas_serializer.data,
            'despesas': despesas_serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def anual(self, request):
        """
        Relatório anual consolidado por mês
        Query params: ano
        """
        ano = request.query_params.get('ano', timezone.now().year)
        
        meses = []
        for mes in range(1, 13):
            receitas = Receita.objects.filter(
                usuario=request.user,
                data__month=mes,
                data__year=ano
            ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
            
            despesas = Despesa.objects.filter(
                usuario=request.user,
                data__month=mes,
                data__year=ano
            ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
            
            meses.append({
                'mes': mes,
                'receitas': receitas,
                'despesas': despesas,
                'saldo': receitas - despesas
            })
        
        return Response({
            'ano': ano,
            'meses': meses
        })
    
    @action(detail=False, methods=['get'])
    def fluxo_caixa(self, request):
        """
        Fluxo de caixa para um período específico
        Query params: data_inicio, data_fim
        """
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        
        if not data_inicio or not data_fim:
            return Response(
                {'error': 'data_inicio e data_fim são obrigatórios'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        receitas = Receita.objects.filter(
            usuario=request.user,
            data__gte=data_inicio,
            data__lte=data_fim
        )
        
        despesas = Despesa.objects.filter(
            usuario=request.user,
            data__gte=data_inicio,
            data__lte=data_fim
        )
        
        total_receitas = receitas.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        total_despesas = despesas.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        
        return Response({
            'periodo': {
                'data_inicio': data_inicio,
                'data_fim': data_fim
            },
            'receitas': {
                'total': total_receitas,
                'quantidade': receitas.count()
            },
            'despesas': {
                'total': total_despesas,
                'quantidade': despesas.count()
            },
            'saldo': total_receitas - total_despesas
        })
