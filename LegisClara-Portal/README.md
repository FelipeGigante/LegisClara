# LegisClara Portal Administrativo

Portal web para controle e gerenciamento da pipeline LegisClara.

## 📋 Funcionalidades

- ✅ **Sistema de Login** - Autenticação mockada para demonstração
- 🎛️ **Dashboard** - Visão geral de estatísticas e métricas
- ▶️ **Controle de Pipeline** - Iniciar/parar processos de forma visual
- 📊 **Atividades** - Registro de execuções e logs
- ⚙️ **Configurações** - Ajustes de parâmetros do sistema

## 🚀 Como Usar

### 1. Abrir o Portal

Abra o arquivo `index.html` no navegador ou use um servidor HTTP local:

```bash
# Opção 1: Servidor Python simples
cd LegisClara-Portal
python -m http.server 8000
# Acesse: http://localhost:8000

# Opção 2: Live Server (VS Code)
# Clique com botão direito em index.html > Open with Live Server
```

### 2. Fazer Login

Use uma das credenciais de demonstração:

- **Usuário:** `admin` | **Senha:** `legisla2024`
- **Usuário:** `parlamentar` | **Senha:** `demo123`
- **Usuário:** `assessor` | **Senha:** `legisla2024`

### 3. Usar o Dashboard

Após login, você terá acesso a:

- **Dashboard**: Métricas e início rápido
- **Controle Pipeline**: Execução manual da pipeline
- **Atividades**: Histórico de logs
- **Configurações**: Toggles de funcionalidades

## 🔌 API Backend (Opcional)

Para integração real com o LegisClara-System, inicie a API:

```bash
cd LegisClara-Portal
pip install flask flask-cors
python api.py
```

A API estará disponível em `http://localhost:5000`

### Endpoints Disponíveis

- `GET /api/status` - Status do sistema
- `POST /api/pipeline/start` - Iniciar pipeline completa
- `POST /api/pipeline/collect` - Coletar apenas proposições
- `GET /api/videos/list` - Listar vídeos gerados
- `GET /api/logs/recent` - Logs recentes
- `GET /api/stats` - Estatísticas gerais

## 🎨 Estrutura de Arquivos

```
LegisClara-Portal/
├── index.html          # Página de login
├── dashboard.html      # Dashboard administrativo
├── api.py             # API REST Flask (opcional)
└── README.md          # Este arquivo
```

## 🔐 Segurança

⚠️ **IMPORTANTE**: Este é um sistema de demonstração!

- As credenciais são mockadas (hardcoded)
- Não há criptografia real
- Sessão é armazenada em `sessionStorage`

**Para produção, implemente:**
- Autenticação real (JWT, OAuth)
- HTTPS obrigatório
- Rate limiting
- Validação de inputs
- Logs de auditoria

## 🎯 Próximos Passos

Para tornar este portal totalmente funcional:

1. ✅ Integrar com a API Flask
2. ✅ Conectar botões do dashboard aos endpoints
3. ✅ Adicionar websockets para atualizações em tempo real
4. ✅ Implementar upload de configurações (.env)
5. ✅ Criar visualização de vídeos gerados

## 📝 Notas

- O portal é 100% responsivo
- Design baseado na identidade visual da Clara
- Sem dependências externas (apenas CDNs de fontes/ícones)
