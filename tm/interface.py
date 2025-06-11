# turing_visual_interface.py
import tkinter as tk
from tkinter import messagebox, ttk
from Machine import Machine
from State import State
from Edge import Edge
import time

class TuringVisualGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Máquina de Turing")
        self.root.geometry("800x600")

        # Área principal
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Área de entrada e execução
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)

        self.label = tk.Label(input_frame, text="Entrada da fita:")
        self.label.pack(side=tk.LEFT, padx=5)

        self.entry = tk.Entry(input_frame, width=40)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.insert(0, "aaabbb")  # Valor padrão

        self.run_button = tk.Button(input_frame, text="Executar", command=self.run_machine)
        self.run_button.pack(side=tk.LEFT, padx=5)

        # Área de visualização da fita
        tape_frame = tk.Frame(main_frame)
        tape_frame.pack(fill=tk.X, pady=10)

        self.canvas = tk.Canvas(tape_frame, height=100, width=780, bg="white")
        self.canvas.pack(pady=5)

        self.status = tk.Label(tape_frame, text="", fg="blue")
        self.status.pack(pady=5)

        # Área de edição de transições
        transitions_frame = tk.LabelFrame(main_frame, text="Editar Transições")
        transitions_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Lista de transições
        list_frame = tk.Frame(transitions_frame)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.transitions_listbox = tk.Listbox(list_frame, width=50, height=15)
        self.transitions_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.transitions_listbox.bind('<<ListboxSelect>>', self.on_transition_select)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.transitions_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.transitions_listbox.yview)

        # Formulário de edição
        edit_frame = tk.Frame(transitions_frame)
        edit_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(edit_frame, text="Estado Atual:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.current_state = tk.Entry(edit_frame, width=10)
        self.current_state.grid(row=0, column=1, sticky=tk.W, pady=2)

        tk.Label(edit_frame, text="Símbolo Lido:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.symbol_read = tk.Entry(edit_frame, width=10)
        self.symbol_read.grid(row=1, column=1, sticky=tk.W, pady=2)

        tk.Label(edit_frame, text="Próximo Estado:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.next_state = tk.Entry(edit_frame, width=10)
        self.next_state.grid(row=2, column=1, sticky=tk.W, pady=2)

        tk.Label(edit_frame, text="Símbolo Escrito:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.symbol_write = tk.Entry(edit_frame, width=10)
        self.symbol_write.grid(row=3, column=1, sticky=tk.W, pady=2)

        tk.Label(edit_frame, text="Direção (D/E):").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.direction = ttk.Combobox(edit_frame, values=["D", "E"], width=7)
        self.direction.grid(row=4, column=1, sticky=tk.W, pady=2)

        # Estado final
        self.is_final = tk.BooleanVar()
        self.final_check = tk.Checkbutton(edit_frame, text="Estado Final", variable=self.is_final)
        self.final_check.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=2)

        # Botões de ação
        button_frame = tk.Frame(edit_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        self.add_button = tk.Button(button_frame, text="Adicionar", command=self.add_transition)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.update_button = tk.Button(button_frame, text="Atualizar", command=self.update_transition)
        self.update_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = tk.Button(button_frame, text="Excluir", command=self.delete_transition)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Inicialização
        self.mt = None
        self.rects = []
        self.texts = []
        self.states = {}
        self.transitions = []
        self.selected_index = None
        
        # Criar estados e transições iniciais
        self.create_default_machine()
        self.update_transitions_list()

    def create_default_machine(self):
        # Limpar estados existentes
        self.states = {}
        self.transitions = []
        
        # Criar estados padrão
        state_names = ['q0', 'q1', 'q2', 'q3', 'q4', 'qf']
        for name in state_names:
            self.states[name] = State(name)
        
        # Definir estado final
        self.states['qf'].setFinal()
        
        # Adicionar transições padrão
        self.add_transition_data('q0', 'a', 'q1', 'A', 'D')
        self.add_transition_data('q0', None, 'q3', None, 'E')
        self.add_transition_data('q0', 'B', 'q4', 'B', 'D')
        
        self.add_transition_data('q1', 'a', 'q1', 'a', 'D')
        self.add_transition_data('q1', 'B', 'q1', 'B', 'D')
        self.add_transition_data('q1', 'b', 'q2', 'B', 'E')
        
        self.add_transition_data('q2', 'a', 'q2', 'a', 'E')
        self.add_transition_data('q2', 'B', 'q2', 'B', 'E')
        self.add_transition_data('q2', 'A', 'q0', 'A', 'D')
        
        self.add_transition_data('q4', 'B', 'q4', 'B', 'D')
        self.add_transition_data('q4', None, 'q3', None, 'E')
        
        self.add_transition_data('q3', 'A', 'q3', 'A', 'E')
        self.add_transition_data('q3', 'B', 'q3', 'B', 'E')
        self.add_transition_data('q3', None, 'qf', None, 'D')

    def add_transition_data(self, current_state, symbol_read, next_state, symbol_write, direction):
        if current_state not in self.states:
            self.states[current_state] = State(current_state)
        if next_state not in self.states:
            self.states[next_state] = State(next_state)
            
        # Adicionar à lista de transições para visualização
        self.transitions.append({
            'current_state': current_state,
            'symbol_read': symbol_read,
            'next_state': next_state,
            'symbol_write': symbol_write,
            'direction': direction
        })
        
        # Adicionar à máquina
        self.states[current_state].addTransition(
            self.states[next_state], 
            symbol_read, 
            symbol_write, 
            direction
        )

    def update_transitions_list(self):
        self.transitions_listbox.delete(0, tk.END)
        for t in self.transitions:
            read_symbol = t['symbol_read'] if t['symbol_read'] is not None else '_'
            write_symbol = t['symbol_write'] if t['symbol_write'] is not None else '_'
            self.transitions_listbox.insert(tk.END, 
                f"{t['current_state']}, {read_symbol} → {t['next_state']}, {write_symbol}, {t['direction']}")

    def on_transition_select(self, event):
        if self.transitions_listbox.curselection():
            index = self.transitions_listbox.curselection()[0]
            self.selected_index = index
            t = self.transitions[index]
            
            self.current_state.delete(0, tk.END)
            self.current_state.insert(0, t['current_state'])
            
            self.symbol_read.delete(0, tk.END)
            if t['symbol_read'] is not None:
                self.symbol_read.insert(0, t['symbol_read'])
            
            self.next_state.delete(0, tk.END)
            self.next_state.insert(0, t['next_state'])
            
            self.symbol_write.delete(0, tk.END)
            if t['symbol_write'] is not None:
                self.symbol_write.insert(0, t['symbol_write'])
            
            self.direction.set(t['direction'])
            
            # Verificar se o próximo estado é final
            self.is_final.set(self.states[t['next_state']].isFinal)

    def add_transition(self):
        try:
            current = self.current_state.get()
            read = self.symbol_read.get() if self.symbol_read.get() else None
            next_s = self.next_state.get()
            write = self.symbol_write.get() if self.symbol_write.get() else None
            direction = self.direction.get()
            
            if not current or not next_s or not direction:
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios")
                return
                
            # Adicionar nova transição
            self.add_transition_data(current, read, next_s, write, direction)
            
            # Atualizar estado final se marcado
            if self.is_final.get():
                self.states[next_s].setFinal()
                
            self.update_transitions_list()
            messagebox.showinfo("Sucesso", "Transição adicionada")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def update_transition(self):
        if self.selected_index is None:
            messagebox.showwarning("Aviso", "Selecione uma transição para atualizar")
            return
            
        try:
            # Remover transição antiga (não há método direto, precisamos recriar a MT)
            old_t = self.transitions[self.selected_index]
            
            # Atualizar com novos valores
            current = self.current_state.get()
            read = self.symbol_read.get() if self.symbol_read.get() else None
            next_s = self.next_state.get()
            write = self.symbol_write.get() if self.symbol_write.get() else None
            direction = self.direction.get()
            
            # Atualizar a lista de transições
            self.transitions[self.selected_index] = {
                'current_state': current,
                'symbol_read': read,
                'next_state': next_s,
                'symbol_write': write,
                'direction': direction
            }
            
            # Recriar a máquina com todas as transições
            self.recreate_machine()
            
            # Atualizar estado final se marcado
            if self.is_final.get():
                self.states[next_s].setFinal()
                
            self.update_transitions_list()
            messagebox.showinfo("Sucesso", "Transição atualizada")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def delete_transition(self):
        if self.selected_index is None:
            messagebox.showwarning("Aviso", "Selecione uma transição para excluir")
            return
            
        try:
            # Remover da lista
            del self.transitions[self.selected_index]
            
            # Recriar a máquina
            self.recreate_machine()
            
            self.selected_index = None
            self.update_transitions_list()
            messagebox.showinfo("Sucesso", "Transição excluída")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def recreate_machine(self):
        # Recriar todos os estados
        self.states = {}
        for t in self.transitions:
            current = t['current_state']
            next_s = t['next_state']
            
            if current not in self.states:
                self.states[current] = State(current)
            if next_s not in self.states:
                self.states[next_s] = State(next_s)
        
        # Adicionar todas as transições
        for t in self.transitions:
            self.states[t['current_state']].addTransition(
                self.states[t['next_state']], 
                t['symbol_read'], 
                t['symbol_write'], 
                t['direction']
            )

    def setup_machine(self, entrada):
        # Criar máquina a partir dos estados atuais
        q0 = self.states.get('q0')  # Assume q0 como estado inicial
        if not q0:
            # Se não tiver q0, pega o primeiro estado disponível
            q0 = list(self.states.values())[0] if self.states else State('q0')
            
        self.mt = Machine(q0, entrada, 20)
        return self.mt

    def draw_tape(self):
        self.canvas.delete("all")
        self.rects = []
        self.texts = []

        cell_width = 30
        start_x = 390 - (cell_width * 5)

        for i in range(self.mt.current - 5, self.mt.current + 12):
            x = start_x + (i - self.mt.current + 5) * cell_width
            rect = self.canvas.create_rectangle(x, 20, x + cell_width, 70, fill="lightgray" if i != self.mt.current else "yellow")
            char = self.mt.fita[i] if 0 <= i < len(self.mt.fita) and self.mt.fita[i] is not None else '_'
            text = self.canvas.create_text(x + cell_width / 2, 45, text=char, font=("Courier", 14))
            self.rects.append(rect)
            self.texts.append(text)

        self.canvas.update()

    def run_machine(self):
        entrada = self.entry.get()
        if not entrada:
            messagebox.showwarning("Aviso", "Digite uma palavra de entrada.")
            return

        self.setup_machine(entrada)
        self.status.config(text=f"Executando... Estado atual: {self.mt.q.getName()}", fg="black")
        self.draw_tape()
        self.root.update()

        try:
            step_count = 0
            max_steps = 100  # Limite para evitar loops infinitos
            
            while step_count < max_steps:
                leitura = self.mt.fita[self.mt.current]
                transicao = self.mt.q.transition(leitura)
                if not transicao:
                    break

                edge = transicao.getEdge()
                escrita = edge.getWrite()
                direcao = edge.getDirection()
                prox_estado = transicao.getState()

                # Mostrar detalhes da transição
                leitura_display = leitura if leitura is not None else '_'
                escrita_display = escrita if escrita is not None else '_'
                self.status.config(text=f"Estado: {self.mt.q.getName()} leu '{leitura_display}', "
                                      f"escreveu '{escrita_display}', "
                                      f"moveu '{direcao}', "
                                      f"foi para {prox_estado.getName()}")

                self.mt.fita[self.mt.current] = escrita
                self.mt.q = prox_estado

                if direcao == 'D':
                    self.mt.current += 1
                elif direcao == 'E':
                    self.mt.current -= 1

                self.draw_tape()
                self.root.update()
                time.sleep(0.5)
                step_count += 1
                
                # Verificar se chegou a um estado final
                if self.mt.q.isFinal:
                    break
            
            if step_count >= max_steps:
                self.status.config(text="Limite de passos atingido. Possível loop infinito.", fg="orange")
            else:
                resultado = "Aceito" if self.mt.q.isFinal else "Rejeitado"
                self.status.config(text=f"Resultado: {resultado} - Estado final: {self.mt.q.getName()}", 
                                 fg="green" if self.mt.q.isFinal else "red")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    gui = TuringVisualGUI(root)
    root.mainloop()
