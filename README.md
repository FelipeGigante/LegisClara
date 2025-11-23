# 🏛️ LegisClara - Plataforma Completa de Engajamento Legislativo

**Sistema 100% automatizado** que democratiza o acesso à informação legislativa brasileira através de IA, transformando proposições complexas da Câmara e Senado em conteúdo educativo e publicando automaticamente nas redes sociais.
Membros: Arthur Brasi, Felipe Gigante, Kelvin Cassiano

---

## 📊 Visão Geral do Ecossistema

O LegisClara é composto por **4 módulos principais** que trabalham juntos para criar um ciclo completo de engajamento cidadão:

```
┌─────────────────────────────────────────────────────────────┐
│                     LEGISCLARA ECOSYSTEM                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   WEBSITE    │───>│    PORTAL    │───>│    SYSTEM    │ │
│  │  Informação  │    │   Admin UI   │    │  Core Engine │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         │                    │                    │         │
│         │                    └────────────────────┘         │
│         │                             │                     │
│         └─────────────────────────────┼─────────────────┐  │
│                                       │                 │  │
│                            ┌──────────▼────────┐        │  │
│                            │       n8n         │        │  │
│                            │  Visual Workflow  │◄───────┘  │
│                            └───────────────────┘           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Componentes do Projeto

### 1. 🌐 **LegisClara-Website**
**Landing page institucional moderna**

- ✅ Design responsivo com identidade visual da Clara
- ✅ Apresentação do projeto e funcionalidades
- ✅ Arquitetura e fluxo de dados
- ✅ Links para Portal Administrativo
- ✅ Informações sobre tecnologias utilizadas

**Tecnologias:**
- HTML5, CSS3, JavaScript
- Font Awesome (ícones)
- Google Fonts (Space Grotesk + Inter)

**Acesso:**
```
LegisClara-Website/LegisClara.html
```

---

### 2. 🎛️ **LegisClara-Portal**
**Dashboard administrativo web para controle da pipeline**

#### Funcionalidades

**Sistema de Login:**
- ✅ Autenticação mockada (3 usuários pré-configurados)
- ✅ Sessão com sessionStorage
- ✅ Design moderno e responsivo

**Credenciais de Demonstração:**
- `admin` / `legisla2024`
- `parlamentar` / `demo123`
- `assessor` / `legisla2024`

**Dashboard Principal:**
- ✅ 4 Cards de estatísticas em tempo real
- ✅ Controle da pipeline (Start/Stop)
- ✅ Logs de atividades
- ✅ Configurações de funcionalidades

**API REST (Flask):**
```python
GET  /api/status              # Status do sistema
POST /api/pipeline/start      # Iniciar pipeline completa
POST /api/pipeline/collect    # Coletar proposições
GET  /api/videos/list         # Listar vídeos gerados
GET  /api/logs/recent         # Logs recentes
GET  /api/stats               # Estatísticas gerais
```

**Tecnologias:**
- Frontend: HTML5, CSS3, JavaScript
- Backend: Flask + Flask-CORS
- Design: Mesma paleta do website (Clara)

**Início Rápido:**
```bash
cd LegisClara-Portal

# Opção 1: Apenas Frontend
# Abra index.html no navegador

# Opção 2: Com API Backend
pip install -r requirements.txt
python api.py
# Acesse: http://localhost:5000
```

**Documentação:** Ver `LegisClara-Portal/README.md`

---

### 3. 🤖 **LegisClara-System**
**Motor principal - Pipeline Python 100% automatizada**

#### Fluxo Completo

```
1. Coleta (Câmara/Senado APIs)
   ↓
2. Processamento IA (Gemini/Claude)
   ↓
3. Geração de Áudio (gTTS)
   ↓
4. Criação de Vídeo (FFmpeg/Wav2Lip)
   ↓
5. Publicação (Instagram Reels)
```

#### Arquitetura

```
LegisClara-System/
├── src/
│   ├── collectors/
│   │   └── camara_collector_simple.py  # API Câmara
│   ├── processors/
│   │   ├── gemini_processor.py         # Google Gemini
│   │   └── claude_processor.py         # Anthropic Claude
│   ├── generators/
│   │   └── advanced_video_generator.py # gTTS + Wav2Lip/FFmpeg
│   └── publishers/
│       └── instagram_publisher.py      # Instagram Graph API
├── assets/
│   └── avatar.jpeg                      # Avatar da Clara
├── data/
│   └── videos/                          # Vídeos gerados
├── Wav2Lip/                             # Lipsync (opcional)
├── main.py                              # Script principal
├── requirements.txt
├── .env.example
└── WAV2LIP_SETUP.md
```

#### Características

- **100% Gratuito**: Gemini API (1500 req/dia)
- **Lipsync Realista**: Wav2Lip (GPU) ou FFmpeg (fallback)
- **Voz Natural**: gTTS (Google Text-to-Speech)
- **Publicação Automática**: Instagram Reels
- **Zero Configuração**: Detecta recursos automaticamente
- **Formato Vertical**: 1080x1920 (Reels/Stories/TikTok)

#### Instalação

```bash
cd LegisClara-System

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar
cp .env.example .env
# Edite .env com suas chaves

