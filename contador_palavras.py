'''
Contador de palavras: programa lê quantas vezes uma palavra aparece em um texto.
Usuário escolhe o texto, assim como escolhe a palavra a contar.
'''
from collections import Counter
import re

def contar_palavras(texto, palavra):
    """
    Conta o número de vezes que uma palavra específica aparece em um texto,
    independentemente de maiúsculas e minúsculas, considerando apenas palavras completas.
    
    Args:
        texto (str): O texto onde a contagem será feita.
        palavra (str): A palavra que será contada.
    
    Returns:
        int: Número de ocorrências da palavra no texto.
    """
    palavras = re.findall(r'\b' + re.escape(palavra) + r'\b', texto, re.IGNORECASE)
    return len(palavras)

# Exemplo
if __name__ == "__main__":
    texto = str(input('Digite um texto: '))
    palavra = str(input('Digite a palavra que quer contar: '))
    resultado = contar_palavras(texto, palavra)
    print(f'A palavra "{palavra}" aparece {resultado} vezes no texto.')
