# 🎭 D-ID Setup - Guia Completo

## Por que D-ID?

O D-ID é a solução **MAIS BARATA** e **MAIS FÁCIL** para gerar vídeos com avatar:

- ✅ **Créditos Grátis** no trial (14 dias)
- ✅ **Sem FFmpeg** necessário
- ✅ **API Simples** - 1 chamada e pronto
- ✅ **Avatar Realista** - Deep learning de ponta
- ✅ **Suporta PT-BR** perfeitamente

## 🆓 Como Usar GRÁTIS

### Opção 1: Trial de 14 Dias (Recomendado)

1. Acesse https://studio.d-id.com/
2. Crie conta (email + senha)
3. **Não precisa cartão de crédito!**
4. Recebe créditos para ~20-50 vídeos

**Quanto dura?**
- 1 vídeo de 60s = ~2-3 créditos
- Trial dá ~100 créditos
- **Você pode testar ~30-50 vídeos grátis!**

### Opção 2: Plano Free (Após Trial)

Após trial, ainda tem plano free:
- 20 créditos/mês permanentes
- ~6-10 vídeos/mês
- Marca d'água no vídeo (removível com edição)

### Opção 3: Pagar (se escalar)

Planos pagos:
- **Lite:** $5.90/mês - 100 créditos (~30 vídeos)
- **Basic:** $29/mês - 500 créditos (~150 vídeos)
- **Advanced:** $196/mês - 5000 créditos (~1500 vídeos)

---

## 🔑 Obter API Key

### Passo a Passo

1. Faça login em https://studio.d-id.com/

2. No menu lateral, clique em **"API"**

3. Clique em **"Create API Key"**

4. Copie a chave (formato: `xxx_yyy_zzz`)

5. **IMPORTANTE:** Guarde em local seguro, não mostra novamente!

### Converter para Base64 (Necessário)

A API do D-ID usa autenticação Basic, então precisa converter:

**No Linux/Mac:**
```bash
echo -n "sua-api-key-aqui:" | base64
```

**No Windows (PowerShell):**
```powershell
$key = "sua-api-key-aqui:"
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($key))
```

**Online (se preferir):**
https://www.base64encode.org/

**Exemplo:**
```
API Key: abc123def456
Base64:  YWJjMTIzZGVmNDU2Og==
```

---

## 🎨 Escolher Avatar

### Avatares Gratuitos do D-ID

O D-ID oferece vários avatares prontos:

1. Acesse https://studio.d-id.com/
2. Vá em **"Create Video"** → **"Presenters"**
3. Escolha avatar (todos gratuitos!)
4. Clique com botão direito na imagem → "Copiar URL"

**Avatares populares:**

```
Avatar Feminino 1 (Rachel):
https://create-images-results.d-id.com/google-oauth2%7C103908445571603294059/upl_JRxp-Y0tgdoEuHqvlmxnv/image.png

Avatar Masculino 1 (John):
https://create-images-results.d-id.com/google-oauth2%7C103908445571603294059/upl_abc123/image.png

Avatar Neutro 1 (Alex):
https://create-images-results.d-id.com/google-oauth2%7C103908445571603294059/upl_def456/image.png
```

### Upload Seu Próprio Avatar

**Requisitos:**
- Foto de rosto frontal
- Boa iluminação
- Fundo neutro (opcional)
- Tamanho: 512x512px a 1024x1024px
- Formato: JPG ou PNG

**Como fazer:**

1. No D-ID Studio, clique **"Upload Image"**
2. Selecione sua foto
3. Aguarde processamento (~30s)
4. Copie URL gerada
5. Use no workflow n8n

**Dica:** Use https://www.remove.bg/ para remover fundo

---

## 🎬 Gerar Vídeo (API)

### Request Básico

```bash
curl -X POST https://api.d-id.com/talks \
  -H "Authorization: Basic $(echo -n 'sua-api-key:' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "source_url": "URL_DO_AVATAR",
    "script": {
      "type": "audio",
      "audio_url": "URL_DO_AUDIO.mp3"
    },
    "config": {
      "fluent": true,
      "pad_audio": 0
    }
  }'
```

### Response

```json
{
  "id": "tlk_abc123",
  "status": "created",
  "created_at": "2025-01-22T12:00:00.000Z"
}
```

### Checar Status

```bash
curl https://api.d-id.com/talks/tlk_abc123 \
  -H "Authorization: Basic $(echo -n 'sua-api-key:' | base64)"
```

**Status possíveis:**
- `created` → Aguardando processamento
- `processing` → Gerando vídeo (2-5 min)
- `done` → Pronto! 🎉
- `error` → Falha ❌

### Response Final (quando done)

```json
{
  "id": "tlk_abc123",
  "status": "done",
  "result_url": "https://d-id-talks.s3.amazonaws.com/abc123/video.mp4",
  "duration": 62.5,
  "created_at": "2025-01-22T12:00:00.000Z",
  "started_at": "2025-01-22T12:00:05.000Z",
  "completed_at": "2025-01-22T12:03:42.000Z"
}
```

---

## ⚙️ Configurações Avançadas

