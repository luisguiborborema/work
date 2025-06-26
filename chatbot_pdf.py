Python
import google.generativeai as genai
import pdfplumber
import os
'''
Configuração de Agente:
Definição de personalidade do agente(Prompt padrão);
Definição de base de dados que o agente irá consultar(PDF);
## Lembre-se de colocar os arquivos de PDF na mesma pasta do código, se não ele não conseguirá encontrar o arquivo para leitura.
'''
# 1. Configure a sua Chave de API
genai.configure(api_key="chave_API_Gemini")

# Função para ler os PDFs
def extrair_texto_de_pdf(caminho_do_pdf):
    if not os.path.exists(caminho_do_pdf):
        print(f"AVISO: O ficheiro PDF não foi encontrado em: {caminho_do_pdf}. A ignorá-lo.")
        return None
    texto_completo = ""
    try:
        with pdfplumber.open(caminho_do_pdf) as pdf:
            for pagina in pdf.pages:
                texto_da_pagina = pagina.extract_text()
                if texto_da_pagina:
                    texto_completo += texto_da_pagina + "\n"
        return texto_completo
    except Exception as e:
        print(f"Ocorreu um erro ao ler o PDF {os.path.basename(caminho_do_pdf)}: {e}")
        return None

# --- CONFIGURAÇÃO DO CHATBOT ---

# 2. Personalidade do Agente
personalidade_bruna = """
Você é especialista em marketing da Viofilmes(agência de marketing). 
O seu nome é Bruna. Você é carismática, educada, profissional, casual, 
atenciosa, empática, curiosa. Responda a todas as perguntas de forma amigável, 
profissional e em português do Brasil. Você não deve inventar informações sobre 
produtos/serviços. Se não souber a resposta, diga: "Não tenho essa informação no 
momento, mas posso verificar para você." Não responda qualquer pergunta(de forma educada e simpática) que não seja relacionado a empresa, serviços/preços e redirecione a conversa para esse assunto.
"""

# 3. Carregue os PDFs - Biblioteca de conhecimento do agente
# !!! IMPORTANTE: Coloque os nomes de todos os seus ficheiros PDF nesta lista.
LISTA_DE_PDFS = [
    "entregaveis.pdf",
    "Estrutura_Viofilme.pdf",
    "tabela_de_precos.pdf"
]

print("A carregar conhecimento dos documentos PDF...")
contexto_completo = ""
diretorio_do_script = os.path.dirname(os.path.abspath(__file__))

# Loop que passa por cada nome de ficheiro na lista
for nome_pdf in LISTA_DE_PDFS:
    caminho_completo_pdf = os.path.join(diretorio_do_script, nome_pdf)
    texto_extraido = extrair_texto_de_pdf(caminho_completo_pdf)
    
    # Se o texto foi extraído com sucesso, junta ao nosso contexto geral
    if texto_extraido:
        # Adicionamos separadores para ajudar a IA a distinguir os documentos
        contexto_completo += f"--- INÍCIO DO DOCUMENTO: {nome_pdf} ---\n"
        contexto_completo += texto_extraido
        contexto_completo += f"--- FIM DO DOCUMENTO: {nome_pdf} ---\n\n"

if not contexto_completo:
    print("ERRO: Nenhum texto foi extraído dos PDFs. A encerrar.")
    exit()

print("Conhecimento carregado com sucesso!")

# 4. Crie a Instrução Inicial Completa
instrucao_inicial = f"""
{personalidade_bruna}

A seguir, está a documentação completa dos serviços da empresa para sua referência e consulta, extraída de vários ficheiros. 
Use este conhecimento para tirar todas as dúvidas dos clientes.

{contexto_completo}

Agora, com base em todo este conhecimento, responda às perguntas dos clientes.
"""

# 5. Inicia o modelo
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
chat = model.start_chat(history=[
    {"role": "user", "parts": [instrucao_inicial]},
    {"role": "model", "parts": ["Entendido. Eu sou a Bruna e estudei todo o material sobre os serviços da Vctimes. Estou pronta para ajudar os clientes. Como posso ser útil hoje?"]}
])

# --- LOOP DE CONVERSA ---
# ... (O loop de conversa permanece até o user pedir a saída ...
print("--- Conversa com a Bruna (Especialista de Serviços) ---")
print("Bruna: Olá! Eu sou a Bruna. Tenho acesso a todos os nossos serviços. Em que posso ajudar?")
print("Digite 'fim' ou 'sair' para terminar.")
print("-" * 60)

while True:
    try:
        user_input = input("Você: ")
        if user_input.lower() in ["fim", "sair"]:
            print("\nBruna: Foi um prazer! Se precisar de mais alguma informação, estarei por aqui.")
            break
        response = chat.send_message(user_input)
        print(f"\nBruna: {response.text}\n")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        break
