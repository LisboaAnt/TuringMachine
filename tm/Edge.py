class Edge:
    def __init__(self, c: str, write: str = None, direction: str = None): # Incluir os outros dados da maquina
        self.c = c
        self.write = write
        self.direction = direction

    def getC(self): return self.c
    def getWrite(self): return self.write
    def getDirection(self): return self.direction

    @staticmethod
    def instance(c: str, write: str = None, direction: str = None):
        return Edge(c, write, direction)

    def equals(self, o):
        if isinstance(o, Edge):
            return (Edge.testAB(self.c, o.getC()) and 
                    Edge.testAB(self.write, o.getWrite()) and 
                    Edge.testAB(self.direction, o.getDirection()))
        return False

    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return self.equals(other)

    def __hash__(self):
        h = hash(self.c) if self.c is not None else 0
        h = 31 * h + (hash(self.write) if self.write is not None else 0)
        h = 31 * h + (hash(self.direction) if self.direction is not None else 0)
        return h

    def __repr__(self):
        if self.write is not None and self.direction is not None:
            return f'[{self.c},{self.write},{self.direction}]'
        return f'[{self.c}]'

    @staticmethod
    def testAB(a: str, b: str):
        return a==b
