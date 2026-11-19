import requests
import time
import re 

API_KEYS = [
   
]

CSE_ID = "84bc418be643b4ef2"

current_key_index = 0

def extrair_cnpj(texto_ou_url):
    """
    Usa regex para encontrar uma sequência de 14 dígitos no texto/URL.
    """
    padrao_cnpj = r"\d{14}"
    
    match = re.search(padrao_cnpj, texto_ou_url)
    
    if match:
        return match.group(0) 
    else:
        return None 

def formatar_cnpj(cnpj_numerico):
    """
    Recebe um CNPJ de 14 dígitos e retorna no formato XX.XXX.XXX/XXXX-XX.
    """
    if not cnpj_numerico:
        return "CNPJ não encontrado."
        
    return f"{cnpj_numerico[:2]}.{cnpj_numerico[2:5]}.{cnpj_numerico[5:8]}/{cnpj_numerico[8:12]}-{cnpj_numerico[12:]}"

def buscar_cnpj(nome_empresa):
    global current_key_index
    tentativas = 0
    
    while tentativas < len(API_KEYS):  
        api_key = API_KEYS[current_key_index]
        url = f"https://www.googleapis.com/customsearch/v1?q={nome_empresa}+CNPJ&key={api_key}&cx={CSE_ID}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                dados = response.json()
                if "items" in dados:
                    return dados["items"][0]["link"]
                else:
                    return "Nenhum resultado encontrado."
            elif response.status_code == 429:  
                print(f"⚠️ Limite atingido para a chave {api_key}, trocando para a próxima...")
                current_key_index = (current_key_index + 1) % len(API_KEYS)
                tentativas += 1
                continue
            else:
                return f"Erro ao buscar: {response.status_code}"
        except Exception as e:
            return f"Erro de exceção: {e}"
    
    return "❌ Todas as chaves atingiram o limite."

empresas = [
    
]

print("--- Extraindo e Formatando CNPJs ---")
for empresa in empresas:
    link_resultado = buscar_cnpj(empresa)
    
    cnpj_numerico = extrair_cnpj(link_resultado)
    
    cnpj_formatado = formatar_cnpj(cnpj_numerico)
    
    print(f"{empresa}: {cnpj_formatado}")
    time.sleep(1)
