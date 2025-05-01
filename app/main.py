from app.downloader import baixar_zips
from app.extractor import extrair_zips
from app.processor import processar_xmls_extraidos
from app.config import PASTA_TEMP, PASTA_MATERIAS, ARQUIVO_LOG, ARQUIVO_ALERTAS

def main():
    baixar_zips()
    extrair_zips()
    with open(ARQUIVO_LOG, 'a', encoding='utf-8') as log, open(ARQUIVO_ALERTAS, 'a', encoding='utf-8') as alertas:
        processar_xmls_extraidos(PASTA_TEMP, log, alertas, PASTA_MATERIAS)

if __name__ == '__main__':
    main()