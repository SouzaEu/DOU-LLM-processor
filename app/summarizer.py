import requests

LLAMA_API_URL = "http://localhost:11434/api/generate"

def resumir_texto(texto):
    prompt = (
        "Leia o texto a seguir e gere:\n"
        "- Um TÍTULO mais curto e legível (sem abreviações e com boas práticas de formatação)\n"
        "- Um RESUMO claro, objetivo, em português simples e técnico, sem usar frases como 'aqui está o resumo'.\n\n"
        "Formato da resposta:\n"
        "TÍTULO: <título resumido>\nRESUMO: <resumo objetivo>\n\n"
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