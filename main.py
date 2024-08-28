import re
import tkinter as tk
from tkinter import messagebox

class Proceso:  #clase de procesos o nodos
  #atributos
  def __init__(self, Id, nombre, operacion, tme):  
    self.Id = Id
    self.nombre = nombre
    self.operacion = operacion
    self.tme = tme

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
    nuevoProceso = Proceso(Id, nombre, operacion, tme)
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
        print(f'Número de proceso: {temp.Id}')
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

class Ventana():  #clase ventana
  #atributos para la clase ventana
  def __init__(self, ventana):
    self.ventana = ventana
    self.ventana.geometry("600x600")
    self.ventana.title("Procesamiento por lotes")
    self.ventana.configure(bg="gray")

    Titulo = tk.Label(ventana, text="Procesamiento por lotes", font=("Arial", 20), bg="green", fg="white")
    Titulo.pack(fill= tk.X)

  # métodos para la clase ventana
  def print():
    pass



def main():
  # Crear una instancia de la clase Proceso
  def nprocesos():
    while True:
      try:
        n = int(input('\nIngrese el número de procesos -> '))
        if n > 0:
          return n
        else:
          print('\nDebe ingresar un número entero positivo')
      except ValueError:
        print('\nEntrada no válida. Por favor ingrese un número entero válido.')
  
  # for _ in range(nprocesos):
  #   proceso = Proceso(
  #     Proceso.getid(),
  #     Proceso.getNombre(),
  #     Proceso.getOperacion(),
  #     Proceso.getTME()
  #   )
  #   procesos = []
  #   procesos.append(proceso)

  ventana = tk.Tk()
  app = Ventana(ventana)
  ventana.mainloop()


if __name__ == "__main__":
  main()