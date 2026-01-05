"""
Script de exemplo para testar a API REST do ELC Contabil
Demonstra como fazer chamadas para os principais endpoints

Autor: Eduardo Luiz
Data: 2024
"""

import requests
from datetime import datetime, timedelta
import json

# Configuração base
BASE_URL = "http://localhost:8000/api/v1"
USERNAME = "Luparele"  # Altere para seu usuário
PASSWORD = "@Ed7148755"     # Altere para sua senha

# Configurar autenticação
auth = (USERNAME, PASSWORD)

# Headers
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def print_response(title, response):
    """Imprime a resposta formatada"""
    print(f"\n{'='*80}")
    print(f"🔹 {title}")
    print(f"{'='*80}")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code in [200, 201]:
        print(f"✅ Sucesso!")
        try:
            data = response.json()
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except:
            print(response.text)
    else:
        print(f"❌ Erro!")
        print(response.text)


def exemplo_1_listar_categorias():
    """Exemplo 1: Listar todas as categorias"""
    url = f"{BASE_URL}/categorias/"
    response = requests.get(url, auth=auth, headers=headers)
    print_response("Exemplo 1: Listar Categorias", response)
    return response


def exemplo_2_criar_fornecedor():
    """Exemplo 2: Criar um novo fornecedor"""
    url = f"{BASE_URL}/fornecedores/"
    data = {
        "tipo": "PJ",
        "nome": "Fornecedor Teste API",
        "nome_fantasia": "Teste API",
        "cpf_cnpj": "12.345.678/0001-99",
        "telefone": "(11) 98765-4321",
        "email": "teste@api.com.br",
        "ativo": True,
        "usuario": 2  # ID do usuário
    }
    response = requests.post(url, auth=auth, headers=headers, json=data)
    print_response("Exemplo 2: Criar Fornecedor", response)
    return response


def exemplo_3_criar_receita(categoria_id=None, fornecedor_id=None):
    """Exemplo 3: Criar uma nova receita"""
    url = f"{BASE_URL}/receitas/"
    data = {
        "descricao": "Venda Teste via API",
        "valor": 2500.00,
        "data": datetime.now().strftime("%Y-%m-%d"),
        "observacoes": "Receita criada via API de teste",
        "usuario": 2  # ID do usuário
    }
    
    if categoria_id:
        data["categoria"] = categoria_id
    if fornecedor_id:
        data["fornecedor"] = fornecedor_id
    
    response = requests.post(url, auth=auth, headers=headers, json=data)
    print_response("Exemplo 3: Criar Receita", response)
    return response


def exemplo_4_criar_despesa(categoria_id=None, fornecedor_id=None):
    """Exemplo 4: Criar uma nova despesa"""
    url = f"{BASE_URL}/despesas/"
    data = {
        "descricao": "Despesa Teste via API",
        "valor": 850.00,
        "data": datetime.now().strftime("%Y-%m-%d"),
        "observacoes": "Despesa criada via API de teste",
        "usuario": 2  # ID do usuário
    }
    
    if categoria_id:
        data["categoria"] = categoria_id
    if fornecedor_id:
        data["fornecedor"] = fornecedor_id
    
    response = requests.post(url, auth=auth, headers=headers, json=data)
    print_response("Exemplo 4: Criar Despesa", response)
    return response


def exemplo_5_listar_receitas_periodo():
    """Exemplo 5: Listar receitas de um período"""
    # Últimos 30 dias
    data_fim = datetime.now()
    data_inicio = data_fim - timedelta(days=30)
    
    url = f"{BASE_URL}/receitas/periodo/"
    params = {
        "data_inicio": data_inicio.strftime("%Y-%m-%d"),
        "data_fim": data_fim.strftime("%Y-%m-%d")
    }
    
    response = requests.get(url, auth=auth, headers=headers, params=params)
    print_response("Exemplo 5: Receitas dos últimos 30 dias", response)
    return response


def exemplo_6_total_receitas_despesas():
    """Exemplo 6: Obter totais de receitas e despesas"""
    # Mês atual
    hoje = datetime.now()
    data_inicio = f"{hoje.year}-{hoje.month:02d}-01"
    data_fim = hoje.strftime("%Y-%m-%d")
    
    # Total de receitas
    url_receitas = f"{BASE_URL}/receitas/total/"
    params = {
        "data_inicio": data_inicio,
        "data_fim": data_fim
    }
    response_receitas = requests.get(url_receitas, auth=auth, headers=headers, params=params)
    print_response("Exemplo 6a: Total de Receitas do Mês", response_receitas)
    
    # Total de despesas
    url_despesas = f"{BASE_URL}/despesas/total/"
    response_despesas = requests.get(url_despesas, auth=auth, headers=headers, params=params)
    print_response("Exemplo 6b: Total de Despesas do Mês", response_despesas)
    
    # Calcular saldo
    if response_receitas.status_code == 200 and response_despesas.status_code == 200:
        receitas = response_receitas.json()['total']
        despesas = response_despesas.json()['total']
        saldo = float(receitas) - float(despesas)
        
        print(f"\n{'='*80}")
        print(f"💰 RESUMO FINANCEIRO DO MÊS")
        print(f"{'='*80}")
        print(f"✅ Receitas: R$ {receitas:,.2f}")
        print(f"❌ Despesas: R$ {despesas:,.2f}")
        print(f"{'📊 Saldo: R$ ' + f'{saldo:,.2f}' if saldo >= 0 else '⚠️ Déficit: R$ ' + f'{abs(saldo):,.2f}'}")


