# 🚀 Início Rápido - LegisClara Portal

## Opção 1: Apenas Frontend (Mais Simples)

### Passo 1: Abrir no Navegador

Simplesmente abra o arquivo `index.html` diretamente no navegador:

```
LegisClara-Portal/index.html
```

### Passo 2: Fazer Login

Use as credenciais:
- **Usuário:** `admin`
- **Senha:** `legisla2024`

### Passo 3: Explorar

Navegue pelas seções do dashboard! Os botões mostrarão alerts simulando as ações.

---

## Opção 2: Com API Backend (Integração Real)

### Passo 1: Instalar Dependências

```bash
cd LegisClara-Portal
pip install -r requirements.txt
```

### Passo 2: Iniciar API

```bash
python api.py
```

Você verá:
```
🚀 LegisClara Portal API
📁 System Path: C:\...\LegisClara-System
🌐 Server: http://localhost:5000
```

### Passo 3: Abrir Frontend

Em outro terminal ou simplesmente abra `index.html` no navegador.

### Passo 4: Testar Integração

No dashboard, clique em "Iniciar Pipeline Completa". Agora fará requisições reais à API!

---

## 🎯 Funcionalidades Disponíveis

### Dashboard Principal
- ✅ Estatísticas em tempo real
- ✅ Botão de início rápido da pipeline
- ✅ Cards de métricas

### Controle de Pipeline
- ✅ Parâmetros configuráveis
- ✅ Seleção de tipos de proposição
- ✅ Limite de vídeos por execução

### Atividades
- ✅ Log histórico de execuções
- ✅ Registro de eventos do sistema

### Configurações
- ✅ Toggles de funcionalidades
- ✅ Ativação/desativação de módulos

---

## 🔧 Personalização

### Alterar Credenciais

Edite `index.html` linha ~175:

```javascript
const validCredentials = {
    'admin': 'legisla2024',
    'seuUsuario': 'suaSenha'  // Adicione aqui
};
```

### Adicionar Novos Usuários

```javascript
'parlamentar': 'senha123',
'assessor': 'legisla2024',
'gestor': 'minhasenha'
```

---

## 📡 Endpoints da API

Se estiver usando a API:

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/status` | GET | Status do sistema |
| `/api/pipeline/start` | POST | Inicia pipeline completa |
| `/api/pipeline/collect` | POST | Coleta proposições |
| `/api/videos/list` | GET | Lista vídeos gerados |
| `/api/logs/recent` | GET | Logs recentes |
| `/api/stats` | GET | Estatísticas |

---

## 🎨 Estrutura Visual

```
┌─────────────────────────────────────────┐
│  LegisClara Portal                      │
├─────────────────────────────────────────┤
│                                         │
│  [Login Page]                           │
│    └─> [Dashboard]                      │
│           ├─> Stats Cards               │
│           ├─> Pipeline Controls         │
│           ├─> Activity Log              │
│           └─> Settings                  │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🔐 Notas de Segurança

⚠️ **DEMO APENAS!**

Este portal é para demonstração. Para produção:

1. Implemente autenticação real (JWT/OAuth)
2. Use HTTPS
3. Adicione validação server-side
4. Implemente rate limiting
5. Use variáveis de ambiente para secrets
6. Configure CORS adequadamente

---

## 💡 Próximos Passos

Depois de explorar o portal:

1. ✅ Integre com a API real
2. ✅ Adicione websockets para updates ao vivo
3. ✅ Implemente upload de arquivos .env
4. ✅ Crie player de vídeos inline
5. ✅ Adicione gráficos de analytics

---

## 🐛 Problemas Comuns

### API não conecta

```bash
# Verifique se está rodando
curl http://localhost:5000/api/status

# Reinstale dependências
pip install -r requirements.txt --force-reinstall
```

### Erro de CORS

A API já tem CORS habilitado. Se persistir:
- Verifique se está acessando via `http://` não `file://`
- Use um servidor HTTP local

### Sessão não persiste

Normal! Usa `sessionStorage`. Ao fechar navegador, perde sessão.

---

Pronto! 🎉 Agora você tem um portal administrativo completo!
