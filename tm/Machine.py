from State import State
class Machine:
    def __init__(self, q: State, w: str, _range: int):
        self.q = q
        self.w = w
        self.fita = []
        self.current = 0

        #Ideia para Turing Machine abaixo, onde _range*2 eh o tamanho da fita da maquina:
        self.set_fita_space(_range)
        self.init_fita(w)
        print(f'Fita inicial: {self.get_fita_string()}')

    # Implementação para Máquina de Turing
    def run(self):
        if self.q is None:
            print("Estado inicial não definido!")
            return False
        
        # Executa a máquina até que não haja mais transições possíveis ou chegue a um estado final
        max_steps = 100  # Limite de passos para evitar loops infinitos
        steps = 0
        
        while steps < max_steps:
            current_symbol = self.fita[self.current]
            
            # Tratando simbolo em branco (None ou _)
            if current_symbol is None:
                current_symbol = None  # Símbolo branco é None para o sistema
                
            transition = self.q.transition(current_symbol)
            
            if transition is None:
                symbol_display = current_symbol if current_symbol is not None else '_'
                print(f'Sem transição para o símbolo "{symbol_display}" no estado {self.q.getName()}')
                break
                
            # Obtém informações da transição
            next_state = transition.getState()
            edge = transition.getEdge()
            write_symbol = edge.getWrite()
            direction = edge.getDirection()
            
            # Realiza a transição
            symbol_display = current_symbol if current_symbol is not None else '_'
            write_display = write_symbol if write_symbol is not None else '_'
            print(f'{self.q.getName()} ({symbol_display}) -> {next_state.getName()}, escreve {write_display}, move {direction}')
            
            # Escreve o símbolo na fita
            self.fita[self.current] = write_symbol
            
            # Atualiza o estado atual
            self.q = next_state
            
            # Move a cabeça de leitura/escrita
            if direction == 'D':  # Direita
                self.current += 1
            elif direction == 'E':  # Esquerda
                self.current -= 1
            
            # Verifica se chegou ao limite da fita
            if self.current < 0 or self.current >= len(self.fita):
                print("Erro: Posição da fita fora dos limites!")
                return False
                
            print(f'Fita: {self.get_fita_string()}')
            
            # Verifica se chegou a um estado final
            if self.q.isFinal:
                return self.print_result()
                
            steps += 1
            
        if steps >= max_steps:
            print("Limite de passos atingido. Possível loop infinito.")
            
        return self.print_result()

    def print_result(self):
        """ Print and Return True (ok) or False (no ok)"""
        if self.q.isFinal:
            print(f'Aceito! Estado final: {self.q.getName()}')
            print(f'Fita final: {self.get_fita_string()}')
        else:
            print(f'Rejeitado. Estado atual: {self.q.getName()}')
        return self.q.isFinal

    def get_fita_string(self):
        """Retorna a fita como uma string, com a posição atual destacada"""
        result = ""
        for i, symbol in enumerate(self.fita):
            if symbol is None:
                symbol = '_'
            if i == self.current:
                result += f"[{symbol}]"
            else:
                result += symbol
        return result

    def init_fita(self, w):
        """Inicializa a fita com a palavra de entrada"""
        for i, a in enumerate(list(w)):
            self.fita[i+1] = a
        self.current = 1  # Posição inicial da cabeça

    def set_fita_space(self, _range):
        self.range = _range
        self.max = self.range*2

        # Inicializa a fita com símbolos em branco (_)
        for i in range(self.max+2):
            self.fita.append(None)  # None representa o símbolo em branco '_'
