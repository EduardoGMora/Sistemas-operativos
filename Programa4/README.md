# Practica 4: Algoritmo de planificación FCFS

Este programa simula el procesamiento por lotes utilizando el algoritmo de planificación First Come First Serve (FCFS). Utiliza una lista enlazada para manejar los procesos y una interfaz gráfica para mostrar el estado de los procesos en diferentes estados: nuevo, listos, en ejecución, bloqueado y terminado.

## Descripción

El programa genera procesos con operaciones y tiempos máximos estimados (TME) aleatorios. Los procesos se agrupan en lotes y se procesan secuencialmente según el algoritmo FCFS. La interfaz gráfica muestra el estado de los procesos en cinco categorías: nuevo, listos, en ejecución, bloqueado y terminado. Además, permite pausar, continuar, interrumpir y manejar errores en los procesos mediante atajos de teclado.

## Estructura del Código

- `Procesos`: Clase que representa un proceso con atributos `Id`, `operacion`, `tme`, `tiempoTranscurrido` y `next`.
- `LL`: Clase que representa una lista enlazada para manejar los procesos.
- `Ventana`: Clase que maneja la interfaz gráfica utilizando `tkinter`.
- `main()`: Función principal que inicializa las listas de procesos, genera los procesos y lanza la interfaz gráfica.

## Uso

1. Ejecuta el programa.
2. Ingresa el número de procesos que deseas generar.
3. Observa cómo se procesan los lotes y se actualiza la interfaz gráfica.
4. Usa los siguientes atajos de teclado para interactuar con los procesos:
   - `Espacio`: Iniciar el procesamiento.
   - `I`: Interrumpir el proceso actual.
   - `E`: Marcar el proceso actual como error.
   - `P`: Pausar el procesamiento.
   - `C`: Continuar el procesamiento.
   - `Enter`: Cerrar el programa.

## Requisitos

- Python 3.x
- Bibliotecas: `random`, `tkinter`, `threading`, `time`

## Ejecución

Para ejecutar el programa, sigue estos pasos:

1. Abre una terminal.
2. Navega al directorio donde se encuentra el archivo `practica4.py`:
   ```sh
   cd path/to/your/directory
   ```
3. Ejecuta el programa con el siguiente comando:
    ```sh
    python practica4.py
    ```

## Estados de Procesamiento
1. Nuevo: Procesos que se acaban de crear, pero aún no han sido admitidos por el sistema operativo en el grupo de procesos ejecutables.
2. Listos: Procesos que están preparados para ejecutarse, en cuanto sea su turno.
3. Ejecución: Proceso que está actualmente en ejecución.
4. Bloqueado: Proceso que no puede ejecutar hasta que se produzca cierto suceso, como la terminación de una operación de E/S.
5. Terminado: Un proceso que ha sido excluido por el sistema operativo del grupo de procesos activos, bien porque se detuvo o porque fue abandonado por alguna razón.