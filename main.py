import re
import tkinter as tk

class Proceso:  #clase de procesos o nodos
  #atributos
  def __init__(self, Id, nombre, operacion, tme):  
    self.Id = Id
    self.nombre = nombre
    self.operacion = operacion
    self.tme = tme

  #métodos
  @staticmethod
  def getid():
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
  def agregartail(self, n, nombre, operacion, tme):  #agregar al final
    nuevoProceso = Proceso(n, nombre, operacion, tme)
    if self.tail is None:
        self.head = nuevoProceso
        self.tail = nuevoProceso
    else:
        self.tail.next = nuevoProceso
        self.tail = nuevoProceso

  def borrarhead(self):  #borrar el primero
    if self.head is None:
        return None
    temp = self.head
    self.head = temp.next
    return temp

  def peekfront(self):  #ver el primero
    return self.head

  def contar(self):  #contar los números de procesos
    temp = self.head
    i = 0
    while temp != None:
        temp = temp.next
        i += 1
    return i


class Ventana():  #clase ventana
  #atributos
  def __init__(self, ventana):
    self.ventana = ventana
    self.ventana.geometry("1000x600")
    self.ventana.title("Procesamiento por lotes")
    self.cajaTexto = tk.Entry(ventana, borderwidth=4, width=10)
    self.cajaTexto.grid(row=0, column=1)
    self.tiempo = 0
    self.relojglobal = tk.Label(ventana, text=f"Reloj Global: {self.tiempo}")
    self.relojglobal.grid(row=0, column=4, padx=150)
    self.lotesp = 0
    self.pendientes = tk.Label(ventana, text=f"Número de Lotes pendientes: {self.lotesp}")
    self.pendientes.grid(row=3, column=0, pady=10)

  # métodos
  def print():
     print('hola mundo')

def main():
  # Crear una instancia de la clase Proceso
  proceso1 = Proceso(Proceso.getid(), Proceso.getNombre(), Proceso.getOperacion(), Proceso.getTME())

  # Imprimir los atributos del proceso
  print(f'Número de proceso: {proceso1.Id}')
  print(f"Nombre del proceso: {proceso1.nombre}")
  print(f"Resultado: {eval(proceso1.operacion)}")
  print(f"Tiempo de ejecución: {proceso1.tme}")

if __name__ == "__main__":
  main()