# Executar
python main.py
```

#### Configuração (.env)

```env
# OBRIGATÓRIO
GEMINI_API_KEY=sua_chave_aqui

# OPCIONAL (para publicação automática)
INSTAGRAM_ACCESS_TOKEN=seu_token
INSTAGRAM_USER_ID=seu_id
```

**Obter chave Gemini (gratuita):**
- https://makersuite.google.com/app/apikey
- 1500 requisições/dia gratuitas

**Obter Instagram API:**
- https://developers.facebook.com/docs/instagram-api/getting-started
- Requer conta Business/Creator

#### Wav2Lip (Lipsync - Opcional)

Para vídeos com sincronização labial realista:

```bash
cd LegisClara-System
git clone https://github.com/Rudrabha/Wav2Lip.git
cd Wav2Lip

# Instalar dependências
pip install torch opencv-python librosa scipy tqdm numba

# Baixar modelo (297MB)
mkdir checkpoints
wget "https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/Eb3LEzbfuKlJiR600lQWRxgBIY27JZg80f7V9jtMfbNDaQ?download=1" -O checkpoints/wav2lip_gan.pth
```

**Ver guia completo:** `LegisClara-System/WAV2LIP_SETUP.md`

#### Performance

| Etapa | Tempo | Hardware |
|-------|-------|----------|
| Coleta | ~5s | Qualquer |
| Gemini | ~10s | Qualquer |
| gTTS | ~2s | Qualquer |
| Wav2Lip (GPU) | ~30s | GPU NVIDIA |
| Wav2Lip (CPU) | ~5min | CPU moderno |
| FFmpeg | ~10s | Qualquer |
| Upload | ~30s | Internet |

**Total:** 1-6min/vídeo

---

### 4. 🔄 **LegisClara-n8n**
**Workflow visual alternativo (sem programação)**

#### Por que n8n?

- ✅ **Interface Visual** - Não precisa programar
- ✅ **Sem FFmpeg** - Usa D-ID direto (com créditos gratuitos)
- ✅ **Fácil Depuração** - Vê dados fluindo entre etapas
- ✅ **Hospedagem Grátis** - n8n Cloud tem plano free
- ✅ **Integrações Prontas** - Instagram, OpenAI, Supabase nativos

#### Fluxo do Workflow

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

#### Instalação

**Opção 1: n8n Cloud (Recomendado)**
```
1. Acesse https://n8n.io
2. Crie conta grátis
3. Import: LegisClara-n8n/workflows/legisclara-workflow.json
4. Configure credenciais
```

**Opção 2: n8n Docker**
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Acesse: http://localhost:5678
```

#### Credenciais Necessárias

1. **OpenAI API** (ChatGPT)
   - https://platform.openai.com/api-keys
   - Custo: ~$0.50 por 100 legislações

2. **ElevenLabs** (Text-to-Speech)
   - https://elevenlabs.io/app/settings/api-keys
   - Gratuito: 10.000 caracteres/mês

3. **D-ID** (Avatar Vídeo) - **GRÁTIS! 🎉**
   - https://studio.d-id.com/
   - 14 dias trial com créditos grátis (~20-50 vídeos)

4. **Supabase** (Storage + Banco)
   - https://supabase.com (100% grátis)

5. **Instagram Business API**
   - https://developers.facebook.com/

#### Custos Mensais (100 Legislações/Mês)

| Serviço | Custo | Plano Gratuito |
|---------|-------|----------------|
| n8n Cloud | $0-20/mês | 5.000 execuções grátis |
| OpenAI GPT-4 | ~$15-30/mês | $5 crédito inicial |
| ElevenLabs | $0-5/mês | 10k chars grátis |
| D-ID | $0-49/mês | **Créditos trial grátis!** |
| Supabase | $0 | 500MB storage grátis |
| Instagram API | $0 | Totalmente grátis |
| **TOTAL** | **$20-104/mês** | **MVP possível 100% grátis!** |

**Documentação:** Ver `LegisClara-n8n/README.md`

---

