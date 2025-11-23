"""
API REST para o Portal Administrativo LegisClara
Fornece endpoints para controle da pipeline via interface web
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os
import sys
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Permitir requisições do frontend

# Caminho para o LegisClara-System
SYSTEM_PATH = Path(__file__).parent.parent / "LegisClara-System"
MAIN_SCRIPT = SYSTEM_PATH / "main.py"


@app.route('/api/status', methods=['GET'])
def get_status():
    """Retorna status atual do sistema"""
    return jsonify({
        'status': 'ok',
        'system_path': str(SYSTEM_PATH),
        'python_version': sys.version
    })


@app.route('/api/pipeline/start', methods=['POST'])
def start_pipeline():
    """Inicia a pipeline completa"""
    try:
        data = request.get_json() or {}
        max_videos = data.get('max_videos', 1)

        # Executar main.py do LegisClara-System
        result = subprocess.run(
            [sys.executable, str(MAIN_SCRIPT)],
            cwd=str(SYSTEM_PATH),
            capture_output=True,
            text=True,
            timeout=3600  # 1 hora timeout
        )

        return jsonify({
            'success': True,
            'message': 'Pipeline executada com sucesso',
            'stdout': result.stdout[-500:] if result.stdout else '',  # Últimos 500 chars
            'stderr': result.stderr[-500:] if result.stderr else ''
        })

    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Pipeline excedeu o tempo limite de 1 hora'
        }), 408

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/pipeline/collect', methods=['POST'])
def collect_only():
    """Apenas coleta proposições sem processar"""
    try:
        # Aqui você poderia importar diretamente o collector
        from sys import path
        path.insert(0, str(SYSTEM_PATH))

        from src.collectors.camara_collector_simple import ColetorCamaraSimples

        coletor = ColetorCamaraSimples()
        proposicoes = coletor.coletar_proposicoes_recentes(limite=10)

        return jsonify({
            'success': True,
            'message': f'{len(proposicoes)} proposições coletadas',
            'count': len(proposicoes),
            'proposicoes': [
                {
                    'id': p.get('id'),
                    'tipo': p.get('tipo'),
                    'numero': p.get('numero'),
                    'ano': p.get('ano'),
                    'ementa': p.get('ementa', '')[:100] + '...'
                }
                for p in proposicoes[:5]  # Retornar apenas primeiras 5
            ]
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/videos/list', methods=['GET'])
def list_videos():
    """Lista vídeos gerados"""
    try:
        videos_dir = SYSTEM_PATH / "data" / "videos"

        if not videos_dir.exists():
            return jsonify({
                'success': True,
                'videos': []
            })

        videos = []
        for file in videos_dir.glob("*_video.mp4"):
            videos.append({
                'filename': file.name,
                'size': file.stat().st_size,
                'created': file.stat().st_ctime
            })

        videos.sort(key=lambda x: x['created'], reverse=True)

        return jsonify({
            'success': True,
            'count': len(videos),
            'videos': videos[:10]  # Últimos 10 vídeos
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/logs/recent', methods=['GET'])
def get_recent_logs():
    """Retorna logs recentes do sistema"""
    try:
        log_file = SYSTEM_PATH / "legisclara.log"

        if not log_file.exists():
            return jsonify({
                'success': True,
                'logs': []
            })

        # Ler últimas 50 linhas
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            recent_lines = lines[-50:]

        logs = []
        for line in recent_lines:
            if ' - ' in line:
                parts = line.split(' - ', 2)
                if len(parts) >= 3:
                    logs.append({
                        'timestamp': parts[0].strip(),
                        'level': parts[1].strip(),
                        'message': parts[2].strip()
                    })

        return jsonify({
            'success': True,
            'count': len(logs),
            'logs': logs
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Retorna estatísticas do sistema"""
    try:
        videos_dir = SYSTEM_PATH / "data" / "videos"
        video_count = len(list(videos_dir.glob("*_video.mp4"))) if videos_dir.exists() else 0

        return jsonify({
            'success': True,
            'stats': {
                'total_videos': video_count,
                'system_status': 'idle',
                'last_execution': None
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("🚀 LegisClara Portal API")
    print(f"📁 System Path: {SYSTEM_PATH}")
    print("🌐 Server: http://localhost:5000")
    print("\n⚠️  IMPORTANTE: Esta é uma API de desenvolvimento")
    print("    Para produção, use um servidor WSGI (Gunicorn, uWSGI)")

    app.run(debug=True, host='0.0.0.0', port=5000)
