"""
Gerador de Vídeos Avançado com Wav2Lip e TTS Melhorado
TTS: Múltiplas opções (pyttsx3, ElevenLabs, Silero)
Avatar: Wav2Lip (lipsync realista - open-source)
"""

import os
import logging
import subprocess
import requests
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Tentar importar bibliotecas opcionais
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    from elevenlabs import ElevenLabs
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False

try:
    import torch
    from silero_tts import silero_tts
    SILERO_AVAILABLE = True
except ImportError:
    SILERO_AVAILABLE = False


class AudioGenerator:
    """Gerador de áudio com múltiplas opções de TTS"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        Inicializa gerador de áudio com melhor qualidade

        Args:
            config: Configuração de voz
                - tts_engine: 'pyttsx3' (melhor), 'elevenlabs' (mais natural), 'silero' (bom), 'gtts' (básico)
                - voice: número da voz (pyttsx3) ou ID (ElevenLabs)
                - speed: velocidade da fala (0.5-2.0)
        """
        self.config = config or {}
        self.tts_engine = self.config.get('tts_engine', 'pyttsx3')  # Padrão melhorado
        self.speed = self.config.get('speed', 1.0)
        self.voice_id = self.config.get('voice', 0)
        
        logger.info(f"🎙️ Usando TTS: {self.tts_engine}")
        
        # Validar engine disponível
        if self.tts_engine == 'pyttsx3' and not PYTTSX3_AVAILABLE:
            logger.warning("pyttsx3 não disponível, usando gTTS")
            self.tts_engine = 'gtts'
        elif self.tts_engine == 'elevenlabs' and not ELEVENLABS_AVAILABLE:
            logger.warning("ElevenLabs não disponível, usando pyttsx3")
            self.tts_engine = 'pyttsx3' if PYTTSX3_AVAILABLE else 'gtts'
        elif self.tts_engine == 'silero' and not SILERO_AVAILABLE:
            logger.warning("Silero não disponível, usando pyttsx3")
            self.tts_engine = 'pyttsx3' if PYTTSX3_AVAILABLE else 'gtts'

    def generate_audio(self, text: str, output_path: str) -> str:
        """
        Gera áudio com melhor qualidade

        Args:
            text: Texto para converter em áudio
            output_path: Caminho para salvar áudio

        Returns:
            Caminho do arquivo de áudio gerado
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        if self.tts_engine == 'pyttsx3':
            return self._generate_pyttsx3(text, output_path)
        elif self.tts_engine == 'elevenlabs':
            return self._generate_elevenlabs(text, output_path)
        elif self.tts_engine == 'silero':
            return self._generate_silero(text, output_path)
        else:
            return self._generate_gtts(text, output_path)

    def _generate_pyttsx3(self, text: str, output_path: str) -> str:
        """Gera áudio com pyttsx3 (vozes nativas, muito melhor que gTTS)"""
        logger.info("🎙️ Gerando áudio com pyttsx3 (voz nativa)...")
        
        try:
            engine = pyttsx3.init()
            
            # Listar e selecionar voz
            voices = engine.getProperty('voices')
            if len(voices) > self.voice_id:
                engine.setProperty('voice', voices[self.voice_id].id)
                logger.info(f"  Voz: {voices[self.voice_id].name}")
            else:
                logger.warning(f"  Voz {self.voice_id} não existe, usando padrão")
            
            # Configurar velocidade (padrão 200)
            rate = int(200 * self.speed)
            engine.setProperty('rate', rate)
            logger.info(f"  Velocidade: {self.speed}x")
            
            # Volume (0.0 - 1.0)
            engine.setProperty('volume', 0.9)
            
            # Gerar áudio
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            
            logger.info(f"✅ Áudio gerado com pyttsx3: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Erro ao gerar com pyttsx3: {e}")
            logger.warning("Voltando para gTTS...")
            return self._generate_gtts(text, output_path)

    def _generate_elevenlabs(self, text: str, output_path: str) -> str:
        """Gera áudio com ElevenLabs (vozes mais naturais e fluidas)"""
        logger.info("🎙️ Gerando áudio com ElevenLabs (voz premium)...")
        
        try:
            api_key = os.getenv('ELEVENLABS_API_KEY')
            if not api_key:
                logger.warning("ELEVENLABS_API_KEY não configurada")
                return self._generate_pyttsx3(text, output_path)
            
            client = ElevenLabs(api_key=api_key)
            
            # Usar voz brasileira padrão se disponível
            voice_id = self.voice_id or "8YV0T5XfXfSu5H7mYkcW"  # Voz neutra em português
            
            response = client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                voice_settings={
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            )
            
            # Salvar áudio
            with open(output_path, 'wb') as f:
                for chunk in response:
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"✅ Áudio gerado com ElevenLabs: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Erro ao gerar com ElevenLabs: {e}")
            logger.warning("Voltando para pyttsx3...")
            return self._generate_pyttsx3(text, output_path)

    def _generate_silero(self, text: str, output_path: str) -> str:
        """Gera áudio com Silero TTS (open-source, muito natural)"""
        logger.info("🎙️ Gerando áudio com Silero TTS...")
        
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
            model, _ = silero_tts(
                language="pt",  # Português
                speaker="baya",  # Voz feminina (ou "kseniya", "xenia", etc)
                device=device
            )
            
            # Gerar áudio
            audio = model.apply_tts(
                text=text,
                speaker="baya",
                sample_rate=24000
            )
            
            # Salvar áudio usando scipy
            from scipy.io import wavfile
            wavfile.write(output_path, 24000, audio)
            
            logger.info(f"✅ Áudio gerado com Silero: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Erro ao gerar com Silero: {e}")
            logger.warning("Voltando para pyttsx3...")
            return self._generate_pyttsx3(text, output_path)

    def _generate_gtts(self, text: str, output_path: str) -> str:
        """Fallback: gTTS (Google Text-to-Speech)"""
        logger.info("🎙️ Gerando áudio com gTTS...")
        
        try:
            from gtts import gTTS
            
            # Usar 'pt' em vez de 'pt-br' (deprecated)
            tts = gTTS(text=text, lang='pt', slow=False)
            tts.save(output_path)
            
            logger.info(f"✅ Áudio gerado com gTTS: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Erro ao gerar áudio: {e}")
            raise


# Compatibilidade com nome antigo
GTTSGenerator = AudioGenerator


class Wav2LipGenerator:
    """Gerador de vídeo com lipsync usando Wav2Lip"""

    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa gerador Wav2Lip

        Args:
            config: Configuração de vídeo
        """
        self.resolution = config.get('resolution', '1080x1920')
        self.fps = config.get('fps', 25)  # Wav2Lip funciona melhor com 25fps
        self.avatar_image = config.get('avatar_image')

        # Path do Wav2Lip (assumindo instalação local)
        self.wav2lip_path = config.get('wav2lip_path', 'Wav2Lip')
        self.checkpoint_path = config.get('checkpoint_path', 'Wav2Lip/checkpoints/Wav2Lip-SD-NOGAN.pt')

        # Validar instalação
        if not os.path.exists(self.wav2lip_path):
            logger.warning(f"Wav2Lip não encontrado em: {self.wav2lip_path}")
            logger.warning("Será usado FFmpeg como fallback")
            self.use_wav2lip = False
        else:
            self.use_wav2lip = True
            logger.info("✅ Wav2Lip disponível")

    def generate_video_with_lipsync(self, audio_path: str, output_path: str) -> str:
        """
        Gera vídeo com lipsync usando Wav2Lip

        Args:
            audio_path: Caminho do arquivo de áudio
            output_path: Caminho para salvar vídeo

        Returns:
            Caminho do vídeo gerado
        """
        if not self.use_wav2lip or not self.avatar_image or not os.path.exists(self.avatar_image):
            logger.warning("Wav2Lip não disponível ou avatar não encontrado. Usando FFmpeg...")
            return self._generate_with_ffmpeg(audio_path, output_path)

        logger.info("🎬 Gerando vídeo com Wav2Lip (lipsync)...")

        try:
            # Preparar comando Wav2Lip
            temp_output = output_path.replace('.mp4', '_wav2lip_temp.mp4')

            cmd = [
                'python',
                f'{self.wav2lip_path}/inference.py',
                '--checkpoint_path', self.checkpoint_path,
                '--face', self.avatar_image,
                '--audio', audio_path,
                '--outfile', temp_output,
                '--fps', str(self.fps),
                '--resize_factor', '1',
                '--nosmooth'
            ]

            logger.debug(f"Executando: {' '.join(cmd)}")

            # Executar Wav2Lip com captura detalhada de erro
            try:
                result = subprocess.run(
                    cmd,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=600  # 10 minutos
                )

                if result.stderr:
                    logger.warning(f"Wav2Lip stderr: {result.stderr}")
                logger.info("✅ Wav2Lip concluído")
                
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ Wav2Lip falhou com código {e.returncode}")
                logger.error(f"Comando: {' '.join(cmd)}")
                if e.stdout:
                    logger.error(f"STDOUT completo:\n{e.stdout}")
                if e.stderr:
                    logger.error(f"STDERR completo:\n{e.stderr}")
                
                # Verificar arquivo de áudio
                if not os.path.exists(audio_path):
                    logger.error(f"❌ Arquivo de áudio não encontrado: {audio_path}")
                else:
                    logger.info(f"✅ Arquivo de áudio existe: {audio_path}")
                
                # Verificar avatar
                if not os.path.exists(self.avatar_image):
                    logger.error(f"❌ Avatar não encontrado: {self.avatar_image}")
                else:
                    logger.info(f"✅ Avatar existe: {self.avatar_image}")
                
                raise

            # Ajustar resolução com FFmpeg
            if os.path.exists(temp_output):
                self._resize_video(temp_output, output_path)
                os.remove(temp_output)
                logger.info(f"✅ Vídeo finalizado: {output_path}")
                return output_path
            else:
                raise Exception("Wav2Lip não gerou arquivo de saída")

        except subprocess.TimeoutExpired:
            logger.error("Timeout ao gerar vídeo com Wav2Lip")
            return self._generate_with_ffmpeg(audio_path, output_path)
        except subprocess.CalledProcessError as e:
            logger.error(f"Erro ao gerar vídeo com Wav2Lip (exit code {e.returncode})")
            if e.stderr:
                logger.error(f"Stderr: {e.stderr}")
            if e.stdout:
                logger.error(f"Stdout: {e.stdout}")
            logger.warning("Usando FFmpeg como fallback...")
            return self._generate_with_ffmpeg(audio_path, output_path)
        except Exception as e:
            logger.error(f"Erro ao gerar vídeo com Wav2Lip: {e}")
            logger.warning("Usando FFmpeg como fallback...")
            return self._generate_with_ffmpeg(audio_path, output_path)

    def _resize_video(self, input_path: str, output_path: str):
        """Redimensiona vídeo para resolução desejada"""
        width, height = self.resolution.split('x')

        cmd = [
            'ffmpeg',
            '-y',
            '-i', input_path,
            '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=#1a237e',
            '-c:v', 'libx264',
            '-crf', '18',
            '-preset', 'medium',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-pix_fmt', 'yuv420p',
            output_path
        ]

        subprocess.run(cmd, check=True, capture_output=True, timeout=300)

    def _generate_with_ffmpeg(self, audio_path: str, output_path: str) -> str:
        """Fallback: gera vídeo com FFmpeg (avatar estático)"""
        logger.info("Gerando vídeo com FFmpeg (avatar estático)...")

        if not self.avatar_image or not os.path.exists(self.avatar_image):
            return self._generate_with_color_bg(audio_path, output_path)

        width, height = self.resolution.split('x')

        cmd = [
            'ffmpeg',
            '-y',
            '-loop', '1',
            '-framerate', str(self.fps),
            '-i', self.avatar_image,
            '-i', audio_path,
            '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=#1a237e',
            '-c:v', 'libx264',
            '-tune', 'stillimage',
            '-preset', 'veryfast',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart',
            '-shortest',
            '-max_muxing_queue_size', '1024',
            output_path
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=300)
            logger.info(f"✅ Vídeo gerado: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Erro ao gerar vídeo com FFmpeg: {e}")
            raise

    def _generate_with_color_bg(self, audio_path: str, output_path: str) -> str:
        """Gera vídeo com fundo colorido"""
        cmd = [
            'ffmpeg',
            '-y',
            '-f', 'lavfi',
            '-i', f'color=c=#1a237e:s={self.resolution}',
            '-i', audio_path,
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-pix_fmt', 'yuv420p',
            '-shortest',
            output_path
        ]

        subprocess.run(cmd, check=True, capture_output=True, timeout=300)
        return output_path


