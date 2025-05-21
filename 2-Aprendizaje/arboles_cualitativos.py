"""
    Funciones y clases para entrtenamiento y predicción con árboles de desición cualitativos utilizando el criterio de entropía
    
    Se asume que los datos vienen en forma de una lista de diccionarios, donde cada diccionario representa una instancia (la cual puede tener nombres de atributos diferentes)
    
      
"""

__author__ = "Julio Waissman"
__date__ = "enero 2025"


import math
from collections import Counter

def entrena_arbol(datos, target, clase_default, 
                  max_profundidad=None, acc_nodo=1, min_ejemplos=0):
    """
    Entrena un árbol de desición utilizando el criterio de entropía
    
    Parámetros: 
    -----------
    datos: list(dict)
        Una lista de diccionarios donde cada diccionario representa una instancia. 
        Cada diccionario tiene al menos un par llave-valor, donde la llave es el nombre de un atributo y el valor es el valor del atributo.
        Todos los diccionarios tienen la misma llave-valor. 
    target: str
        El nombre del atributo que se quiere predecir
    clase_default: str
        El valor de la clase por default
    max_profundidad: int
        La máxima profundidad del árbol. Si es None, no hay límite de profundidad
    acc_nodo: int
        El porcentaje de acierto mínimo para considerar un nodo como hoja
    min_ejemplos: int
        El número mínimo de ejemplos para considerar un nodo como hoja
        
    Regresa:
    --------
    nodo: Nodo
        El nodo raíz del árbol de desición
    
    """
    atributos = list(datos[0].keys())
    atributos.remove(target)
        
    # Criterios para deterinar si es un nodo hoja
    if  len(datos) == 0 or len(atributos) == 0:
        return NodoQ(terminal=True, clase_default=clase_default)
    
    clases = Counter(d[target] for d in datos)
    clase_default = clases.most_common(1)[0][0]
    
    if (max_profundidad == 0 or 
        len(datos) <= min_ejemplos or 
        clases.most_common(1)[0][1] / len(datos) >= acc_nodo):
        
        return NodoQ(terminal=True, clase_default=clase_default)
    
    variable = selecciona_variable(datos, target, atributos)
    nodo = NodoQ(terminal=False, atributo=variable, clase_default=clase_default)
    
    for valor in set(d[variable] for d in datos):
        datos_hijo = [d for d in datos if d[variable] == valor]
        nodo.hijos[valor] = entrena_arbol(
            datos_hijo, 
            target, 
            clase_default, 
            max_profundidad - 1 if max_profundidad is not None else None,
            acc_nodo, min_ejemplos
        )
    return nodo

def selecciona_variable(datos, target, atributos):
    """
    Selecciona el atributo que mejor separa las clases
    
    Parámetros:
    -----------
    datos: list(dict)
        Una lista de diccionarios donde cada diccionario representa una instancia. 
        Cada diccionario tiene al menos un par llave-valor, donde la llave es el nombre de un atributo y el valor es el valor del atributo. Todos los diccionarios tienen la misma llave-valor. 
    target: str
        El nombre del atributo que se quiere predecir
    atributos: list(str)
        La lista de atributos a considerar
        
    Regresa:
    --------
    atributo: str
        El nombre del atributo que mejor separa las clases
    """
    
    entropia = entropia_clase(datos, target)
    ganancia = {a: ganancia_informacion(datos, target, a, entropia) for a in atributos}
    return max(ganancia, key=ganancia.get)

def entropia_clase(datos, target):
    """
    Calcula la entropía de la clase
    
    Parámetros:
    -----------
    datos: list(dict)
        Una lista de diccionarios donde cada diccionario representa una instancia. 
        Cada diccionario tiene al menos un par llave-valor, donde la llave es el nombre de un atributo y el valor es el valor del atributo. Todos los diccionarios tienen la misma llave-valor. 
    target: str
        El nombre del atributo que se quiere predecir
        
    Regresa:
    --------
    entropia: float
        La entropía de la clase
    """
    
    clases = Counter(d[target] for d in datos)
    total = sum(clases.values())
    return -sum((c/total) * math.log2(c/total) for c in clases.values())

