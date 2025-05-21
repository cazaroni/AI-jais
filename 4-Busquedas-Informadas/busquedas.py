"""
busquedas.py
------------
Clases y algoritmos necesarios para desarrollar agentes de
búsquedas en entornos determinísticos conocidos discretos
completamente observables
"""

__author__ = 'juliowaissman'

from collections import deque
import heapq

class ModeloBusqueda:
    def acciones_legales(self, estado):
        raise NotImplementedError("No implementado todavía.")
    def sucesor(self, estado, accion):
        raise NotImplementedError("No implementado todavía.")
    def costo_local(self, estado, accion):
        return 1

class ProblemaBusqueda:
    def __init__(self, x0, meta, modelo):
        def es_meta(estado):
            self.num_nodos += 1
            return meta(estado)
        self.es_meta = es_meta
        self.x0 = x0
        self.modelo = modelo
        self.num_nodos = 0

class Nodo:
    def __init__(self, estado, accion=None, padre=None, costo_local=0):
        self.estado = estado
        self.accion = accion
        self.padre = padre
        self.costo = 0 if not padre else padre.costo + costo_local
        self.profundidad = 0 if not padre else padre.profundidad + 1
        self.nodos_visitados = 0

    def expande(self, modelo):
        return [ Nodo(modelo.sucesor(self.estado,a), a, self, modelo.costo_local(self.estado,a))
                 for a in modelo.acciones_legales(self.estado) ]

    def genera_plan(self):
        if not self.padre:
            return [(self.estado, self.costo)]
        plan = self.padre.genera_plan()
        return plan + [self.accion, (self.estado, self.costo)]

    def __lt__(self, other):
        return self.profundidad < other.profundidad

# --- Búsquedas no informadas (ya implementadas en tu repo) ---
def busqueda_ancho(problema):
    if problema.es_meta(problema.x0):
        return Nodo(problema.x0)
    frontera = deque([Nodo(problema.x0)])
    visitados = {problema.x0}
    while frontera:
        nodo = frontera.popleft()
        for hijo in nodo.expande(problema.modelo):
            if hijo.estado in visitados: continue
            if problema.es_meta(hijo.estado):
                hijo.nodos_visitados = problema.num_nodos
                return hijo
            frontera.append(hijo)
            visitados.add(hijo.estado)
    return None

def busqueda_profundo(problema, max_profundidad=None):
    frontera = deque([Nodo(problema.x0)])
    visitados = {problema.x0: 0}
    while frontera:
        nodo = frontera.pop()
        if problema.es_meta(nodo.estado):
            nodo.nodos_visitados = problema.num_nodos
            return nodo
        if max_profundidad is not None and nodo.profundidad >= max_profundidad:
            continue
        for hijo in nodo.expande(problema.modelo):
            if hijo.estado not in visitados or visitados[hijo.estado] > hijo.profundidad:
                frontera.append(hijo)
                visitados[hijo.estado] = hijo.profundidad
    return None

def busqueda_profundidad_iterativa(problema, max_profundidad=20):
    for d in range(max_profundidad):
        res = busqueda_profundo(problema, d)
        if res: return res
    return None

def busqueda_costo_uniforme(problema):
    frontera = []
    heapq.heappush(frontera, (0, Nodo(problema.x0)))
    visitados = {problema.x0: 0}
    while frontera:
        _, nodo = heapq.heappop(frontera)
        if problema.es_meta(nodo.estado):
            nodo.nodos_visitados = problema.num_nodos
            return nodo
        for hijo in nodo.expande(problema.modelo):
            if hijo.estado not in visitados or hijo.costo < visitados[hijo.estado]:
                visitados[hijo.estado] = hijo.costo
                heapq.heappush(frontera, (hijo.costo, hijo))
    return None

# ---------------------------------------------------------------------
# Problema 1: Búsqueda A*
# ---------------------------------------------------------------------
def busqueda_A_estrella(problema, heuristica):
    """
    Búsqueda A* mínima:
     - f = g + h
     - usa un heap para la frontera.
    """
    frontera = []
    inicio = Nodo(problema.x0)
    heapq.heappush(frontera, (heuristica(inicio), inicio))
    visitados = {problema.x0: 0}
    while frontera:
        f_act, nodo = heapq.heappop(frontera)
        if problema.es_meta(nodo.estado):
            nodo.nodos_visitados = problema.num_nodos
            return nodo
        for hijo in nodo.expande(problema.modelo):
            g = hijo.costo
            f_nuevo = g + heuristica(hijo)
            if hijo.estado not in visitados or g < visitados[hijo.estado]:
                visitados[hijo.estado] = g
                heapq.heappush(frontera, (f_nuevo, hijo))
    return None
