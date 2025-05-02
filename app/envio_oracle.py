import cx_Oracle
import json

def enviar_para_banco(arquivo_json, conexao):
    with open(arquivo_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    resumo_simplificado_texto = "\n".join(dados.get("resumo_simplificado", []))

    cursor = conexao.cursor()
    insert_sql = '''
    INSERT INTO RESUMOS_DOU (
        ORGAO,
        DATA_PUBLICACAO,
        TITULO,
        TITULO_RESUMIDO,
        CONTEUDO,
        DESCRICAO_BREVE,
        RESUMO_SIMPLIFICADO,
        ORGAO_RESUMIDO,
        DATA_NORMA
    )
    VALUES (
        :1, TO_DATE(:2, 'YYYY-MM-DD'), :3, :4, :5, :6, :7, :8, TO_DATE(:9, 'YYYY-MM-DD')
    )
    '''
    cursor.execute(insert_sql, (
        dados['orgao'],
        dados['data'],
        dados['titulo'],
        dados['titulo_resumido'],
        dados['conteudo'],
        dados.get('descricao_breve', ''),
        resumo_simplificado_texto,
        dados.get('orgao_resumido', ''),
        dados.get('data_norma', '')
    ))
    conexao.commit()
    cursor.close()
