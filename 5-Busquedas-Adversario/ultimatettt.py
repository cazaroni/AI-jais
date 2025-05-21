#!/usr/bin/env python3
from copy import deepcopy

class UltimateTTT:
    def __init__(self):
        # macro: 9 celdas (0=jugable, 1=X gana, 2=O gana, -1=empate)
        self.estado_inicial = ([0]*9, [[0]*9 for _ in range(9)], 1, None)

    @staticmethod
    def check_board(board):
        lines = [(0,1,2),(3,4,5),(6,7,8),
                 (0,3,6),(1,4,7),(2,5,8),
                 (0,4,8),(2,4,6)]
        for a,b,c in lines:
            if board[a] != 0 and board[a] == board[b] == board[c]:
                return board[a]
        if all(cell != 0 for cell in board):
            return -1
        return None

    def acciones(self, estado):
        macro, micros, jugador, next_b = estado
        moves = []
        if next_b is not None and macro[next_b] == 0:
            for cell in range(9):
                if micros[next_b][cell] == 0:
                    moves.append((next_b, cell))
        else:
            for mb in range(9):
                if macro[mb] == 0:
                    for cell in range(9):
                        if micros[mb][cell] == 0:
                            moves.append((mb, cell))
        return moves

    def resultado(self, estado, accion):
        macro, micros, jugador, _ = estado
        mb, cell = accion
        new_macro = list(macro)
        new_micros = deepcopy(micros)
        new_micros[mb][cell] = jugador
        win = self.check_board(new_micros[mb])
        if win is not None:
            new_macro[mb] = win
        # si la próxima sub-board está decidida, permitimos “cualquiera”
        next_b = cell if new_macro[cell] == 0 else None
        return (new_macro, new_micros, 3-jugador, next_b)

    def terminal_test(self, estado):
        macro, micros, jugador, next_b = estado
        if self.check_board(macro) is not None:
            return True
        # si no quedan acciones, es terminal
        return not bool(self.acciones(estado))

    def utility(self, estado, jugador_obj):
        winner = self.check_board(estado[0])
        if winner == jugador_obj:
            return  1
        if winner == 3-jugador_obj:
            return -1
        return 0

    def mostrar(self, estado):
        mac, mic, jugador, nb = estado
        sym = {0: '.', 1: 'X', 2: 'O'}
        out = []
        for R in range(3):
            for r in range(3):
                row = []
                for C in range(3):
                    mb = 3*R + C
                    row.append(''.join(sym[c] for c in mic[mb][3*r:3*r+3]))
                out.append(' | '.join(row))
            out.append('-'*11)
        return '\n'.join(out)

def minimax_search(juego, estado, depth):
    """Devuelve la mejor acción para el jugador turno en 'estado'."""
    jugador_max = estado[2]

    def max_val(est, d):
        if juego.terminal_test(est) or d == 0:
            return juego.utility(est, jugador_max)
        v = float('-inf')
        for a in juego.acciones(est):
            v = max(v, min_val(juego.resultado(est, a), d-1))
        return v

    def min_val(est, d):
        if juego.terminal_test(est) or d == 0:
            return juego.utility(est, jugador_max)
        v = float('inf')
        for a in juego.acciones(est):
            v = min(v, max_val(juego.resultado(est, a), d-1))
        return v

    best_score, best_action = float('-inf'), None
    for a in juego.acciones(estado):
        score = min_val(juego.resultado(estado, a), depth-1)
        if score > best_score:
            best_score, best_action = score, a
    return best_action

def jugar_uttt():
    juego = UltimateTTT()
    estado = juego.estado_inicial
    jugador_hum = 1      # 1=X, 2=O
    profundidad  = 3     # ajuste rápido para que corra en CLI

    while True:
        print(juego.mostrar(estado))
        if juego.terminal_test(estado):
            u = juego.utility(estado, jugador_hum)
            if u ==  1: print("¡Has ganado!")
            if u == -1: print("Has perdido.")
            if u ==  0: print("Empate.")
            break

        if estado[2] == jugador_hum:
            posibles = juego.acciones(estado)
            print("Movimientos válidos:", posibles)
            try:
                mb, cell = map(int, input("Tu jugada (mb,cell): ").split(','))
                if (mb,cell) not in posibles:
                    print("Movimiento inválido, intenta de nuevo.")
                    continue
            except:
                print("Formato incorrecto, usa mb,cell.")
                continue
            estado = juego.resultado(estado, (mb,cell))
        else:
            print("IA pensando…")
            a = minimax_search(juego, estado, profundidad)
            print("La IA juega:", a)
            estado = juego.resultado(estado, a)

if __name__ == "__main__":
    jugar_uttt()
