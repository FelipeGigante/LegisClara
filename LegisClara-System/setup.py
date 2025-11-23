"""
Script de Setup do LegisClara
Facilita instalação e configuração inicial
"""

import os
import sys
import subprocess
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def print_header(text):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python_version():
    """Verifica versão do Python"""
    print_header("Verificando Python")

    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ é necessário!")
        print(f"   Versão atual: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)

    print(f"✅ Python {version.major}.{version.minor}.{version.micro} OK")


def check_ffmpeg():
    """Verifica se FFmpeg está instalado"""
    print_header("Verificando FFmpeg")

    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ FFmpeg instalado")
            return True
    except FileNotFoundError:
        pass

    print("⚠️  FFmpeg não encontrado!")
    print("   Instale FFmpeg:")
    print("   - Windows: https://ffmpeg.org/download.html")
    print("   - Linux: sudo apt install ffmpeg")
    print("   - macOS: brew install ffmpeg")
    return False


def create_env_file():
    """Cria arquivo .env se não existir"""
    print_header("Configurando .env")

    if Path('.env').exists():
        print("⚠️  .env já existe, pulando...")
        return

    env_example = Path('.env.example')
    if env_example.exists():
        import shutil
        shutil.copy('.env.example', '.env')
        print("✅ Arquivo .env criado")
        print("   ⚠️  EDITE .env com suas API keys!")
    else:
        print("❌ .env.example não encontrado")


def install_dependencies():
    """Instala dependências Python"""
    print_header("Instalando Dependências")

    print("Instalando pacotes Python...")
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("✅ Dependências instaladas com sucesso")
    else:
        print("❌ Erro ao instalar dependências:")
        print(result.stderr)
        sys.exit(1)


def create_directories():
    """Cria diretórios necessários"""
    print_header("Criando Diretórios")

    dirs = [
        'logs',
        'data/raw',
        'data/processed',
        'data/videos',
        'data/reports',
        'database'
    ]

    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

    print("✅ Diretórios criados")


def initialize_database():
    """Inicializa banco de dados"""
    print_header("Inicializando Banco de Dados")

    try:
        from src.database import Database
        db = Database()
        print("✅ Banco de dados inicializado")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")


def main():
    """Função principal de setup"""
    print("\n" + "=" * 60)
    print("  🏛️  LegisClara - Setup")
    print("  Sistema de Engajamento Cidadão")
    print("=" * 60)

    # Verificações
    check_python_version()
    ffmpeg_ok = check_ffmpeg()

    # Setup
    create_directories()
    create_env_file()
    install_dependencies()
    initialize_database()

    # Resumo final
    print_header("Setup Concluído!")

    print("✅ Instalação básica completa\n")
    print("📝 Próximos passos:")
    print("   1. Edite o arquivo .env com suas API keys")
    print("   2. Revise config/config.yaml")

    if not ffmpeg_ok:
        print("   3. Instale FFmpeg")

    print("\n🚀 Para executar:")
    print("   python main.py")

    print("\n📖 Documentação completa:")
    print("   Leia README.md e EXEMPLOS.md")

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
