# 🚀 Guia Rápido - LegisClara n8n

## Setup em 15 Minutos

### 1️⃣ Crie Contas Gratuitas (5 min)

```
✅ n8n Cloud: https://n8n.io (5.000 execuções grátis/mês)
✅ OpenAI: https://platform.openai.com ($5 crédito inicial)
✅ ElevenLabs: https://elevenlabs.io (10k caracteres grátis)
✅ D-ID: https://studio.d-id.com (CRÉDITOS GRÁTIS no trial!)
✅ Supabase: https://supabase.com (500MB grátis)
```

### 2️⃣ Configure Supabase (3 min)

1. Crie projeto novo
2. Vá em **Storage** → Criar bucket `videos` (público)
3. Vá em **SQL Editor** → Cole e execute:

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
  data_publicacao TIMESTAMPTZ DEFAULT NOW()
);
```

4. Copie credenciais de **Project Settings** → **API**

### 3️⃣ Importe Workflow no n8n (2 min)

1. Faça login no n8n Cloud
2. Clique **"New"** → **"Import from File"**
3. Selecione `LegisClara-n8n/workflows/legisclara-workflow.json`
4. Workflow aparecerá com 16 nós conectados

### 4️⃣ Configure Credenciais (5 min)

Clique em cada nó destacado e configure:

**OpenAI API:**
```
Tipo: OpenAI
API Key: sk-proj-...
```

**ElevenLabs:**
```
Tipo: HTTP Header Auth
Header Name: xi-api-key
Header Value: <sua-chave>
```

**D-ID:**
```
Tipo: HTTP Header Auth
Header Name: Authorization
Header Value: Basic <sua-chave-base64>
```

Para converter D-ID key:
```bash
echo -n "sua-api-key-aqui:" | base64
```

**Supabase:**
```
Project URL: https://xxx.supabase.co
Service Role Key: eyJhb...
```

### 5️⃣ Teste Manual (5 min)

1. Clique **"Execute Workflow"** (▶️ no topo)
2. Aguarde ~5-10 minutos (D-ID demora)
3. Veja cada nó ficar verde ✅
4. Verifique vídeo no Supabase Storage

### 6️⃣ Ative Agendamento

1. Toggle **"Active"** no topo do workflow
2. Executará automaticamente todo dia às 09:00

---

## 🎬 Primeiro Vídeo em 10 Minutos

Se quiser pular APIs e testar mais rápido:

### Modo Teste Simplificado

1. Desconecte nós 1-4 (coleta)
2. No nó "5. Processar com OpenAI", adicione dados manualmente:

```json
{
  "tipo": "PL",
  "numero": "1234",
  "ano": "2025",
  "ementa": "Dispõe sobre a criação do programa nacional de banda larga gratuita para escolas públicas."
}
```

3. Execute apenas nós 5-16
4. Vídeo gerado em ~3-5 minutos!

---

## 📊 Fluxo Visual

```
COLETA (Nós 1-4)
├─ Senado API
├─ Câmara API
└─ Normalizar dados
      ↓
PROCESSAMENTO (Nós 5-6)
├─ OpenAI (análise)
└─ Extrair JSON
      ↓
GERAÇÃO (Nós 7-10)
├─ ElevenLabs (áudio)
├─ D-ID (vídeo) ⏱️ 2-5min
├─ Aguardar processamento
└─ Baixar vídeo
      ↓
PUBLICAÇÃO (Nós 11-14)
├─ Upload Supabase
├─ Gerar caption
├─ Publicar Instagram
└─ Salvar no banco
      ↓
NOTIFICAÇÃO (Nós 15-16)
├─ Email (opcional)
└─ Discord/Slack
```

---

## ⚡ Checklist de Verificação

Antes da primeira execução:

- [ ] n8n instalado/logado
- [ ] Workflow importado
- [ ] 5 credenciais configuradas (OpenAI, ElevenLabs, D-ID, Supabase, Instagram)
- [ ] Bucket Supabase `videos` criado e público
- [ ] Tabela `publicacoes` criada no Supabase
- [ ] Instagram Business Account conectado
- [ ] Teste manual executado com sucesso
- [ ] Vídeo apareceu no Supabase Storage
- [ ] Post publicado no Instagram

---

## 🔍 Debug Rápido

### Workflow não executa?
→ Verifique se está "Active" (toggle verde)

### Erro no nó OpenAI?
→ Verifique API key e créditos em https://platform.openai.com/usage

### Erro no nó D-ID?
→ Confira se converteu key para Base64 corretamente

### Vídeo não aparece no Supabase?
→ Bucket "videos" está público? Políticas RLS desabilitadas?

### Instagram rejeita publicação?
→ Token expirado? Renovar a cada 60 dias

---

## 💡 Dicas Pro

### 1. Reduza Custos
- Use `gpt-3.5-turbo` em vez de `gpt-4o-mini`
- Processe apenas 2-3 legislações por dia
- Use voz D-ID em vez de ElevenLabs

### 2. Aumente Qualidade
- Upgrade ElevenLabs para vozes premium
- Upload seu próprio avatar no D-ID
- Adicione legendas com AssemblyAI

### 3. Escale Gradualmente
- Comece com 1 vídeo/dia
- Monitore custos semanalmente
- Automatize apenas após 1 mês de testes

---

## 📞 Precisa de Ajuda?

**Documentação completa:** `README.md`

**Problemas comuns:**
- D-ID timeout? Aumente `maxAttempts` no nó 9
- OpenAI rate limit? Adicione nó "Wait" de 5s
- Instagram rejeita? Verifique tamanho do vídeo (<100MB)

**Comunidade n8n:**
- Fórum: https://community.n8n.io/
- Discord: https://discord.gg/n8n

---

## 🎯 Próximos Passos

Após primeiro vídeo funcionando:

1. ✅ Configure Instagram API (se ainda não fez)
2. ✅ Ajuste horário de execução (nó 1)
3. ✅ Configure webhooks de notificação
4. ✅ Teste com diferentes tipos de legislação
5. ✅ Monitore custos da OpenAI
6. ✅ Escale para 5-10 legislações/dia

**Bom trabalho! 🚀**
