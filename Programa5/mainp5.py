# Autor: Eduardo Mora
import tkinter as tk
import ProcesosClass as pc
import LLClass as ll
import VentanaClass as vc

def main():
  listaNuevos = ll.LL()  #Lista de procesos nuevos
  listaEspera = ll.LL()  #Lista de procesos en espera
  listaEjecucion = ll.LL()  #Lista de procesos en ejecución
  listaBloqueados = ll.LL()  #Lista de procesos bloqueados
  listaTerminados = ll.LL()  #Lista de procesos terminados

  # Crear una instancia de la clase Proceso
  def nprocesos():
     while True:
      try:
        n = int(input('\nIngrese el número de procesos -> '))
        if n > 0:
          return n
        print('\nDebe ingresar un número entero positivo')
      except ValueError:
        print('\nEntrada no válida. Por favor ingrese un número entero válido.')
  
  #hacer autocremental el Id
  Id = 0
  for _ in range(nprocesos()):
    Id += 1
    listaNuevos.agregarTail(Id, pc.Procesos.getOperacion(), pc.Procesos.getTME(), 0)
  
  def obtener_quantum():
    while True:
      try:
        quantum = int(input('\nIngrese el quantum -> '))
        if quantum > 0:
          return quantum
        print('\nDebe ingresar un número entero positivo')
      except ValueError:
        print('\nEntrada no válida. Por favor ingrese un número entero válido.')
  quantum = obtener_quantum()

  ventana = tk.Tk()
  app = vc.Ventana(ventana, listaNuevos, listaEspera, listaEjecucion, listaBloqueados, listaTerminados, quantum)
  ventana.mainloop()

if __name__ == "__main__":
  main()
