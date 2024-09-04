import re
import tkinter as tk
from tkinter import simpledialog, messagebox
import time

class Procesos:  #clase de procesos o nodos
  #atributos
  def __init__(self, Id, nombre, operacion, tme):  
    self.Id = Id
    self.nombre = nombre
    self.operacion = operacion
    self.tme = tme
    self.next = None  # Inicializar el apuntador al siguiente nodo como None

  #métodos
  @staticmethod
  def getId():
    while True:
      try:
        Id = int(input('\nIngrese el número de proceso -> '))
        if Id>0:
          return Id
        else:
          print('\nDebe de ingresar un número entero positivo')
      except ValueError:
        print('\nEntrada no valida. Por favor ingrese un número entero valido ')

  @staticmethod
  def getNombre():
    while True:
      nombre = input("\nIngrese un nombre -> ").strip()
      if nombre:
        return nombre
      else:
        print('\nEl nombre no puede estar vacío, inténtalo de nuevo.')

  @staticmethod
  def getOperacion():  
   # Definir una función para validar la operación
    def es_operacion_valida(operacion):
      # Permitir solo números, operadores matemáticos, espacios y paréntesis
      patron = r'^[0-9+\-*/%(). ]+$'
      return re.match(patron, operacion) is not None

    while True:
      operacion = input("\nEscribe una operación matemática: ").strip()
      if es_operacion_valida(operacion):
        return operacion
      else:
        print("\nOperación inválida. Solo se permiten números y operadores matemáticos.")
        
  @staticmethod
  def getTME():
    while True:
      try:
        tme = int(input('\nIngrese el tiempo de ejecución del proceso -> '))
        if tme>0:
          return tme
        else:
          print('\nDebe de ingresar un número entero positivo')
      except ValueError:
        print('\nEntrada no valida. Por favor ingrese un número entero valido ')


class LL:  #clase de estructura de datos Linked list
  def __init__(self):  #apuntadores
    self.head = None
    self.tail = None

  #métodos
  def agregarTail(self, Id, nombre, operacion, tme):  #agregar al final
    nuevoProceso = Procesos(Id, nombre, operacion, tme)
    if self.tail is None:
      self.head = nuevoProceso
      self.tail = nuevoProceso
    else:
      self.tail.next = nuevoProceso
      self.tail = nuevoProceso

  def borrarHead(self):  #borrar el primero
    if self.head is None:
      return None
    temp = self.head
    self.head = temp.next
    if self.head is None:
      self.tail = None
    return temp

  def peekFront(self):  #ver el primero
    return self.head

  def contar(self):  #contar los números de procesos
    temp = self.head
    i = 0
    while temp != None:
      temp = temp.next
      i += 1
    return i
  
  def mostrarLista(self):  #mostrar los procesos
    temp = self.head
    while temp != None:
      print(f'\nNúmero de proceso: {temp.Id}')
      print(f"Nombre del proceso: {temp.nombre}")
      print(f"Resultado: {eval(temp.operacion)}")
      print(f"Tiempo de ejecución: {temp.tme}")
      temp = temp.next

  def mostrarProceso(self, proceso):  #mostrar un proceso
    print(f'Número de proceso: {proceso.Id}')
    print(f"Nombre del proceso: {proceso.nombre}")
    print(f"Resultado: {eval(proceso.operacion)}")
    print(f"Tiempo de ejecución: {proceso.tme}")

  def buscar(self,Id):
    temp = self.head
    while temp != None:
      if temp.Id == Id:
        return self.mostrarProceso(temp)
      temp = temp.next
    return None
  
