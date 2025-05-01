import requests
from datetime import date
from app.config import LOGIN_EMAIL, LOGIN_SENHA, TIPO_DOU, URL_LOGIN, URL_DOWNLOAD, ZIP_DOWNLOAD_DIR
import os

s = requests.Session()

def fazer_login():
    payload = {"email": LOGIN_EMAIL, "password": LOGIN_SENHA}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    response = s.request("POST", URL_LOGIN, data=payload, headers=headers)
    return response.ok and s.cookies.get("inlabs_session_cookie")

def baixar_zips():
    if not fazer_login():
        print("Erro ao fazer login no portal Inlabs. Verifique credenciais.")
        return

    cookie = s.cookies.get("inlabs_session_cookie")
    today = date.today().strftime("%Y-%m-%d")

    for secao in TIPO_DOU.split():
        print(f"Baixando seção {secao}...")
        nome_arquivo = f"{today}-{secao}.zip"
        url = f"{URL_DOWNLOAD}{today}&dl={nome_arquivo}"
        headers = {'Cookie': f'inlabs_session_cookie={cookie}', 'origem': '736372697074'}

        response = s.get(url, headers=headers)
        if response.status_code == 200 and response.content.startswith(b'PK'):
            os.makedirs(ZIP_DOWNLOAD_DIR, exist_ok=True)
            zip_path = os.path.join(ZIP_DOWNLOAD_DIR, nome_arquivo)
            with open(zip_path, "wb") as f:
                f.write(response.content)
            print(f"✔ Arquivo salvo: {zip_path}")
        else:
            print(f"✘ Nenhum arquivo disponível ou conteúdo inválido para {secao}")