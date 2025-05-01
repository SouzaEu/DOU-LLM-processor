
from utils.arquivos import garantir_pastas, salvar_json, limpar_temp
from utils.texto import limpar_texto, nome_arquivo_seguro
from utils.resumo import resumir_conteudo
from parser.dou_parser import parse_article
from lxml import etree
import os
from dotenv import load_dotenv

load_dotenv()

PASTA_TEMP = 'temp_xml_DO1'
PASTA_MATERIAS = 'saida_materias'
PASTA_RESUMOS = 'saida_resumos'
ARQUIVO_LOG = 'log_processamento.txt'
ARQUIVO_ALERTAS = 'alertas_erro.txt'

def processar_xmls_extraidos(pasta_xml, log, alertas):
    arquivos_xml = [f for f in os.listdir(pasta_xml) if f.lower().endswith('.xml')]
    for arquivo_xml in arquivos_xml:
        caminho_xml = os.path.join(pasta_xml, arquivo_xml)
        try:
            tree = etree.parse(caminho_xml)
            materias = parse_article(tree)
            for materia in materias:
                orgao = limpar_texto(materia.get('orgao'))
                titulo = limpar_texto(materia.get('titulo'))
                conteudo = limpar_texto(materia.get('conteudo') or materia.get('texto'))
                if not (orgao and titulo and conteudo):
                    continue
                base_nome = nome_arquivo_seguro(f"{orgao}_{titulo}")[:80]
                materia_formatada = {
                    "orgao": orgao,
                    "data": materia.get('data'),
                    "titulo": titulo,
                    "conteudo": conteudo
                }
                salvar_json(materia_formatada, os.path.join(PASTA_MATERIAS, f"{base_nome}.json"))
                resumo = resumir_conteudo(conteudo)
                resumo_formatado = {
                    "orgao": orgao,
                    "data": materia_formatada["data"],
                    "titulo": titulo,
                    "resumo_simplificado": resumo
                }
                salvar_json(resumo_formatado, os.path.join(PASTA_RESUMOS, f"{base_nome}_resumo.json"))
                log.append(f"Processado e resumido: {titulo}")
        except Exception as e:
            alertas.append(f"Erro em {arquivo_xml}: {str(e)}")

def main():
    garantir_pastas()
    log_geral = []
    alertas = []
    processar_xmls_extraidos(PASTA_TEMP, log_geral, alertas)
    with open(ARQUIVO_LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_geral))
    if alertas:
        with open(ARQUIVO_ALERTAS, 'w', encoding='utf-8') as f:
            f.write('\n'.join(alertas))
    print(f"\nFinalizado processamento manual de XMLs.")
    if alertas:
        print(f"{len(alertas)} alertas encontrados.")

if __name__ == '__main__':
    main()
