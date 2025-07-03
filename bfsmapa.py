
import time   # para poner pausas y que la animación se vea más linda
import os     # para limpiar la pantalla y que se vea mejor el mapa en la consola
from collections import deque  # para usar una cola eficiente

def crear_mapa(filas, columnas):
    # creo una matriz con filas x columnas llena de ceros
    return [[0 for _ in range(columnas)] for _ in range(filas)]

def pedir_coordenada_valida(mensaje, filas, columnas):
    # esta función pide al usuario que ingrese una fila y columna válidas
    while True:
        fila = int(input(f"{mensaje} - fila: "))
        columna = int(input(f"{mensaje} - columna: "))
        if 0 <= fila < filas and 0 <= columna < columnas:
            return (fila, columna)  # si es válido, devuelvo la coordenada
        else:
            print("Coordenadas fuera del mapa. intenta de nuevo.")

def inicio_destino(mapa):
    
    filas = len(mapa)
    columnas = len(mapa[0])

    print(" Ingresa las coordenadas de inicio y destino:")
    inicio = pedir_coordenada_valida("Inicio", filas, columnas)
    destino = pedir_coordenada_valida("Destino", filas, columnas)

    mapa[inicio[0]][inicio[1]] = 4  # marco la salida con un 4 (🚩)
    mapa[destino[0]][destino[1]] = 5  # marco la meta con un 5 (📍)

    return inicio, destino

def pedir_obstaculos(mapa, inicio, destino):
   
    filas = len(mapa)
    columnas = len(mapa[0])

    print("\nTipos de obstáculos:")
    print("1 - 🏢 Edificio (bloquea el paso)")
    print("2 - 💧 Agua (bloquea el paso)")
    print("3 - 🧱 Muro temporal (desaparece después)")

    cantidad = int(input("cuántos obstáculos querés agregar?: "))
    obstaculos = []

    for i in range(cantidad):
        tipo = int(input(f"\nobstáculo #{i+1} - Tipo (1/2/3): "))

        while True:
            fila = int(input(" Fila del obstáculo: "))
            columna = int(input("Columna del obstáculo: "))
            coord = (fila, columna)

            # valido que la posición esté dentro del mapa, que no esté repetida
            # y que no sea la posición de inicio o destino
            if 0 <= fila < filas and 0 <= columna < columnas:
                if coord not in [(f, c) for f, c, _ in obstaculos] and coord != inicio and coord != destino:
                    obstaculos.append((fila, columna, tipo))
                    break
                else:
                    print("Ya usaste esa coordenada. Intenta otra.")
            else:
                print("Fuera del mapa. Probá de nuevo.")
    return obstaculos

def agregar_obstaculos(mapa, obstaculos):
    # acá marco en el mapa las posiciones y tipos de obstáculos que se eligieron
    for fila, columna, tipo in obstaculos:
        mapa[fila][columna] = tipo

def algoritmo_bfs(mapa, inicio, destino):

    cola = deque()  # creo la cola donde guardo nodos por explorar
    cola.append(inicio)  # empiezo desde el nodo inicial

    padres = {}  # para reconstruir el camino como antes
    visitados = set()  # para no visitar dos veces el mismo lugar
    visitados.add(inicio)

    # guardo las posiciones de los muros temporales (tipo 3) para eliminarlos después
    murallas = {}
    for fila in range(len(mapa)):
        for columna in range(len(mapa[0])):
            if mapa[fila][columna] == 3:
                murallas[(fila, columna)] = True

    while cola:
        actual = cola.popleft()  # saco el primero que entró

        if actual == destino:
            # si llego al final, reconstruyo el camino desde atrás como siempre
            camino = []
            while actual in padres:
                camino.append(actual)
                actual = padres[actual]
            camino.append(inicio)
            camino.reverse()
            return camino, murallas

        # defino los vecinos de actual (arriba, abajo, izquierda, derecha)
        vecinos = [
            (actual[0] - 1, actual[1]),
            (actual[0] + 1, actual[1]),
            (actual[0], actual[1] - 1),
            (actual[0], actual[1] + 1),
        ]

        for vecino in vecinos:
            fila, col = vecino

            # me fijo que el vecino esté dentro del mapa
            if not (0 <= fila < len(mapa) and 0 <= col < len(mapa[0])):
                continue

            valor = mapa[fila][col]

            # si el vecino es edificio (1), agua (2) o muro (3), no puedo pasar
            if valor in [1, 2, 3]:
                continue

            # si ya lo visité antes, lo ignoro
            if vecino in visitados:
                continue

            padres[vecino] = actual  # anoto de dónde vine
            visitados.add(vecino)  # marco como visitado
            cola.append(vecino)  # agrego a la cola para seguir explorando

    # si salí del while sin encontrar, devuelvo camino vacío
    return [], murallas


def mostrar_mapa(mapa):
    
    emojis = {
        0: "⬜",  # camino libre
        1: "🏢",  # edificio
        2: "💧",  # agua
        3: "🧱",  # muro temporal
        4: "🚩",  # inicio
        5: "📍",  # destino
        6: "✨",  # camino encontrado por el algoritmo
    }
    for fila in mapa:
        for celda in fila:
            print(emojis.get(celda, "⬜"), end=" ")
        print()
    print()
    time.sleep(0.4)  # hago una pausa para que se vea la animación

def mostrar_camino_animado(mapa, camino, murallas):
    for i, (fila, col) in enumerate(camino):
        if mapa[fila][col] == 0:
            mapa[fila][col] = 6  # marco el camino en las celdas libres

        # cada 2 pasos elimino un 25% de las murallas que quedan
        if i % 2 == 0 and murallas:
            cantidad = max(1, int(len(murallas) * 0.25))
            for coord in list(murallas.keys())[:cantidad]:
                f, c = coord
                mapa[f][c] = 0  # la muralla desaparece y queda camino libre
                del murallas[coord]

        # limpio pantalla y muestro mapa actualizado para la animación
        os.system("cls" if os.name == "nt" else "clear")
        mostrar_mapa(mapa)

def main():
   
    filas = int(input("ingrese la cantidad de filas: "))
    columnas = int(input("ingrese la cantidad de columnas: "))

    mapa = crear_mapa(filas, columnas)  # creo el mapa vacío

    inicio, destino = inicio_destino(mapa)  # pido y marco inicio y destino

    obstaculos = pedir_obstaculos(mapa, inicio, destino)  # pido obstáculos

    agregar_obstaculos(mapa, obstaculos)  # los agrego al mapa

    mostrar_mapa(mapa)  # muestro el mapa antes de buscar camino

    input("presiona ENTER para comenzar la búsqueda...")  # pausa para que lo vea

    camino, murallas = algoritmo_bfs(mapa, inicio, destino)


    if camino:
        input("presiona ENTER para ver el recorrido final con animación...")
        mostrar_camino_animado(mapa, camino, murallas)  # muestro animado
        print(f"Cantidad de pasos del camino: {len(camino)}")
    else:
        print("No se encontró ningún camino ")

if __name__ == "__main__":
    main()
