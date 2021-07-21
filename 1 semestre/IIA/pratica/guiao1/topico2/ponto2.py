# ponto 2
lista = [[0,1],[4,5],[7,8]]
lista1 = [1,6,2,5,5,2,5,2]
lista2 = [1,2,3,1,2,3,1,2,3,9,10,9,4,4,5,5,5,5,5]
# ex1
def separar(lista):
    if lista==[]:
        return ([],[])
    res = separar(lista[0:len(lista)-1])
    res[0].append(lista[len(lista)-1][0])
    res[1].append(lista[len(lista)-1][1])
    
    return res

print(separar(lista))

#ex2
def remove_e_conta(lista,elem):
    if(lista == []):
        return ([],0)

    res = remove_e_conta(lista[0:len(lista)-1],elem)
    if(lista[len(lista)-1] == elem):
      aux = list(res)
      aux[1] +=1
      res = tuple(aux)
    else: # vai acrescentar o elemento
      res[0].append(lista[len(lista)-1]) 
      
    return res


elem = 2
print(remove_e_conta(lista1,elem))

#ex3
def contaElem(lista):
  if(lista==[]):
    return []
  res = contaElem(lista[0:len(lista)-1])

  if(len(res)==0):
      res.append((lista[0],1))
  else:
    elem = lista[len(lista)-1]
    tam = len(res)
    b = False
    for i in range(0,tam):
        if(res[i][0] == elem):
            aux = list(res[i])
            aux[1] +=1
            res[i]=tuple(aux)
            b = True
    if(b==False):
        res.append((elem,1))
  return res
  
print(contaElem(lista2))