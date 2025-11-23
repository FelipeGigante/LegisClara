# 🏛️ LegisClara - Versão n8n

Sistema automatizado de engajamento cidadão em discussões legislativas usando **n8n** (plataforma de automação visual).

## 🎯 Por que n8n?

- ✅ **Interface Visual** - Não precisa programar, apenas conectar nós
- ✅ **Sem FFmpeg** - Usa D-ID direto (com créditos gratuitos)
- ✅ **Fácil Depuração** - Vê dados fluindo entre etapas
- ✅ **Hospedagem Grátis** - n8n Cloud tem plano free
- ✅ **Integrações Prontas** - Instagram, OpenAI, Supabase nativos

## 📊 Fluxo do Workflow

```
1. Trigger (09:00 diário)
   ↓
2. Coletar Senado + Câmara (APIs abertas)
   ↓
3. Unir e Normalizar Dados
   ↓
4. Processar com OpenAI (ChatGPT-4)
   ↓
5. Gerar Áudio (ElevenLabs - voz PT-BR)
   ↓
6. Gerar Vídeo (D-ID - avatar animado, GRÁTIS)
   ↓
7. Upload Supabase (storage grátis)
   ↓
8. Publicar Instagram (Reels)
   ↓
9. Salvar no Banco + Notificar
```

## 🚀 Instalação

### Opção 1: n8n Cloud (Recomendado para Iniciantes)

1. Acesse https://n8n.io e crie conta grátis
2. Faça login no dashboard
3. Clique em "Workflows" → "Import from File"
4. Selecione `workflows/legisclara-workflow.json`
5. Configure credenciais (veja seção abaixo)

### Opção 2: n8n Self-Hosted (Docker)

```bash
# Instalar n8n via Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Acessar http://localhost:5678
# Importar workflow: workflows/legisclara-workflow.json
```

### Opção 3: n8n Desktop (Windows/Mac/Linux)

1. Baixe de https://n8n.io/download
2. Instale e execute
3. Acesse http://localhost:5678
4. Importe o workflow

## ⚙️ Configuração de Credenciais

Após importar o workflow, configure estas credenciais no n8n:

### 1. OpenAI API (ChatGPT)

```
Tipo: OpenAI
Nome: OpenAI API
API Key: sk-...
```

**Como obter:**
- https://platform.openai.com/api-keys
- Custo: ~$0.50 por 100 legislações processadas

### 2. ElevenLabs (Text-to-Speech)

```
Tipo: HTTP Header Auth
Nome: ElevenLabs API Key
Header: xi-api-key
Value: <sua-chave>
```

**Como obter:**
- https://elevenlabs.io/app/settings/api-keys
- Plano gratuito: 10.000 caracteres/mês
- Voz recomendada: `21m00Tcm4TlvDq8ikWAM` (Rachel - Multilingual)

### 3. D-ID (Avatar Vídeo) - GRÁTIS! 🎉

```
Tipo: HTTP Header Auth
Nome: D-ID API Key
Header: Authorization
Value: Basic <sua-chave-base64>
```

**Como obter CRÉDITOS GRÁTIS:**
1. Acesse https://studio.d-id.com/
2. Crie conta (14 dias trial)
3. Vá em "API" → "Create API Key"
4. **IMPORTANTE:** Você tem créditos grátis para ~20-50 vídeos!

**Converter chave para Base64:**
```bash
echo -n "sua-api-key-aqui:" | base64
```

### 4. Supabase (Storage + Banco)

```
Tipo: Supabase
Nome: Supabase
Project URL: https://xxx.supabase.co
Service Role Key: eyJhb...
```

**Setup Supabase (GRÁTIS):**

1. Crie projeto em https://supabase.com
2. Vá em "Storage" → Criar bucket "videos" (público)
3. Copie credenciais de "Project Settings" → "API"
4. Crie tabela de publicações:

```sql
CREATE TABLE publicacoes (
  id BIGSERIAL PRIMARY KEY,
  legislacao_id TEXT NOT NULL,
  plataforma TEXT NOT NULL,
  post_id TEXT,
  url TEXT,
  caption TEXT,
  video_url TEXT,
  status TEXT DEFAULT 'pendente',
  data_publicacao TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_legislacao ON publicacoes(legislacao_id);
CREATE INDEX idx_status ON publicacoes(status);
```

### 5. Instagram Business API

```
Tipo: Instagram OAuth2
Nome: Instagram Business
Client ID: <seu-app-id>
Client Secret: <seu-app-secret>
User ID: <seu-instagram-business-id>
```

**Setup Instagram API:**

1. Acesse https://developers.facebook.com/
2. Crie app → "Business" type
3. Adicione produto "Instagram Graph API"
4. Configure Instagram Business Account
5. Gere Access Token de longa duração (60 dias)

**Tutorial completo:**
https://developers.facebook.com/docs/instagram-api/getting-started

### 6. Email (SMTP - Opcional)

```
Tipo: SMTP
Nome: Gmail SMTP
Host: smtp.gmail.com
Port: 587
User: seu-email@gmail.com
Password: <senha-de-app>
```

**Senha de App Gmail:**
1. Ative 2FA em https://myaccount.google.com/security
2. Gere senha: https://myaccount.google.com/apppasswords

## 🎮 Como Usar

### Teste Manual (Primeira Execução)

1. Abra workflow no n8n
2. Clique em "Execute Workflow" (botão ▶️)
3. Acompanhe cada nó acendendo (verde = sucesso, vermelho = erro)
4. Clique em cada nó para ver dados processados
5. Verifique vídeo gerado no Supabase Storage
6. Confira publicação no Instagram

### Execução Automática (Produção)

O workflow está configurado para rodar **diariamente às 09:00**.

