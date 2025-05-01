import os
from app.summarizer import resumir_texto
from lxml import etree
from utils.texto import limpar_texto, nome_arquivo_seguro
from utils.arquivos import salvar_json
from parser.dou_parser import parse_article

def processar_xmls_extraidos(pasta_xml, log, alertas, pasta_materias):
    arquivos_xml = [f for f in os.listdir(pasta_xml) if f.lower().endswith('.xml')]
    for arquivo_xml in arquivos_xml:
        caminho_xml = os.path.join(pasta_xml, arquivo_xml)
        try:
            tree = etree.parse(caminho_xml)
            materias = parse_article(tree)
            for materia in materias[:3]:  # Limitar a 3 matérias para testes
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
                resultado = resumir_texto(conteudo)
                materia_formatada['titulo_resumido'] = resultado['titulo_resumido']
                materia_formatada['resumo'] = resultado['resumo']
                salvar_json(materia_formatada, os.path.join(pasta_materias, f"{base_nome}.json"))
                log.write(f"[OK] {arquivo_xml}\n")
        except Exception as e:
            alertas.write(f"[ERRO] {arquivo_xml} - {str(e)}\n")