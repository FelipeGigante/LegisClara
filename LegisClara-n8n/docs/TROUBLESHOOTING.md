# 🔧 Troubleshooting - LegisClara n8n

Soluções para problemas comuns do workflow.

---

## 🚨 Problemas de Execução

### Workflow não inicia automaticamente

**Sintomas:**
- Schedule configurado para 09:00
- Workflow marcado como "Active"
- Mas não executa

**Causas possíveis:**

1. **Timezone incorreto**
   ```
   Verificar: Workflow Settings → Timezone
   Solução: Definir como "America/Sao_Paulo"
   ```

2. **n8n não está rodando**
   ```
   Self-hosted: Verificar container Docker
   Cloud: Verificar status em status.n8n.io
   ```

3. **Execução desabilitada**
   ```
   Verificar: Toggle "Active" está verde?
   Solução: Clicar para ativar
   ```

**Fix rápido:**
```
1. Desativar workflow (toggle Active)
2. Aguardar 10 segundos
3. Reativar workflow
4. Testar execução manual primeiro
```

---

### Workflow para no meio

**Sintomas:**
- Execução começa normalmente
- Para em nó específico
- Não mostra erro

**Causas possíveis:**

1. **Timeout de rede**
   ```
   Nó afetado: APIs externas (Senado, Câmara, D-ID)
   Solução: Aumentar timeout nas opções do nó
   ```

2. **Rate limiting**
   ```
   Nó afetado: OpenAI, ElevenLabs, D-ID
   Solução: Adicionar nó "Wait" entre execuções
   ```

3. **Memória insuficiente (self-hosted)**
   ```
   Verificar: docker stats
   Solução: Aumentar limite de memória
   ```

**Fix rápido:**
```javascript
// Adicionar retry automático
// No nó Code, envolva chamadas em:

async function withRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(r => setTimeout(r, 2000 * (i + 1)));
    }
  }
}
```

---

## 🔑 Problemas de Autenticação

### OpenAI: "Invalid API Key"

**Verificar:**
```
1. Key começa com "sk-proj-" ou "sk-"?
2. Key foi copiada completa (sem espaços)?
3. Tem créditos na conta?
```

**Testar key:**
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Se retornar JSON com modelos = OK
# Se erro 401 = Key inválida
```

**Solução:**
1. Regenerar key em https://platform.openai.com/api-keys
2. Atualizar credencial no n8n
3. Testar novamente

---

### ElevenLabs: "Unauthorized"

**Verificar:**
```
1. Header correto: "xi-api-key"
2. Key copiada completa
3. Tem caracteres disponíveis no plano?
```

**Testar key:**
```bash
curl https://api.elevenlabs.io/v1/user \
  -H "xi-api-key: $ELEVENLABS_API_KEY"

# Se retornar JSON com usuário = OK
# Se erro 401 = Key inválida
```

**Solução:**
1. Verificar usage em https://elevenlabs.io/app/usage
2. Regenerar key se necessário
3. Atualizar no n8n (HTTP Header Auth)

---

### D-ID: "Authentication Failed"

**Verificar:**
```
1. Key foi convertida para Base64?
2. Base64 inclui ":" no final da key?
3. Header correto: "Authorization: Basic ..."
```

**Testar conversão:**
```bash
# Converter key
echo -n "sua-api-key-aqui:" | base64

# Testar
curl https://api.d-id.com/talks \
  -H "Authorization: Basic $(echo -n 'sua-key:' | base64)"

# Se retornar 400 (bad request) = Auth OK, falta body
# Se retornar 401 = Auth inválida
```

**Fix:**
```
1. Reconverter key (não esqueça ":" no final!)
2. Copiar Base64 resultante
3. Atualizar credencial n8n
4. Formato: "Basic YWJjMTIzOg=="
```

---

### Supabase: "Invalid API Key"

**Verificar:**
```
1. Usando Service Role Key (não anon key!)
2. URL completa: https://xxx.supabase.co
3. Bucket "videos" existe e é público?
```

**Testar:**
```bash
curl https://xxx.supabase.co/rest/v1/ \
  -H "apikey: $SUPABASE_SERVICE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_KEY"

