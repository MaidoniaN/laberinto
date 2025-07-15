"""
 ACIF102
 Semana 4 - Tarea Sumativa 1
 Desarrollado por Alonso Cid Riveros
 mail: a.cidriveros@uandresbello.edu
""" 
import random       # Importamos RADOM para declarar los objetos de forma aleatoria.

#----------- INICIO DEL METODO DE LECTURA --------------#
"""
    El bloque de codigo proporcionado para esta sumativa considera una matriz cuadrada de 10x10 la cual esta 'codificada' al interior del __main__
    Sin embargo, en el encargo del trabajo, se solicita que se utilice un mapa, contenido en un archivo txt, proporcionado como suministro.
    Es por esta razon que se debe generar una rutina que permita leer archivo txt y transformarlo en una matriz.
    Este suministro considera lo siguiente:
    - Siempre sera una matriz cuadrada
    - Los # (coloquialmente llamado 'Gato') son muros
    - Los ' ' (espacios) son casillas por donde puede moverse el agente.

    En el codigo proporcionado por el profesor, las paredes son 1 (unos) y las casillas para despazarse son 0 (ceros), razon por la cual, junto con leer
    el mapa desde el archivo .txt, procederé a reemplazar los '#' por '1' y los espacios por '0'. Junto con ello, y para facilitar el desarrollo, se almacenará
    la ubicacion de la partida (S) en la variable 'inicio' y el final (E) en la variable 'fin'
    el metodo retorna la matriz (matriz[]) la partida (inicio) y el final (fin).
"""
# Metodo para leer el mapa desde un archivo de texto.
def procesar_mapa(nombre_archivo):
    # Abrimos el archivo de texto solo en modo lectura
    with open(nombre_archivo, 'r') as archivo:
        # Leemos linea por linea el archivo
        lineas = archivo.readlines()
    
    # A cada linea le eliminamos el salto de fin de linea
    lineas = [linea.strip('\n') for linea in lineas]
    
    # Inicializacion de variables
    matriz = []     # Almacenara la Matriz
    inicio = None   # Almacenara la posicion de S (Inicio)
    fin = None      # Almacenara la posicion de E (Fin)
    
    # El codigo que reutilizaremos, define los 0 como espacios y los 1 como las paredes
    # Por este motivo los espacios en el TXT seran reemplazados por 0
    # Mientras que los # seran reemplazados por 1.
    for i, linea in enumerate(lineas):
        fila = []           # Lista que almacenara los elemento y construira la matriz fila por fila.
        for j, caracter in enumerate(linea):
            if caracter == '#':     # Si Encontramos un # ...
                fila.append(1)      # ... lo reemplazamos por un 1
            elif caracter == ' ':   # Si Encontramos un ' ' (espacio) ...
                fila.append(0)      # ... lo reemplazamos por un 0
            elif caracter == 'S':   # Si Encontramos el Inicio S lo almacenamos antes de reemplazar por 0
                inicio = (i, j)     # Guardamos posición de inicio
                fila.append(0)      # Reemplazamos con 0
            elif caracter == 'E':   # Si Encontramos el Fin E lo almacenamos antes de reemplazar por 0
                fin = (i, j)        # Guardamos posición de fin
                fila.append(0)      # Reemplazamos con 0
            else:
                fila.append(0)   # Por defecto, otros caracteres como 0
        matriz.append(fila)
    
    return matriz, inicio, fin      # Retornamos la Matriz, la Posicion Inicial y la Posicion Final.
#----------- FIN DEL METODO DE LECTURA --------------#

