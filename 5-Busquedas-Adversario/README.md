![](ia.png)

# Búsquedas con adversarios (minimax)

**Evaluación de competencias 5**


## Objetivos

1. Reforzar los conocimientos de los métodos de búsquedas por
   adversarios, en particular el algoritmo Minimax con poda $\alpha$-$\beta$
   en su versión para dos jugadores por turnos.

2. Desarrollar habilidades para establecer heurísticas de ordenamiento
   de jugadas con el fin de reducir los tiempos de búsqueda.

3. Desarrollar habilidades y conocimientos para establecer medidas de
   estimación de utilidad, al aprender a generar funciones de
   características y establecer pesos entre estos. 

4. Desarrollar un juego simple con motor de IA.

Adicionalmente, en los programas se intenta mostrar un estilo de programación
más orientado al paradigma funcional.

Si bien se agradece si el juego tiene interfase gráfica, no es necesario y
se prioriza el desarrollo de las heurísticas y la programación del juego sobre
la GUI.

Es de realtar que la UX de una aplicación es fundamental para su éxito, por lo que no 
debe minimizarse esa parte esencial de todo sistema, pero no es parte de las
competencias a desarrollar en el curso de IA.

## Instrucciones

1. En el archivo `juegos_simplificados.py` se ofrecen clases para
   juego de tablero por turnos. Revisa el código y procura entender a
   grandes rasgos como funciona. El archivo `gato.py` es un
   ejemplo de uso sencillo con el juego del gato. Es importante
   aclarar que este es un ejemplo con fines didácticos y toda posible
   optimización en tiempo o uso dememoria se evitó siempre que eso
   implicara obscurecer el proceso de búsqueda con adversarios, por lo
   que el entorno es bastante ineficiente en estos términos.

2. En el archivo `minimax.py` viene ya el algoritmo de Minimax con algunas de
   sus adaptaciones básicas a juegos de dos jugadores por turnos. 
   También se propone una adaptación para que juegue limitado en el 
   tiempo y no en la profundidad.

3. En el archivo `conecta4.py` se incluye el juego de conecta 4 
   (si quieres información de como se
   juega la puedes consultar
   [aqui](http://en.wikipedia.org/wiki/Connect_Four)). En el archivo se
   ofrece el juego programado. Dentro del método hay dos funciones 
   que impactan mucho en la calidad del juego: `ordena_centro`
   y `evalua_3con`.  Desarrolla tu propias funciones con el fin de
   lograr mejores búsquedas a mayor profundidad (20 puntos).

4. Ahora tienes que desarrollar tu propio juego, las heurísticas de ordenamiento
   y de evaluación, y probarlo. Para esto te propongo dos juegos a escoger:

   - [Ultimate TicTacToe](https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe)
   - [Otello](https://en.wikipedia.org/wiki/Reversi)
   
   En cualquiera de los dos casos es muy importante desarrollar lo siguiente:

   1. Un juego basado en la clase `ModeloJuegoZT2` del módulo `juegos_simplificado.py`.
   2. Al menos una función de ordenamiento
   3. Al menos una función de evaluación
   4. El script necesario para poder jugar el juego (CLI o GUI)
   
   Para la evaluación del juego desarrollado, el motor de IA tendrá que ganarme en el juego.


