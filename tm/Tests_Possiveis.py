from State import State
from Machine import Machine

def teste_anbn(): # Livre de contexto
    print("{ a^nb^n | n>=0 }")
    q0 = State('q0')
    q1 = State('q1')
    q2 = State('q2')
    q3 = State('q3')
    q4 = State('q4')
    qf = State('qf')
    qf.setFinal()

    q0.addTransition(q1, 'a', 'A', 'D')
    q0.addTransition(q3, None, None, 'E')
    q0.addTransition(q4, 'B', 'B', 'D')

    q1.addTransition(q1, 'a', 'a', 'D')
    q1.addTransition(q1, 'B', 'B', 'D')
    q1.addTransition(q2, 'b', 'B', 'E')

    q2.addTransition(q2, 'a', 'a', 'E')
    q2.addTransition(q2, 'B', 'B', 'E')
    q2.addTransition(q0, 'A', 'A', 'D')

    q4.addTransition(q4, 'B', 'B', 'D')
    q4.addTransition(q3, None, None, 'E')

    q3.addTransition(q3, 'A', 'A', 'E')
    q3.addTransition(q3, 'B', 'B', 'E')
    q3.addTransition(qf, None, None, 'D')

    # Modificar para entrada válida - mesmo número de 'a's e 'b's
    w = 'aaabbb'  # 3 'a's e 3 'b's
    # A entrada original 'aaabbbb' foi rejeitada porque tem 3 'a's e 4 'b's

    mt = Machine(q0, w, 20)
    mt.run()

def teste_y_x(): # Regular
    print("{ w in Σ^* | w é um número binario multiplo de 3}")
    q0 = State('q0')
    q1 = State('q1')
    q2 = State('q2')
    q0.setFinal()

    q0.addTransition(q0, '0', 'a', 'D')
    q0.addTransition(q1, '1', 'b', 'D')

    q1.addTransition(q0, '1', 'b', 'D')
    q1.addTransition(q2, '0', 'a', 'D')

    q2.addTransition(q2, '1', 'b', 'D')
    q2.addTransition(q1, '0', 'a', 'D')

    w = '0000110'

    mt = Machine(q0, w, 20)
    mt.run()

if __name__ == "__main__":
    teste_anbn()
