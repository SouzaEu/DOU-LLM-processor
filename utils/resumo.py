
import openai
import os
import cx_Oracle
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_DSN = os.getenv('DB_DSN')

def salvar_resumo_no_banco(orgao, data, titulo, resumo):
    try:
        connection = cx_Oracle.connect(DB_USER, DB_PASS, DB_DSN)
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO RESUMOS_REGULATORIOS (ORGAO, DATA_PUBLICACAO, TITULO, RESUMO)
            VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD'), :3, :4)
        """, (orgao, data, titulo, resumo))
        connection.commit()
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

def resumir_conteudo(conteudo, orgao, data, titulo):
    prompt = f"""Resuma o seguinte conteúdo regulatório em português simples, focado nas mudanças mais importantes para empresas afetadas:\n\n{conteudo}"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um analista regulatório."},
            {"role": "user", "content": prompt}
        ]
    )
    resumo = response['choices'][0]['message']['content'].strip()
    salvar_resumo_no_banco(orgao, data, titulo, resumo)
    return resumo