# Se retornar {} = OK
# Se 401 = Key inválida
```

**Criar bucket:**
```sql
-- No SQL Editor do Supabase
INSERT INTO storage.buckets (id, name, public)
VALUES ('videos', 'videos', true);

-- Criar política pública
CREATE POLICY "Public Access"
ON storage.objects FOR SELECT
USING (bucket_id = 'videos');
```

---

### Instagram: "Token Expired"

**Problema comum:** Tokens expiram a cada 60 dias

**Verificar expiração:**
```bash
curl -X GET "https://graph.facebook.com/v18.0/debug_token?input_token=$INSTAGRAM_TOKEN&access_token=$INSTAGRAM_TOKEN"

# Procurar "data_access_expires_at"
```

**Renovar token:**
```
1. Acesse https://developers.facebook.com/tools/explorer/
2. Selecione seu app
3. Gere novo token com permissões:
   - instagram_basic
   - instagram_content_publish
   - pages_read_engagement
4. Atualize no n8n
```

**Automatizar renovação (avançado):**
```javascript
// Adicionar nó no workflow para renovar token mensalmente
const response = await fetch(
  `https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=${appId}&client_secret=${appSecret}&fb_exchange_token=${currentToken}`
);
```

---

## 📡 Problemas de API

### Senado/Câmara: "Timeout" ou "No Data"

**Causas:**
```
1. API fora do ar (comum em finais de semana)
2. Muitas requisições simultâneas
3. Legislações já coletadas (duplicadas)
```

**Verificar status:**
```bash
# Testar Senado
curl "https://legis.senado.leg.br/dadosabertos/materia/pesquisa/lista?tramitando=S"

# Testar Câmara
curl "https://dadosabertos.camara.leg.br/api/v2/proposicoes"

# Se timeout ou 502/503 = API fora do ar
```

**Solução:**
```javascript
// Adicionar tratamento de erro no nó "4. Normalizar Dados"

try {
  // Processar dados
} catch (error) {
  console.log('Erro ao processar APIs Gov:', error);
  // Continuar com dados em cache ou pular
  return [];
}
```

**Fallback:**
```
1. Coletar de apenas 1 fonte (Senado OU Câmara)
2. Usar dados históricos do banco
3. Executar em horário diferente
```

---

### OpenAI: "Rate Limit Exceeded"

**Limites:**
```
Tier 1 (novo): 3 RPM (requests/minuto)
Tier 2 ($5+): 60 RPM
Tier 3 ($50+): 3.500 RPM
```

**Solução rápida:**
```javascript
// Adicionar delay entre processamentos
// No nó "5. Processar com OpenAI"

const items = $input.all();
const results = [];

for (const item of items) {
  const result = await processWithOpenAI(item);
  results.push(result);

  // Aguardar 20 segundos (3 RPM = 1 req a cada 20s)
  await new Promise(r => setTimeout(r, 20000));
}

return results;
```

**Upgrade de tier:**
```
1. Adicionar $5+ de créditos
2. Aguardar tier upgrade (automático em 24h)
3. Verificar em https://platform.openai.com/account/limits
```

---

### D-ID: "Video Creation Failed"

**Causas comuns:**

1. **Áudio muito longo**
   ```
   Limite: 5 minutos
   Solução: Reduzir roteiro para <90 segundos
   ```

2. **Avatar inválido**
   ```
   Verificar: URL acessível publicamente?
   Formato: JPG/PNG
   Tamanho: <5MB
   ```

3. **Créditos insuficientes**
   ```
   Verificar: https://studio.d-id.com/account
   Solução: Aguardar renovação mensal ou fazer upgrade
   ```

**Debug:**
```javascript
// No nó "8. Gerar Vídeo (D-ID)", adicionar log

console.log('Criando vídeo D-ID:', {
  avatar: $json.avatar_url,
  audio: $json.audio_url,
  credits: 'verificar no dashboard'
});

