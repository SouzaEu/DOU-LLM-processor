import os
from dotenv import load_dotenv

load_dotenv()

# Variáveis de ambiente
LOGIN_EMAIL = os.getenv("INLABS_EMAIL")
LOGIN_SENHA = os.getenv("INLABS_SENHA")

# Diretórios e URLs
PASTA_TEMP = "temp"
PASTA_MATERIAS = "output/materias"
PASTA_RESUMOS = "output/resumos"
ARQUIVO_LOG = "logs/log_processamento.txt"
ARQUIVO_ALERTAS = "logs/alertas_erro.txt"
ZIP_DOWNLOAD_DIR = "downloads"

TIPO_DOU = "DO1 DO2 DO3"
URL_LOGIN = "https://inlabs.in.gov.br/logar.php"
URL_DOWNLOAD = "https://inlabs.in.gov.br/index.php?p="

# Criação automática de pastas
os.makedirs(PASTA_TEMP, exist_ok=True)
os.makedirs(PASTA_MATERIAS, exist_ok=True)
os.makedirs(PASTA_RESUMOS, exist_ok=True)
os.makedirs(ZIP_DOWNLOAD_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)