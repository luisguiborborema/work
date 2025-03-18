import requests # type: ignore
import pandas as pd
import time
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

# Carregar a lista de CNPJs
arquivo = "lista_cnpj.xlsx" # Nome do arquivo
df = pd.read_excel(arquivo) # Supondo que a coluna se chama 'CNPJ'

# Função para validar CNPJ (verifica se tem 14 dígitos)
def validar_cnpj(cnpj):
    cnpj = "".join(filter(str.isdigit, str(cnpj))) # Remove caracteres não numéricos
    return cnpj if len(cnpj) == 14 else None

# Função para consultar CNPJ na API escolhida (ReceitaWS)
def consultar_cnpj(cnpj):
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    headers = {"User-Agent": "Mozilla/5.0"} # Evita bloqueios na API

    try:
        resposta = requests.get(url, headers = headers)

        # Se a API bloqueou por excesso de requisições, aguarde e tente novamente
        if resposta.status_code == 429: # Erro de excesso de requisições
            print(f"Limite de requisições atingido! Aguardando 10 segundos antes de continuar...")
            time.sleep(10)
            return consultar_cnpj(cnpj) # Tentar novamente
        
        if resposta.status_code == 200:
            dados = resposta.json()
            return {
                "CNPJ": cnpj,
                "Razão Social": dados.get("nome", ""),
                "Situação": dados.get("situacao", ""),
                "Data Situação": dados.get("data_situacao", ""),
                "Atividade Principal": dados.get("atividade_principal", [{}])[0].get("text", ""),
                "UF": dados.get("uf", ""),
                "Munícipio": dados.get("municipio", ""),
            }
        else:
            return {"CNPJ": cnpj, "Erro": f"Falha na consulta (Status: {resposta.status_code})"}
        
    except Exception as e:
        return {"CNPJ": cnpj, "Erro": f"Erro inesperado: {str(e)}"}
    
# Criar uma lista para armazenar os resultados
resultados = []

# Iniciar contagem de tempo
tempo_inicio = time.time()

# Consultar todos os CNPJs
total = len(df)
for i, cnpj in enumerate(df["CNPJ"]):
    cnpj_validado = validar_cnpj(cnpj)

    if not cnpj_validado:
        print(f"Pulando CNPJ inválido: {cnpj}")
        resultados.append({"CNPJ": cnpj, "Erro": "CNPJ inválido"})
        continue
    
    print(f"Consultando {i+1}/{total}: {cnpj_validado}")
    resultado = consultar_cnpj(cnpj_validado)
    resultados.append(resultado)

    time.sleep(3) # Pequena pausa para evitar bloqueios

# Finalizar contagem de tempo
tempo_fim = time.time()
tempo_decorrido = tempo_fim - tempo_inicio

# Converter tempo decorrido para horas, minutos e segundos
horas = int(tempo_decorrido // 3600)
minutos = int((tempo_decorrido % 3600) // 60)
segundos = int(tempo_decorrido % 60)

# Criar um DataFrame com os resultados e salvar em Excel e gerar uma nova planilha
df_resultados = pd.DataFrame(resultados)
df_resultados.to_excel("resultado_consulta_cnpjs.xlsx", index = False)

print("Consulta finalizada! Resultados salvos na pasta com nome 'resultado_consulta_cnpjs.xlsx'")
print(f"Tempo total de execução: {horas}h {minutos}m {segundos}s")
