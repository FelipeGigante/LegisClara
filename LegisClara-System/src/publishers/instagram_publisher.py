"""
Publicador Automático para Instagram
Usa Instagram Graph API para publicar Reels automaticamente
"""

import os
import time
import logging
import requests
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class InstagramPublisher:
    """Publicador de Reels no Instagram via Graph API"""

    def __init__(self, access_token: str, user_id: str):
        """
        Inicializa publicador do Instagram

        Args:
            access_token: Token de acesso do Instagram Graph API
            user_id: ID do usuário/página do Instagram
        """
        self.access_token = access_token
        self.user_id = user_id
        self.base_url = "https://graph.facebook.com/v24.0"

    def publish_reel(self, video_url: str, caption: str) -> Dict[str, Any]:
        """
        Publica um Reel no Instagram

        Args:
            video_url: URL pública do vídeo (precisa estar hospedado)
            caption: Legenda do post

        Returns:
            Dicionário com dados da publicação
        """
        logger.info("📤 Publicando Reel no Instagram...")

        try:
            # Passo 1: Criar container de mídia
            container_id = self._create_media_container(video_url, caption)

            if not container_id:
                raise Exception("Falha ao criar container de mídia")

            logger.info(f"✅ Container criado: {container_id}")

            # Passo 2: Aguardar processamento
            logger.info("⏳ Aguardando processamento do vídeo...")
            if not self._wait_for_processing(container_id):
                raise Exception("Timeout ou erro no processamento do vídeo")

            # Aguardar extra para garantir que está 100% pronto
            logger.info("⏳ Aguardando 15s adicionais para garantir processamento completo...")
            time.sleep(15)

            # Passo 3: Publicar
            post_id = self._publish_container(container_id)

            if not post_id:
                raise Exception("Falha ao publicar container")

            logger.info(f"✅ Reel publicado! ID: {post_id}")

            # Obter URL do post
            post_url = f"https://www.instagram.com/reel/{post_id}"

            return {
                'status': 'publicado',
                'post_id': post_id,
                'url': post_url,
                'video_url': video_url
            }

        except Exception as e:
            logger.error(f"Erro ao publicar no Instagram: {e}")
            return {
                'status': 'erro',
                'erro': str(e)
            }

    def _create_media_container(self, video_url: str, caption: str) -> Optional[str]:
        """Cria container de mídia para o Reel"""
        url = f"{self.base_url}/{self.user_id}/media"

        # Limitar caption a 2200 caracteres
        if len(caption) > 2200:
            caption = caption[:2197] + "..."

        payload = {
            'media_type': 'REELS',
            'video_url': video_url,
            'caption': caption,
            'share_to_feed': True,
            'access_token': self.access_token
        }

        try:
            logger.info(f"Criando container com payload: media_type={payload['media_type']}, video_url={video_url[:50]}...")
            response = requests.post(url, data=payload, timeout=60)
            response.raise_for_status()

            data = response.json()
            logger.info(f"Container criado com sucesso. Resposta: {data}")
            return data.get('id')

        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao criar container: {e}")
            if hasattr(e, 'response') and e.response:
                try:
                    error_data = e.response.json()
                    logger.error(f"Erro detalhado da API: {error_data}")
                except:
                    logger.error(f"Resposta da API (texto): {e.response.text}")
            return None

    def _wait_for_processing(self, container_id: str, max_wait: int = 600) -> bool:
        """Aguarda processamento do vídeo (máx 5 minutos)"""
        url = f"{self.base_url}/{container_id}"
        params = {
            'fields': 'status_code',
            'access_token': self.access_token
        }

        start_time = time.time()

        while time.time() - start_time < max_wait:
            try:
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()

                data = response.json()
                status = data.get('status_code')

                if status == 'FINISHED':
                    return True
                elif status == 'ERROR':
                    logger.error("Erro no processamento do vídeo")
                    return False

                # Aguardar antes de verificar novamente
                time.sleep(5)

            except Exception as e:
                logger.warning(f"Erro ao verificar status: {e}")
                time.sleep(5)

        logger.error("Timeout ao aguardar processamento")
        return False

    def _publish_container(self, container_id: str) -> Optional[str]:
        """Publica o container processado"""
        url = f"{self.base_url}/{self.user_id}/media_publish"

        payload = {
            'creation_id': container_id,
            'access_token': self.access_token
        }

        try:
            logger.info(f"Publicando container {container_id}...")
            response = requests.post(url, data=payload, timeout=60)
            logger.info(f"Status da publicação: {response.status_code}")
            response.raise_for_status()

            data = response.json()
            logger.info(f"Publicação concluída. Resposta: {data}")
            return data.get('id')

        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao publicar: {e}")
            if hasattr(e, 'response') and e.response:
                try:
                    error_data = e.response.json()
                    logger.error(f"Erro detalhado: {error_data}")
                except:
                    logger.error(f"Resposta da API (texto): {e.response.text}")
            return None


class VideoHosting:
    """
    Utilitário para hospedar vídeos temporariamente
    Para Instagram Graph API funcionar, vídeo precisa estar em URL pública
    """

    @staticmethod
    def upload_to_tmpfiles(video_path: str) -> Optional[str]:
        """
        Faz upload do vídeo para tmpfiles.org (temporário, grátis)

        Args:
            video_path: Caminho do arquivo de vídeo

        Returns:
            URL pública do vídeo ou None se falhar
        """
        logger.info("📤 Fazendo upload do vídeo...")

        try:
            with open(video_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    'https://tmpfiles.org/api/v1/upload',
                    files=files,
                    timeout=300
                )

            response.raise_for_status()
            data = response.json()

            if data.get('status') == 'success':
                # tmpfiles.org retorna URL no formato /dl/xxxxx
                # Precisamos modificar para o formato direto
                url = data['data']['url']
                # Converter de https://tmpfiles.org/xxxxx para https://tmpfiles.org/dl/xxxxx
                if '/dl/' not in url:
                    url = url.replace('tmpfiles.org/', 'tmpfiles.org/dl/')

                logger.info(f"✅ Vídeo hospedado: {url}")
                return url
            else:
                logger.error("Erro no upload")
                return None

        except Exception as e:
            logger.error(f"Erro ao fazer upload: {e}")
            return None

    @staticmethod
    def upload_to_catbox(video_path: str) -> Optional[str]:
        """
        Faz upload do vídeo para catbox.moe (permanente, grátis, sem expiração)

        Args:
            video_path: Caminho do arquivo de vídeo

        Returns:
            URL pública do vídeo ou None se falhar
        """
        logger.info("📤 Fazendo upload do vídeo para Catbox...")

        try:
            with open(video_path, 'rb') as f:
                files = {'fileToUpload': f}
                data = {'reqtype': 'fileupload'}

                response = requests.post(
                    'https://catbox.moe/user/api.php',
                    files=files,
                    data=data,
                    timeout=300
                )

            response.raise_for_status()

            # Catbox retorna apenas a URL como texto
            url = response.text.strip()

            if url.startswith('http'):
                logger.info(f"✅ Vídeo hospedado permanentemente: {url}")
                return url
            else:
                logger.error(f"Resposta inesperada: {url}")
                return None

        except Exception as e:
            logger.error(f"Erro ao fazer upload: {e}")
            return None
