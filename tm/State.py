from Edge import Edge
from Transition import Transition

class State:
    def __init__(self, name: str):
        self.name = name
        self.isFinal = False
        self.transitions = []

    def getName(self): return self.name
	
    def setFinal(self): self.isFinal = True

    def addTransition(self, state, c: str, write: str = None, direction: str = None):
        """Adiciona uma transição com símbolo de leitura, escrita e direção"""
        edge = Edge(c, write, direction)
        return self.addTransitions(state, edge)

    def addTransitions(self, state, *edges):
        for edge in edges:
            transition = Transition(state, edge)
            if transition in self.transitions: #if (self.transitions.contains(transition))
                continue
            self.transitions.append(transition)
        return self

    def transition(self, _c: str):
        """Retorna a transição para o símbolo _c, se existir"""
        for t in self.transitions:
            e = t.getEdge()
            if (_c is None and e.getC() is None) or (e.getC() is not None and e.getC() == _c):
                return t
        return None
    
    def equals(self, s):
        if isinstance(s, State):
            return s.getName() == self.getName()
        return False
    
    def hashCode(self):
        return hash(self.getName())