class VideoGeneratorOrchestrator:
    """Orquestrador de geração de vídeos com TTS melhorado + Wav2Lip"""

    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa orquestrador

        Args:
            config: Configuração completa
        """
        tts_config = config.get('tts', {})
        self.tts = AudioGenerator(tts_config)  # Usar AudioGenerator com melhor qualidade

        video_config = config.get('video', {})
        self.video_gen = Wav2LipGenerator(video_config)

        self.data_dir = Path('data/videos')
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def generate_video_from_processamento(self, processamento: Dict[str, Any],
                                         legislacao_id: int) -> Dict[str, Any]:
        """
        Gera vídeo completo a partir do processamento

        Args:
            processamento: Dados processados da legislação
            legislacao_id: ID da legislação

        Returns:
            Metadados do vídeo gerado
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = f"legislacao_{legislacao_id}_{timestamp}"

        # Preparar roteiro completo para áudio
        roteiro = processamento['roteiro_video']

        script_audio = (
            f"{roteiro['gancho']} "
            f"{roteiro['desenvolvimento']} "
            f"{roteiro['impacto']} "
            f"{roteiro['call_to_action']}"
        )

        # Gerar áudio com TTS melhorado
        audio_path = str(self.data_dir / f"{base_name}_audio.mp3")
        logger.info("🎙️ Gerando áudio com TTS melhorado...")
        self.tts.generate_audio(script_audio, audio_path)

        # Gerar vídeo com Wav2Lip (ou FFmpeg fallback)
        video_path = str(self.data_dir / f"{base_name}_video.mp4")
        logger.info("🎬 Gerando vídeo com lipsync...")
        self.video_gen.generate_video_with_lipsync(audio_path, video_path)

        # Obter metadados
        duracao = self._get_video_duration(video_path)
        tamanho_mb = self._get_video_size_mb(video_path)

        return {
            'arquivo_audio': audio_path,
            'arquivo_video': video_path,
            'duracao_segundos': duracao,
            'tamanho_mb': tamanho_mb,
            'resolucao': self.video_gen.resolution
        }

    def _get_video_duration(self, video_path: str) -> float:
        """Obtém duração do vídeo em segundos"""
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
        except:
            return 0.0

    def _get_video_size_mb(self, video_path: str) -> float:
        """Obtém tamanho do vídeo em MB"""
        try:
            size_bytes = os.path.getsize(video_path)
            return size_bytes / (1024 * 1024)
        except:
            return 0.0
