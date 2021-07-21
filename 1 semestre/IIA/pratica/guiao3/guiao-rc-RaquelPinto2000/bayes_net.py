from itertools import product


class BayesNet:

#ldep=lista de probabilidades condicionadas -> depois calculamos a probabilidade conjunta
    def __init__(self, ldep=None):  # Why not ldep={}? See footnote 1.
        if not ldep:
            ldep = {}
        self.dependencies = ldep

    # The network data is stored in a dictionary that
    # associates the dependencies to each variable:
    # { v1:deps1, v2:deps2, ... }
    # These dependencies are themselves given
    # by another dictionary that associates conditional
    # probabilities to conjunctions of mother variables:
    # { mothers1:cp1, mothers2:cp2, ... }
    # The conjunctions are frozensets of pairs (mothervar,boolvalue)
    def add(self,var,mothers,prob):
        self.dependencies.setdefault(var,{})[frozenset(mothers)] = prob

    # Joint probability for a given conjunction of
    # all variables of the network
    def jointProb(self,conjunction):
        prob = 1.0
        # 2 listas - 1 do conjunton e a outra do self.net
        for (var,val) in conjunction:
            for (mothers,p) in self.dependencies[var].items():
                if mothers.issubset(conjunction):
                    prob*=(p if val else 1-p)
        return prob
        """ ou -> aulas teoricas (implementacoes diferentes)
        prob = 1.0
        for (x,b) in conjunction:
            for (y,mothers,p) in self.net:
                if y==x:
                    # todas as maes m=(z,bz) existem na conjunction
                    if all (m in conjunction for m in mothers):
                        prob *= p if b else 1-p
        return prob
        """
        # exemplo da aula teorica -> slide 101
        # self.dependencies('a') --> { { ('t',True),('r',True)}} : 0.95,
        #                           { ('t',True), ('r',False)} :0.29,
        #                           ....}
        
    #exercicio 2 
    def individualProb(self,boolvalue,varRede):
        conjunto = self.conjunctions(self.ancentors(boolvalue))
        prob = 0
        for i in conjunto:
            prob += self.jointProb(i+[(boolvalue,varRede)])
        return prob

    #da nos as mothers
    def ancentors(self,boolvalue):
        #motherProb =  self.dependencies[boolvalue]
        #mother =[m[0] for m in motherProb.keys()[0]]
        mother = [v for (v,x) in list(self.dependencies[boolvalue].keys())[0]]
        result = mother
        for m in mother:
            result += self.ancentors(m)
        return list(set(result))
    
    # product([1,2], [3,4]) == [(1,3), (1,4), (2,3), (2,4)].
    #map(...) -> serve para aplicarmos uma função a cada elemento de uma lista, 
    #retornando uma nova lista contendo os elementos resultantes da aplicação da função.
    def conjunctions(self,boolvalue):
        conjunto = product([True,False], repeat=len(boolvalue))
        return list(map(lambda c : list(zip(boolvalue,c)),conjunto))
        #zip (...) -> função recebe iteráveis como argumentos e retorna um iterador.
        #que gera muitos tuplos contendo elementos de cada iterável, pode aceitar 
        #qualquer tipo de iterável (arquivos,listas,tuplos,dicionários,conjuntos,...)


    """
    #Exercicio 11 do guiao tp -> SOF2018
    #Aula teorica
    ST = sobrecarga de trabalho 
    CP = cara preocupada
    PA = precisa de ajuda
    CEA = correio electronico acumulado
    PAL = utilizador esta a usar o PAL
    UER - utilizacao exagerada do rato

    Probabilidades independentes:
    P(ST) = 0.6
    P(PAL) = 0.05

    Probabilidades dependentes:
    P(CP| ST & PA) = 0.02
    P(CP| ST & ~PA) = 0.01
    P(CP| ~ST & PA) = 0.011
    P(CP| ~ST & ~PA) = 0.001

    P(CEA | ST)=0.9
    P(CEA | ~ST)=0.001

    P(PA | PAL) = 0.25
    P(PA | ~PAL) = 0.004

    P(UER | PAL & PA) = 0.9
    P(UER | PAL & ~PA) = 0.9
    P(UER | ~PAL & PA) = 0.1
    P(UER | ~PAL & ~PA) = 0.01

            ST          PAL
            |\          | \ 
            | \         |  \ 
            |  \       PA   \ 
            CEA  \     /  \   \  
                \   /    \  /  
                    CP      UER

    """

# Footnote 1:
# Default arguments are evaluated on function definition,
# not on function evaluation.
# This creates surprising behaviour when the default argument is mutable.
# See:
# http://docs.python-guide.org/en/latest/writing/gotchas/#mutable-default-arguments