#----------- METODO OBJETOS ALEATORIOS --------------#
"""
    Los objetos se sembraran directamente en la ruta encontrada entre el inicio del laberinto y el fin de este
    de este modo nos aseguraremos que todos los elementos puedan ser alcanzados o 'recogidos' por el agente.
    Se pasa como parametro la ruta obtenida (ruta) y la lista con elementos 'recogidos' por el agente (actuales). Esta ultima, en su primera iteracion será una lista vacia
    en su segunda llamada, si el inventario del agente supera los 10 espacios, sera llamada con una lista de 10 elementos.
    Esto permitira gestionar que cada grupo de objetos sembrados no contenga elementos repetidos.
"""
def sembrar_objetos(ruta, actuales):
    # Acortamos el Path, eliminando el primer y el ultimo objeto, para que no concidan con el Start y el End entregados en el mapa.
    ruta_aux = ruta[1:-1]
    # Seleccionar 10 índices aleatorios únicos (sin repetición)
    # Para evitar que se el objeto sembrado, tomamos la ruta principal encontrada y le sacamos los elementos actuales.
    ruta_filtrada = [elem for elem in ruta_aux if elem not in actuales]
    # Verificamos que haya suficientes en la ruta para sembrar los 10 objetos.
    if len(ruta_filtrada) < 10:
        print("No hay suficientes elementos únicos para seleccionar 10 sin repetición.")
        return []
    
    # Tomamos la ruta_filtrada y aleatoriamente le extraemos 10 indices
    indices= random.sample(range(len(ruta_filtrada)), 10)
    # Ordenamos los indices, ya que queremos despazarnos ordenadamente por la ruta
    indices_ordenados = sorted(indices)
    
    # Extraer las posiciones correspondientes (en orden original)
    sembrado_ordenado = [ruta_filtrada[i] for i in indices_ordenados]

    # Retornamos sembrado_ordenado con la lista de 10 tuplas ordenadas.
    return sembrado_ordenado

#----------- FIN DEL METODO DE OBJETOS --------------#

#----------- METODO A*  --------------#
"""
    Metodo de busqueda proporcionado por el docente.
    Permite identificar una ruta optima entre un punto S(start) y otro punto E(end)
    Utilzia una funcion heuristica como la distancia de manhatan para realizar sus calculos.

"""
def a_star_append_pop(maze, start, end):
    rows, cols = len(maze), len(maze[0])

    # 1. Función Heurística (Distancia de Manhattan)
    def heuristic(node, end):
        return abs(node[0] - end[0]) + abs(node[1] - end[1])
    
    # 2. Inicialización de Estructuras de Datos
    # open_set == almacenamos los nodos que visitamos
    open_set = []
    open_set.append((0, start)) # Usamos append para añadir el inicio

    # g_Score es una matriz que al final tiene los mejores valores para recorrer el laberinto
    # g_Score declara todos los elementos de la matriz con valores 'inf' (infinito)
    g_score = { (r, c): float('inf') for r in range(rows) for c in range(cols) }
    g_score[start] = 0

    # CORRECTED LINE HERE
    # f_score es igual al g_score pero local,. el g_score es GLOBAL.
    # f_Score declara todos los elementos de la matriz con valores 'inf' (infinito)
    f_score = { (r, c): float('inf') for r in range(rows) for c in range(cols) } 
    f_score[start] = heuristic(start, end)

    # came_from almacena las casillas seleccionadas que formaran parte de la ruta.
    came_from = {}

    # 3. Bucle Principal del Algoritmo A*
    while open_set:
        # Buscar el nodo con el menor f_score manualmente
        # (Esto es lo que hace que sea menos eficiente que heapq para grandes conjuntos)
        min_f = float('inf')        # Declara e inicializa el min_f en infinito (float('inf'))
        current_node_tuple = None   # Declara current_node_tuple como vacio (None)
        # Recorre el open_set y lo va agregando a item
        for item in open_set:
            if item[0] < min_f:
                min_f = item[0]             # Si, a min_f le asigna el valor de item[0]
                current_node_tuple = item   # y a current_note_tuple le asigna el item completo.

        # en caso que el nodo actual, en revision no contenga ningun item
        if current_node_tuple is None: # Should not happen if open_set is not empty
            break # Or handle error, this is a safeguard
            
        # Se declara current_f y current_node y se les asigna el valor del current_node_tuple obtenido anteriormente. (nodo con el menor f_score)
        current_f, current_node = current_node_tuple        
        open_set.remove(current_node_tuple) # Elimina esa entrada de la lista

        # Si hemos llegado al objetivo, reconstruimos y devolvemos el camino.
        if current_node == end:
            # Se pasan como parametros la ruta (came_from) que se lleva recorrida hasta este punto + el nodo actual (current_node) que contiene las coordenadas
            # de la casilla final
            path_final = reconstruct_path(came_from, current_node)
            # La ruta 'reconstruida' (path_final) es retornada. este es el punto de termino del metodo A*
            return path_final
        
        # 4. Exploración de Vecinos
        # Con un ciclo for, recorre la fila (dr) y la columna (dc) de los valores pasados como direcciones []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Movimientos declarados (abajo, arriba, derecha, izquierda)
        for dr, dc in directions:
            # Se declara la variable neighbor, el cual corresponde al nodo actual + las alternativas de movimiento.
            neighbor = (current_node[0] + dr, current_node[1] + dc)
            #Aseguramos un movimiento válido dentro del maze
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                # Evalua si el vecino contiene un 0 (por donde puede circular)
                if maze[neighbor[0]][neighbor[1]] == 0:
                    # Se crea la variable tentative_g_score y se le asigna el valor de g_score del current_node + 1
                    tentative_g_score = g_score[current_node] + 1
                    # Si tentative_g_score es menor que g_score[neighbor]
                    # Se procede a generar los intercambios correspondinetes para evaluar
                    if tentative_g_score < g_score[neighbor]:
                        # Almacenamos el valor del nodo actual en came_from
                        came_from[neighbor] = current_node 
                        # actualizamos los valores de g_score y f_score 
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                        # Agregamos al open_set la tupla (f_score[neighbor], neighbor)
                        open_set.append((f_score[neighbor], neighbor))
    # Si el bucle termina y no se encuentra el objetivo, significa que no hay camino.
    return None

