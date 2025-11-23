"""
Gerador de Vídeos Avançado com Wav2Lip e gTTS
TTS: gTTS (Google Text-to-Speech - gratuito)
Avatar: Wav2Lip (lipsync realista - open-source)
"""

import os
import logging
import subprocess
import requests
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from gtts import gTTS

logger = logging.getLogger(__name__)


class GTTSGenerator:
    """Gerador de áudio usando gTTS (Google Text-to-Speech)"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        Inicializa gerador de áudio gTTS

        Args:
            config: Configuração de voz (opcional)
        """
        self.lang = 'pt-br'  # Português brasileiro
        self.slow = False

        if config:
            self.lang = config.get('lang', 'pt-br')
            self.slow = config.get('slow', False)

    def generate_audio(self, text: str, output_path: str) -> str:
        """
        Gera áudio a partir de texto usando gTTS

        Args:
            text: Texto para converter em áudio
            output_path: Caminho para salvar áudio

        Returns:
            Caminho do arquivo de áudio gerado
        """
        logger.info("Gerando áudio com gTTS (Google Text-to-Speech)...")

        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Gerar áudio
            tts = gTTS(text=text, lang=self.lang, slow=self.slow)
            tts.save(output_path)

            logger.info(f"✅ Áudio gerado: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Erro ao gerar áudio: {e}")
            raise


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
        self.checkpoint_path = config.get('checkpoint_path', 'Wav2Lip/checkpoints/wav2lip_gan.pth')

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

            # Executar Wav2Lip
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutos
            )

            logger.info("✅ Wav2Lip concluído")

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
    """Orquestrador de geração de vídeos com gTTS + Wav2Lip"""

    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa orquestrador

        Args:
            config: Configuração completa
        """
        tts_config = config.get('tts', {})
        self.tts = GTTSGenerator(tts_config)

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

        # Gerar áudio com gTTS
        audio_path = str(self.data_dir / f"{base_name}_audio.mp3")
        logger.info("🎙️ Gerando áudio com gTTS...")
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
