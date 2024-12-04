# Practica 5: Algoritmo de planificación Round-Robin

Este programa simula el procesamiento por lotes utilizando el algoritmo de planificación Round-Robin. Utiliza una lista enlazada para manejar los procesos y una interfaz gráfica para mostrar el estado de los procesos en diferentes estados: nuevo, listos, en ejecución, bloqueado y terminado.

## Descripción

El programa genera procesos con operaciones y tiempos máximos estimados (TME) aleatorios. Los procesos se agrupan en lotes y se procesan secuencialmente según el algoritmo Round-Robin con un quantum definido por el usuario. La interfaz gráfica muestra el estado de los procesos en cinco categorías: nuevo, listos, en ejecución, bloqueado y terminado. Además, permite pausar, continuar, interrumpir y manejar errores en los procesos mediante atajos de teclado.

## Estructura del Código

- [`ProcesosClass.py`](/Programa5/ProcesosClass.py): Clase que representa un proceso con atributos `Id`, `operacion`, `tme`, `tiemporestante`, `tiemposervicio`, `tiempollegada`, `tiemporetorno` y `tiempoespera`.
- [`LLClass.py`](/Programa5/LLClass.py): Clase que representa una lista enlazada para manejar los procesos.
- [`VentanaClass.py`](/Programa5/VentanaClass.py): Clase que maneja la interfaz gráfica utilizando `tkinter`.
- [`mainP5.py`](/Programa5/MainP5.py): Función principal que inicializa las listas de procesos, genera los procesos y lanza la interfaz gráfica.

## Uso

1. Ejecuta el programa.
2. Ingresa el número de procesos que deseas generar.
3. Ingresa el quantum para el algoritmo Round-Robin.
4. Observa cómo se procesan los lotes y se actualiza la interfaz gráfica.
5. Usa los siguientes atajos de teclado para interactuar con los procesos:
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
2. Navega al directorio donde se encuentra el archivo `mainP5.py`:
   ```sh
   cd path/to/your/directory
   ```
3. Ejecuta el programa con el siguiente comando:
    ```sh
    python mainP5.py
    ```

## Estados de procesamiento
1. Nuevo: Procesos que se acaban de crear, pero aún no han sido admitidos por el sistema operativo en el grupo de procesos ejecutables.
2. Listos: Procesos que están preparados para ejecutarse, en cuanto sea su turno.
3. Ejecución: Proceso que está actualmente en ejecución.
4. Bloqueado: Proceso que no puede ejecutar hasta que se produzca cierto suceso, como la terminación de una operación de E/S.
5. Terminado: Un proceso que ha sido excluido por el sistema operativo del grupo de procesos activos, bien porque se detuvo o porque fue abandonado por alguna razón.