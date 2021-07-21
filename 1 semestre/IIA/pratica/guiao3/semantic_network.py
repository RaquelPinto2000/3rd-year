

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


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

class AssocOne(Relation):
    def __init__(self,e1,assoc,e2):
       Relation.__init__(self,e1,assoc,e2)
       
class AssocNum(Relation):
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

    def list_associations(self):
        result = [ d.relation.name for d in self.declarations if isinstance(d.relation, Association)]
        return list(set(result))

    def list_objects(self):
        result = [ d.relation.entity1 for d in self.declarations if isinstance(d.relation, Member)]
        return list(set(result))

    def list_users(self):
        result = [d.user for d in self.query_local()]
        return list(set(result))

    def list_types(self):
        result = [d.relation.entity2 for d in self.declarations if isinstance(d.relation, Subtype) or isinstance(d.relation, Member)]
        otherRes = [d.relation.entity1 for d in self.declarations if isinstance(d.relation, Subtype)]
        otherRes+=result
        return list(set(otherRes))

    def list_local_associations(self, userGiven):
        result = [ d.relation.name for d in self.query_local(e1 = userGiven) if isinstance(d.relation, Association)]
        return list(set(result))

    def list_relations_by_user(self, userGiven):
        result = [d.relation.name for d in self.query_local(user=userGiven)]
        return list(set(result))

    def associations_by_user(self,userGiven):
        result = [ d.relation.name for d in self.query_local(user = userGiven) if not isinstance(d.relation, Member) and not isinstance(d.relation, Subtype)]
        return len(set(result))

    def list_local_associations_by_user(self, userGiven):
        result = [ (d.relation.name, d.user) for d in self.query_local(e1 = userGiven) if isinstance(d.relation, Association)]
        return list(set(result))

    def predecessor(self, upper, lower):
       parents = [d.relation.entity2 for d in self.declarations if not isinstance(d.relation, Association) and d.relation.entity1 == lower]
       for p in parents:
            if p == upper:
               return True
            if self.predecessor(upper, p):
               return True
       return False
    
    def predecessor_path(self, upper, lower):
        parents = [d.relation.entity2 for d in self.declarations if not isinstance(d.relation, Association) and d.relation.entity1 == lower]
        for p in parents:
            if p == upper :
                return [upper, lower]
            pathUP = self.predecessor_path(upper, p)
            if pathUP!= None:
                return pathUP + [lower]   #lower == p
        return None


    def query(self, entity, assertion=None):
        parents = [d.relation.entity2 for d in self.query_local(e1 = entity)]

        ldecl = [d for d in self.query_local(e1 = entity, rel = assertion) if isinstance(d.relation, Association)]

        for p in parents:
            ldecl+= self.query(p, assertion)

        return ldecl

    def query2(self, entity, assertion = None):
        tmp = self.query(entity, assertion)
        others = [d for d in self.query_local(e1 = entity, rel = assertion) if isinstance(d.relation, Member) or isinstance(d.relation, Subtype)]
        return tmp + others

    def query_cancel(self, entity, assertion= None):
        """parents = [d.relation.entity2 for d in self.query_local(e1 = entity)]
        ldecl = [d for d in self.query_local(e1 = entity, rel = assertion) if isinstance(d.relation, Association)]                   
        assertions = [d.rel for d in self.query_local(e1 = entity, rel = assertion) if isinstance(d.relation, Association)]                   

        if(assertion not in assertions):
            for p in parents:
                ldecl += self.query_cancel(p, assertion)
        return ldecl
        """
        ldecl = [ d for d in self.query_local(e1 = entity, rel=assoc)
                  if not isinstance(d.relation,Association) ]
        if decl==[]:
            parents = [ d.relation.entity2 for d in self.query_local(e1=entity)
                        if not isinstance(d.relation,Association) ]
            for p in parents:
                ldecl +=self.query_cancel(p,assoc)
        return ldecl

        def query_down (self,entity,assoc,first=True):
            ldecl = [] if first else [d for d in self.query_local(e1=entity)
                                      if isinstance(d.relation,Association) ]
            children = [ d.relation.entity1 for d in self.query_local(e2=entity)
                        if not isinstance(d.relation.Association) ]
            for c in children:
                ldecl += self.query_down(c,assos,False)
            return ldecl

        def query_induce(self,type,assoc):
            ldecl = self.query_down(type,assoc)
            values = [ d.relation.entity2 for d in ldecl ]
            val_freqs = Counter(values)
            return val_freqs.most_common(1)[0][0]
        def query_local_assoc(self,entity,assoc):
            ldecl = [] if 

            return ldecl

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
    

