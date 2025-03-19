from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
from time import sleep

# Iniciar o navegador
driver = webdriver.Chrome()
driver.get('https://pepesburger.com.br/delivery/pepesburger.com.br/tabs/home')

# Aguarde um tempo extra para garantir que a página carregue totalmente
sleep(5)  # Tempo extra para carregar JavaScript

wait = WebDriverWait(driver, 20)  # Aumentado para evitar TimeoutException

# Rolar a página para garantir que todos os elementos carreguem
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(3)  # Pequena espera para garantir que os preços carreguem

# Verificar manualmente se os elementos existem antes de continuar
try:
    produtos = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//p[@class='store-item-name']")))
    print(f"✅ {len(produtos)} produtos encontrados.")
except:
    print("⚠️ Nenhum produto encontrado. Verifique se a XPath está correta.")
    produtos = []

try:
    precos = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//p[contains(@class, 'store-item-price')]/span")))
    print(f"✅ {len(precos)} preços encontrados.")
except:
    print("⚠️ Nenhum preço encontrado. Verifique se a XPath está correta.")
    precos = []

# Criar lista final para armazenar os dados
produtos_precos = []

# Se não houver produtos ou preços, interrompe a execução
if not produtos or not precos:
    print("❌ Não foi possível coletar dados. Encerrando...")
    driver.quit()
    exit()

# Garantir que temos produtos e preços correspondentes
for i in range(min(len(produtos), len(precos))):  # Evita erro caso haja mais preços que produtos
    nome_produto = driver.execute_script("return arguments[0].textContent;", produtos[i]).strip()
    preco_produto = driver.execute_script("return arguments[0].textContent;", precos[i]).strip()

    if not nome_produto:
        nome_produto = "Produto não encontrado"
    if not preco_produto:
        preco_produto = "Preço não encontrado"

    produtos_precos.append((nome_produto, preco_produto))
    print(f"Produto: {nome_produto}, Preço: {preco_produto}")  # Debug

# Definir o caminho absoluto do arquivo CSV
caminho_csv = os.path.join(os.getcwd(), "preços.csv")

# Criar arquivo CSV e armazenar os dados
with open(caminho_csv, 'w', encoding='utf-8', newline='') as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(["Produto", "Preço"])  # Cabeçalho
    escritor.writerows(produtos_precos)

print(f"✅ Dados salvos em '{caminho_csv}' com sucesso.")

# Fechar o navegador
driver.quit()

