import os
import zipfile
import json
from app.config import ZIP_DOWNLOAD_DIR, PASTA_TEMP, PASTA_RESUMOS
from utils.arquivos import salvar_json

def extrair_zips():
    os.makedirs(PASTA_TEMP, exist_ok=True)
    arquivos_zip = [f for f in os.listdir(ZIP_DOWNLOAD_DIR) if f.endswith('.zip')]
    zip_validos = 0
    for zip_nome in arquivos_zip:
        zip_path = os.path.join(ZIP_DOWNLOAD_DIR, zip_nome)
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(PASTA_TEMP)
            print(f"✔ Extraído: {zip_nome}")
            zip_validos += 1
        except zipfile.BadZipFile:
            print(f"✘ Arquivo corrompido ou inválido: {zip_nome}")

    if zip_validos == 0:
        # Cria JSON indicando que não houve publicação
        mensagem = {
            "data": os.path.basename(arquivos_zip[0])[:10] if arquivos_zip else "data_desconhecida",
            "mensagem": "Nenhuma publicação do DOU foi encontrada nesta data. Feriado ou indisponibilidade."
        }
        os.makedirs(PASTA_RESUMOS, exist_ok=True)
        salvar_json(mensagem, os.path.join(PASTA_RESUMOS, "aviso_dia_sem_dou.json"))
        print("⚠ Nenhum ZIP válido encontrado. Mensagem registrada.")