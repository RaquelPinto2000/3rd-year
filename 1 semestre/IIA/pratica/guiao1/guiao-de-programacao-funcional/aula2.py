import math 

#Exercicio 4.1
impar = lambda x : x%2!=0

#Exercicio 4.2
positivo = lambda x : x>0

#Exercicio 4.3
comparar_modulo = lambda x,y : abs(x)<abs(y)

#Exercicio 4.4
cart2pol = lambda x, y : (math.sqrt((pow(x, 2)+pow(y, 2))), math.atan2(y, x))

#Exercicio 4.5
ex5 = lambda f,g,h : lambda x,y,z : h(f(x,y),g(y,z))

#Exercicio 4.6
def quantificador_universal(lista, f):
    if(lista==[]):
        return True
    if f(lista[0]):
        return quantificador_universal(lista[1:],f)
    return False

#Exercicio 4.9
    
def ordem(lista, f):
    if(lista == []):
        return None
    
    min = ordem(lista[0:len(lista)-1], f)

    if(min == None):
        min = lista[0]
    elif(f(min, lista[len(lista)-1]) == False):
        min = lista[len(lista)-1]
    return min

#Exercicio 4.10
def filtrar_ordem(lista, f):
    if(lista == []):
        return None
    
    min = ordem(lista[0:len(lista)-1], f)

    if(min == None):
        min = lista[0]
    elif(f(min, lista[len(lista)-1]) == False):
        min = lista[len(lista)-1]
    
    lista1=lista[:]
    while(min in lista1):
        lista1.remove(min)
    return (min,lista1)

#Exercicio 5.2
def ordenar_seleccao(lista, ordem):
    if(lista == []):
        return []

    (min, l) = filtrar_ordem(lista,ordem)
    return [min] + ordenar_seleccao(l, ordem)
