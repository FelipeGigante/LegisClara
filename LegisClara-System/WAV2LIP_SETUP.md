# 🎭 Instalação do Wav2Lip (Opcional)

O Wav2Lip permite criar vídeos com sincronização labial (lipsync) realista. É opcional - o sistema funciona sem ele usando FFmpeg (avatar estático).

## ⚠️ Requisitos

- **GPU NVIDIA** com CUDA (recomendado) ou CPU (mais lento)
- **8GB+ RAM**
- **Python 3.10**
- **Windows/Linux/Mac**

## 📦 Instalação

### 1. Clone o Wav2Lip

```bash
cd C:\Users\lipeg\OneDrive\Área de Trabalho\LegisClara\LegisClara-System
git clone https://github.com/Rudrabha/Wav2Lip.git
cd Wav2Lip
```

### 2. Instale Dependências

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install opencv-python librosa scipy tqdm numba
```

**Nota:** Para CPU apenas (sem GPU):
```bash
pip install torch torchvision torchaudio
```

### 3. Baixe o Modelo Pré-treinado

```bash
# Criar diretório de checkpoints
mkdir -p checkpoints

# Baixar modelo (297MB)
# Opção 1: Link direto
wget "https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/Eb3LEzbfuKlJiR600lQWRxgBIY27JZg80f7V9jtMfbNDaQ?download=1" -O checkpoints/wav2lip_gan.pth

# Opção 2: Google Drive (se wget não funcionar)
# 1. Acesse: https://drive.google.com/uc?id=1fQtBSYEyuai9MjBe2pfYa_ldpXJbdukW
# 2. Baixe wav2lip_gan.pth
# 3. Mova para Wav2Lip/checkpoints/
```

### 4. Teste a Instalação

```bash
python inference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face ../assets/avatar.jpeg --audio ../data/videos/test_audio.mp3 --outfile test_output.mp4
```

Se funcionar, você verá `test_output.mp4` com lipsync!

## 🎯 Integração com LegisClara

O LegisClara detecta automaticamente se o Wav2Lip está instalado:

- **Com Wav2Lip:** Vídeos com lipsync realista
- **Sem Wav2Lip:** Avatar estático (FFmpeg fallback)

Nenhuma configuração adicional necessária!

## 🚀 Uso com GPU

Para melhor performance, instale CUDA Toolkit:

1. Baixe: https://developer.nvidia.com/cuda-downloads
2. Instale CUDA 11.8
3. Reinstale PyTorch com CUDA:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

## 📊 Performance

| Hardware | Tempo/Vídeo | Qualidade |
|----------|-------------|-----------|
| GPU RTX 3060 | ~30s | Excelente |
| GPU GTX 1060 | ~1min | Ótima |
| CPU (i7) | ~5min | Boa |

## 🔧 Troubleshooting

### Erro: "CUDA out of memory"
**Solução:** Reduza resolução do avatar ou use CPU

### Erro: "checkpoint not found"
**Solução:** Verifique se `checkpoints/wav2lip_gan.pth` existe

### Vídeo sem áudio
**Solução:** Reinstale ffmpeg-python: `pip install --force-reinstall ffmpeg-python`

## 💡 Dicas

1. **Imagem do Avatar:**
   - Use foto frontal, bem iluminada
   - Resolução mínima: 512x512
   - Formato: JPEG ou PNG

2. **Performance:**
   - GPU é 10x+ mais rápida que CPU
   - Feche outros programas durante geração

3. **Qualidade:**
   - Quanto melhor a foto, melhor o resultado
   - Áudio limpo = melhor sincronização

## ❌ Desinstalar

```bash
cd C:\Users\lipeg\OneDrive\Área de Trabalho\LegisClara\LegisClara-System
rm -rf Wav2Lip
```

O LegisClara volta a usar FFmpeg automaticamente.
