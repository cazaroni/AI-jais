import math
import random
import pandas as pd
from collections import Counter

class NodoN:
    def __init__(self, terminal, clase_default, atributo=None, valor=None):
        self.terminal = terminal
        self.clase_default = clase_default
        self.atributo = atributo
        self.valor = valor
        self.hijo_menor = None
        self.hijo_mayor = None
    
    def predice(self, instancia):
        if self.terminal:
            return self.clase_default               
        if instancia[self.atributo] < self.valor:
            return self.hijo_menor.predice(instancia)       
        return self.hijo_mayor.predice(instancia)

def entrena_arbol(datos, target, clase_default, 
                  max_profundidad=None, acc_nodo=1.0, min_ejemplos=0,
                  variables_seleccionadas=None):
    """
    Entrena un árbol de decisión binario usando entropía.
    Soporta DataFrame o lista de dicts.
    """
    # 1) Si es DataFrame, convierte a list of dicts
    if isinstance(datos, pd.DataFrame):
        datos = datos.to_dict(orient='records')
    
    # 2) Si no hay instancias, nodo hoja
    if len(datos) == 0:
        return NodoN(terminal=True, clase_default=clase_default)

    # 3) Atributos disponibles (excluyendo target)
    atributos = list(datos[0].keys())
    atributos.remove(target)

    # 4) Muestra aleatoria de variables para este nodo
    if isinstance(variables_seleccionadas, int):
        atributos = random.sample(atributos, min(variables_seleccionadas, len(atributos)))

    # 5) Si ya no quedan atributos, nodo hoja
    if not atributos:
        return NodoN(terminal=True, clase_default=clase_default)

    # 6) Calcular clases y actualizar clase por default
    clases = Counter(d[target] for d in datos)
    clase_default = clases.most_common(1)[0][0]

    # 7) Parada por profundidad, min_ejemplos o pureza
    if (max_profundidad == 0 or
        len(datos) <= min_ejemplos or
        clases.most_common(1)[0][1] / len(datos) >= acc_nodo):
        return NodoN(terminal=True, clase_default=clase_default)

    # 8) Seleccionar mejor atributo y punto de corte
    variable, valor = selecciona_variable_valor(datos, target, atributos)
    nodo = NodoN(terminal=False, clase_default=clase_default,
                 atributo=variable, valor=valor)

    # 9) Dividir en dos subconjuntos
    menores = [d for d in datos if d[variable] < valor]
    mayores = [d for d in datos if d[variable] >= valor]

    # Si la división no separa (uno de los dos queda vacío), volvemos a hoja
    if len(menores) == 0 or len(mayores) == 0:
        return NodoN(terminal=True, clase_default=clase_default)

    # 10) Recursión en cada rama
    nuevo_depth = max_profundidad - 1 if max_profundidad is not None else None
    nodo.hijo_menor = entrena_arbol(
        menores, target, clase_default,
        max_profundidad=nuevo_depth,
        acc_nodo=acc_nodo,
        min_ejemplos=min_ejemplos,
        variables_seleccionadas=variables_seleccionadas
    )
    nodo.hijo_mayor = entrena_arbol(
        mayores, target, clase_default,
        max_profundidad=nuevo_depth,
        acc_nodo=acc_nodo,
        min_ejemplos=min_ejemplos,
        variables_seleccionadas=variables_seleccionadas
    )
    return nodo


def selecciona_variable_valor(datos, target, atributos):
    entropia = entropia_clase(datos, target)
    # Para cada atributo, obtengo (valor_corte, ganancia) y elijo el mejor par
    mejor = max(
        ((a, maxima_ganancia_informacion(datos, target, a, entropia))
         for a in atributos),
        key=lambda x: x[1][1]
    )
    return mejor[0], mejor[1][0]

def entropia_clase(datos, target):
    clases = Counter(d[target] for d in datos)
    total = sum(clases.values())
    return -sum((c/total) * math.log2(c/total) for c in clases.values())

def maxima_ganancia_informacion(datos, target, atributo, entropia):
    lista_valores = [(d[atributo], d[target]) for d in datos]
    lista_valores.sort(key=lambda x: x[0])
    candidatos = []
    for (v1, v2), (v3, v4) in zip(lista_valores, lista_valores[1:]):
        if v2 != v4:
            punto = (v1 + v3) / 2
            g = ganancia_informacion(datos, target, atributo, punto, entropia)
            candidatos.append((punto, g))
    return max(candidatos, key=lambda x: x[1])

def ganancia_informacion(datos, target, atributo, valor, entropia):
    d_menor = [d for d in datos if d[atributo] < valor]
    d_mayor = [d for d in datos if d[atributo] >= valor]
    e_menor = entropia_clase(d_menor, target)
    e_mayor = entropia_clase(d_mayor, target)
    total = len(datos)
    return entropia - (len(d_menor)/total)*e_menor - (len(d_mayor)/total)*e_mayor

def predice_arbol(arbol, ejemplos):
    import pandas as pd

    if isinstance(ejemplos, dict):
        return arbol.predice(ejemplos)

    if isinstance(ejemplos, pd.DataFrame):
        return [arbol.predice(row) for _, row in ejemplos.iterrows()]

    return [arbol.predice(ej) for ej in ejemplos]

def evalua_arbol(arbol, datos, target):
    preds = predice_arbol(arbol, datos)
    true = [d[target] for d in (datos.to_dict('records') if isinstance(datos, pd.DataFrame) else datos)]
    return sum(p == t for p, t in zip(preds, true)) / len(true)

def imprime_arbol(nodo, nivel=0):
    if nodo.terminal:
        print("    "*nivel + f"La clase es {nodo.clase_default}")
    else:
        print("    "*nivel + f"Si {nodo.atributo} < {nodo.valor} entonces:")
        imprime_arbol(nodo.hijo_menor, nivel+1)
        print("    "*nivel + f"Si {nodo.atributo} >= {nodo.valor} entonces:")
        imprime_arbol(nodo.hijo_mayor, nivel+1)
