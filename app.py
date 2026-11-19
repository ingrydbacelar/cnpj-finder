import re
import time
from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__, static_folder="static", static_url_path="")

# ATENÇÃO: mova estas chaves para variáveis de ambiente / arquivo .env
# antes de compartilhar ou versionar este projeto (ex.: GitHub).
API_KEYS = [
    "AIzaSyAhxF6PUuC_Y7G04O7dXyycKp10F3DN3ZE",
    "AIzaSyAU1ETESDMXKmFpjKI-NBFBx9MmePrxxQk",
    "AIzaSyBDTHxEmm2LsBAvCGMRHbaqgpEOSNepLzM",
    "AIzaSyDHePVmaWSpixhiEdcj-C470YeAKth38dI",
    "AIzaSyAkr373yZgGOmsU6p0jGhO7z1FIiNBxELw",
    "AIzaSyCuIWnbKDAVyM4UoQKwKjf7SJk9-jBBm-U",
    "AIzaSyAB_0rkOoYL_TTle4fx8ITBct4BgPkOV1o",
    "AIzaSyDnGTTObFZWnKOEeXTmyuwADDQ1J7isa8o",
    "AIzaSyC0v6VwNK_awjfLWRfBrhgt_307-YMK35E",
    "AIzaSyAkNdzaR2Y33IdahwR2zXBGTfXGGhy5S3Q",
    "AIzaSyAnEux9X4tSNgm7MYWF6KTRcbWsrIa1JKg",
    "AIzaSyA1kMgZP4ZlZcyJjBFHYuZIPQwTjKsC6gI",
    "AIzaSyA7RvFrmXjsektOq8en5qmILRDxsA2q8BA",
]

CSE_ID = "84bc418be643b4ef2"

current_key_index = 0


def extrair_cnpj(texto_ou_url):
    """Usa regex para encontrar uma sequência de 14 dígitos no texto/URL."""
    if not texto_ou_url:
        return None
    padrao_cnpj = r"\d{14}"
    match = re.search(padrao_cnpj, texto_ou_url)
    return match.group(0) if match else None


def formatar_cnpj(cnpj_numerico):
    """Recebe um CNPJ de 14 dígitos e retorna no formato XX.XXX.XXX/XXXX-XX."""
    if not cnpj_numerico:
        return None
    return f"{cnpj_numerico[:2]}.{cnpj_numerico[2:5]}.{cnpj_numerico[5:8]}/{cnpj_numerico[8:12]}-{cnpj_numerico[12:]}"


def buscar_cnpj(nome_empresa):
    global current_key_index
    tentativas = 0

    while tentativas < len(API_KEYS):
        api_key = API_KEYS[current_key_index]
        url = (
            "https://www.googleapis.com/customsearch/v1"
            f"?q={nome_empresa}+CNPJ&key={api_key}&cx={CSE_ID}"
        )

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                dados = response.json()
                if "items" in dados:
                    return dados["items"][0]["link"], None
                return None, "Nenhum resultado encontrado."
            elif response.status_code == 429:
                current_key_index = (current_key_index + 1) % len(API_KEYS)
                tentativas += 1
                continue
            else:
                return None, f"Erro ao buscar: {response.status_code}"
        except Exception as e:
            return None, f"Erro de exceção: {e}"

    return None, "Todas as chaves atingiram o limite."


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/style.css")
def style_css():
    return send_from_directory("static", "style.css")


@app.route("/script.js")
def script_js():
    return send_from_directory("static", "script.js")


@app.route("/api/buscar", methods=["POST"])
def api_buscar():
    payload = request.get_json(silent=True) or {}
    empresas = payload.get("empresas", [])
    empresas = [e.strip() for e in empresas if e and e.strip()]

    if not empresas:
        return jsonify({"error": "Envie ao menos um nome de empresa."}), 400

    resultados = []
    for empresa in empresas:
        link, erro = buscar_cnpj(empresa)
        cnpj_numerico = extrair_cnpj(link) if link else None
        cnpj_formatado = formatar_cnpj(cnpj_numerico)

        resultados.append({
            "empresa": empresa,
            "link": link,
            "cnpj": cnpj_formatado,
            "erro": erro if not cnpj_formatado else None,
        })
        time.sleep(1)  # mesmo intervalo do script original, para não estourar limites

    return jsonify({"resultados": resultados})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
