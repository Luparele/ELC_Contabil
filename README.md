# 💼 ELC Contábil - Sistema de Gestão Financeira

Sistema web desenvolvido em Django para gestão financeira completa com controle de receitas, despesas, fornecedores, contas bancárias e categorias.

## ✨ Funcionalidades

### 🎯 Gestão Financeira Completa
- ✅ Controle de receitas e despesas
- ✅ Gestão de fornecedores
- ✅ Múltiplas contas bancárias
- ✅ Categorização de transações
- ✅ Sistema de alertas financeiros
- ✅ Filtros avançados por período, categoria e fornecedor

### 📊 Relatórios e Visualizações
- ✅ Dashboard interativo com gráficos
- ✅ Exportação para Excel
- ✅ Relatórios em PDF profissionais
- ✅ Análise de fluxo de caixa
- ✅ Integração com Power BI

### 🎨 Interface e Experiência
- ✅ Dark Mode / Light Mode
- ✅ Progressive Web App (PWA)
- ✅ Responsivo para mobile e desktop
- ✅ Interface moderna e intuitiva

## 🚀 Tecnologias

- **Backend:** Python 3.x, Django 5.2.7
- **Database:** SQLite (27 tabelas)
- **Frontend:** HTML5, CSS3, JavaScript
- **Relatórios:** ReportLab, OpenPyXL
- **PWA:** Service Workers, Web Manifest
- **BI:** Power BI Desktop com DAX

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/Luparele/ELC_Contabil.git
cd ELC_Contabil
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute as migrações
```bash
python manage.py migrate
```

### 5. Crie um superusuário
```bash
python manage.py createsuperuser
```

### 6. Execute o servidor
```bash
python manage.py runserver
```

Acesse: `http://localhost:8000`

## 📁 Estrutura do Projeto

```
ELC_Contabil/
├── APP/                        # Aplicação principal
│   ├── models.py              # Modelos de dados
│   ├── views.py               # Lógica de negócio
│   ├── urls.py                # Rotas
│   └── templates/             # Templates HTML
├── ELC_Contabil/              # Configurações do projeto
│   ├── settings.py            # Configurações Django
│   ├── urls.py                # URLs principais
│   └── wsgi.py                # WSGI config
├── media/                     # Upload de arquivos
├── staticfiles/               # Arquivos estáticos coletados
├── manage.py                  # Script de gerenciamento
├── requirements.txt           # Dependências Python
├── INSTRUCOES_POVOAR.md      # Instruções para popular BD
└── SUGESTOES_MELHORIAS.md    # Roadmap de melhorias
```

## 🔧 Configurações Importantes

### PWA (Progressive Web App)
O sistema está configurado como PWA e pode ser instalado em:
- ✅ Android (Chrome)
- ✅ Windows 11 (Edge/Chrome)
- ✅ iOS/iPadOS (Safari)

### Power BI Integration
O projeto inclui integração com Power BI:
- Database SQLite com 27 tabelas
- Relacionamentos configurados
- Medidas DAX para análises financeiras

## 📊 Funcionalidades Principais

### Dashboard
- Visão geral financeira
- Gráficos de receitas vs despesas
- Top fornecedores
- Alertas de vencimento

### Gestão de Transações
- CRUD completo
- Filtros avançados
- Busca por texto
- Ordenação customizável

### Fornecedores
- Cadastro completo
- Histórico de transações
- Análise de gastos por fornecedor

### Contas Bancárias
- Múltiplas contas
- Saldo consolidado
- Transferências entre contas

### Categorias
- Categorização personalizada
- Análise por categoria
- Relatórios segmentados

## 🎨 Temas

O sistema possui dois temas:
- 🌞 **Light Mode** - Tema claro padrão
- 🌙 **Dark Mode** - Tema escuro para reduzir fadiga visual

## 📱 Progressive Web App

Instale o ELC Contábil como aplicativo nativo:

1. Acesse o sistema pelo navegador
2. Clique no ícone de instalação
3. Confirme a instalação
4. Use como app nativo!

## 🔒 Segurança

- Autenticação de usuários
- Proteção CSRF
- Validação de dados
- Sanitização de inputs

## 📈 Exportações

### Excel
- Exportação completa de transações
- Formatação profissional
- Filtros preservados

### PDF
- Relatórios formatados
- Informações de fornecedores
- Layout profissional

## 🤝 Contribuindo

Este é um projeto privado. Para sugestões ou melhorias, consulte o arquivo `SUGESTOES_MELHORIAS.md`.

## 📄 Licença

Projeto de uso privado - Todos os direitos reservados.

## 👤 Autor

**Eduardo Luparele**
- Desenvolvimento e Manutenção
- GitHub: [@Luparele](https://github.com/Luparele)

## 🔄 Versão

**v2.0** - Sistema completo com PWA, Dark Mode e integração Power BI

---

⭐ **Sistema em produção e constantemente atualizado!**
