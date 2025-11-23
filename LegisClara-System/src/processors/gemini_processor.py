"""
Processador de Legislações usando Google Gemini API
Gera resumos acessíveis e roteiros para vídeos
"""

import json
import logging
from typing import Dict, Any
import google.generativeai as genai

logger = logging.getLogger(__name__)


class GeminiProcessor:
    """Processador de legislações com Google Gemini (gratuito)"""

    def __init__(self, api_key: str):
        """
        Inicializa processador Gemini

        Args:
            api_key: Chave da API Google Gemini
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')  # Modelo gratuito

    def processar_legislacao(self, legislacao: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa uma legislação gerando resumo acessível e roteiro

        Args:
            legislacao: Dados da legislação

        Returns:
            Dicionário com dados processados
        """
        logger.info(
            f"Processando {legislacao['tipo']} {legislacao['numero']}/{legislacao['ano']}"
        )

        try:
            # Preparar prompt
            prompt = self._build_prompt(legislacao)

            # Chamar Gemini API
            response = self.model.generate_content(prompt)

            # Parse da resposta
            resultado = self._parse_resposta(response.text)

            if not resultado:
                raise ValueError("Resposta do Gemini não retornou dados válidos")

            logger.info(f"Legislação processada com sucesso")
            return resultado

        except Exception as e:
            logger.error(f"Erro ao processar legislação: {e}")
            raise

    def _build_prompt(self, legislacao: Dict[str, Any]) -> str:
        """Constrói o prompt para o Gemini"""
        texto = legislacao.get('texto_completo', legislacao['ementa'])[:4000]

        prompt = f"""Você é uma influenciadora digital que transforma notícias do Congresso em conteúdo acessível.

Analise esta proposição legislativa e crie um resumo MUITO acessível em linguagem simples:

**Tipo:** {legislacao['tipo']} {legislacao['numero']}/{legislacao['ano']}
**Ementa:** {legislacao['ementa']}
**Autor:** {legislacao.get('autor', 'Não informado')}
**Texto Completo:**
{texto}

Retorne APENAS um JSON (sem markdown, sem ```json```) com esta estrutura EXATA:

{{
  "titulo_simples": "Título curto e chamativo (máx 60 caracteres)",
  "resumo_cidadao": "Resumo em 2-3 frases MUITO simples, como se explicasse para uma criança",
  "quem_impacta": "Quem é afetado por isso",
  "roteiro_video": {{
    "gancho": "Frase de abertura impactante (10-15 palavras)",
    "desenvolvimento": "Explicação do que muda (30-40 palavras)",
    "impacto": "Como isso afeta as pessoas (20-30 palavras)",
    "call_to_action": "Chamada para engajamento (10-15 palavras)"
  }},
  "pergunta_engajamento": "Pergunta para comentários",
  "hashtags": ["#tag1", "#tag2", "#tag3"]
}}

IMPORTANTE:
- Use linguagem de 8ª série do ensino fundamental
- Seja objetiva e clara
- Evite jargão jurídico
- Foque no impacto prático
- Seja neutra, sem viés político
"""

        return prompt

    def _parse_resposta(self, resposta: str) -> Dict[str, Any]:
        """
        Parse da resposta JSON do Gemini

        Args:
            resposta: Texto da resposta

        Returns:
            Dicionário parseado
        """
        try:
            # Limpar resposta (remover markdown se houver)
            resposta_limpa = resposta.strip()

            # Remover ```json e ``` se existirem
            if resposta_limpa.startswith('```json'):
                resposta_limpa = resposta_limpa[7:]
            if resposta_limpa.startswith('```'):
                resposta_limpa = resposta_limpa[3:]
            if resposta_limpa.endswith('```'):
                resposta_limpa = resposta_limpa[:-3]

            resposta_limpa = resposta_limpa.strip()

            # Encontrar JSON
            start_idx = resposta_limpa.find('{')
            end_idx = resposta_limpa.rfind('}') + 1

            if start_idx == -1 or end_idx == 0:
                logger.error("JSON não encontrado na resposta")
                return None

            json_str = resposta_limpa[start_idx:end_idx]
            return json.loads(json_str)

        except json.JSONDecodeError as e:
            logger.error(f"Erro ao parsear JSON: {e}")
            logger.debug(f"Resposta recebida: {resposta}")
            return None

    def gerar_caption_social(self, processamento: Dict[str, Any],
                            legislacao: Dict[str, Any]) -> str:
        """
        Gera caption para redes sociais

        Args:
            processamento: Dados processados da legislação
            legislacao: Dados originais da legislação

        Returns:
            Caption formatada
        """
        # Resumo breve
        resumo_completo = processamento['resumo_cidadao']
        frases = resumo_completo.split('.')[:2]
        resumo_breve = '.'.join(frases) + '.'

        caption = f"""{processamento['titulo_simples']}

{resumo_breve}

💬 {processamento['pergunta_engajamento']}

📋 {legislacao['tipo']} {legislacao['numero']}/{legislacao['ano']}
👤 Autor: {legislacao.get('autor', 'Não informado')}

{' '.join(processamento['hashtags'])}

#LegislacaoBrasileira #CidadaniaAtiva #DemocraciaParticipativa"""

        return caption