"""
    El metodo reconstruct_path() recibe como parametros la lista came_from y  current_node para armar la ruta
    entre el punto de partida y el final, pero la arma desde el fin hasta el inicio
    Al momento de retornar lo hacer con el path[::-1] (-1 significa invertida), de este modo se puede 'leer' el path
    desde el inicio al fin.
"""

def reconstruct_path(came_from, current_node):
    #Reconstruye el camino desde el nodo final hasta el inicio.
    path = []
    while current_node in came_from:
        path.append(current_node)
        current_node = came_from[current_node]
    path.append(current_node)  # Añadir el nodo de inicio
    #print ("PATH= ",path[::-1])
    return path[::-1]  # Invertir el camino

# --- CLASE PRINCIPAL ---
if __name__ == "__main__":
    
    # Entregamos el nombre del archivo txt con el mapa, las posiciones S y E en el mapa seran el inicio y fin
    nombre_archivo = "mapa.txt"
    # Llamamos el metodo procesar_mapa con el nombre del archivo de texto como argumento
    matriz_mapa, pos_inicio, pos_fin = procesar_mapa(nombre_archivo)
    # Asignamos la matriz_mapa obtenida a maze y los valores de pos_inicio y pos_fin a start y end respectivamente
    maze = matriz_mapa
    start = pos_inicio
    end = pos_fin

    # Declaramos una lista de objetos vacia, que almacenara los objetos sembrados y recogidos por el agente
    list_objetos=[]
    # La variable inventario contendra la cantidad de objetos que puede 'recoger' el agente.
    inventario=0
    ingreso = False
    # El siguiente bloque de codigo busca validar el ingreso de datos, sin 'bloquear' la ejecucion manejando la excepcion con un bloque try-except.
    while ingreso is False:
        try:
            inventario = int(input("Ingrese la capacidad del inventario: "))
            ingreso = True
        except ValueError:
            Inventario = 0  # Valor por defecto en caso de error
            print("Se asignó 0 porque no ingresaste un número válido")
            print(inventario)
    
    print("La Capacidad del inventario es: ", inventario)

    print("Buscando la Mejor Ruta para Salir")
    # Llamamos el metodo a_star_append_pop, le entregamos como parametros el mapa(maze), el inicio(start) y el fin(end)
    # El resultado (la ruta) lo almacenamos en path
    path = a_star_append_pop(maze, start, end)

    # Llamamos al metodo sembrar_objetos, con los parametros path (lista de posiciones para llegar desde el Inicio al Fin)
    # y list_objetos, el cual en esta primera llamada esta vacio.
    sembrado = sembrar_objetos(path, list_objetos)
    
    val_path=False
    
    # Si la ruta devuelta tiene contenido.
    if path:
        print("Camino Principal Encontrado:")
        # Preparamos todo para mostrar el mapa con la ruta.
        # Para no modificar el mapa almacenado en Maze creamos una copia y lo almacenamos en display_maze     
        display_maze = [row[:] for row in maze]
        # Recorremos la ruta path
        for r, c in path:
            # En donde la coordenada de path no sea igual al inicio o fin
            if (r, c) != start and (r, c) != end:
                # Se le asigna a display_maze un * en la coordenada de cada elemento de path.
                display_maze[r][c] = '*'
        # Recorremos la matriz por filas ...
        for r in range(len(maze)):
            # ... Y luego por columnas
            for c in range(len(maze[0])):
                # Si la coordenada corresponde al inicio (S) (start)imprimimos 'S'
                if (r,c) == start:
                    print('S', end=' ')
                # Si la coordenada corresponde al final (E) (end)imprimimos 'E'
                elif (r,c) == end:
                    print('E', end=' ')
                # Si la coordenada corresponde '*' imprimimos un *
                elif display_maze[r][c] == '*':
                    print('*', end=' ')
                # Si no, impimimos el contenido del mapa para esa coordenada.
                else:
                    print(maze[r][c], end=' ')
            print()
        print(f"\nLongitud del camino: {len(path) - 1} pasos")
        val_path=True
    else:
        print("No se encontró un camino.")

