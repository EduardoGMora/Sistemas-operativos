import ProcesosClass as pc

class LL:  #clase de estructura de datos Linked list
  def __init__(self):  #apuntadores
    self.head = None
    self.tail = None

  #métodos
  def agregarTail(self, Id, operacion, tme, tiemporestante, tiempoTranscurrido = 0, tiempollegada = 0, tiemporetorno = 0, tiempoespera = 0):  #agregar al final
    nuevoProceso = pc.Procesos(Id, operacion, tme, tiemporestante, tiempoTranscurrido, tiempollegada, tiemporetorno, tiempoespera)
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
    while temp is not None:
      temp = temp.next
      i += 1
    return i
  
  def mostrarLista(self):  #mostrar la lista de procesos
    temp = self.head
    while temp is not None:
      print(f'\nNúmero de proceso: {temp.Id}')
      print(f"Resultado: {temp.operacion}")
      print(f"Tiempo de Máximo de Ejecución: {temp.tme}")
      print(f"Tiempo Restante: {temp.tiemporestante}")
      print(f"Tiempo Transcurrido: {temp.tiempoTranscurrido}")
      temp = temp.next

  def mostrarProceso(self, proceso):  #mostrar un proceso
    print(f'Número de proceso: {proceso.Id}')
    print(f"Resultado: {proceso.operacion}")
    print(f"Tiempo de Máximo de Ejecución: {proceso.tme}")
    print(f"Tiempo Restante: {proceso.tiemporestante}")
    print(f"Tiempo Transcurrido: {proceso.tiempoTranscurrido}")

  def buscar(self,Id):
    temp = self.head
    while temp is not None:
      if temp.Id == Id:
        return self.mostrarProceso(temp)
      temp = temp.next
    return None