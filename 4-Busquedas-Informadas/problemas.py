import busquedas
import math

class CamionMagico(busquedas.ModeloBusqueda):
    def acciones_legales(self, x):
        return ['caminar', 'camion'] if x > 0 else ['caminar','camion']

    def sucesor(self, x, accion):
        if accion == 'caminar':
            return x + 1
        if accion == 'camion':
            return 2 * x
        return x

    def costo_local(self, x, accion):
        return 1 if accion == 'caminar' else 2

    @staticmethod
    def bonito(x):
        return f"Posición {x}"

class PblCamionMágico(busquedas.ProblemaBusqueda):
    def __init__(self, N):
        modelo = CamionMagico()
        super().__init__(1, lambda s: s == N, modelo)
        self.N = N

def h_1_camion_magico(nodo):
    """
    Heurística trivial: caminar uno a la vez hasta N.
    Admisible porque nunca sobreestima (siempre ≥ coste real mínimo).
    """
    # nodo.estado <= N, pero si excede, devolvemos 0
    return max(0, nodo.problema.N - nodo.estado) if hasattr(nodo, 'problema') else 0

def h_2_camion_magico(nodo):
    """
    Heurística de número de saltos en camión:
    Estimamos cuántas duplicaciones faltan * 2 minutos.
    Trivialmente admisible (puede subestimar).
    """
    if not hasattr(nodo, 'problema'): return 0
    x = nodo.estado
    N = nodo.problema.N
    if x <= 0 or x >= N: return 0
    pasos = math.ceil(math.log(N / x, 2))
    return pasos * 2


class CuboRubik(busquedas.ModeloBusqueda):
    def acciones_legales(self, estado):
        return []
    def sucesor(self, estado, accion):
        return estado
    def costo_local(self, estado, accion):
        return 1
    @staticmethod
    def bonito(estado):
        return str(estado)

class PblCuboRubik(busquedas.ProblemaBusqueda):
    def __init__(self, estado_inicial):
        modelo = CuboRubik()
        super().__init__(estado_inicial, lambda s: True, modelo)

def h_1_problema_1(nodo):
    """Heurística trivial 1 (siempre 0)."""
    return 0

def h_2_problema_1(nodo):
    """Heurística trivial 2 (siempre 0)."""
    return 0

def compara_metodos(problema, heur1, heur2):
    sol1 = busquedas.busqueda_A_estrella(problema, heur1)
    sol2 = busquedas.busqueda_A_estrella(problema, heur2)
    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50)
    print(f"{'A* h1':^12}{sol1.costo:^18}{sol1.nodos_visitados:^20}")
    print(f"{'A* h2':^12}{sol2.costo:^18}{sol2.nodos_visitados:^20}")
    print('-' * 50)

if __name__ == "__main__":
    # Ejemplo rápido:
    N = 10
    problema1 = PblCamionMágico(N)
    problema1.problema = problema1  # para que heurísticas puedan leer N
    compara_metodos(problema1, h_1_camion_magico, h_2_camion_magico)

    prueba_rubik = PblCuboRubik(())
    compara_metodos(prueba_rubik, h_1_problema_1, h_2_problema_1)
