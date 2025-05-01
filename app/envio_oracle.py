# Script preparado para futura integração com Oracle Database via cx_Oracle

import cx_Oracle
import os
import json

def enviar_para_banco(arquivo_json, conexao):
    with open(arquivo_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    cursor = conexao.cursor()
    insert_sql = '''
    INSERT INTO RESUMOS_DOU (ORGAO, DATA_PUBLICACAO, TITULO, TITULO_RESUMIDO, CONTEUDO, RESUMO)
    VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD'), :3, :4, :5, :6)
    '''
    cursor.execute(insert_sql, (
        dados['orgao'],
        dados['data'],
        dados['titulo'],
        dados['titulo_resumido'],
        dados['conteudo'],
        dados['resumo']
    ))
    conexao.commit()
    cursor.close()