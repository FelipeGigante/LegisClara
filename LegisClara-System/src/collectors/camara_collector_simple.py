"""
Coletor Simplificado - Apenas Câmara dos Deputados
Coleta notícias e proposições para divulgação
"""

import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class CamaraCollector:
    """Coletor simplificado de proposições da Câmara dos Deputados"""

    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa coletor da Câmara

        Args:
            config: Configuração da API da Câmara
        """
        self.base_url = config.get('base_url', 'https://dadosabertos.camara.leg.br/api/v2')
        self.timeout = config.get('timeout', 30)

    def collect_recent_proposicoes(self, days_back: int = 7,
                                   tipos: List[str] = None) -> List[Dict[str, Any]]:
        """
        Coleta proposições recentes da Câmara

        Args:
            days_back: Número de dias para buscar no passado
            tipos: Tipos de proposição (PEC, PL, etc)

        Returns:
            Lista de proposições coletadas
        """
        if tipos is None:
            tipos = ['PEC', 'PL', 'PLP', 'MP']

        data_inicio = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        data_fim = datetime.now().strftime('%Y-%m-%d')

        proposicoes = []

        for tipo in tipos:
            try:
                props_tipo = self._fetch_proposicoes_by_tipo(
                    tipo, data_inicio, data_fim
                )
                proposicoes.extend(props_tipo)
                logger.info(f"Coletadas {len(props_tipo)} proposições do tipo {tipo}")
            except Exception as e:
                logger.error(f"Erro ao coletar {tipo} da Câmara: {e}")

        return proposicoes

    def _fetch_proposicoes_by_tipo(self, tipo: str, data_inicio: str,
                                    data_fim: str) -> List[Dict[str, Any]]:
        """Busca proposições por tipo e período"""
        url = f"{self.base_url}/proposicoes"

        params = {
            'siglaTipo': tipo,
            'dataInicio': data_inicio,
            'dataFim': data_fim,
            'ordenarPor': 'id',
            'ordem': 'DESC',
            'itens': 10
        }

        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()

        data = response.json()
        proposicoes = []

        for prop in data.get('dados', []):
            try:
                detalhes = self.get_proposicao_detalhes(prop['id'])
                if detalhes:
                    proposicoes.append(detalhes)
            except Exception as e:
                logger.warning(f"Erro ao processar proposição {prop.get('id')}: {e}")

        return proposicoes

    def get_proposicao_detalhes(self, proposicao_id: int) -> Optional[Dict[str, Any]]:
        """
        Busca detalhes completos de uma proposição

        Args:
            proposicao_id: ID da proposição na Câmara

        Returns:
            Dicionário com dados da proposição
        """
        try:
            url = f"{self.base_url}/proposicoes/{proposicao_id}"

            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            prop = response.json()['dados']

            # Buscar autores
            autores = self._get_autores(proposicao_id)
            autor_principal = autores[0] if autores else 'Não informado'

            # Processar data
            data_apresentacao = None
            if prop.get('dataApresentacao'):
                data_apresentacao = datetime.fromisoformat(
                    prop['dataApresentacao'].replace('Z', '+00:00')
                ).isoformat()

            # Texto completo (ementa + justificação)
            texto_completo = prop.get('ementa', '')
            if prop.get('justificativa'):
                texto_completo += f"\n\nJUSTIFICATIVA:\n{prop['justificativa']}"

            return {
                'id_externo': str(proposicao_id),
                'tipo': prop.get('siglaTipo', ''),
                'numero': prop.get('numero'),
                'ano': prop.get('ano'),
                'ementa': prop.get('ementa', ''),
                'texto_completo': texto_completo,
                'autor': autor_principal,
                'data_apresentacao': data_apresentacao,
                'status': self._get_status(prop),
                'url_oficial': self._build_url(proposicao_id)
            }

        except Exception as e:
            logger.error(f"Erro ao buscar detalhes da proposição {proposicao_id}: {e}")
            return None

    def _get_autores(self, proposicao_id: int) -> List[str]:
        """Busca lista de autores de uma proposição"""
        try:
            url = f"{self.base_url}/proposicoes/{proposicao_id}/autores"

            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            autores_data = response.json().get('dados', [])
            return [
                autor.get('nome', 'Desconhecido')
                for autor in autores_data
            ]

        except Exception as e:
            logger.warning(f"Erro ao buscar autores: {e}")
            return []

    def _get_status(self, proposicao: Dict) -> str:
        """Determina status da proposição"""
        situacao = proposicao.get('statusProposicao', {})
        return situacao.get('descricaoSituacao', 'Em tramitação')

    def _build_url(self, proposicao_id: int) -> str:
        """Constrói URL oficial da proposição"""
        return f"https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao={proposicao_id}"
