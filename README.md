# **Semana 4 - Sumativa 1**
### **Alonso Cid Riveros - a.cidriveros@uandresbello.edu**  

---
## **Contexto y solicitud**
El desarrollo de esta aplicación busca elaborar un programa en Python que
permita la aplicación de técnicas de búsqueda para la resolución de un problema concreto.

El contexto del programa es el siguiente:

- En un archivo de texto llamado "mapa.txt" se encuentra una matriz cuadrada, en donde cada elemento permite formar un laberinto de la siguiente forma:
  - Las paredes del laberinto son '#'
  - Los espacios por donde se puede desplazar un agente son " " (espacios)
  - El punto de partida está identificado con una S.
  - El punto de termino está identificado con una E

- El programa debe buscar la ruta más corta entre S y E respetando los muros y los márgenes del mapa.

- Agente y recolección de objetos
  - Además, se sembrarán objetos, en bloques de 10, los cuales deben ser recogidos por el agente y almacenarlos en su inventario.
  - El tamaño del inventario será ingresado por teclado por el usuario.
  - Si el tamaño del inventario es superior a 10, se deben resembrar más objetos, sin que las posiciones se repitan con las anteriores.

## **Desarrollo de la aplicación**

La aplicación cuenta con un método `__main__` el cual permite articular la solución, llamando a los distintos métodos creados para alcanzar los objetivos solicitados.
A continuación una descripción de como está estructurada la aplicacion.

- El método `__main__` invoca el método `def procesar_mapa(nombre_archivo)`
- El método `def procesar_mapa(nombre_archivo)` es el responsable de leer el archivo "mapa.txt" (el cual debe estar almacenado en la misma carpeta en donde está la aplicación). Este suministro considera lo siguiente:
    - Siempre será una matriz cuadrada
    - Los # (coloquialmente llamado 'Gato') son muros
    - Los ' ' (espacios) son casillas por donde puede moverse el agente.
    - En el código proporcionado por el profesor, las paredes son 1 (unos) y las casillas para desplazarse son 0 (ceros), razón por la cual, junto con leer el mapa desde el archivo .txt, procederé a reemplazar los '#' por '1' y los espacios por '0'. Junto con ello, y para facilitar el desarrollo, se almacenará la ubicación de la partida (S) en la variable 'inicio' y el final (E) en la variable 'fin' el método retorna la matriz (matriz[]) la partida (inicio) y el final (fin).

- Una vez retornado los valores `matriz`, `inicio` y `fin`, son asignados a las variables `maze`, `start` y `end` respectivamente. El método `__main__` solicita al usuario que ingrese el tamaño del **inventario** del agente.
- a continuación, el `__main__` utiliza el método `a_star_append_pop` para buscar la ruta entre el Inicio y el Final del laberinto `path = a_star_append_pop(maze, start, end)`

- El método `a_star_append_pop` es proporcionado por el docente y básicamente realiza una búsqueda del mejor camino utilizando el algoritmo A*, el cual combina un 'Costo Acumulado y una Heurística (Distancia Manhattan)'. 

  - Este método realiza el llamado del método `reconstruct_path`, el cual permite construir una lista con los elementos de la ruta, su llamado es el siguiente `def reconstruct_path(came_from, current_node)`

- Retornada la ruta (path), en el `__main__` se invoca al método `sembrar_objetos` mediante la instrucción `sembrado = sembrar_objetos(path, list_objetos)`.
  - En el método `sembrar_objetos` los objetos se sembrarán directamente en la ruta encontrada entre el inicio del laberinto y el fin de este, de este modo nos aseguraremos que todos los elementos puedan ser alcanzados o 'recogidos' por el agente.
  - Se pasa como parámetro la ruta obtenida (ruta) y la lista con elementos 'recogidos' por el agente (actuales). Este último parámetro, en su primera iteración será una lista vacía. En su segunda llamada, si el inventario del agente supera los 10 espacios, será llamada con una lista de 10 elementos. Esto permitirá gestionar que cada grupo de objetos sembrados no contenga elementos repetidos. El método retorna una lista ordenada con las coordenadas de los objetos, la cual es almacenada en la variable **sembrado**

- De vuelta en el `__main__` se despliega el laberinto con la ruta, identificada con '*', entre el Inicio (S) y el Fin (E) del laberinto.

  A continuación, se despliega el mismo laberinto con la ruta, identificada con * , entre el Inicio (S) y el Fin (E) del laberinto., pero esta vez muestra los 10 objetos sembrados, identificados con un **@**

- Continuando en el `__main__` se inicia un ciclo controlado relacionado con la cantidad de elementos del **inventario** del agente(ingresado previamente por teclado).

  - En este ciclo, lo primero que se controla es el comportamiento del índice para garantizar el correcto recorrido de las listas obtenidas anteriormente.

  - Se define que para cada objeto sembrado se debe buscar la ruta optima, comenzando desde el punto de partida, identificado ahora como **'A'**, y terminando en cada elemento sembrado identificado como **'B'**.

  - Con estos datos identificados, se realiza la llamada al método `a_star_append_pop`, pero esta vez con los nuevos parámetros de inicio y fin mediante la siguiente sentencia `path_aux = a_star_append_pop(maze,l_start,l_end)`. Como se observa, esta nueva ruta es almacenada en `path_aux`.

  - Con la nueva ruta, se vuelve a desplegar el laberinto con la nueva ruta, identificada con * , entre los objetos, identificando el Inicio con **"A"** y el Fin con **"B"** y el camino recorrido entre **"A"** y **"B"** con * (asteriscos).
  
  - En cada iteracion muestra informacion relavante para seguir la ruta entre los objetos

    `Iteracion  12  de  12 - Inicio(A) (4, 5) :: Fin(B) (1, 6)`

    `Capacidad del Inventario:  12`

    `Objetos recogidos:  12 - Espacio en inventario:  0 `


  - El ciclo termina cuando se llena el inventario y muestra un mensaje por pantalla con la cantidad de elementos recogidos y una lista con la coordenada de cada elemento.

  - **Consideración** si el inventario es superior a 10, se vuelve a llamar el método `sembrar_objetos` con la instrucción `sembrado = sembrar_objetos(path, list_objetos)`, pero esta vez `list_objetos` contendrá los 10 objetos "recogidos" por el agente. De acuerdo a cómo esta desarrollado el método, esto nos permitirá no repetir un objeto ya “recogido” en este nuevo sembrado.

#### **Para mas detalles de instrucciones, revisar comentarios al interior del mismo codigo.**
