
import re

def limpar_texto(texto):
    if not texto:
        return None
    texto = texto.strip().replace('\n', ' ').replace('\r', ' ')
    return ' '.join(texto.split())

def nome_arquivo_seguro(nome):
    return re.sub(r'[\\/:*?"<>|]', '_', nome)
