# Practica 2: Simulación de Procesamiento por Lotes

Este programa simula el procesamiento por lotes utilizando una lista enlazada para manejar los procesos y una interfaz gráfica para mostrar el estado de los procesos en espera, en ejecución y terminados.

## Descripción

El programa genera procesos con operaciones y tiempos máximos estimados (TME) aleatorios. Los procesos se agrupan en lotes de 5 y se procesan secuencialmente. La interfaz gráfica muestra el estado de los procesos en tres categorías: en espera, en ejecución y terminados. Además, permite pausar, continuar, interrumpir y manejar errores en los procesos mediante atajos de teclado.

## Estructura del Código

- `Procesos`: Clase que representa un proceso con atributos `Id`, `operacion` y `tme`.
- `LL`: Clase que representa una lista enlazada para manejar los procesos.
- `Ventana`: Clase que maneja la interfaz gráfica utilizando `tkinter`.
- `main()`: Función principal que inicializa las listas de procesos, genera los procesos y lanza la interfaz gráfica.

## Uso

1. Ejecuta el programa.
2. Ingresa el número de procesos que deseas generar.
3. Observa cómo se procesan los lotes y se actualiza la interfaz gráfica.
4. Usa los siguientes atajos de teclado para interactuar con los procesos:
   - `Espacio`: Iniciar el procesamiento.
   - `E`: Interrumpir el proceso actual.
   - `W`: Marcar el proceso actual como error.
   - `P`: Pausar el procesamiento.
   - `C`: Continuar el procesamiento.
   - `Enter`: Cerrar el programa.

## Requisitos

- Python 3.x
- Bibliotecas: `random`, `tkinter`, `keyboard`, `time`

## Ejecución

Para ejecutar el programa, sigue estos pasos:

1. Abre una terminal.

2. Navega al directorio donde se encuentra el archivo `practica2.py`:
   ```sh
   cd path/to/your/directory

3. Ejecuta el programa con el siguiente comando:
    ```sh
    python practica2.py
