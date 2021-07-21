# ponto 1 

lista = [0,1,2]
lista1 = [4,5,6]
lista2 = [lista,lista1]
listaC = [9,8,8,9]
lista3=[3,5,7]

def tamanho (lista): # nao podes usar o len(lista) pq se nao nao e recursivo
    if lista==[]:
        return 0
    return 1+tamanho(lista[1:])
print(tamanho(lista))


def soma(lista):
    if tamanho(lista) == 1:
        return lista[0]
    add = lista[0]+soma(lista[1:])
    return add

print(soma(lista))

def procura(lista,elem):
    if lista==[]:
        return False
    return lista[0]==elem or procura(lista[1:],elem)

print(procura(lista,1))  # TRUE
print(procura(lista,10))  # FALSE

def concatenate(lista,lista1):# lista + lista1
    if (lista1 ==[]):
        return lista[:]  # faz a copia da lista 1 -lista1[:] 
    aux = concatenate(lista, lista1[0:len(lista1)-1])
    aux.append(lista1[len(lista1)-1]) 
    # funcao append acresenta o elemento entre() a lista aux neste caso
    return aux
    

print(concatenate(lista,lista1))

def inverter(lista): # reverse()
    if lista==[]:
        return []
    aux = inverter(lista[1:])
    aux[len(aux):] = [lista[0]]
    return aux

print(inverter(lista))

def capicua(lista):
    aux=lista[:]
    if inverter(lista) == aux:
        return True
    return False

#OU
#if(lista==[]):
#		return True
	#return lista[0] == lista[len(lista)-1] and capicua(lista[1:len(lista)-1])

print(capicua(lista)) # FALSE
print(capicua(listaC)) # TRUE

def concatenateList(lista2):
    if lista2[0]==[]:
        return lista2[1]
    return concatenate(lista2[0],lista2[1])
#OU
#if lista==[]:
#		return []
#	aux = explode(lista[:len(lista)-1])
#	aux += lista[len(lista)-1]
#	return aux
print(concatenateList(lista2))


def substituir(lista,x,y):
    if(lista==[]):
        return []
    aux = substituir(lista[:len(lista)-1],x,y)

    if(lista[len(lista)-1]==x):
        aux[len(lista)-1:]=[y]
    else:
        aux[len(lista)-1:]=[lista[len(lista)-1]]
    
    return aux

print(substituir(lista,1,8)) # 0,8,2


# ver ex 9---------- NAO ESTA BEM-----------
def uniaoOrdenada(lista1,lista3):

    if (lista3 == []):
        return lista1[:]
    
    aux = uniaoOrdenada(lista1,lista3[0:len(lista3)-1])
    aux.append(lista3[len(lista3)-1])
    if(aux[len(aux)-1]<aux[len(aux)-2]):
        Ordenar(aux)
    return aux

def Ordenar(aux):
    count = len(aux)-2
    while(aux[count] > aux[count+1]):
        temp = aux[count]
        aux[count]=aux[count+1]
        aux[count+1]=temp
        count -=1
    return aux
# OU -> este acho que da bem
#def junta_ordenado(lista1, lista2):
#	if(lista2 == []):
#		return lista1[:]
	
#	res = junta_ordenado(lista1, lista2[0:len(lista2)-1])
#	res.append(lista2[len(lista2)-1])
#	if(res[len(res)-1] < res[len(res)-2]):
#		ordenar(res)
	
#	return res

#def ordenar(lista):
#	index = len(lista)-2
#	while(lista[index] > lista[index+1]):
#		temp = lista[index]
#		lista[index] = lista[index+1]
#		lista[index+1] = temp
#		index -= 1
#	return lista

#print(uniaoOrdenada(lista1,lista3))


def subconjuntos(lista):
    if lista==[]:
        return [[]]
    aux = subconjuntos(lista[1:])

    return aux + [[lista[0]] + y for y in aux]


print(subconjuntos(lista))