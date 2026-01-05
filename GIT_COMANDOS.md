# 🎓 Git - Comandos Essenciais e Avançados

## 🚀 Comandos Básicos

### Configuração Inicial
```bash
# Configurar nome
git config --global user.name "Eduardo Luparele"

# Configurar email
git config --global user.email "seu-email@gmail.com"

# Verificar configurações
git config --list
```

### Iniciar Repositório
```bash
# Inicializar novo repositório
git init

# Clonar repositório existente
git clone https://github.com/Luparele/ELC_Contabil.git
```

### Comandos do Dia a Dia
```bash
# Ver status dos arquivos
git status

# Adicionar arquivos específicos
git add arquivo.py

# Adicionar todos os arquivos
git add .

# Commitar com mensagem
git commit -m "Mensagem descritiva"

# Adicionar e commitar em um comando
git commit -am "Mensagem"

# Enviar para o GitHub
git push

# Baixar atualizações
git pull
```

## 🌿 Trabalhando com Branches

```bash
# Criar nova branch
git branch nome-da-branch

# Mudar para outra branch
git checkout nome-da-branch

# Criar e mudar para nova branch
git checkout -b nova-feature

# Listar branches
git branch

# Listar todas as branches (incluindo remotas)
git branch -a

# Deletar branch local
git branch -d nome-da-branch

# Deletar branch remota
git push origin --delete nome-da-branch

# Mesclar branch na atual
git merge nome-da-branch
```

## 📝 Histórico e Logs

```bash
# Ver histórico de commits
git log

# Ver histórico resumido
git log --oneline

# Ver histórico com gráfico
git log --graph --oneline --all

# Ver alterações de um commit específico
git show hash-do-commit

# Ver quem modificou cada linha
git blame arquivo.py
```

## ⏪ Desfazer Alterações

```bash
# Desfazer alterações não commitadas
git checkout -- arquivo.py

# Remover arquivo do stage (após git add)
git reset HEAD arquivo.py

# Desfazer último commit (mantém alterações)
git reset --soft HEAD~1

# Desfazer último commit (remove alterações)
git reset --hard HEAD~1

# Reverter um commit específico
git revert hash-do-commit
```

## 🔄 Sincronização

```bash
# Adicionar repositório remoto
git remote add origin https://github.com/usuario/repo.git

# Ver repositórios remotos
git remote -v

# Buscar alterações (sem mesclar)
git fetch

# Baixar e mesclar
git pull

# Enviar branch específica
git push origin nome-da-branch

# Forçar push (CUIDADO!)
git push --force
```

## 🏷️ Tags (Versões)

```bash
# Criar tag
git tag v1.0.0

# Criar tag anotada
git tag -a v1.0.0 -m "Versão 1.0.0 - Lançamento inicial"

# Listar tags
git tag

# Enviar tag para remoto
git push origin v1.0.0

# Enviar todas as tags
git push --tags

# Deletar tag local
git tag -d v1.0.0

# Deletar tag remota
git push origin --delete v1.0.0
```

## 🔍 Comandos Úteis

```bash
# Ver diferenças não commitadas
git diff

# Ver diferenças entre commits
git diff commit1 commit2

# Ver arquivos modificados
git diff --name-only

# Buscar por texto nos commits
git log --grep="texto"

# Buscar commits de autor específico
git log --author="Eduardo"

# Ver tamanho do repositório
git count-objects -vH

# Limpar arquivos não rastreados
git clean -fd
```

## 🎯 Workflows Comuns

### Workflow para Nova Feature
```bash
# 1. Criar branch para feature
git checkout -b feature/nova-funcionalidade

# 2. Fazer alterações e commits
git add .
git commit -m "✨ feat: adiciona nova funcionalidade"

# 3. Voltar para main e atualizar
git checkout main
git pull

# 4. Mesclar feature na main
git merge feature/nova-funcionalidade

# 5. Enviar para GitHub
git push

# 6. Deletar branch da feature
git branch -d feature/nova-funcionalidade
```

### Workflow para Correção Rápida
```bash
# 1. Criar branch de hotfix
git checkout -b hotfix/corrige-bug

# 2. Fazer correção
git add .
git commit -m "🐛 fix: corrige bug crítico"

# 3. Voltar para main
git checkout main

# 4. Mesclar hotfix
git merge hotfix/corrige-bug

# 5. Enviar
git push

# 6. Deletar branch
git branch -d hotfix/corrige-bug
```

## 🎨 Emojis para Commits

| Emoji | Código | Uso |
|-------|--------|-----|
| 🎉 | `:tada:` | Initial commit |
| ✨ | `:sparkles:` | Nova feature |
| 🐛 | `:bug:` | Bug fix |
| 📚 | `:books:` | Documentação |
| 🎨 | `:art:` | UI/Style |
| ♻️ | `:recycle:` | Refactoring |
| 🚀 | `:rocket:` | Performance |
| 🔒 | `:lock:` | Segurança |
| 🔧 | `:wrench:` | Config |
| ✅ | `:white_check_mark:` | Testes |

### Exemplo de uso:
```bash
git commit -m "✨ feat: adiciona exportação para PDF"
git commit -m "🐛 fix: corrige erro no cálculo de saldo"
git commit -m "📚 docs: atualiza README com novas instruções"
```

## ⚠️ Dicas Importantes

### ✅ Boas Práticas
- Commits pequenos e frequentes
- Mensagens descritivas
- Sempre faça `git pull` antes de `git push`
- Use branches para features
- Revise antes de fazer merge

### ❌ Evite
- Commits muito grandes
- Mensagens genéricas ("fix", "update")
- Push direto na main sem review
- Commitar arquivos sensíveis (.env, db.sqlite3)
- Force push em branches compartilhadas

## 🆘 Emergências

### Commitei arquivo sensível
```bash
# Remover do último commit
git rm --cached arquivo-sensivel.txt
git commit --amend

# Se já fez push, precisa reescrever história (CUIDADO!)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch arquivo-sensivel.txt" \
  --prune-empty --tag-name-filter cat -- --all
```

### Perdi commits
```bash
# Ver histórico de referências
git reflog

# Recuperar commit perdido
git checkout hash-do-commit
```

## 📖 Recursos Adicionais

- **Documentação oficial:** https://git-scm.com/doc
- **Git Cheat Sheet:** https://education.github.com/git-cheat-sheet-education.pdf
- **Visualizador interativo:** https://git-school.github.io/visualizing-git/

---

**📌 Salve este arquivo para referência rápida!**

Desenvolvido por Eduardo Luparele
