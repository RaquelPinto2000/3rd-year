

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)

#exercicio 15
# Subclasse AssocOne
class AssocOne(Relation):
    def __init__(self,e1,assoc,e2=None):
        Relation.__init__(self,e1,assoc,e2)

#exercicio 15
# Subclasse AssocNum
class AssocNum(Relation):
    def __init__(self,e1,assoc,e2):
        #if(type(e1) == int or type(e2)==int):
        Relation.__init__(self,e1,assoc,e2)
        #Relation.__init__(self,None,assoc,None)

# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    def __str__(self):
        return my_list2string(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)

#A função query local permite obter informação local (ou seja, propriedades não herdadas)
#sobre as várias entidades presentes na rede. Esta função pode receber como parâmetros o utiliza-
#dor (user), o nome da primeira entidade envolvida na relação (e1), o nome da relação (rel) e o
#nome da segunda entidade envolvida na relação (e2). A função vai devolver todas as declarações
#que satisfazem os parâmetros especificados, podendo alguns deles ser omitidos.
# esta nao faz heranca do conhecimento
    def query_local(self,user=None,e1=None,rel=None,e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

#isinstance(object, classinfo)
#Devolve True se o argumento object é uma instância do argumento classinfo, 
#ou de uma subclasse dele (direta, indireta ou virtual). Se object não é um 
#objeto do tipo dado, a função sempre devolve False. Se classinfo é uma tupla 
#de tipos de objetos (ou recursivamente, como outras tuplas), devolve True se
#object é uma instância de qualquer um dos tipos. Se classinfo não é um tipo
#ou tupla de tipos ou outras tuplas, é lançada uma exceção TypeError.
    
    #exercicio 1
    def list_associations(self):
        result = [ d.relation.name for d in self.declarations if isinstance(d.relation,Association)]
        return list(set(result))

    #exercicio 2
    def list_objects(self):
        result = [d.relation.entity1 for d in self.declarations if isinstance(d.relation,Member)]
        return list(set(result))

    #exercicio 3
    def list_users(self):
        result = [d.user for d in self.query_local()]
        return list(set(result))
    
    #exercicio 4 
    def list_types(self):
        result = [d.relation.entity1 for d in self.declarations if isinstance(d.relation, Subtype)]
        result += [d.relation.entity2 for d in self.declarations if isinstance(d.relation, Subtype) or isinstance(d.relation, Member)]
        return list(set(result))

    #exercicio 5
    def list_local_associations(self,entityGiven):
        result = [d.relation.name for d in self.declarations if d.relation.entity1==entityGiven and isinstance(d.relation, Association)]
        return list(set(result))

    #exercicio 6
    def list_relations_by_user(self, userGiven):
        result = [d.relation.name for d in self.declarations if d.user==userGiven]
        return list(set(result))
    
    #exercicio 7
    def associations_by_user(self, userGiven):
        #podemos usar not isinstance(d.relation, Member) and not isinstance(d.relation, Subtype) para deixarmos declaracoes de lado = isinstance(d.relation,Association)
        result = [d.relation.name for d in self.declarations if d.user==userGiven and isinstance(d.relation,Association)]
        return len(list(set(result))) # set e para nao haver repetidos

    #exercicio 8
    def list_local_associations_by_user(self,entityGiven):
        result = [ (d.relation.name, d.user)for d in self.declarations if d.relation.entity1==entityGiven and isinstance(d.relation,Association)]
        return list(set(result))

    #exercicio 9
    def predecessor(self,entityGiven1,entityGiven2):
        parent = list(set([d.relation.entity2 for d in self.declarations if not isinstance(d.relation, Association) and d.relation.entity1 == entityGiven2]))
        if parent == None:
            return False
        if entityGiven1 in parent: # se forem iguais sao a mesma coisa -> true
            return True
        for i in parent:
            if self.predecessor(entityGiven1, i): # se for predecessor -> true
                return True
        return False

    #exercicio 10
    def predecessor_path(self,entityGiven1,entityGiven2):
        parent = list(set([d.relation.entity2 for d in self.declarations if not isinstance(d.relation, Association) and d.relation.entity1 == entityGiven2]))
        for i in parent:
            if i == entityGiven1: # se forem iguais sao a mesma coisa -> caminho = [entityGiven1,entityGiven2]
                return [entityGiven1,entityGiven2]
            pathPredecessor = self.predecessor_path (entityGiven1,i)
            if pathPredecessor != None: 
                # entityGiven2 == ultimo p
                return pathPredecessor + [entityGiven2] # se for predecessor -> caminho desde a entityGiven1 (1 entidade) até à entityGiven2 (2 entidade)
        return None

    #exercicio 11
    def query(self,entityGiven,association=None):
        parent = [d.relation.entity2 for d in self.query_local(e1=entityGiven) if not isinstance(d.relation, Association)]
        result = [d for d in self.query_local(e1=entityGiven, rel=association) if isinstance(d.relation, Association)]
        for i in parent:
            result+=self.query(i, association)
        return result
    
    def query2(self,entityGiven, relation=None):
        aux = self.query(entityGiven,relation)
        # declaracoes locais (incluindo Member e Subtype) ou herdadas (apenas Association ->  rel=relation)
        aux1 = [d for d in self.query_local(e1=entityGiven, rel=relation) if not isinstance(d.relation, Association)]
        return aux + aux1

    #exercicio 12
    def query_cancel(self,entityGiven,association=None):
        result = [d for d in self.query_local(e1=entityGiven, rel=association) if isinstance(d.relation, Association)]
        if result == []: # cancelamento de herança
            parent = [d.relation.entity2 for d in self.query_local(e1=entityGiven) if not isinstance(d.relation, Association)]
            for i in parent:
                result += self.query_cancel(i,association)
        return result
    
    #exercicio 13
    def query_down(self,entityGiven,association,first=True): # first serve para ver se e o no raiz (se for o result = [] pq o raiz nao tem pai (e1))
        children = [d.relation.entity1 for d in self.declarations if d.relation.entity2 == entityGiven and not isinstance(d.relation, Association)]
        if children ==[]:
            return []
        result = []
        for i in children:
            for d in self.declarations:
                if isinstance(d.relation,Association) and association ==d.relation.name and (d.relation.entity1 == i or d.relation.entity2 ==i):
                    result.append(d)
        for i in children:
            result+=self.query_down(i,association)
        return result
    
    #exercicio 14
    def query_induce(self,entityGiven,association):
        descendente = self.query_down(entityGiven,association)
        aux = [d.relation.entity1 if d.relation.entity2==association else d.relation.entity2 for d in descendente]
        dic={}
        for i in aux:
            if i in dic:
                dic[i]+=1
            else:
                dic[i]=0
        return max(dic,key=dic.get) # da o maximo entre 2 numeros
        #Nao resultou:
        #aux = [d.relation.entity2 for d in descendente]
        #Counter é um contador que controla quantas vezes os valores equivalentes são adicionados
        #valores = Counter(aux)
        #most_common(n) -> Retorna uma lista dos n elementos mais comuns e suas contagens. Se n não for especificado, most_common() retorna todos os elementos no contador. Elementos com contagens iguais são ordenados arbitrariamente
        #return valores.most_common(1)[0][0] # ver isto se der mal

    #exercicio 15
    def query_local_assoc(self,entityGiven,association):
        dicAssocOne={} # contar os valores mais frequentes em AssocOne
        dicAssoc={} # contar os valores mais frequentes em Association
        countAssoc = 0
        media=0
        soma = 0 # soma dos elementos para calcular a media
        count=0 # contar quantos elementos tem para fazer a media
        for d in self.declarations:
            if d.relation.entity1 == entityGiven and d.relation.name==association:
                if isinstance(d.relation,AssocOne): # AssocOne -> contar a frequencia em que ocorre os valores
                    if d.relation.entity2 in dicAssocOne:
                        dicAssocOne[d.relation.entity2] +=1
                    else:
                        dicAssocOne[d.relation.entity2]=1
                elif isinstance(d.relation,AssocNum): # AssocNum -> fazer media dos valores
                    count +=1
                    soma += d.relation.entity2      
                elif isinstance(d.relation,Association): #Association -> contar a frequencia em que ocorre os valores
                    if d.relation.entity2 in dicAssoc:
                        dicAssoc[d.relation.entity2] +=1
                    else:
                        dicAssoc[d.relation.entity2] =1
        
        if dicAssocOne: # para o AssocOne
            val = max(dicAssocOne, key=dicAssocOne.get)
            freq = dicAssocOne[max(dicAssocOne, key=dicAssocOne.get)]/sum(dicAssocOne.values())
            return (val, freq)
        elif soma !=0 and count!=0: # para o AssocNum (media)
            media=soma/count
            return media
        elif dicAssoc: # para o Association
            countAssoc = sum(dicAssoc.values()) # valores das frequencias
            aux = [(value,(dicAssoc[value]/countAssoc)) for value in dicAssoc] 
            aux.sort(key=(lambda x:x[1]),reverse=True) #ordenar o result por ordem decrescente das frequencias
            result=[]
            countAssoc=0
            # acrenscentar ao resultado 1 os que tem a soma das frequências > 0.75 depois os outros todos
            for i in aux:
                if (i[1] + countAssoc) >0.75:
                    result.append(i)
                    break
                result.append(i)
                countAssoc+=i[1]
            return result

    #Nao resultou:
    """
    def query_local_assoc(self,entityGiven,association):
        count=0
        soma=0
        num=False
        for d in self.query_local(e1=entityGiven) :
            if isinstance(d.relation,Association): #E uma associacao
                aux = query_induce(entityGiven,association)
                aux[1].sort(reverse=True) #ordenar o result por ordem decrescente das frequencias
                if(aux[0][1] > 0.75):
                    result = aux[0][1]
                for i in aux:
                    if(somafreq(result) > 0.75):
                        result += aux[i]
            if isinstance(d.relation,AssocOne):
                result = query_induce(entityGiven,association)
            if isinstance(d.relation,AssocNum):
                soma+=d.entity1 + d.entity2
                count+=1
                num=True
        if(num==True):
            result = soma/count
        return result
    """


    #exercicio 16
    def query_assoc_value(self,E,A): #E=entityGiven, A = association
        #declaracoes locais:
        declarations= [ d.relation.entity2 for d in self.query_local(e1=E,rel=A) if isinstance(d.relation,Association)]
        #Se todas as declarações locais de A em E atribuem o mesmo valor, V , à associação,
        #então é retornado esse valor, não levando em conta os valores eventualmente herdado
        if (len(set([d for d in declarations]))): # declaracoes locais de A em E tem o mesmo valor se o len(set(...)) =1 
            return declarations[0]
        #declaracoes herdadas (query -> locais e herdadas com o if fica so as herdadas)
        auxdecl = [d.relation.entity2 for d in self.query(E,A) if(d.relation.entity2 not in declarations)]
        
        dic={}
        # contar a frequencia em que ocorre os valores
        for i in declarations+auxdecl:
            if i in dic:
                dic[i]+=1
            else:
                dic[i]=1

        for j in dic: # calculos das percentagens
            l=0
            h=0
            if len(declarations) >0:
                l=(dic[j]/len(declarations))*100
            if len(auxdecl) >0:
                h=(dic[j]/len(auxdecl))*100
            dic[j]=(l+h)/2

        return max(dic,key=dic.get)

#funcao auxiliar para calcular a soma das frequencias de uma lista
"""
    def somafreq(soma):
        result=0
        for i in soma:
            result += soma[i][1]
        return result
"""
# Funcao auxiliar para converter para cadeias de caracteres
# listas cujos elementos sejam convertiveis para
# cadeias de caracteres
def my_list2string(list):
   if list == []:
       return "[]"
   s = "[ " + str(list[0])
   for i in range(1,len(list)):
       s += ", " + str(list[i])
   return s + " ]"
    

