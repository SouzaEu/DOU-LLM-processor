import os
import zipfile
from lxml import etree
from datetime import datetime

# CONFIGURAÇÕES
PASTA_ZIP = 'entrada_zip'
PASTA_SAIDA = 'saida_xml'
PASTA_TEMP = 'temp_xml'
ARQUIVO_LOG = 'log_processamento.txt'
ARQUIVO_ALERTAS = 'alertas_erro.txt'

# Garantir pastas necessárias
for pasta in [PASTA_SAIDA, PASTA_TEMP]:
    os.makedirs(pasta, exist_ok=True)

# 🔥 PARSERS 🔥

def parse_dou(xml_tree):
    """
    Parser específico para arquivos do Diário Oficial da União (DOU)
    """
    root = xml_tree.getroot()
    materias_extraidas = []

    for secao in root.findall('.//secao'):
        for materia in secao.findall('materia'):
            materias_extraidas.append({
                'identificador': materia.findtext('identificador'),
                'orgao': materia.findtext('orgao'),
                'dataPublicacao': materia.findtext('dataPublicacao'),
                'titulo': materia.findtext('titulo'),
                'texto': materia.findtext('texto')
            })
    return materias_extraidas

# Exemplos de parsers vazios para outras fontes futuras
def parse_anvisa(xml_tree):
    """
    Parser específico para arquivos da Anvisa
    """
    return []

def parse_ibama(xml_tree):
    """
    Parser específico para arquivos do Ibama
    """
    return []

def parse_receita_federal(xml_tree):
    """
    Parser específico para arquivos da Receita Federal
    """
    return []

# Mapeamento de parser
parser_map = {
    'DO1': parse_dou,
    'DO2': parse_dou,  # Exemplo: outros DOs podem usar o mesmo parser inicialmente
    'DO3': parse_dou,
    # 'ANVISA': parse_anvisa,
    # 'IBAMA': parse_ibama,
    # 'RECEITA': parse_receita_federal,
}

# Funções auxiliares
def extrair_nome_fonte(nome_arquivo):
    """ Extrai a fonte do nome do arquivo zip: exemplo 2025-04-23-DO1 -> DO1 """
    partes = nome_arquivo.replace('.zip', '').split('-')
    if len(partes) >= 3:
        return partes[2]
    return None

def processar_zip(zip_path, log, alertas):
    nome_zip = os.path.basename(zip_path)
    fonte = extrair_nome_fonte(nome_zip)

    if not fonte or fonte not in parser_map:
        alertas.append(f"Fonte desconhecida ou não mapeada para o arquivo: {nome_zip}")
        return

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(PASTA_TEMP)
            for nome_arquivo in zip_ref.namelist():
                caminho_xml = os.path.join(PASTA_TEMP, nome_arquivo)
                
                tree = etree.parse(caminho_xml)
                parser = parser_map[fonte]
                materias = parser(tree)

                # Salva o resultado (aqui vamos apenas salvar como XML limpo para exemplo)
                if materias:
                    novo_arquivo = nome_arquivo.replace('.xml', '_limpo.xml')
                    caminho_saida = os.path.join(PASTA_SAIDA, novo_arquivo)
                    
                    # Cria XML de saída simples
                    root_saida = etree.Element('materias')

                    for mat in materias:
                        materia_elem = etree.SubElement(root_saida, 'materia')
                        for key, value in mat.items():
                            if value:
                                child = etree.SubElement(materia_elem, key)
                                child.text = value

                    tree_saida = etree.ElementTree(root_saida)
                    tree_saida.write(caminho_saida, pretty_print=True, xml_declaration=True, encoding='UTF-8')

                    log.append(f"Processado {nome_arquivo} com parser {fonte}")
                else:
                    alertas.append(f"Nenhuma matéria extraída em {nome_arquivo}")

    except Exception as e:
        alertas.append(f"Erro ao processar {nome_zip}: {str(e)}")

    finally:
        limpar_temp()

def limpar_temp():
    """ Limpa a pasta temporária """
    for arquivo in os.listdir(PASTA_TEMP):
        caminho = os.path.join(PASTA_TEMP, arquivo)
        if os.path.isfile(caminho):
            os.remove(caminho)

def main():
    log_geral = []
    alertas = []

    arquivos_zip = [f for f in os.listdir(PASTA_ZIP) if f.endswith('.zip')]

    for arquivo_zip in arquivos_zip:
        caminho_zip = os.path.join(PASTA_ZIP, arquivo_zip)
        processar_zip(caminho_zip, log_geral, alertas)

    # Salvar log
    with open(ARQUIVO_LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_geral))

    # Salvar alertas
    if alertas:
        with open(ARQUIVO_ALERTAS, 'w', encoding='utf-8') as f:
            f.write('\n'.join(alertas))

    print(f"Processados {len(arquivos_zip)} arquivos zip.")
    if alertas:
        print(f"Atenção: houve {len(alertas)} alertas! Verifique {ARQUIVO_ALERTAS}.")

if __name__ == '__main__':
    main()
