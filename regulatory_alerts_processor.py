import os
import zipfile
import json
import requests
from datetime import date
from lxml import etree
from dotenv import load_dotenv
import openai
import re

# Carrega variáveis do .env
load_dotenv()

# Configurações
PASTA_ZIP = 'entrada_zip'
PASTA_TEMP = 'temp_xml'
PASTA_MATERIAS = 'saida_materias'
PASTA_RESUMOS = 'saida_resumos'
ARQUIVO_LOG = 'log_processamento.txt'
ARQUIVO_ALERTAS = 'alertas_erro.txt'

login_email = os.getenv('LOGIN_EMAIL')
senha = os.getenv('LOGIN_SENHA')
openai.api_key = os.getenv('OPENAI_API_KEY')

tipo_dou = "DO1 DO2 DO3"
url_login = "https://inlabs.in.gov.br/logar.php"
url_download = "https://inlabs.in.gov.br/index.php?p="

s = requests.Session()

# 🔥 PARSERS 🔥
def parse_article(xml_tree):
    root = xml_tree.getroot()
    materias = []
    for article in root.findall('.//article'):
        materias.append({
            'orgao': article.attrib.get('artCategory', ''),
            'data': article.attrib.get('pubDate', ''),
            'titulo': article.attrib.get('name', ''),
            'conteudo': article.findtext('.//Texto') or article.findtext('.//body')
        })
    return materias

def parse_dou(xml_tree):
    root = xml_tree.getroot()
    materias = []
    for secao in root.findall('.//secao'):
        for materia in secao.findall('materia'):
            materias.append({
                'orgao': materia.findtext('orgao'),
                'data': materia.findtext('dataPublicacao'),
                'titulo': materia.findtext('titulo'),
                'conteudo': materia.findtext('texto')
            })
    return materias

def parse_generico(xml_tree):
    root = xml_tree.getroot()
    materias = []
    for materia in root.findall('.//materia'):
        mat = {}
        for elem in materia.iterchildren():
            if elem.tag and elem.text:
                mat[elem.tag] = elem.text.strip()
        materias.append(mat)
    return materias

parser_map = {
    'DO1': parse_article,
    'DO2': parse_article,
    'DO3': parse_article,
}

# Funções auxiliares
def limpar_texto(texto):
    if not texto:
        return None
    texto = texto.strip().replace('\n', ' ').replace('\r', ' ')
    return ' '.join(texto.split())

def extrair_nome_fonte(nome_arquivo):
    partes = nome_arquivo.replace('.zip', '').split('-')
    return partes[2] if len(partes) >= 3 else None

def garantir_pastas():
    for pasta in [PASTA_ZIP, PASTA_TEMP, PASTA_MATERIAS, PASTA_RESUMOS]:
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

def resumir_conteudo(conteudo):
    prompt = f"""
Resuma o seguinte conteúdo regulatório em português simples, focado nas mudanças mais importantes para empresas afetadas:

{conteudo}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um analista regulatório."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

def salvar_json(dados, caminho_saida):
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def nome_arquivo_seguro(nome):
    # Substitui caracteres inválidos por _
    return re.sub(r'[\\/:*?"<>|]', '_', nome)

def processar_zip(zip_path, log, alertas):
    nome_zip = os.path.basename(zip_path)
    fonte = extrair_nome_fonte(nome_zip)
    parser = parser_map.get(fonte, parse_generico)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(PASTA_TEMP)
            for nome_arquivo in zip_ref.namelist():
                if not nome_arquivo.lower().endswith('.xml'):
                    continue  # Só processa arquivos XML
                caminho_xml = os.path.join(PASTA_TEMP, nome_arquivo)
                tree = etree.parse(caminho_xml)
                materias = parser(tree)

                for materia in materias:
                    orgao = limpar_texto(materia.get('orgao'))
                    titulo = limpar_texto(materia.get('titulo'))
                    conteudo = limpar_texto(materia.get('conteudo') or materia.get('texto'))

                    if not (orgao and titulo and conteudo):
                        continue

                    base_nome = f"{orgao}_{titulo}".replace(' ', '_')[:80]

                    materia_formatada = {
                        "orgao": orgao,
                        "data": materia.get('data') or materia.get('dataPublicacao'),
                        "titulo": titulo,
                        "conteudo": conteudo
                    }

                    caminho_materia = os.path.join(PASTA_MATERIAS, f"{base_nome}.json")
                    salvar_json(materia_formatada, caminho_materia)

                    # Agora gera o resumo
                    resumo = resumir_conteudo(conteudo)

                    resumo_formatado = {
                        "orgao": orgao,
                        "data": materia_formatada["data"],
                        "titulo": titulo,
                        "resumo_simplificado": resumo
                    }

                    caminho_resumo = os.path.join(PASTA_RESUMOS, f"{base_nome}_resumo.json")
                    salvar_json(resumo_formatado, caminho_resumo)

                    log.append(f"Processado e resumido: {titulo}")

    except Exception as e:
        alertas.append(f"Erro em {nome_zip}: {str(e)}")

    finally:
        limpar_temp()

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
                caminho_materia = os.path.join(PASTA_MATERIAS, f"{base_nome}.json")
                salvar_json(materia_formatada, caminho_materia)
                resumo = resumir_conteudo(conteudo)
                resumo_formatado = {
                    "orgao": orgao,
                    "data": materia_formatada["data"],
                    "titulo": titulo,
                    "resumo_simplificado": resumo
                }
                caminho_resumo = os.path.join(PASTA_RESUMOS, f"{base_nome}_resumo.json")
                salvar_json(resumo_formatado, caminho_resumo)
                log.append(f"Processado e resumido: {titulo}")
        except Exception as e:
            alertas.append(f"Erro em {arquivo_xml}: {str(e)}")

def main():
    garantir_pastas()
    #hoje = date.today()
    #data_str = hoje.strftime("%Y-%m-%d")
    #baixar_zips(data_str)
    log_geral = []
    alertas = []
    #arquivos_zip = [f for f in os.listdir(PASTA_ZIP) if f.endswith('.zip')]
    #for arquivo_zip in arquivos_zip:
    #    caminho_zip = os.path.join(PASTA_ZIP, arquivo_zip)
    #    processar_zip(caminho_zip, log_geral, alertas)
    # Processar XMLs extraídos manualmente
    processar_xmls_extraidos('temp_xml_DO1', log_geral, alertas)
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
