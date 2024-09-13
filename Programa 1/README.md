# Programa 1: Simulación de Procesamiento por Lotes

Este programa simula el procesamiento por lotes utilizando una lista enlazada para manejar los procesos y una interfaz gráfica para mostrar el estado de los procesos en espera, en ejecución y terminados.

## Descripción

El programa genera procesos con operaciones y tiempos máximos estimados (TME) proporcionados por el usuario. Los procesos se agrupan en lotes de 4 y se procesan secuencialmente. La interfaz gráfica muestra el estado de los procesos en tres categorías: en espera, en ejecución y terminados.

## Estructura del Código

- `Procesos`: Clase que representa un proceso con atributos `Id`, `nombre`, `operacion` y `tme`.
- `LL`: Clase que representa una lista enlazada para manejar los procesos.
- `Ventana`: Clase que maneja la interfaz gráfica utilizando `tkinter`.
- `main()`: Función principal que inicializa las listas de procesos, genera los procesos y lanza la interfaz gráfica.

## Uso

1. Ejecuta el programa.
2. Ingresa el número de procesos que deseas generar.
3. Ingresa los detalles de cada proceso (Id, nombre, operación y tiempo de ejecución).
4. Observa cómo se procesan los lotes y se actualiza la interfaz gráfica.

## Requisitos

- Python 3.x
- Bibliotecas: `re`, `tkinter`

## Ejecución

Para ejecutar el programa, sigue estos pasos:

1. Abre una terminal.
2. Navega al directorio donde se encuentra el archivo `practica1.py`:
   ```sh
   cd path/to/your/directory
3. Ejecuta el programa con el siguiente comando
   ```sh
   python main.py

