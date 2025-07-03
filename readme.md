# 🔎 simulador de camino usando bfs en consola

este proyecto es un buscador visual de caminos cortos en un mapa tipo grilla usando el algoritmo **bfs (búsqueda en anchura)**. se ejecuta todo en consola, con animaciones hechas con emojis para que se entienda bien lo que pasa.

## 🧠 cómo funciona

el programa genera un mapa vacío, donde podés:
- elegir el punto de inicio 🚩
- elegir el punto de destino 📍
- agregar obstáculos como:
  - 🏢 edificios: bloquean el paso
  - 💧 agua: también bloquea el paso (en esta versión)
  - 🧱 muros temporales: desaparecen durante la animación

una vez que se arma el mapa, el programa usa **bfs** para buscar el camino más corto desde el inicio hasta el destino, evitando todos los obstáculos. si encuentra un camino, lo muestra paso a paso animado ✨. si no hay camino posible, te avisa.

## ⚙️ tecnologías usadas

- python 3
- `collections.deque` para la cola del bfs
- `os` para limpiar la consola entre pasos
- `time` para animaciones con pausas

## 🗺️ símbolos usados en el mapa

| emoji | significado           |
|-------|------------------------|
| ⬜     | camino libre           |
| 🏢     | obstáculo (edificio)   |
| 💧     | agua (obstáculo)       |
| 🧱     | muro temporal          |
| 🚩     | punto de inicio        |
| 📍     | punto de destino       |
| ✨     | camino encontrado      |

## 📌 pasos para usarlo

1. ejecutá el programa
2. ingresá el tamaño del mapa (filas y columnas)
3. indicá las coordenadas de inicio y destino
4. agregá obstáculos (te deja elegir tipo y posición)
5. presioná ENTER para que empiece la búsqueda
6. si hay camino, vas a ver la animación del recorrido con efectos

## 💡 posibles mejoras

- permitir que el agua sea transitable pero más costosa (y ahí usar a*)
- agregar diagonales como movimientos válidos
- modo visual con interfaz (tkinter o pygame)
- guardar el mapa en archivo