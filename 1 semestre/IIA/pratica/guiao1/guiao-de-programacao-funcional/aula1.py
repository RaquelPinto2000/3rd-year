#Exercicio 1.1
def comprimento(lista):
	if(lista == []):
		return 0
	return 1 + comprimento(lista[1:])

#Exercicio 1.2
def soma(lista):
	if(lista == []):
		return 0
	return lista[0] + soma(lista[1:])

#Exercicio 1.3
def existe(lista, elem):
	if lista==[]:
		return False
	return lista[0]==elem or existe(lista[1:],elem)

#Exercicio 1.4
def concat(l1, l2):
	if(l2 == []):
		return l1[:]
	aux = concat(l1, l2[0:len(l2)-1])
	aux.append(l2[len(l2)-1])
	return aux

#Exercicio 1.5
def inverte(lista):
	if lista==[]:
		return []
	aux = inverte(lista[1:])
	aux[len(aux):] = [lista[0]]
	return aux

#Exercicio 1.6
def capicua(lista):
	if(lista==[]):
		return True
	return lista[0] == lista[len(lista)-1] and capicua(lista[1:len(lista)-1])

#Exercicio 1.7
def explode(lista):
	if lista==[]:
		return []
	aux = explode(lista[:len(lista)-1])
	aux += lista[len(lista)-1]
	return aux

#Exercicio 1.8
def substitui(lista, original, novo):
	if(lista==[]):
		 return []
	aux = substitui(lista[:len(lista)-1],original,novo)
	
	if(lista[len(lista)-1]==original):
		aux[len(lista)-1:]=[novo]
	else:
		aux[len(lista)-1:]=[lista[len(lista)-1]]
	
	return aux

#Exercicio 1.9
def junta_ordenado(lista1, lista2):
	if(lista2 == []):
		return lista1[:]
	
	res = junta_ordenado(lista1, lista2[0:len(lista2)-1])
	res.append(lista2[len(lista2)-1])
	if(res[len(res)-1] < res[len(res)-2]):
		ordenar(res)
	
	return res

def ordenar(lista):
	index = len(lista)-2
	while(lista[index] > lista[index+1]):
		temp = lista[index]
		lista[index] = lista[index+1]
		lista[index+1] = temp
		index -= 1
	return lista

#Exercicio 2.1
def separar(lista):
	if lista==[]:
		return ([],[])
	res = separar(lista[0:len(lista)-1])
	res[0].append(lista[len(lista)-1][0])
	res[1].append(lista[len(lista)-1][1])
    
	return res

#Exercicio 2.2
def remove_e_conta(lista, elem):
	if(lista == []):
		return ([],0)

	res = remove_e_conta(lista[0:len(lista)-1],elem)
	if(lista[len(lista)-1] == elem):
		aux = list(res)
		aux[1] +=1
		res = tuple(aux)
	else:
		res[0].append(lista[len(lista)-1]) 
      
	return res

#Exercicio 3.1
def cabeca(lista):
	if lista==[]:
		return None
	return lista[0]

#Exercicio 3.2
def cauda(lista):
	if lista==[]:
		return None 
	return lista[1:]

#Exercicio 3.3
def juntar(l1, l2):
	if(len(l1)!=len(l2)):
		return None
	elif(l1 == [] and l2 == []):
		return []
	result = juntar(l1[0:len(l1)-1], l2[0:len(l2)-1])
	result.append((l1[len(l1)-1], l2[len(l2)-1]))
	return result

#Exercicio 3.4
def menor(lista):
	if len(lista)==0 or lista==[]:
		return None
	min = menor(lista[0:len(lista)-1])
	if(min == None):
		min = lista[0]
	if(min > lista[len(lista)-1]):
		min = lista[len(lista)-1]
	return min

#Exercicio 3.6
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
