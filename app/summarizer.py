import requests

LLAMA_API_URL = "http://localhost:11434/api/generate"

def resumir_texto(texto):
    prompt = (
        "Você é um assistente especializado em regulamentos governamentais e legislação brasileira.\n"
        "Leia atentamente o texto a seguir e produza duas coisas:\n\n"
        "1. Um TÍTULO objetivo e informativo com no máximo 12 palavras, usando português claro e seguindo boas práticas de formatação. Evite siglas não explicadas e termos técnicos desnecessários.\n"
        "2. Um RESUMO com até 4 parágrafos curtos, em português simples, explicando:\n"
        "- Qual é a principal mudança ou novidade?\n"
        "- Quem é impactado por essa mudança?\n"
        "- O que muda na prática para empresas ou gestores?\n"
        "- Quando isso passa a valer?\n\n"
        "Evite frases como 'aqui está o resumo' e não repita o conteúdo sem explicá-lo. Escreva de forma didática, como se estivesse explicando para uma pequena empresa.\n\n"
        "Formato da resposta:\n"
        "TÍTULO: <título claro e informativo>\nRESUMO: <resumo bem estruturado>\n\n"
        f"TEXTO:\n{texto}"
    )
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(LLAMA_API_URL, json=payload, timeout=60)
        if response.ok:
            resultado = response.json().get("response", "")
            if "TÍTULO:" in resultado and "RESUMO:" in resultado:
                partes = resultado.split("RESUMO:")
                titulo = partes[0].replace("TÍTULO:", "").strip()
                resumo = partes[1].strip()
                return {"titulo_resumido": titulo, "resumo": resumo}
            else:
                return {"titulo_resumido": "Título não gerado", "resumo": resultado.strip()}
        else:
            return {"titulo_resumido": "Erro", "resumo": "[Erro ao obter resumo: resposta inválida da API]"}
    except Exception as e:
        return {"titulo_resumido": "Erro", "resumo": f"[Erro ao obter resumo: {str(e)}]"}