// Verificar logs em Executions → Details
```

---

## 💾 Problemas de Storage

### Supabase: "Upload Failed"

**Causas:**

1. **Bucket não existe**
   ```sql
   -- Criar bucket
   INSERT INTO storage.buckets (id, name, public)
   VALUES ('videos', 'videos', true);
   ```

2. **Arquivo muito grande**
   ```
   Limite free: 50MB por arquivo
   Solução: Comprimir vídeo ou upgrade para Pro
   ```

3. **Políticas RLS bloqueando**
   ```sql
   -- Desabilitar RLS para bucket
   ALTER TABLE storage.objects DISABLE ROW LEVEL SECURITY;

   -- Ou criar política pública
   CREATE POLICY "Anyone can upload"
   ON storage.objects FOR INSERT
   WITH CHECK (bucket_id = 'videos');
   ```

**Testar upload manual:**
```javascript
// No n8n, criar nó de teste

const supabase = createClient(
  $env.SUPABASE_URL,
  $env.SUPABASE_SERVICE_KEY
);

const { data, error } = await supabase.storage
  .from('videos')
  .upload('test.mp4', file);

console.log('Upload result:', { data, error });
```

---

### Vídeo baixado mas corrompido

**Verificar:**
```bash
# Testar URL do D-ID
curl -I "https://d-id-talks.s3.amazonaws.com/xxx/video.mp4"

# Se 403 Forbidden = URL expirada
# Se 404 Not Found = Vídeo deletado
# Se 200 OK = URL válida
```

**Solução:**
```javascript
// URLs do D-ID expiram em 24h!
// Baixar e fazer upload imediatamente

const videoResponse = await fetch($json.result_url);
const videoBuffer = await videoResponse.buffer();

// Upload para Supabase IMEDIATAMENTE
await supabase.storage.from('videos').upload(filename, videoBuffer);
```

---

## 📱 Problemas de Publicação

### Instagram: "Upload Failed"

**Causas:**

1. **Formato de vídeo incorreto**
   ```
   Requisitos Instagram Reels:
   - Formato: MP4
   - Codec: H.264
   - Resolução: 1080x1920 (9:16)
   - Duração: 15-90 segundos
   - Tamanho: <100MB
   ```

2. **Vídeo não acessível publicamente**
   ```
   Verificar: URL pública do Supabase
   Solução: Bucket marcado como público
   ```

3. **Caption muito longa**
   ```
   Limite: 2.200 caracteres
   Solução: Reduzir texto ou hashtags
   ```

**Validar vídeo:**
```bash
# Verificar codec
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name \
  -of default=noprint_wrappers=1:nokey=1 \
  video.mp4

# Deve retornar: h264
```

**Converter se necessário:**
```bash
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920" \
  -c:v libx264 \
  -preset fast \
  -crf 23 \
  output.mp4
```

---

### Email: "SMTP Error"

**Causas:**

1. **Senha de app incorreta (Gmail)**
   ```
   NÃO usar senha da conta!
   Usar senha de app: https://myaccount.google.com/apppasswords
   ```

2. **2FA não habilitado**
   ```
   Gmail exige 2FA para senhas de app
   Habilitar em: https://myaccount.google.com/security
   ```

3. **Porta bloqueada**
   ```
   Tentar portas alternativas:
   - 587 (TLS)
   - 465 (SSL)
   - 25 (menos seguro)
   ```

**Testar SMTP:**
```bash
# Via telnet
telnet smtp.gmail.com 587

# Ou via Python
python3 -c "
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('user@gmail.com', 'senha-app')
print('SMTP OK')
"
```

---

## 🐛 Problemas Específicos do n8n

### "Out of Memory"

**Sintomas:**
- Workflow trava
- n8n reinicia
- Execuções desaparecem

**Solução (Docker):**
```bash
# Aumentar limite de memória
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  --memory="2g" \  # <-- Aumentar para 2GB
  n8nio/n8n