def exemplo_7_dashboard():
    """Exemplo 7: Obter dados do dashboard"""
    hoje = datetime.now()
    url = f"{BASE_URL}/relatorios/dashboard/"
    params = {
        "mes": hoje.month,
        "ano": hoje.year
    }
    
    response = requests.get(url, auth=auth, headers=headers, params=params)
    print_response("Exemplo 7: Dashboard Atual", response)
    return response


def exemplo_8_relatorio_mensal():
    """Exemplo 8: Relatório mensal completo"""
    hoje = datetime.now()
    url = f"{BASE_URL}/relatorios/mensal/"
    params = {
        "mes": hoje.month,
        "ano": hoje.year
    }
    
    response = requests.get(url, auth=auth, headers=headers, params=params)
    print_response("Exemplo 8: Relatório Mensal Completo", response)
    return response


def exemplo_9_categorias_receitas_despesas():
    """Exemplo 9: Listar receitas e despesas por categoria"""
    hoje = datetime.now()
    data_inicio = f"{hoje.year}-{hoje.month:02d}-01"
    data_fim = hoje.strftime("%Y-%m-%d")
    params = {
        "data_inicio": data_inicio,
        "data_fim": data_fim
    }
    
    # Receitas por categoria
    url_receitas = f"{BASE_URL}/receitas/por_categoria/"
    response_receitas = requests.get(url_receitas, auth=auth, headers=headers, params=params)
    print_response("Exemplo 9a: Receitas por Categoria", response_receitas)
    
    # Despesas por categoria
    url_despesas = f"{BASE_URL}/despesas/por_categoria/"
    response_despesas = requests.get(url_despesas, auth=auth, headers=headers, params=params)
    print_response("Exemplo 9b: Despesas por Categoria", response_despesas)


def exemplo_10_buscar_fornecedores():
    """Exemplo 10: Buscar fornecedores"""
    url = f"{BASE_URL}/fornecedores/"
    
    # Buscar por nome
    params = {"search": "teste"}
    response = requests.get(url, auth=auth, headers=headers, params=params)
    print_response("Exemplo 10: Buscar Fornecedores", response)
    
    return response


def exemplo_11_fluxo_caixa():
    """Exemplo 11: Fluxo de caixa do período"""
    hoje = datetime.now()
    data_fim = hoje
    data_inicio = hoje - timedelta(days=90)  # Últimos 90 dias
    
    url = f"{BASE_URL}/relatorios/fluxo_caixa/"
    params = {
        "data_inicio": data_inicio.strftime("%Y-%m-%d"),
        "data_fim": data_fim.strftime("%Y-%m-%d")
    }
    
    response = requests.get(url, auth=auth, headers=headers, params=params)
    print_response("Exemplo 11: Fluxo de Caixa (90 dias)", response)
    return response


def exemplo_12_atualizar_receita(receita_id):
    """Exemplo 12: Atualizar uma receita existente"""
    url = f"{BASE_URL}/receitas/{receita_id}/"
    data = {
        "descricao": "Receita Atualizada via API",
        "valor": 3000.00,
        "observacoes": "Valor atualizado"
    }
    
    response = requests.patch(url, auth=auth, headers=headers, json=data)
    print_response("Exemplo 12: Atualizar Receita", response)
    return response


def main():
    """Função principal - executa todos os exemplos"""
    print(f"""
    {'='*80}
    🚀 EXEMPLOS DE USO DA API REST - ELC CONTABIL
    {'='*80}
    
    Este script demonstra as principais funcionalidades da API.
    
    ⚠️  Certifique-se de:
    1. Ter o servidor rodando: python manage.py runserver
    2. Configurar USERNAME e PASSWORD no início deste arquivo
    3. Ter pelo menos uma categoria cadastrada
    
    {'='*80}
    """)
    
    input("Pressione ENTER para começar os testes...")
    
    # Executar exemplos
    try:
        # 1. Listar categorias
        exemplo_1_listar_categorias()
        
        # 2. Criar fornecedor
        resp_fornecedor = exemplo_2_criar_fornecedor()
        fornecedor_id = None
        if resp_fornecedor.status_code == 201:
            fornecedor_id = resp_fornecedor.json().get('id')
        
        # 3 e 4. Criar receita e despesa
        exemplo_3_criar_receita(fornecedor_id=fornecedor_id)
        exemplo_4_criar_despesa(fornecedor_id=fornecedor_id)
        
        # 5. Listar receitas do período
        exemplo_5_listar_receitas_periodo()
        
        # 6. Totais
        exemplo_6_total_receitas_despesas()
        
        # 7. Dashboard
        exemplo_7_dashboard()
        
        # 8. Relatório mensal
        exemplo_8_relatorio_mensal()
        
        # 9. Por categoria
        exemplo_9_categorias_receitas_despesas()
        
        # 10. Buscar fornecedores
        exemplo_10_buscar_fornecedores()
        
        # 11. Fluxo de caixa
        exemplo_11_fluxo_caixa()
        
        print(f"\n{'='*80}")
        print("✅ Todos os exemplos foram executados!")
        print(f"{'='*80}\n")
        
        print("""
        📚 Para mais informações:
        - Swagger UI: http://localhost:8000/swagger/
        - ReDoc: http://localhost:8000/redoc/
        - Documentação: API_DOCUMENTATION.md
        """)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Não foi possível conectar à API.")
        print("Certifique-se de que o servidor está rodando:")
        print("   python manage.py runserver")
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")


if __name__ == "__main__":
    main()