# La variabla val_path nos sirve para separar el codigo, si encuentra una ruta entre S y E, junto con imprimir el mapa y la ruta
# nos permite sembrar los objetos (en bloques de 10 objetos) en la misma ruta.
if val_path:
    # Imprimiremos el MAPA con el inicio, el fin, la ruta entre estos 2 puntos y los objetos sembrados, identificados mediante un @ (arroba)
    print("CAMINO PRINCIPAL CON OBJETOS ALEATORIOS '@' (max 10)")
    # Preparamos todo para mostrar el mapa con la ruta.
    # Para no modificar el mapa almacenado en Maze creamos una copia y lo almacenamos en display_maze     
    display_maze = [row[:] for row in maze]
    # Recorremos la ruta path
    for r, c in path:
        # En donde la coordenada de path no sea igual al inicio o fin
        if (r, c) != start and (r, c) != end:
            # Se le asigna a display_maze un * en la coordenada de cada elemento de path.
            display_maze[r][c] = '*'
    # Luego marcamos las posiciones de los objetos sembrados con una X, pero podemos marcarlos luego con un @
    for r, c in sembrado:
        if (r, c) != start and (r, c) != end:
            display_maze[r][c] = 'X'
    # Recorremos la matriz por filas ...
    for r in range(len(maze)):
        # ... Y luego por columnas
        for c in range(len(maze[0])):
            # Si la coordenada corresponde al inicio (S) (start)imprimimos 'S'
            if (r,c) == start:
                print('S', end=' ')
            # Si la coordenada corresponde al final (E) (end)imprimimos 'E'
            elif (r,c) == end:
                print('E', end=' ')
            # Si la coordenada corresponde '*' imprimimos un *
            elif display_maze[r][c] == '*':
                print('*', end=' ')
            # Si la coordenada corresponde a un objeto sembrado, lo marcamos con @
            elif display_maze[r][c] == 'X':
                print('@', end=' ')
            # Si no, impimimos el contenido del mapa para esa coordenada.
            else:
                print(maze[r][c], end=' ')
        print()
print("presione enter para continuar")
input()

