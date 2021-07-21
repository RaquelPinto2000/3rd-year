#ex1
lista = [9,7,8,1,2,0,4]

def selectionSort(lista):
    lista1=lista[:]
    for i in range(len(lista1)):
        min=i
        for j in range(i+1,len(lista1)):
            if(lista1[min] >lista1[j]):
                min = j
        
        lista1[i],lista1[min] = lista1[min],lista1[i]
    return lista1
    
print(selectionSort(lista)) # [0, 1, 2, 4, 7, 8, 9]

def bubbleSort (lista):
    lista1=lista[:]
    tamanho = len(lista)
    for i in range(tamanho-1):
        for j in range(tamanho-i-1):
            if(lista1[j]>lista1[j+1]):
                lista1[j],lista1[j+1] = lista1[j+1],lista1[j]
            
    return lista1
print(bubbleSort(lista)) #[0, 1, 2, 4, 7, 8, 9]

#funcao auxiliar do quicksort
def posicao(list,low,high):
    i = (low-1)         # index of smaller element
    pivot = list[high]     # pivot
 
    for j in range(low, high):
 
        # If current element is smaller than or
        # equal to pivot
        if list[j] <= pivot:
 
            # increment index of smaller element
            i = i+1
            list[i], list[j] = list[j], list[i]
 
    list[i+1], list[high] = list[high], list[i+1]
    return (i+1)

def quickSort(lista,low,high):
    if len(lista) == 1:
        return lista
    if low < high:
 
        # pi is partitioning index, lista[p] is now
        # at right place
        pi = posicao(lista, low, high)
 
        # Separately sort elements before
        # partition and after partition
        quickSort(lista, low, pi-1)
        quickSort(lista, pi+1, high)
    return lista
lista1 = [9,7,8,1,2,0,4]
print(quickSort(lista1,0,len(lista)-1)) #[0, 1, 2, 4, 7, 8, 9]

#ex2
def OrdenarSelecao(lista):
    if(lista == []):
        return []

    (min, l) = MinList(lista)
    return [min] + OrdenarSelecao(l)

#print(OrdenarSelecao(lista)) # -> nao sei que resultado experar... O stor nao tinha teste para esta(nao sei se funciona ou nao)

#funcoes auxiliares
def verIgual(x,y):
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