def ganancia_informacion(datos, target, atributo, entropia):
    """
    Calcula la ganancia de información de un atributo
    
    Parámetros:
    -----------
    datos: list(dict)
        Una lista de diccionarios donde cada diccionario representa una instancia. 
        Cada diccionario tiene al menos un par llave-valor, donde la llave es el nombre de un atributo y el valor es el valor del atributo. Todos los diccionarios tienen la misma llave-valor. 
    target: str
        El nombre del atributo que se quiere predecir
    atributo: str
        El nombre del atributo a considerar
    entropia: float
        La entropía de la clase
        
    Regresa:
    --------
    ganancia: float
        La ganancia de información del atributo
    """
    
    total = len(datos)
    ganancia = entropia
    
    for valor in set(d[atributo] for d in datos):
        datos_valor = [d for d in datos if d[atributo] == valor]
        ganancia -= (len(datos_valor) / total) * entropia_clase(datos_valor, target)  
    return ganancia


def predice_arbol(arbol, datos):
    return [arbol.predice(d) for d in datos]

def evalua_arbol(arbol, datos, target):
    predicciones = predice_arbol(arbol, datos)
    return sum(1 for p, d in zip(predicciones, datos) if p == d[target]) / len(datos)

def imprime_arbol(nodo, nivel=0, valor=" "):
    if nodo.terminal:
        print("    " * nivel + f"Si valor es {valor}, la clase es {nodo.clase_default}")
    else:
        if valor == " ": 
            print("    " * nivel 
                  + f"Si el atributo es {nodo.atributo} entonces:")
        else:
            print("    " * nivel 
                  + f"Si el valor es {valor} y el atributo es {nodo.atributo} entonces:")
        for valor, hijo in nodo.hijos.items():
            imprime_arbol(hijo, nivel + 1, valor)
 
class NodoQ:
    def __init__(self, terminal, clase_default, atributo=None):
        self.terminal = terminal
        self.clase_default = clase_default
        self.atributo = atributo
        self.hijos = {}
    
    def predice(self, instancia):
        if self.terminal:
            return self.clase_default       
        valor = instancia[self.atributo]        
        if valor not in self.hijos:
            return self.clase_default       
        return self.hijos[valor].predice(instancia)
    
   
def main():
    datos = [
        {"color": "rojo", "tamano": "grande", "sabor": "dulce", "clase": "manzana"},
        {"color": "verde", "tamano": "grande", "sabor": "dulce", "clase": "sandia"},
        {"color": "rojo", "tamano": "pequeno", "sabor": "dulce", "clase": "uva"},
        {"color": "verde", "tamano": "grande", "sabor": "amargo", "clase": "sandia"},
        {"color": "verde", "tamano": "pequeno", "sabor": "amargo", "clase": "uva"},
        {"color": "rojo", "tamano": "grande", "sabor": "amargo", "clase": "manzana"},
        {"color": "rojo", "tamano": "pequeno", "sabor": "dulce", "clase": "uva"},
        {"color": "verde", "tamano": "pequeno", "sabor": "dulce", "clase": "uva"},
        {"color": "rojo", "tamano": "grande", "sabor": "amargo", "clase": "manzana"},
        {"color": "verde", "tamano": "pequeno", "sabor": "amargo", "clase": "uva"},
        {"color": "rojo", "tamano": "pequeno", "sabor": "amargo", "clase": "manzana"},
        {"color": "verde", "tamano": "grande", "sabor": "dulce", "clase": "sandia"},
        {"color": "rojo", "tamano": "pequeno", "sabor": "dulce", "clase": "uva"},
        {"color": "verde", "tamano": "pequeno", "sabor": "amargo", "clase": "uva"},
        {"color": "rojo", "tamano": "grande", "sabor": "amargo", "clase": "manzana"},
        {"color": "verde", "tamano": "pequeno", "sabor": "dulce", "clase": "uva"},
        {"color": "rojo", "tamano": "grande", "sabor": "amargo", "clase": "manzana"}
    ]
    
    raiz = entrena_arbol(datos, "clase", "uva")
    imprime_arbol(raiz)
    
    acc = evalua_arbol(raiz, datos, "clase")
    print(f"El acierto en los mismos datos que se entrenó es {acc}")
    return None

if __name__ == "__main__":
    main()
