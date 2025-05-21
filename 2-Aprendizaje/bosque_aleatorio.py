# bosque_aleatorio.py

import random
from collections import Counter
from arboles_numericos import entrena_arbol, predice_arbol

def muestrea_con_reemplazo(df, n):
    return df.sample(n=n, replace=True, random_state=random.randrange(1<<30))

def entrena_bosque(datos,
                   target,
                   clase_default,
                   M=10,
                   max_profundidad=None,
                   acc_nodo=1.0,
                   min_ejemplos=0,
                   num_variables=None):
    """
    Entrena un bosque de M árboles de decisión.
    
    Parámetros:
    - datos: DataFrame que incluye features + columna target.
    - target: nombre de la columna objetivo.
    - clase_default: clase a usar si no se puede dividir.
    - M: número de árboles.
    - max_profundidad: profundidad máxima de cada árbol (None = sin límite).
    - acc_nodo: accuracy mínima en un nodo para detener división.
    - min_ejemplos: mínimo de ejemplos en un nodo para dividir.
    - num_variables: si es entero, número de atributos a muestrear en cada nodo.
    
    Retorna:
    - lista de raíces de árbol (el “bosque”).
    """
    bosque = []
    n = len(datos)
    for i in range(M):
        muestra = muestrea_con_reemplazo(datos, n)
        arbol = entrena_arbol(
            datos=muestra,
            target=target,
            clase_default=clase_default,
            max_profundidad=max_profundidad,
            acc_nodo=acc_nodo,
            min_ejemplos=min_ejemplos,
            variables_seleccionadas=num_variables
        )
        bosque.append(arbol)
    return bosque

def predice_bosque(bosque, ejemplo):
    preds = [predice_arbol(arbol, ejemplo) for arbol in bosque]
    voto = Counter(preds).most_common(1)[0][0]
    return voto
