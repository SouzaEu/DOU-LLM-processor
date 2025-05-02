import requests
from datetime import datetime

LLAMA_API_URL = "http://localhost:11434/api/generate"

def resumir_texto(texto):
    prompt = (
        "Você é um assistente especializado em legislação brasileira.\n\n"
        "A partir do texto abaixo, gere os seguintes campos de forma clara e útil para exibição em sistemas e celulares:\n\n"
        "1. TÍTULO CURTO: Resuma a norma de forma objetiva em até 12 palavras.\n"
        "   Exemplo: 'Prorrogação do Processo Seletivo para Professor Substituto'.\n"
        "2. DESCRIÇÃO BREVE: Em até 2 frases, explique diretamente a novidade ou impacto da norma.\n"
        "3. RESUMO SIMPLIFICADO: De 3 a 6 tópicos com até 15 palavras cada, destacando os pontos principais.\n"
        "4. ÓRGÃO RESUMIDO: Nome claro e compacto da instituição responsável, sem cargos nem formalidades. Ex: 'IFES - Campus Centro Serrano', 'Banco Central'.\n"
        "5. DATA DA NORMA: No formato YYYY-MM-DD, mesmo se aproximada com base no texto.\n\n"
        "Formato esperado:\n"
        "TÍTULO: <...>\n"
        "DESCRIÇÃO BREVE: <...>\n"
        "RESUMO SIMPLIFICADO:\n- ...\n- ...\n"
        "ÓRGÃO: <...>\n"
        "DATA DA NORMA: <...>\n\n"
        f"TEXTO:\n{texto}"
    )

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        print("⏳ Enviando texto ao modelo LLaMA para gerar resumo...")
        response = requests.post(LLAMA_API_URL, json=payload, timeout=180)

        if response.ok:
            resultado = response.json().get("response", "")
            titulo = ""
            descricao_breve = ""
            resumo_topicos = []
            orgao = ""
            data_norma = ""

            linhas = resultado.splitlines()
            for linha in linhas:
                if linha.startswith("TÍTULO:"):
                    titulo = linha.replace("TÍTULO:", "").strip()
                elif linha.startswith("DESCRIÇÃO BREVE:"):
                    descricao_breve = linha.replace("DESCRIÇÃO BREVE:", "").strip()
                elif linha.startswith("- "):
                    resumo_topicos.append(linha.strip())
                elif linha.startswith("ÓRGÃO:"):
                    orgao = linha.replace("ÓRGÃO:", "").strip()
                elif linha.startswith("DATA DA NORMA:"):
                    data_norma = linha.replace("DATA DA NORMA:", "").strip()
                    try:
                        datetime.strptime(data_norma, "%Y-%m-%d")
                    except ValueError:
                        data_norma = ""

            return {
                "titulo_resumido": titulo,
                "descricao_breve": descricao_breve,
                "resumo_simplificado": resumo_topicos,
                "orgao_resumido": orgao,
                "data_norma": data_norma
            }
        else:
            return {
                "titulo_resumido": "Erro",
                "descricao_breve": "",
                "resumo_simplificado": ["Erro na resposta da API"],
                "orgao_resumido": "",
                "data_norma": ""
            }
    except Exception as e:
        return {
            "titulo_resumido": "Erro",
            "descricao_breve": "",
            "resumo_simplificado": [f"Erro: {str(e)}"],
            "orgao_resumido": "",
            "data_norma": ""
        }
