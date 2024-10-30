import re

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
      nombre = str(input("\nIngrese un nombre -> ").strip())
      if nombre:
        return nombre
      else:
        print('\nEl nombre no puede estar vacío, inténtalo de nuevo.')

  @staticmethod
  def getOperacion():
    # Definir una función para validar la operación
    def es_operacion_valida(operacion):
      # Permitir solo números, operadores matemáticos (+, -, *, /, %, ()), y espacios
      patron = r'^[0-9+\-*/%(). ]+$'
      return re.match(patron, operacion) is not None
    
    while True:
      operacion = input("\nEscribe una operación matemática: ").strip()

      # Verificar si la operación contiene solo caracteres válidos
      if not es_operacion_valida(operacion):
        print("\nOperación inválida. Solo se permiten números y operadores matemáticos.")
        continue  # Volver a pedir la operación

      # Intentar evaluar la operación
      try:
        resultado = eval(operacion)
        return operacion  # Si es válida, devolver la operación
      except ZeroDivisionError:
        print("Error: No se puede dividir entre 0. Inténtalo de nuevo.")
      except Exception as e:
        print(f"Error en la operación: {str(e)}. Inténtalo de nuevo.")
              
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
