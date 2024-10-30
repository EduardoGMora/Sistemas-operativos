import random

class Procesos:  #clase de procesos o nodos
  #atributos
  def __init__(self, Id, operacion, tme, tiempoTranscurrido):  
    self.Id = Id
    self.operacion = operacion
    self.tme = tme
    self.tiempoTranscurrido = tiempoTranscurrido
    self.next = None  # Inicializar el apuntador al siguiente nodo como None

  @staticmethod
  def getOperacion():
    operadores = ['+', '-', '*', '/', '%']  # Lista de operadores matemáticos
    num1 = random.randint(0, 100)
    num2 = random.randint(0, 100)

    operador = random.choice(operadores)

    if num2 == 0 and operador == '/' or operador == '%':
      num2 = random.randint(1, 100)

    operacion = f"{num1} {operador} {num2}"

    return operacion
              
  @staticmethod
  def getTME():
    tme = random.randint(5, 18) # Tiempo de ejecución aleatorio entre 5 y 18 segundos
    return tme