class Ventana:
  def __init__(self, ventana): 
    self.ventana = ventana
    self.ventana.geometry("1000x800")
    self.ventana.title("Procesamiento por lotes")
    self.titulo = tk.Label(ventana, text="Procesamiento por lotes", bg="lightblue", font=("Arial", 20))
    self.titulo.pack(fill=tk.X)

    self.procesos_enespera = LL() # Crear una lista enlazada para almacenar los procesos en espera

    # Ventana inicial para ingresar el número de procesos
    self.label_procesos = tk.Label(ventana, text="Número de Procesos:", font=("Arial", 14), height=2)
    self.label_procesos.pack()
    self.entry_procesos = tk.Entry(ventana)
    self.entry_procesos.pack()
    # Botón para generar formularios
    self.btn_crear_formularios = tk.Button(ventana, text="Crear formularios", font=("Arial", 10), command=self.crear_formularios, padx=10, pady=5)
    self.btn_crear_formularios.pack()    

    # Frame para los formularios
    self.frame_formularios = tk.Frame(ventana)
    self.frame_formularios.pack(pady=10)

  def crear_formularios(self):
    # Limpiar los elementos previos
    for widget in self.ventana.winfo_children():
      widget.destroy()

    # Mostrar el título
    titulo = tk.Label(self.ventana, text="Procesamiento por lotes", bg="lightblue", font=("Arial", 20))
    titulo.pack(fill=tk.X)
    
    try:
      num_procesos = int(self.entry_procesos.get())
      if num_procesos <= 0:
        raise ValueError
    except ValueError:
      messagebox.showerror("Error", "Por favor ingrese un número entero positivo.")
      return




     # Botón para agregar procesos
    self.btn_agregar_procesos = tk.Button(self.ventana, text="Agregar Procesos", command=self.mostrarprocesos)

    # Crear los formularios para cada proceso
    self.formularios = []
    for i in range(num_procesos):
      frame = tk.Frame(self.frame_formularios)
      frame.pack(pady=5)

      label_id = tk.Label(frame, text=f"Proceso {i + 1} - ID:")
      label_id.grid(row=0, column=0)
      entry_id = tk.Entry(frame)
      entry_id.grid(row=0, column=1)

      label_nombre = tk.Label(frame, text="Nombre:")
      label_nombre.grid(row=1, column=0)
      entry_nombre = tk.Entry(frame)
      entry_nombre.grid(row=1, column=1)

      label_operacion = tk.Label(frame, text="Operación:")
      label_operacion.grid(row=2, column=0)
      entry_operacion = tk.Entry(frame)
      entry_operacion.grid(row=2, column=1)

      label_tme = tk.Label(frame, text="Tiempo Ejecución:")
      label_tme.grid(row=3, column=0)
      entry_tme = tk.Entry(frame)
      entry_tme.grid(row=3, column=1)

      self.formularios.append({
        "id": entry_id,
        "nombre": entry_nombre,
        "operacion": entry_operacion,
        "tme": entry_tme
      })
    
      self.btn_agregar_procesos.pack()

  def mostrarprocesos(self):
    # Limpiar los elementos previos
    for widget in self.ventana.winfo_children():
      widget.destroy()

    # mostrar lotes en la terminal
    self.procesos_enespera.mostrarLista()
  
    #mostrar lotes pendientes
    self.label_lotes_pendientes = tk.Label(self.ventana, text=f'Lotes pendientes: {self.lotes_pendientes}', font=("Arial", 14), height=2)
    self.label_lotes_pendientes.grid(row=0, column=0)

    # mostrar contenedor de procesos en espera
    self.frame_procesos_enespera = tk.Frame(self.ventana, bg="FFDDDD", width=200, height=200)
    self.frame_procesos_enespera.grid(row=1, column=0)

    # mostrar contenedor de procesos en ejecución
    self.frame_procesos_enejecucion = tk.Frame(self.ventana, bg="lightyellow", width=200, height=200)
    self.frame_procesos_enejecucion.grid(row=1, column=1)

    # mostrar contenedor de procesos terminados
    self.frame_procesos_terminados = tk.Frame(self.ventana, bg="DDFFDD", width=200, height=200)
    self.frame_procesos_terminados.grid(row=1, column=2)


def main():
  ventana = tk.Tk()
  app = Ventana(ventana)
  ventana.mainloop()

if __name__ == "__main__":
  main()



# def main():
#   lista_procesos = LL()

#   # Crear una instancia de la clase Proceso
#   def nprocesos():
#     while True:
#       try:
#         n = int(input('\nIngrese el número de procesos -> '))
#         if n > 0:
#           return n
#         else:
#           print('\nDebe ingresar un número entero positivo')
#       except ValueError:
#         print('\nEntrada no válida. Por favor ingrese un número entero válido.')
  
#   for _ in range(nprocesos()):
#     lista_procesos.agregarTail(Procesos.getId(), Procesos.getNombre(), Procesos.getOperacion(), Procesos.getTME())

#   ventana = tk.Tk()
#   lista_procesos.mostrarLista()
#   if lista_procesos.contar() % 5 == 0:
#     pass

#   app = Ventana(ventana, lotes_pendientes=2)
#   ventana.mainloop()


# if __name__ == "__main__":
#   main()

  