Para ativar:
1. Clique em "Active" (toggle no topo do workflow)
2. O n8n executará automaticamente todos os dias

### Monitoramento

**Ver histórico de execuções:**
1. Menu lateral → "Executions"
2. Veja sucessos/falhas
3. Clique para debug detalhado

**Alertas:**
- Configure webhook do Discord/Slack no nó "16. Notificação Final"
- Receba alerta a cada execução

## 💰 Custos Mensais (Processando 100 Legislações/Mês)

| Serviço | Custo | Plano Gratuito |
|---------|-------|----------------|
| **n8n Cloud** | $0-20/mês | 5.000 execuções grátis |
| **OpenAI GPT-4** | ~$15-30/mês | $5 crédito inicial |
| **ElevenLabs** | $0-5/mês | 10k chars grátis |
| **D-ID** | $0-49/mês | **Créditos trial grátis!** |
| **Supabase** | $0 | 500MB storage grátis |
| **Instagram API** | $0 | Totalmente grátis |
| **TOTAL** | **$20-104/mês** | **MVP possível 100% grátis!** |

## 🔧 Personalização

### Mudar Voz (ElevenLabs)

No nó "7. Gerar Áudio", altere `voice_id`:

```json
// Vozes em Português:
"21m00Tcm4TlvDq8ikWAM"  // Rachel (Feminina, calma)
"pNInz6obpgDQGcFmaJgB"  // Adam (Masculina, forte)
"yoZ06aMxZJJ28mfd3POQ"  // Sam (Neutro, jornalístico)
```

Liste todas: https://api.elevenlabs.io/v1/voices

### Mudar Avatar (D-ID)

No nó "8. Gerar Vídeo (D-ID)", altere `source_url`:

```
// Avatar padrão D-ID (gratuito)
https://create-images-results.d-id.com/google-oauth2%7C103908445571603294059/upl_JRxp-Y0tgdoEuHqvlmxnv/image.png

// Seu próprio avatar (upload na D-ID)
https://create-images-results.d-id.com/seu-usuario/seu-avatar.jpg
```

### Filtrar Tipos de Legislação

No nó "4. Normalizar Dados", adicione filtro:

```javascript
// Apenas PECs e PLs importantes
const tiposPermitidos = ['PEC', 'PL', 'MP'];
legislacoes = legislacoes.filter(leg => tiposPermitidos.includes(leg.tipo));
```

### Adicionar LinkedIn

1. Duplique nó "13. Publicar Instagram"
2. Altere para nó "LinkedIn"
3. Configure OAuth do LinkedIn
4. Conecte após nó "12. Gerar Caption"

## 🐛 Troubleshooting

### Erro: "OpenAI API Rate Limit"

**Solução:** Adicione nó "Wait" (5 segundos) entre processamentos.

### Erro: "D-ID - Insufficient Credits"

**Soluções:**
1. Verifique créditos em https://studio.d-id.com/
2. Use avatar diferente (alguns consomem mais)
3. Reduza qualidade do vídeo em `config`

### Erro: "Instagram - Invalid Access Token"

**Solução:**
- Tokens expiram a cada 60 dias
- Regenere em https://developers.facebook.com/tools/explorer/
- Configure renovação automática (avançado)

### Erro: "Supabase - Storage Upload Failed"

**Verificar:**
1. Bucket "videos" existe?
2. Bucket é público?
3. Service Role Key está correta?

### Vídeo D-ID demora muito

**Normal!** D-ID leva 2-5 minutos por vídeo.

O nó "9. Aguardar Processamento" faz polling a cada 10 segundos (máx 5 minutos).

Se timeout:
- Aumente `maxAttempts` no código
- Ou processe em lote menor (1-2 vídeos por vez)

## 📈 Otimizações

### Reduzir Custos

1. **Usar GPT-3.5 em vez de GPT-4:**
   - No nó "5. Processar com OpenAI"
   - Altere modelo para `gpt-3.5-turbo`
   - Custo cai 10x (~$1.50/mês)

2. **Processar menos legislações:**
   - No nó "4. Normalizar Dados"
   - Altere `.slice(0, 5)` para `.slice(0, 2)`

3. **Usar voz sintética do D-ID:**
   - Pule nó "7. Gerar Áudio"
   - No nó "8", use `script.input` direto
   - Economiza ElevenLabs

### Aumentar Qualidade

1. **Voz mais natural:**
   - Upgrade ElevenLabs para Pro ($22/mês)
   - Acesso a vozes premium

2. **Avatar customizado:**
   - Upload sua foto no D-ID
   - Vídeo mais autêntico

3. **Legendas hardcoded:**
   - Adicione nó FFmpeg (ou AssemblyAI)
   - Gere legendas automáticas
   - Queima no vídeo

## 🔐 Segurança

**NUNCA commite credenciais!**

O n8n armazena credenciais criptografadas.

Para exportar workflow sem credenciais:
1. Menu workflow → "Settings"
2. "Export" → Desmarque "Include Credentials"

## 📞 Suporte

**Problemas com n8n:**
- Docs: https://docs.n8n.io/
- Fórum: https://community.n8n.io/
- Discord: https://discord.gg/n8n

**Problemas com LegisClara:**
- Abra issue no GitHub do projeto
- Ou me contate diretamente

## 🚀 Próximos Passos

Após configurar:

1. ✅ **Teste manual** - Execute 1 vez e valide resultado
2. ✅ **Ative agendamento** - Toggle "Active" no workflow
3. ✅ **Configure alertas** - Discord/Slack webhook
4. ✅ **Monitore custos** - OpenAI usage dashboard
5. ✅ **Escale gradualmente** - Comece com 2-3 legislações/dia

## 📄 Licença

MIT - Use livremente para fortalecer a democracia! 🇧🇷
