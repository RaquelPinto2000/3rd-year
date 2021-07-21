import math

# ex1
impar = lambda x : x%2!=0
print(impar(5)) # true
print(impar(6)) # false

#ex2
positivo = lambda x : x>0 # se x>0 (positivo) retorna true
print(positivo(5)) # true
print(positivo(-9)) # False

# ex3
compNum = lambda x,y : abs(x)<abs(y)

print (compNum(7,8))  # True
print (compNum(7,-8)) # True
print (compNum(9,6))  # False
print (compNum(-9,-6)) #False

#ex4
#coordpol = lambda cart : (sqrt(cart[0]**2+cart[1]**2),atan2(cart[1],cart[0]))
#ou
cart2pol = lambda x, y : (math.sqrt((pow(x, 2)+pow(y, 2))), math.atan2(y, x))
#funcao atan2 e a funcao arco tangente
print (cart2pol(1, 1)) # (1.4142135623730951, 0.7853981633974483)

#ex5
def myfunc(f,g,h):
    return lambda x,y,z : h(f(x,y),g(y,z))
#ou
# myfunc = lambda f,g,h : lambda x,y,z : h(f(x,y),g(y,z))

s= lambda x,y : x+y
m= lambda x,y : x*y
b= lambda x,y: x-y

funcao = myfunc(s,m,b)
print(funcao(4,3,-5)) # 22

# ex6 -> ver se esta bem e fazer com expressao lambda

def verUniversal (x): #funcao auxiliar (f do enunciado)
    if(2*x == x+x):
        return True
    return False

def Universal(lista):
    i=0
    while i!=len(lista):
        ver = verUniversal(lista[i])
        i+=1
        if(ver==False):
            return False
    return True


# ex 6 como diz no enunciado
#def Universal(lista,f):
#    if(lista==[])
#        return True
#    if f(lista[0]):
#        return Universal(lista[1:],f)
#    return False

lista = [1,2,3]
print(Universal(lista)) # true


#ex 7 ->  ver se esta bem e fazer com expressao lambda
def Existencial(ista):
    i=0
    while i!=len(lista):
        ver = verUniversal(lista[i])
        i+=1
        if(ver):
            return True
    return False
    
lista1 = [4,5,6]
print(Existencial(lista1)) # true

# ex 7 como diz no enunciado
#def Existencial(lista,f):
#    if(lista==[])
#        return False
#    if f(lista[0]):
#        return True
#    return Existencial(lista[1:],f)


#ex8
def procura(lista,elem): #funcao auxiliar
    if lista==[]:
        return False
    return lista[0]==elem or procura(lista[1:],elem)
    
def Ocorrer(lista,lista2):
    if(lista==[] or lista2==[]):
        return False
    for i in range(len(lista)):
        ver = procura(lista2,lista[i])
        if(ver==False):
            return False
    return True

lista2 = [1,8,6,5,4,7,5]
lista3 = [8,6,5]
print(Ocorrer(lista3,lista2)) #True
print(Ocorrer(lista2,lista3)) #False

# ex9
def verIgual(x,y): # funcao de relacao de ordem (a minha -> a do stor deve de ser diferente)
    if(x==y):
        return True
    return False

def ordem(lista):
    if(lista==[]):
        return None
    min = ordem(lista[0:len(lista)-1])
    if(min == None):
        min=lista[0]
    elif(verIgual(min,lista[len(lista)-1]) == False):
        min = lista[len(lista)-1]
    return min
print(ordem(lista)) # -> nao sei que resultado experar... NO TESTE DO STOR PASSOU

# ex10
def MinList(lista):
    if(lista==[]):
        return None
    min = ordem(lista[0:len(lista)-1])
    if(min == None):
        min=lista[0]
    elif(verIgual(min,lista[len(lista)-1]) == False):
        min = lista[len(lista)-1]
    
    lista1=lista[:]
    while(min in lista1):
        lista1.remove(min)
    return (min,lista1)
print(MinList(lista)) # -> nao sei que resultado experar... NO TESTE DO STOR PASSOU

#ex11
def Triplo(lista):
    if(len(lista)<2):
        return None

    if(lista==[]):
        return None
    min = ordem(lista[0:len(lista)-1])
    if(min == None):
        min=lista[0]
    elif(verIgual(min,lista[len(lista)-1]) == False):
        min = lista[len(lista)-1]
    lista1=lista[:]
    while(min in lista1):
        lista1.remove(min)

    if(lista1==[]):
        return None
    min1 = ordem(lista1[0:len(lista1)-1])
    if(min1 == None):
        min1=lista1[0]
    elif(verIgual(min1,lista1[len(lista1)-1]) == False):
        min1 = lista1[len(lista1)-1]
    
    lista2=lista1[:]
    while(min1 in lista2):
        lista2.remove(min1)
    return (min,min1,lista2)
    
print(Triplo(lista))  # -> nao sei que resultado experar... O stor nao tinha teste para esta(nao sei se funciona ou nao)

#ex12 -> nao sei esta (gameiro tbm fez assim)
def coordpolList(lista):
    if(lista==[]):
        return []

    result = coordpolList(lista[0:len(lista)-1])
    result.append(cart2pol(lista[len(lista)-1][0], lista[len(lista)-1][1]))
    return result

lista4=[1,2,3,4]
#print(coordpolList(lista4))

#ex13 ->nao sei testar esta funcao
def UniaoOrdenada(lista,lista1,f):
    if (lista1 == []):
        return lista[:]
    aux = UniaoOrdenada(lista,lista1[0:len(lista1)-1],f)
    aux.append(lista1[len(lista1)-1])
    f(aux)
    return aux
# ex14 -> nao sei testar esta funcao
def concatenar (lista,f): 
    aux =lista[0]
    aux1 = lista[1]
    res=[]
    for i in range(len(lista[0])):
        res[i] = f(aux[i])
        res.append(f(aux1[i]))
    return res
        
#ex15 -> nao sei testar

def Homologos(lista,f):
    if(len(lista[0]) != len(lista[1])):
        return None
    aux =lista[0]
    aux1 = lista[1]
    for i in range(len(lista[0])):
        return (f(aux[i]),f(aux1[i]))

#ex16 -> nao percebi bem o enunciado e nao sei testar
def reducao(lista,f,elemNeutro):
    aux =lista[0]
    res=[]
    for i in range(len(lista[0])):
        res = f(aux[i])
    return res