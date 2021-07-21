# ponto 3

lista = [1,2,3,4,5,6,7,8,9]
lista1 = [7,8,9]
listaMediana = [4,5,6,7,9,10]
lista2 = []
lista3 = [10,5,8,4,9,3,8,2,5]

# ex1
def returnCabeca(lista):
    if lista==[]:
        return None
    return lista[0]

print(returnCabeca(lista)) #1
print(returnCabeca(lista1)) #7
print(returnCabeca(lista2)) # None

#ex2
def returnCauda(lista):
    if lista==[]:
        return None 
    return lista[1:]

print(returnCauda(lista)) #[2,3,4,5,6,7,8,9]
print(returnCauda(lista1)) #[8,9]
print(returnCauda(lista2)) # None

#ex3
def homologos(l1,l2):
    if(len(l1)!=len(l2)):
        return None
    elif(l1 == [] and l2 == []):
        return []
    result = homologos(l1[0:len(l1)-1], l2[0:len(l2)-1])
    result.append((l1[len(l1)-1], l2[len(l2)-1]))
    return result

print(homologos(lista,lista3)) 
#[(1, 10), (2, 5), (3, 8), (4, 4), (5, 9), (6, 3), (7, 8), (8, 2), (9, 5)]

#ex4
def minimo (lista):
    if len(lista)==0:
        return None
    if len(lista)==1:
        return lista[0]
    min = minimo(lista[1:])

    if lista[0]<min:
        min = lista[0]

    return min
# OU
#if len(lista)==0 or lista==[]:
#		return None
#	min = menor(lista[0:len(lista)-1])
#	if(min == None):
#		min = lista[0]
#	if(min > lista[len(lista)-1]):
#		min = lista[len(lista)-1]
#	return min

print(minimo(lista)) # 1
print(minimo(lista1)) # 7
print(minimo(lista2)) # None
print(minimo(lista3)) # 2

#ex5
def minElem(lista):
    if len(lista)==0:
        return None
    if len(lista)==1:
        return lista[0]
    min = minimo(lista[1:])
    lista1=lista[:]
    if lista[0]<min:
        min = lista[0]
    while(min in lista1):
        lista1.remove(min)
    
    return (min,lista1)

print(minElem(lista)) # (1,[2,3,4,5,6,7,8,9])
print(minElem(lista1)) # (7,[8,9])
print(minElem(lista2)) # None
print(minElem(lista3)) # (2,[10,5,8,4,9,3,8,5])



#ex 6
def max_min(lista):

    if len(lista)==0:
        return None

    if(len(lista))==1:
        return (lista[0],lista[0])

    min,max = max_min(lista[1:])
    
    if lista[0]<min:
        min = lista[0]
    if lista[0]>max:
        max = lista[0]

    return (min,max)
    
print(max_min(lista)) # (1,9)
print(max_min(lista1)) # (7,9)
print(max_min(lista2)) # None
print(max_min(lista3)) # (2,10)

#ex 7-------
def TwoMinElem(lista):
    if len(lista)==0:
        return None
    if len(lista)==1:
        return lista[0]
    min = minimo(lista[1:])
    lista1=lista[:]
    if lista[0]<min:
        min = lista[0]
    while(min in lista1):
        lista1.remove(min)
    
    if len(lista1)==0:
        return None
    if len(lista1)==1:
        return lista1[0]
    min1 = minimo(lista1[1:])
    lista2=lista1[:]
    if lista1[0]<min1:
        min1 = lista1[0]
    while(min1 in lista2):
        lista2.remove(min1)

    return (min,min1,lista2)

print(TwoMinElem(lista)) # (1,2,[3,4,5,6,7,8,9])
print(TwoMinElem(lista1)) # (7,8,[9])
print(TwoMinElem(lista2)) # None
print(TwoMinElem(lista3)) # (2,3,[10,5,8,4,9,8,5])


def soma(lista):
    if len(lista) == 1:
        return lista[0]
    add = lista[0]+soma(lista[1:])
    return add

# ex 8 
def Med (lista):
    if lista==[]:
        return None

    add = lista[0]+soma(lista[1:])
    media = add/len(lista)
    if impar(len(lista)) == True:
        mediana = lista[len(lista)//2]
        
    else:
        mediana = (lista[(len(lista)//2)-1] + lista[(len(lista)//2)])/2
    
    return (media,mediana)

def impar(i):
    if i %2 ==0:
        return False
    else:
        return True


print(Med(lista)) # (5.0,5)
print(Med(lista1)) # (8.0,8)
print(Med(lista2)) # None
print(Med(listaMediana)) # (6.8(3),6.5)

def ordenado (lista):
    for x in len(lista):
        if(lista[x+1]<lista[x]):
            return False
    return True

#print( ordenado(lista))