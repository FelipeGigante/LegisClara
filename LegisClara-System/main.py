"""
LegisClara - Influenciadora Digital Legislativa
Sistema completo com gTTS, Wav2Lip e publicação automática no Instagram

Fluxo:
1. Coleta dados da Câmara dos Deputados
2. Processa com Gemini (gratuito)
3. Gera áudio com gTTS (gratuito)
4. Gera vídeo com Wav2Lip lipsync (ou FFmpeg fallback)
5. Publica automaticamente no Instagram
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

from src.collectors.camara_collector_simple import CamaraCollector
from src.processors.gemini_processor import GeminiProcessor
from src.generators.advanced_video_generator import VideoGeneratorOrchestrator
from src.publishers.instagram_publisher import InstagramPublisher, VideoHosting

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('legisclara.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class LegisClara:
    """Sistema completo LegisClara com publicação automática"""

    def __init__(self):
        """Inicializa o sistema"""
        load_dotenv()

        # API Keys
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.instagram_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.instagram_user_id = os.getenv('INSTAGRAM_USER_ID')

        if not self.gemini_key:
            raise ValueError("GEMINI_API_KEY não configurada no .env")

        self.auto_publish = self.instagram_token and self.instagram_user_id

        if not self.auto_publish:
            logger.warning("⚠️  Instagram não configurado - vídeos não serão publicados")
        else:
            logger.info("✅ Instagram configurado")

        # Configurações
        self.camara_config = {'base_url': 'https://dadosabertos.camara.leg.br/api/v2', 'timeout': 30}
        self.video_config = {
            'tts': {'lang': 'pt-br', 'slow': False},
            'video': {
                'resolution': '1080x1920',
                'fps': 25,
                'avatar_image': 'assets/avatar.jpeg',
                'wav2lip_path': 'Wav2Lip',
                'checkpoint_path': 'Wav2Lip/checkpoints/wav2lip_gan.pth'
            }
        }

        self.collector = CamaraCollector(self.camara_config)
        self.processor = GeminiProcessor(self.gemini_key)
        self.video_gen = VideoGeneratorOrchestrator(self.video_config)

        if self.auto_publish:
            self.publisher = InstagramPublisher(self.instagram_token, self.instagram_user_id)

        Path('data/videos').mkdir(parents=True, exist_ok=True)
        Path('assets').mkdir(parents=True, exist_ok=True)

        logger.info("🎬 LegisClara inicializado!")

    def executar(self, days_back=7, auto_publish=True):
        logger.info("🚀 INICIANDO LEGISCLARA\n")

        proposicoes = self.collector.collect_recent_proposicoes(days_back=days_back)
        if not proposicoes:
            logger.warning("Nenhuma proposição encontrada")
            return

        logger.info(f"✅ {len(proposicoes)} proposições coletadas\n")
        videos_gerados = []

        for i, prop in enumerate(proposicoes[:1], 1):
            logger.info(f"\n{'='*70}\n📝 PROPOSIÇÃO {i}/\n{'='*70}")
            logger.info(f"{prop['tipo']} {prop['numero']}/{prop['ano']}\n")

            try:
                processamento = self.processor.processar_legislacao(prop)
                logger.info(f"✅ {processamento['titulo_simples']}\n")

                video_metadata = self.video_gen.generate_video_from_processamento(processamento, i)
                logger.info(f"✅ Vídeo: {video_metadata['arquivo_video']}\n")

                caption = self.processor.gerar_caption_social(processamento, prop)
                caption_path = video_metadata['arquivo_video'].replace('.mp4', '_caption.txt')
                with open(caption_path, 'w', encoding='utf-8') as f:
                    f.write(caption)

                videos_gerados.append({'video_path': video_metadata['arquivo_video'], 'caption': caption})

            except Exception as e:
                logger.error(f"❌ Erro: {e}")
                continue

        if auto_publish and self.auto_publish and videos_gerados:
            logger.info("\n📤 PUBLICANDO NO INSTAGRAM\n")

            for i, vd in enumerate(videos_gerados, 1):
                try:
                    video_url = VideoHosting.upload_to_catbox(vd['video_path'])
                    if video_url:
                        result = self.publisher.publish_reel(video_url, vd['caption'])
                        if result['status'] == 'publicado':
                            logger.info(f"✅ Publicado: {result['url']}\n")
                except Exception as e:
                    logger.error(f"❌ Erro: {e}\n")

        logger.info(f"\n✨ CONCLUÍDO! {len(videos_gerados)} vídeos em data/videos/\n")


def main():
    try:
        sistema = LegisClara()
        sistema.executar(days_back=7, auto_publish=True)
    except KeyboardInterrupt:
        logger.info("\n⏸️  Interrompido")
    except Exception as e:
        logger.error(f"\n❌ Erro: {e}")


if __name__ == '__main__':
    main()
