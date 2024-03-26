def juros_simples(c, i, t):
    j = c * (i/12) * t
    return j

def juros_composto(c, i, t):
    m = c * (1+i) ** t
    j = m - c
    return j
    
    

c = float(input('Digite o valor do capital inicial: '))
i = float(input('Digite o valor da taxa aplicada: '))
t = float(input('Digite quantos meses seu dinheiro ficará aplicado: '))

print(juros_composto(c, i, t))