### Config Completo

```json
{
  "source_url": "URL_AVATAR",
  "script": {
    "type": "audio",
    "audio_url": "URL_AUDIO",
    "reduce_noise": true  // Reduz ruído de fundo
  },
  "config": {
    "fluent": true,  // Movimentos mais naturais
    "pad_audio": 0,  // Sem padding no áudio
    "driver_expressions": {
      "expressions": [
        {
          "start_frame": 0,
          "expression": "neutral",  // ou "happy", "serious", "surprised"
          "intensity": 1.0
        }
      ]
    },
    "result_format": "mp4",  // ou "webm", "gif"
    "stitch": true,  // Une áudio + vídeo
    "logo": {
      "url": "URL_LOGO.png",  // Marca d'água customizada
      "position": [10, 10]
    }
  }
}
```

### Expressões Disponíveis

```
neutral    → Neutro (padrão)
happy      → Feliz
serious    → Sério
surprised  → Surpreso
```

### Formatos de Saída

```
mp4   → Melhor qualidade (recomendado)
webm  → Menor tamanho
gif   → Animação (sem som)
```

---

## 🐛 Troubleshooting

### Erro: "Insufficient Credits"

**Solução:**
1. Verifique créditos em https://studio.d-id.com/account
2. Trial acabou? Use plano Free (20 créditos/mês)
3. Ou faça upgrade para Lite ($5.90/mês)

### Erro: "Invalid Source URL"

**Causas:**
- URL do avatar não está acessível
- Imagem muito grande (>5MB)
- Formato inválido (use JPG/PNG)

**Solução:**
- Use avatares oficiais do D-ID
- Comprima imagem com https://tinypng.com/
- Hospede em CDN público (Imgur, Cloudinary)

### Erro: "Invalid Audio URL"

**Causas:**
- Áudio não está acessível publicamente
- Formato inválido (use MP3)
- Áudio muito longo (max 5 min)

**Solução:**
- Hospede áudio no Supabase Storage (público)
- Converta para MP3 se necessário
- Reduza duração para <90 segundos

### Vídeo demora muito

**Normal:** 2-5 minutos de processamento

**Se >10 minutos:**
1. Verifique status via API
2. Pode estar em fila (horário de pico)
3. Contate suporte se >30 min

### Qualidade do vídeo ruim

**Melhorias:**
1. Use avatar em alta resolução (1024x1024px)
2. Áudio limpo sem ruído de fundo
3. Ative `"fluent": true` no config
4. Use `"reduce_noise": true` no script

---

## 💰 Otimizar Custos

### Estratégias

**1. Use Cache de Avatares**
- Gere avatar 1x e reutilize
- Economiza 50% dos créditos

**2. Áudio Curto**
- Vídeos <60s custam menos
- Ideal: 45-60 segundos

**3. Batch Processing**
- Processe vários de uma vez
- Evita overhead de criação

**4. Qualidade Adaptativa**
```json
{
  "config": {
    "result_format": "webm",  // Menor que MP4
    "stitch": false  // Não une (economiza)
  }
}
```

---

## 📊 Limites da API

### Rate Limits (Plano Free)

```
Requisições: 6/minuto
Vídeos simultâneos: 3
Duração máxima: 5 minutos
Tamanho avatar: 5MB
```

### Rate Limits (Plano Pago)

```
Requisições: 30/minuto
Vídeos simultâneos: 10
Duração máxima: 30 minutos
Tamanho avatar: 20MB
```

---

## 🚀 Integração com n8n

No workflow LegisClara, o D-ID está no **nó 8**:

```json
{
  "url": "https://api.d-id.com/talks",
  "method": "POST",
  "authentication": "headerAuth",
  "headers": {
    "Authorization": "Basic {{ $env.DID_API_KEY_BASE64 }}"
  },
  "body": {
    "source_url": "{{ $env.DID_AVATAR_URL }}",
    "script": {
      "type": "audio",
      "audio_url": "{{ $json.audio_url }}"
    },
    "config": {
      "fluent": true,
      "pad_audio": 0,
      "result_format": "mp4"
    }
  }
}
```

**Polling (nó 9):**
```javascript
// Aguarda até status = "done"
const maxAttempts = 30;  // 30 tentativas
const delayMs = 10000;   // 10 segundos entre tentativas
// Total: até 5 minutos de espera
```

---

## 📞 Suporte D-ID

**Documentação oficial:**
https://docs.d-id.com/

**API Reference:**
https://docs.d-id.com/reference/talks

**Status da API:**
https://status.d-id.com/

**Suporte:**
support@d-id.com

---

## ✅ Checklist

Antes de usar D-ID no n8n:

- [ ] Conta criada no D-ID
- [ ] API Key gerada
- [ ] Key convertida para Base64
- [ ] Base64 adicionada ao n8n (credencial)
- [ ] Avatar escolhido (URL copiada)
- [ ] Testado via Postman/curl
- [ ] Verificado créditos disponíveis
- [ ] Configurado timeout no nó 9 (polling)

**Pronto! Você está pronto para gerar vídeos com avatar! 🎬**
