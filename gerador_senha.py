import random 
import string
print('Gerador de Senhas')
print('-'*30)

# Caracteres permitidos: números, letras maiusculas e minusculas, caracteres especiais
caracteres = string.ascii_letters + string.digits + string.punctuation

# Gera uma senha com 8 digitos
senha = ''.join(random.choices(caracteres, k=8))

print(f'Senha gerada: {senha}')
print('-'*30)
