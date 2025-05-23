from app.config import PASTA_ZIP, PASTA_TEMP, PASTA_MATERIAS, PASTA_RESUMOS

import os
import json

def garantir_pastas():
    for pasta in [PASTA_ZIP, PASTA_TEMP, PASTA_MATERIAS, PASTA_RESUMOS]:
        os.makedirs(pasta, exist_ok=True)

def limpar_temp():
    for arquivo in os.listdir(PASTA_TEMP):
        caminho = os.path.join(PASTA_TEMP, arquivo)
        if os.path.isfile(caminho):
            os.remove(caminho)

def salvar_json(dados, caminho_saida):
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
