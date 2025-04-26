import os
import zipfile
import requests
from datetime import date, datetime
from lxml import etree

# CONFIGURAÇÕES
PASTA_ZIP = 'entrada_zip'
PASTA_SAIDA = 'saida_xml'
PASTA_TEMP = 'temp_xml'
ARQUIVO_LOG = 'log_processamento.txt'
ARQUIVO_ALERTAS = 'alertas_erro.txt'

login_email = "vinnysouzav@gmail.com"
senha = "Viver0944"
tipo_dou = "DO1 DO2 DO3"  # Pode adicionar DO1E, DO2E, DO3E

url_login = "https://inlabs.in.gov.br/logar.php"
url_download = "https://inlabs.in.gov.br/index.php?p="

s = requests.Session()

# 🔥 PARSERS 🔥
def parse_dou(xml_tree):
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

def parse_anvisa(xml_tree):
    return []

def parse_ibama(xml_tree):
    return []

def parse_receita_federal(xml_tree):
    return []

parser_map = {
    'DO1': parse_dou,
    'DO2': parse_dou,
    'DO3': parse_dou,
}

# Funções auxiliares
def extrair_nome_fonte(nome_arquivo):
    partes = nome_arquivo.replace('.zip', '').split('-')
    if len(partes) >= 3:
        return partes[2]
    return None

def garantir_pastas():
    for pasta in [PASTA_ZIP, PASTA_SAIDA, PASTA_TEMP]:
        os.makedirs(pasta, exist_ok=True)

def baixar_zips(data_str):
    login_payload = {"email": login_email, "password": senha}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    print("Fazendo login...")
    s.post(url_login, data=login_payload, headers=headers)

    for dou_secao in tipo_dou.split(' '):
        url_arquivo = f"{url_download}{data_str}&dl={data_str}-{dou_secao}.zip"
        cabecalho_arquivo = {'Cookie': 'inlabs_session_cookie=' + s.cookies.get('inlabs_session_cookie', ''), 'origem': '736372697074'}
        response = s.get(url_arquivo, headers=cabecalho_arquivo)

        if response.status_code == 200:
            caminho_zip = os.path.join(PASTA_ZIP, f"{data_str}-{dou_secao}.zip")
            with open(caminho_zip, 'wb') as f:
                f.write(response.content)
            print(f"Baixado: {caminho_zip}")
        else:
            print(f"Falha ao baixar {data_str}-{dou_secao}.zip (Status {response.status_code})")

def limpar_temp():
    for arquivo in os.listdir(PASTA_TEMP):
        caminho = os.path.join(PASTA_TEMP, arquivo)
        if os.path.isfile(caminho):
            os.remove(caminho)

def processar_zip(zip_path, log, alertas):
    nome_zip = os.path.basename(zip_path)
    fonte = extrair_nome_fonte(nome_zip)

    if not fonte or fonte not in parser_map:
        alertas.append(f"Fonte desconhecida: {nome_zip}")
        return

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(PASTA_TEMP)
            for nome_arquivo in zip_ref.namelist():
                caminho_xml = os.path.join(PASTA_TEMP, nome_arquivo)
                
                tree = etree.parse(caminho_xml)
                parser = parser_map[fonte]
                materias = parser(tree)

                if materias:
                    novo_arquivo = nome_arquivo.replace('.xml', '_limpo.xml')
                    caminho_saida = os.path.join(PASTA_SAIDA, novo_arquivo)

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
                    alertas.append(f"Nenhuma matéria extraída de {nome_arquivo}")

    except Exception as e:
        alertas.append(f"Erro em {nome_zip}: {str(e)}")

    finally:
        limpar_temp()

def main():
    garantir_pastas()
    
    hoje = date.today()
    data_str = hoje.strftime("%Y-%m-%d")

    baixar_zips(data_str)

    log_geral = []
    alertas = []
    
    arquivos_zip = [f for f in os.listdir(PASTA_ZIP) if f.endswith('.zip')]
    for arquivo_zip in arquivos_zip:
        caminho_zip = os.path.join(PASTA_ZIP, arquivo_zip)
        processar_zip(caminho_zip, log_geral, alertas)

    with open(ARQUIVO_LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_geral))

    if alertas:
        with open(ARQUIVO_ALERTAS, 'w', encoding='utf-8') as f:
            f.write('\n'.join(alertas))

    print(f"✅ Processo concluído: {len(arquivos_zip)} arquivos.")
    if alertas:
        print(f"⚠️ {len(alertas)} alertas encontrados. Veja {ARQUIVO_ALERTAS}.")

if __name__ == '__main__':
    main()
