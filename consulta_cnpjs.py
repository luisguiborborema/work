import requests
import pandas as pd
import time
import os
import re 

# Listando arquivos da pasta
# print('Arquivos na pasta atual:', os.listdir())

# Carregar a lista de CNPJs do Excel
arquivo = r"C:\Users\guibo\OneDrive\Área de Trabalho\Projeto 1\teste\teste_cnpj.xlsx"
if not os.path.exists(arquivo):
    print(f'Erro: O arquivo "{arquivo}" não foi encontrado!')
else:
    print(f'Arquivo encontrado, seguindo com a leitura...')

# Função para consultar o CNPJ antes de chamá-la
def consultar_cnpj(cnpj):
    """Consulta um CNPJ na API da ReceitaWS"""
    
    # 🔹 Remover pontos, barra e traço do CNPJ
    cnpj_limpo = re.sub(r"\D", "", cnpj)  # Remove tudo que não for número
    
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj_limpo}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Necessário para evitar bloqueios
    
    try:
        resposta = requests.get(url, headers=headers)
        
        if resposta.status_code == 429:  # API bloqueou por excesso de requisições
            print("Muitas requisições! Aguardando 10 segundos...")
            time.sleep(10)
            return consultar_cnpj(cnpj)  # Tentar novamente
        
        if resposta.status_code == 200:
            dados = resposta.json()
            return {
                "CNPJ": cnpj,
                "Razão Social": dados.get("nome", ""),
                "Situação": dados.get("situacao", ""),
                "Data Situação": dados.get("data_situacao", ""),
                "Atividade Principal": dados.get("atividade_principal", [{}])[0].get("text", ""),
                "UF": dados.get("uf", ""),
                "Município": dados.get("municipio", ""),
            }
        else:
            return {"CNPJ": cnpj, "Erro": f"Falha na consulta (Status: {resposta.status_code})"}
    
    except Exception as e:
        return {"CNPJ": cnpj, "Erro": f"Erro inesperado: {str(e)}"}

# Carrega a lista de CNPJs do Excel
df = pd.read_excel(arquivo)

# Lista para armazenar os resultados
resultados = []

# Percorrer a lista de CNPJs
for cnpj in df["CNPJ"]:
    cnpj_str = str(cnpj).zfill(14)  # Garantir 14 dígitos
    print(f"Consultando CNPJ: {cnpj_str}...")
    
    resultado = consultar_cnpj(cnpj_str)
    resultados.append(resultado)
    
    time.sleep(2)  # Pausa para evitar bloqueios

# Salvar os resultados em um novo arquivo Excel
df_resultados = pd.DataFrame(resultados)
df_resultados.to_excel("resultado_consulta_cnpjs.xlsx", index=False)

print("Consulta finalizada! Resultados salvos.")
