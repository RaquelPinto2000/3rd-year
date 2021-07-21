from tree_search import *
from cidades import *
from strips import *
  

class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth'): 
        super().__init__(problem,strategy)
        #inicialização das variaveis offset e depth
        self.offset = 0
        self.depth = 0

    def hybrid1_add_to_open(self,lnewnodes):
        par=[] #lista com os nos das posicoes pares
        impar=[] #lista com os nos das posicoes impares
        for i in range(len(lnewnodes)):
            if(i%2==0):#se a posicao for par
                par.append(lnewnodes[i])
            else: # se for impar
                impar.append(lnewnodes[i])
        par = par[::-1] #inverter as posicoes pares 
        self.open_nodes = par +  self.open_nodes + impar
        return self.open_nodes 
        
    def hybrid2_add_to_open(self,lnewnodes):
        #creio que o problema esta na inicializacao das variaveis para o search2()
        self.open_nodes = self.open_nodes + lnewnodes
        #self.open_nodes.sort(key=lambda n:  n.depth - n.offset)
        return self.open_nodes
       
    def search2(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            #acho que esta a dar mal porque a inicializacao do depth e do offset nao esta bem feita
            #if(self.depth==node.depth):
                #offset é incrementado sempre que os nos tenham a mesma profundidade
            #    self.offset = self.offset + 1 
            #self.depth = self.parent.depth + 1 if node.parent != None else 0
            if self.problem.goal_test(node.state):
                self.terminal = len(self.open_nodes)+1
                self.solution = node
                return self.get_path(node)
            self.non_terminal+=1
            node.children = []            
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if newstate not in self.get_path(node):
                    self.depth =  self.depth +1
                    newnode = SearchNode(newstate,node)
                    node.children.append(newnode)                   
            self.add_to_open(node.children)
        return None

    def search_from_middle(self):
        #meio entre o inicial e o final
        m = self.problem.domain.middle(self.problem.initial,self.problem.goal)
        p_inicial = SearchProblem(self.problem.domain,self.problem.initial,m)
        p_final = SearchProblem(self.problem.domain,m,self.problem.goal)
        self.from_init = MyTree(p_inicial) # primeira parte da arvore
        self.to_goal = MyTree(p_final) #segunda parte da arvore
        #retorna a concatenacao das duas arvores
        return self.from_init.search() + self.to_goal.search() 

class MinhasCidades(Cidades):

    # state that minimizes heuristic(state1,middle)+heuristic(middle,state2)
    def middle(self,city1,city2):
        min=100000        
        for i in self.coordinates: #percorre as cidades todas
            h = self.heuristic(city1,i) + self.heuristic(i,city2) 
            if(i != city1 and i != city2): #cidades nao podem ser iguais
                if(h<min): #encontrar o minimo e a cidade correrpondente
                    min = h
                    city = i
        return city        

class MySTRIPS(STRIPS):
    def result(self, state, action):
        #NovoEstado = EstadoAtual - EfeitoNegativo + EfeitoPositivo
        state2 = [c for c in state if c not in action.neg]
        return state2 + action.pos

    def sort(self,state):
        string =state[:]
        string.sort(key=lambda p: str(p)) #ordenar strings
        return string

