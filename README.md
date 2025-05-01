# MVP - BackEnd Processador de DOU com LLaMA

Este projeto automatiza o download, extração, processamento e resumo de publicações do DOU (Diário Oficial da União), utilizando um modelo de linguagem local (LLaMA via Ollama). É modular e preparado para múltiplos órgãos no futuro.

---

## ✅ Funcionalidades

- Baixa arquivos `.zip` do DOU (seções DO1, DO2, DO3) do **dia atual**
- Extrai os `.xml` e processa os conteúdos
- Gera `JSON` com os metadados (órgão, data, título, conteúdo)
- Envia o conteúdo para o **modelo LLaMA local** e salva o resumo
- Se não houver publicação (ex: feriados), gera um aviso em `output/resumos/`
- Preparado para integração com **banco Oracle** (script incluso)

---

## 🛠️ Como rodar o projeto (passo a passo)

### 1. Clone o repositório ou extraia o .zip
Certifique-se de estar na raiz do projeto.

### 2. Instale o Python e as dependências
Recomendado Python 3.10+
```bash
pip install -r requirements.txt
```

### 3. Instale e rode o Ollama
Baixe em: [https://ollama.com/download](https://ollama.com/download)

Depois, execute:
```bash
ollama run llama3
```

### 4. Crie o arquivo `.env` com suas credenciais Inlabs
Na raiz do projeto, crie `.env` com:
```
INLABS_EMAIL=seu@email.com
INLABS_SENHA=sua_senha
```

### 5. Execute o script
Estando na raiz do projeto:
```bash
python -m app.main
```

---

## 📦 Saídas do sistema

- `output/materias/` → JSONs com metadados completos
- `output/resumos/` → JSONs com resumo via LLaMA
- `logs/` → Logs de sucesso e erro
- `temp/` → XMLs temporários extraídos

---

## 🧠 Integração com Oracle

O script `app/envio_oracle.py` está pronto para uso futuro.  
O esquema sugerido está em `estrutura_oracle.txt`.

Instale a lib:
```bash
pip install cx_Oracle
```

Depois edite:
```python
dsn = cx_Oracle.makedsn("host", port, sid="XE")
conn = cx_Oracle.connect("usuario", "senha", dsn)
enviar_para_banco("output/resumos/exemplo.json", conn)
```

---

## 🧩 Como adicionar novos órgãos

Crie novos módulos:
- `downloader_anvisa.py`
- `extractor_anvisa.py`
- `processor_anvisa.py`

Depois importe e chame dentro do `main.py`.

---

## 🧪 Teste rápido

Se não houver publicação no dia:
```json
{
  "data": "2025-05-01",
  "mensagem": "Nenhuma publicação do DOU foi encontrada nesta data. Feriado ou indisponibilidade."
}
```

---

## 👨‍💻 Autor
Pedro Merisi | MVP FIAP + LLaMA + Oracle + Python