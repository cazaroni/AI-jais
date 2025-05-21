import utileria as ut
import arboles_cualitativos as ac
import os
import random

# Descarga y descomprime los datos

url = 'https://archive.ics.uci.edu/static/public/19/car+evaluation.zip'
archivo = 'datos/car.zip'
archivo_datos = 'datos/car.data'
atributos = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class']
target = 'class'

# url = 'https://archive.ics.uci.edu/static/public/73/mushroom.zip'
# archivo = 'datos/mushroom.zip'
# archivo_datos = 'datos/agaricus-lepiota.data'
# atributos = ['class', 'cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor', 'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color', 'stalk-shape', 'stalk-root', 'stalk-surface-above-ring', 'stalk-surface-below-ring', 'stalk-color-above-ring', 'stalk-color-below-ring', 'veil-type', 'veil-color', 'ring-number', 'ring-type', 'spore-print-color', 'population', 'habitat']
# target = 'class'

if not os.path.exists('datos'):
    os.makedirs('datos')
if not os.path.exists(archivo):
    ut.descarga_datos(url, archivo)
    ut.descomprime_zip(archivo)
    
# Lee los datos
datos = ut.lee_csv(archivo_datos, atributos=atributos, separador=',')


# Selecciona un conjunto de entrenamiento y de validación
random.seed(42)
random.shuffle(datos)
N = int(0.8*len(datos))
datos_entrenamiento = datos[:N]
datos_validacion = datos[N:]

# Para diferentes profundidades
errores = []
for profundidad in [1, 3, 5, None]:
    arbol = ac.entrena_arbol(
        datos_entrenamiento, 
        target, 
        atributos, 
        max_profundidad=profundidad
    )
    error_en_muesta = ac.evalua_arbol(arbol, datos_entrenamiento, target)
    error_en_validacion = ac.evalua_arbol(arbol, datos_validacion, target)
    errores.append( (profundidad, error_en_muesta, error_en_validacion) )

# Muetsra los errores
print('d'.center(10) + 'Ein'.center(15) + 'E_out'.center(15))
print('-' * 40)
for profundidad, error_entrenamiento, error_validacion in errores:
    print(
        f'{profundidad}'.center(10) 
        + f'{error_entrenamiento:.4f}'.center(15) 
        + f'{error_validacion:.4f}'.center(15)
    )
print('-' * 40 + '\n')    


# Y Ahora entrenamos un árbol por única vez con todos los datos
arbol = ac.entrena_arbol(datos, target, atributos, max_profundidad=3)
ac.imprime_arbol(arbol)