print("\nA CONTINUACION EL AGENTE RECOGERA OBJETO POR OBJETO HASTA LLENAR SU INVENTARIO")
# Declaramos un contador para manipular la lista de sembrados, independiente del contador de inventario
# Util en caso que el inventario sea superior a 10
cont = 0
for i in range(inventario):
    # Tenemos que controlar el inicio del mapa, no sera parte de un objeto.
    # En la primera iteracion, el inicio sera el Start del mapa y el objeto final sera el primer objeto sembrado
    # La posicion del objeto sera agregada a la lista de objetos.
    if i == 0:
        cont = i
        l_start=start
        l_end = sembrado[cont]
        list_objetos.append(l_end)
        
    # Si el ciclo esta entre la posicion 1 (partiendo en 0) y 9, tiene un comportamiento relativamente normal.
    # El inicio de la ruta del objeto es la posicion anterior (donde quedo el agente), la posicion final corresponde al siguiente elemento del sembrado.
    # La posicion del objeto sera agregada a la lista de objetos.    
    elif i>0 and i<=9:
        cont = i
        l_start = l_end
        l_end = sembrado[cont]
        list_objetos.append(l_end)
    
    # Si llegamos a la decima iteracion (i==9), se nos acabaron los objetos sembrados.
    # volvemos a llamar a la rutina de sembrado y reescribimos la lista 'sembrado' estas 10 nuevas ubicaciones.
    elif(i==10):
        # Si llegamos a las 10 iteraciones i==9 (parte en 0) se nos acabaran los elementos sembrados
        # Tenemos que generar un nuevo sembrado aleatorio de objetos.
        # Volvemos a iniciar en el Start del tablero
        sembrado = sembrar_objetos(path, list_objetos)
        #print("Nuevo Sembrado: ", sembrado)
        cont=i-10
        # Para recorrer estos nuevos elementos sembrados, el inicio local (l_start) le asignamos la coordenada de inicio (start)
        l_start = start
        l_end = sembrado[cont]
        list_objetos.append(l_end)

    elif(i>10):
        # Si llegamos a las 10 iteraciones i==9 (parte en 0) se nos acabaran los elementos sembrados
        # Tenemos que generar un nuevo sembrado aleatorio de objetos.
        # Volvemos a iniciar en el Start del tablero
        cont=i-10
        l_start = l_end
        l_end = sembrado[cont]
        list_objetos.append(l_end)

    # Bloque que muestra una guia del proceso que se lleva a cabo durante el recorrido del agente por el laberinto
    print("\nIteracion ",i+1," de ",inventario,"- Inicio(A)",l_start,":: Fin(B)",l_end)
    print("Capacidad del Inventario: ",inventario,"\nObjetos recogidos: ",(i+1),"- Espacio en inventario: ",inventario-(i+1),"\n")

    # Con el Mapa, con el inicio local (l_start) y con el fin local (l_end) llamamos a la funcion para obtener la ruta entre estos 2 puntos.
    # La nueva ruta la almacenamos en path_aux
    path_aux = a_star_append_pop(maze,l_start,l_end)

    # Rutina que se repite para mostrar la matriz y sus componentes.
    display_maze = [row[:] for row in maze]
    # Primero los * para la ruta entre los 2 puntos.
    for r, c in path_aux:
        if (r, c) != l_start and (r, c) != l_end:
            display_maze[r][c] = '*'

    # Luego marcamos las posiciones de los objetos sembrados con una X, pero podemos marcarlos luego con un @
    for r, c in sembrado:
        if (r, c) != l_start and (r, c) != l_end:
            display_maze[r][c] = 'X'
    
    # Recorremos la matriz por filas ...
    for r in range(len(maze)):
        # ... Y luego por columnas
        for c in range(len(maze[0])):
            # Si la coordenada corresponde al inicio, de la ruta del objeto, la marcamos con A
            if (r,c) == l_start:
                print('A', end=' ')
            # Si la coordenada corresponde al final, de la ruta del objeto, la marcamos con B
            elif (r,c) == l_end:
                print('B', end=' ')
            # Si la coordenada corresponde a la ruta entre A y B, la marcamos con *
            elif display_maze[r][c] == '*':
                print('*', end=' ')
            # Si la coordenada corresponde a un objeto sembrado, lo marcamos con @
            elif display_maze[r][c] == 'X':
                print('@', end=' ')
            # Si no, impimimos el contenido del mapa para esa coordenada.
            else:
                print(maze[r][c], end=' ')
        print()
    print("Presiona Enter para continuar")
    input()  # presionando Enter continuamos con el siguiente camino entre el objeto actual y el siguiente.

# Mostramos a modo de resumen la informacion de los objetos 'recogidos' por el agente
print("\nObjetos en inventario: ", len(list_objetos))   # La Cantidad de Objetos
print("Lista de Objetos Recogidos")                     # Una lista con los Objetos.
for row in (list_objetos):
    print(row)
print("\nFIN DEL PROGRAMA")