```

**Solução (Cloud):**
```
Upgrade plano para ter mais memória
Ou: Processar menos itens por vez
```

---

### "Execution Timed Out"

**Causa:** Workflow demora >5 minutos (limite cloud)

**Solução:**
```
1. Dividir workflow em 2 (coletar → processar separadamente)
2. Usar webhooks para continuar execução
3. Upgrade para plano pago (timeout maior)
```

**Dividir workflow:**
```
Workflow 1 (Coletar):
1. Trigger diário
2. Coletar Senado + Câmara
3. Salvar no banco Supabase
4. Chamar webhook do Workflow 2

Workflow 2 (Processar):
1. Webhook trigger
2. Ler legislações do banco
3. Processar + Gerar vídeos
4. Publicar
```

---

### Credenciais não funcionam

**Reset credenciais:**
```
1. n8n → Settings → Credentials
2. Encontrar credencial com problema
3. Deletar
4. Recriar do zero
5. Testar com nó HTTP Request simples
```

**Exportar/Importar:**
```
Ao exportar workflow:
☑️ Marcar "Include Credentials" se for importar no mesmo n8n
☐ Desmarcar se for compartilhar (segurança)
```

---

## 🔍 Debug Avançado

### Ver dados em cada nó

```
1. Executar workflow manualmente
2. Clicar em cada nó (fica verde quando sucesso)
3. Ver tab "Output" para dados processados
4. Tab "Input" para dados recebidos
5. Tab "Logs" para console.log()
```

### Adicionar logs customizados

```javascript
// Em qualquer nó Code
console.log('DEBUG:', {
  timestamp: new Date().toISOString(),
  data: $json,
  env: $env.NODE_ENV
});

// Logs aparecem em:
// - Cloud: Executions → Details → Logs
// - Self-hosted: docker logs n8n
```

### Testar nós isoladamente

```
1. Desconectar nó do fluxo
2. Adicionar nó "Set" antes (dados fake)
3. Executar apenas esse trecho
4. Verificar output
5. Reconectar ao fluxo
```

---

## 📞 Quando Pedir Ajuda

### Informações para incluir

```markdown
**Problema:**
[Descreva o que está acontecendo]

**Nó afetado:**
[Nome do nó, ex: "8. Gerar Vídeo (D-ID)"]

**Erro exato:**
[Copie mensagem de erro completa]

**Dados de entrada:**
[JSON recebido pelo nó]

**Esperado:**
[O que deveria acontecer]

**Já tentei:**
- [ ] Verificar credenciais
- [ ] Testar API manualmente (curl)
- [ ] Ver logs de execução
- [ ] Pesquisar no fórum n8n
```

### Onde pedir ajuda

```
n8n Community: https://community.n8n.io/
Discord n8n: https://discord.gg/n8n
GitHub Issues: [se bug confirmado]
Stack Overflow: tag "n8n"
```

---

## ✅ Checklist Preventiva

Execute semanalmente:

- [ ] Verificar créditos OpenAI
- [ ] Verificar caracteres ElevenLabs
- [ ] Verificar créditos D-ID
- [ ] Verificar storage Supabase (GB usado)
- [ ] Renovar token Instagram (se >45 dias)
- [ ] Backup do workflow (Export)
- [ ] Verificar logs de erro
- [ ] Testar execução manual
- [ ] Limpar vídeos antigos do Supabase

**Automatize checagens:**
```javascript
// Adicionar ao final do workflow

const alerts = [];

if ($json.openai_credits < 1) {
  alerts.push('⚠️ OpenAI: Créditos baixos!');
}

if ($json.did_credits < 10) {
  alerts.push('⚠️ D-ID: Menos de 10 créditos!');
}

if ($json.supabase_storage_mb > 400) {
  alerts.push('⚠️ Supabase: 80% do storage usado!');
}

// Enviar alertas via Discord/Email
if (alerts.length > 0) {
  await sendAlert(alerts.join('\n'));
}
```

---

**Problemas persistem?**

Abra issue detalhada no GitHub ou contate suporte. 🚀
