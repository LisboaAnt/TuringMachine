class TuringEdge:
    def __init__(self, simbolo_lido, simbolo_escrito, direcao):
        self.simbolo_lido = simbolo_lido
        self.simbolo_escrito = simbolo_escrito
        self.direcao = direcao

    def getSimboloLido(self):
        return self.simbolo_lido

    def getSimboloEscrito(self):
        return self.simbolo_escrito

    def getDirecao(self):
        return self.direcao

    def __repr__(self):
        return f"[{self.simbolo_lido},{self.simbolo_escrito},{self.direcao}]" 