## 🎨 Identidade Visual

### Paleta de Cores (baseada na Clara)

```css
--primary-dark: #0f172a     /* Terno escuro */
--primary-blue: #1e3a8a     /* Azul institucional */
--accent-purple: #8b5cf6    /* Fundo da imagem */
--accent-cyan: #06b6d4      /* Holograma do tablet */
--text-light: #f8fafc
--text-dim: #94a3b8
```

### Tipografia

- **Títulos:** Space Grotesk (700, 500)
- **Corpo:** Inter (300, 400, 600, 700)

---

## 🚀 Início Rápido por Perfil

### Para Parlamentares/Assessores
**Use o Portal Administrativo**

```bash
# 1. Abra o website
LegisClara-Website/LegisClara.html

# 2. Clique em "Acessar Portal"

# 3. Login:
Usuário: parlamentar
Senha: demo123

# 4. Inicie a pipeline pelo dashboard
```

### Para Desenvolvedores (Python)
**Use o LegisClara-System**

```bash
cd LegisClara-System
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Configure .env
python main.py
```

### Para Não-Programadores
**Use o n8n**

```bash
# 1. Acesse n8n.io
# 2. Crie conta grátis
# 3. Import workflow
# 4. Configure credenciais
# 5. Ative!
```

---

## 📁 Estrutura Completa do Projeto

```
LegisClara/
│
├── LegisClara-Website/          # 🌐 Landing page
│   ├── LegisClara.html
│   └── clara.jpeg
│
├── LegisClara-Portal/           # 🎛️ Dashboard Admin
│   ├── index.html               # Login
│   ├── dashboard.html           # Dashboard
│   ├── api.py                   # API Flask
│   ├── requirements.txt
│   ├── README.md
│   └── QUICKSTART.md
│
├── LegisClara-System/           # 🤖 Motor Python
│   ├── src/
│   │   ├── collectors/
│   │   ├── processors/
│   │   ├── generators/
│   │   └── publishers/
│   ├── assets/
│   ├── data/
│   ├── Wav2Lip/                 # Opcional
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── WAV2LIP_SETUP.md
│   └── CHANGELOG.md
│
├── LegisClara-n8n/              # 🔄 Workflow Visual
│   ├── workflows/
│   │   └── legisclara-workflow.json
│   ├── config/
│   ├── docs/
│   └── README.md
│
└── README.md                    # 📖 Este arquivo
```

---

## 💰 Comparação de Custos

### LegisClara-System (Python)
**100% GRATUITO**

| Serviço | Custo | Limite |
|---------|-------|--------|
| API Câmara | Grátis | Ilimitado |
| Gemini API | Grátis | 1500 req/dia |
| gTTS | Grátis | Ilimitado |
| FFmpeg | Grátis | Ilimitado |
| Wav2Lip | Grátis | Ilimitado |
| Instagram API | Grátis | 200 posts/dia |

### LegisClara-n8n (Visual)
**$20-104/mês** (ou grátis com créditos trial)

| Serviço | Custo/Mês |
|---------|-----------|
| n8n Cloud | $0-20 |
| OpenAI GPT-4 | $15-30 |
| ElevenLabs | $0-5 |
| D-ID | $0-49 |
| Supabase | $0 |
| Instagram | $0 |

---

## 🎯 Casos de Uso

### 1. Gabinete Parlamentar
- Use **Portal** para controlar publicações
- Monitore engajamento em tempo real
- Ajuste frequência de posts

### 2. Organização Cívica
- Use **System** para autonomia total
- Customize mensagens e avatares
- Integre com seus sistemas

### 3. Pesquisador/Acadêmico
- Use **n8n** para experimentos rápidos
- Visualize fluxo de dados
- Teste diferentes modelos de IA

### 4. Startup Civic Tech
- Use **System** como base
- Expanda com novos recursos
- Customize para outras legislaturas

---

## 🛠️ Tecnologias Utilizadas

### Frontend
- HTML5, CSS3, JavaScript
- Font Awesome 6.4
- Google Fonts

### Backend Python
- Flask + Flask-CORS
- Requests
- Google Generative AI (Gemini)
- Anthropic Claude
- gTTS (Google Text-to-Speech)
- FFmpeg
- Wav2Lip (opcional)

### n8n Workflow
- OpenAI GPT-4
- ElevenLabs TTS
- D-ID Avatar
- Supabase Storage
- Instagram Graph API

### DevOps
- Docker (n8n)
- Git
- Python venv

---

## 📊 Roadmap Geral

