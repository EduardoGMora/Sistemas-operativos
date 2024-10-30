import ProcesosClass as pc

class LL:  #clase de estructura de datos Linked list
  def __init__(self):  #apuntadores
    self.head = None
    self.tail = None

  #métodos
  def agregarTail(self, Id, operacion, tme):  #agregar al final
    nuevoProceso = pc.Procesos(Id, operacion, tme)
    if self.tail is None:
      self.head = nuevoProceso
      self.tail = nuevoProceso
    else:
      self.tail.next = nuevoProceso
      self.tail = nuevoProceso

  # switch del proceso en espera y el último proceso del lote
  def switch(self, tamano_lote):
    if self.head is None or self.head.next is None:
      return
    
    temp = self.head
    self.head = self.head.next
    
    self.insertar(temp.Id, temp.operacion, temp.tme, tamano_lote)

  def insertar(self, Id, operacion, tme, tamano_lote):  #insertar un proceso en una posición específica
    nuevoProceso = Procesos(Id, operacion, tme)
    
    # Caso de lista vacía, insertar al principio
    if self.head is None:
        self.head = nuevoProceso
        return
    
    temp = self.head
    j = 0

    while temp.next is not None and j < tamano_lote - 1:
      temp = temp.next
      j += 1
    
    # Insertar el nuevo proceso al final del lote
    nuevoProceso.next = temp.next
    temp.next = nuevoProceso

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
      print(f"Tiempo de ejecución: {temp.tme}")
      temp = temp.next

  def mostrarProceso(self, proceso):  #mostrar un proceso
    print(f'Número de proceso: {proceso.Id}')
    print(f"Resultado: {proceso.operacion}")
    print(f"Tiempo de ejecución: {proceso.tme}")

  def buscar(self,Id):
    temp = self.head
    while temp is not None:
      if temp.Id == Id:
        return self.mostrarProceso(temp)
      temp = temp.next
    return None
  
  def hacerLotes(self):
    lotes = []
    lote_actual = []
    temp = self.head
    contador = 0
    
    # Iterar sobre la lista y agrupar en lotes de 4
    while temp is not None:
      lote_actual.append(temp)
      contador += 1

      # Si el lote actual tiene 5 procesos, lo agregamos a la lista de lotes
      if contador == 5:
        lotes.append(lote_actual)
        lote_actual = []  # Reiniciar el lote
        contador = 0

      # Pasar al siguiente proceso
      temp = temp.next

    # Agregar el último lote si no está vacío
    if len(lote_actual) > 0:
      lotes.append(lote_actual)

    return lotes  # Retorna la lista de lotes
