#encoding: utf8
#Raquel Pinto - 92948

from semantic_network import *
from bayes_net import *
from constraintsearch import *
from itertools import product

class MyBN(BayesNet):

    def individual_probabilities(self):
        result=[]
        #obter as variaveis das dependencies -> chaves das dependencies
        for (var,dic1) in self.dependencies.items(): 
            conjunto = self.conjunctions(self.ancentors(var))
            prob = 0
            for i in conjunto:
                prob += self.jointProb(i+[(var,True)]) # calcular probabilidade de uma variavel
            result += [var,prob] #associar a probabilidade a uma determinada variavel
        return result
    
    #Função auxiliar
    def ancentors(self,boolvalue):
        mother = [v for (v,x) in list(self.dependencies[boolvalue].keys())[0]]
        result = mother
        for m in mother:
            result += self.ancentors(m)
        return list(set(result))
    
    #Função auxiliar
    def conjunctions(self,boolvalue):
        conjunto = product([True,False], repeat=len(boolvalue))
        return list(map(lambda c : list(zip(boolvalue,c)),conjunto))


class MySemNet(SemanticNetwork):
    def __init__(self):
        SemanticNetwork.__init__(self)

    def translate_ontology(self):
        #entidades = [d for d in self.declarations if isinstance(d.relation, Subtype)]
        entidades2=[]
        listaString=[]
        for d in self.declarations: # obter as entidades2
            if isinstance (d.relation, Subtype):
                entidades2.append(d.relation.entity2)
            entidades2 = list(set(entidades2))
        entidades2 = self.ordenar(entidades2)
       
        for e2 in entidades2: #para cada entidade2 atribui se as suas entidades1
            entidades1=[]
            for d in self.declarations:
                if isinstance (d.relation, Subtype):
                    if e2==d.relation.entity2:
                        entidades1.append(d.relation.entity1)
            entidades1= list(set(entidades1))
            entidades1 = self.ordenar(entidades1)
            #modificações na string
            string = "Qx "
            count=0
            e2=e2.title() # primeira letra maiúscula
            for e1 in entidades1:
                e1=e1.title()
                count+=1
                if count==len(entidades1):
                    string += e1 + "(x) => " + e2 +"(x)"
                else:
                    string += e1 + "(x) or "
            listaString.append(string)
        return listaString
    
    #Função auxiliar para ordenar strings alfabeticamente
    def ordenar (self,lista): 
        string =lista[:]
        string.sort(key=lambda p: str(p))
        return string

    def query_inherit(self,entity,assoc):
        #lista de associações localmente declaradas
        result = [d for d in self.query_local(e1=entity, relname=assoc) if isinstance(d.relation, Association)]
        #para a associação inversa
        for d in self.declarations:
            if isinstance(d.relation, Association) and d.relation.inverse == assoc and d.relation.entity2==entity:
                result.append(d)
        #para a associação que tem o nome assoc
        parent = [d.relation.entity2 for d in self.query_local(e1=entity) if not isinstance(d.relation, Association)]
        for i in parent:
            result+=self.query_inherit(i, assoc)
        return result

    def query(self,entity,relname):
        #Associações que tem tiplo de propriedades maioritário
        NewAssociations=[]
        for d in self.declarations:
            if isinstance(d.relation, Association):
                aux = d.relation.assoc_properties()
                if aux[0] != None and aux[1] != None or aux[2]!=None:
                    NewAssociations.append(aux)

        result=[]
        #As relacoes de membro e subtipo deve ser tratado da maneira usual
        for d in self.query_local(e1 = entity, relname = relname):
            if isinstance(d.relation, Member) and d.relation.entity1==entity and d.relation.entity2 not in result:
                result.append(d.relation.entity2)
            if isinstance(d.relation, Subtype) and d.relation.entity1==entity and d.relation.entity2 not in result:
                result.append(d.relation.entity2)

        #Associações com cardinality 'single'
        for d in self.query_cancel(entity,relname):
            if isinstance(d.relation, Association) and d.relation.cardinality=='single' and d.relation.entity1==entity and d.relation.entity2 not in result:
                # se a associação tiver um tiplo de propriedades maioritario -> cancela a herança
                if(d.relation.assoc_properties() in NewAssociations): 
                    self.query_cancel(d.relation.entity2,relname)
                    result.append(d.relation.entity2)
                else:
                   result.append(d.relation.entity2)
        
        #Associações com cardinality 'multiple'
        for d in self.query_inherit(entity,relname):
            if isinstance(d.relation, Association) and d.relation.cardinality=='multiple' and d.relation.entity1==entity and d.relation.entity2 not in result:
                result.append(d.relation.entity2)
        return result
    
    #Função auxiliar para cancelamento de herança
    def query_cancel(self,entityGiven,association=None):
        result = [d for d in self.query_local(e1=entityGiven, relname=association) if isinstance(d.relation, Association)]
        if result == []: # cancelamento de herança
            parent = [d.relation.entity2 for d in self.query_local(e1=entityGiven) if not isinstance(d.relation, Association)]
            for i in parent:
                result += self.query_cancel(i,association)
        return result
    
    #Função para contar quantas vezes e que uma associação aparece
    def assoc_values (self,lista):
        valores=[]
        for i in range(0,len(lista)):
            count=0
            for j in range(i,len(lista)):
                if lista[i]==lista[j]:
                    count+=1
            if lista[i] not in valores:
                valores.append(lista[i],count)
        return valores


class MyCS(ConstraintSearch):
    
    def search_all(self,domains=None,xpto=None):
        # Pode usar o argumento 'xpto' para passar mais
        # informação, caso precise
        #
        if domains==None:
            domains = self.domains

        # se alguma variavel tiver lista de valores vazia, falha
        if any([lv==[] for lv in domains.values()]):
            return None

        # se nenhuma variavel tiver mais do que um valor possivel, sucesso
        if all([len(lv)==1 for lv in list(domains.values())]):
            return { v:lv[0] for (v,lv) in domains.items() }

        allSolution=[] # lista de soluções
        solution=None
        # continuação da pesquisa
        for var in domains.keys():
            if len(domains[var])>1:
                for val in domains[var]:
                    newdomains = dict(domains)
                    newdomains[var] = [val]
                    edges = [(v1,v2) for (v1,v2) in self.constraints if v2==var] #perquisa com restrições
                    newdomains = self.constraint_propagation(newdomains,edges) #perquisa com restrições
                    solution = self.search(newdomains)
                    # se encontrou solução e se esta ainda não existir acrescenta na lista de soluções 
                    if solution != None and solution not in allSolution: 
                        allSolution.append(solution)
        return allSolution