### Concluído ✅
- [x] Sistema Python completo
- [x] Workflow n8n funcional
- [x] Portal administrativo web
- [x] Website institucional
- [x] Integração Instagram
- [x] Processamento com Gemini/Claude
- [x] Geração de vídeo (FFmpeg/Wav2Lip)
- [x] API REST para portal

### Em Desenvolvimento 🚧
- [ ] TikTok automático
- [ ] YouTube Shorts automático
- [ ] Legendas automáticas (Whisper)
- [ ] Dashboard analytics completo
- [ ] Múltiplos avatares
- [ ] Agendamento de posts
- [ ] Análise de sentimento dos comentários
- [ ] Relatórios parlamentares em PDF

### Futuro 🔮
- [ ] App mobile (React Native)
- [ ] Integração LinkedIn
- [ ] Twitter/X posts
- [ ] Chatbot interativo
- [ ] Gamificação (badges, ranking)
- [ ] API pública para desenvolvedores

---

## 🤝 Contribuindo

Contribuições são bem-vindas!

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Áreas que Precisam de Ajuda

- 📱 Front-end do Portal (React/Vue)
- 🎨 Design/UX improvements
- 🌍 Internacionalização (i18n)
- 📊 Analytics e métricas
- 🧪 Testes automatizados
- 📝 Documentação

---

## 📝 Licença

MIT License - Use livremente para fortalecer a democracia!

Ver `LICENSE` para mais detalhes.

---

## 🙏 Créditos

### Tecnologias
- [Google Gemini](https://ai.google.dev/) - LLM gratuita
- [Anthropic Claude](https://anthropic.com/) - LLM avançada
- [gTTS](https://gtts.readthedocs.io/) - Text-to-Speech
- [Wav2Lip](https://github.com/Rudrabha/Wav2Lip) - Lipsync
- [FFmpeg](https://ffmpeg.org/) - Processamento de vídeo
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api) - Publicação
- [n8n](https://n8n.io/) - Workflow automation
- [D-ID](https://d-id.com/) - Avatar animado
- [ElevenLabs](https://elevenlabs.io/) - Voice synthesis
- [Supabase](https://supabase.com/) - Backend-as-a-Service

### Dados
- [API Câmara dos Deputados](https://dadosabertos.camara.leg.br/)
- [API Senado Federal](https://legis.senado.leg.br/dadosabertos/)

---

## 📞 Suporte

### Problemas Técnicos
- **GitHub Issues**: [Reportar Bug](https://github.com/FelipeGigante/LegisClara/issues)
- **Email**: [Contato]

### Comunidade
- **n8n Community**: https://community.n8n.io/
- **Discussões**: GitHub Discussions

### Documentação
- **System**: `LegisClara-System/README.md`
- **Portal**: `LegisClara-Portal/README.md`
- **n8n**: `LegisClara-n8n/README.md`
- **Wav2Lip**: `LegisClara-System/WAV2LIP_SETUP.md`

---

## ⚠️ Avisos Importantes

1. **Revisão de Conteúdo**: Este é um sistema educacional. Sempre revise o conteúdo gerado antes de publicar.

2. **Limites de API**: Respeite os limites das APIs gratuitas:
   - Gemini: 1500 req/dia
   - Instagram: 200 posts/dia
   - Dados Abertos: Sem limite oficial (use com responsabilidade)

3. **Tokens Instagram**: Expiram a cada 60 dias. Configure renovação automática.

4. **Custos n8n**: Monitore uso para não exceder plano gratuito.

5. **GPU para Wav2Lip**: Recomendado mas não obrigatório (CPU funciona).

6. **Responsabilidade**: O uso desta ferramenta é de responsabilidade do usuário. Certifique-se de estar em conformidade com as leis de direitos autorais e políticas das plataformas.

---

## 🇧🇷 Desenvolvido para democratizar informação legislativa brasileira

**Clara, a influenciadora digital que aproxima cidadãos das decisões que afetam suas vidas.**

---

**Última atualização:** Novembro 2024
**Versão:** 1.0.0
**Status:** ✅ Produção

---

## 🎓 Para Começar Agora

**Escolha seu caminho:**

1. **Quero apenas visualizar** → Abra `LegisClara-Website/LegisClara.html`
2. **Quero testar o controle** → Abra `LegisClara-Portal/index.html` (login: admin/legisla2024)
3. **Quero rodar a pipeline** → `cd LegisClara-System && python main.py`
4. **Quero usar interface visual** → Configure n8n e importe workflow
5. **Quero desenvolver** → Leia documentação técnica em cada subpasta

**Dúvidas?** Comece pelo `QUICKSTART.md` de cada módulo!

---

💙 Feito com Python, IA e democracia
