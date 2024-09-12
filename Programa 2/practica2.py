import re
import random
import tkinter as tk

class Procesos:  #clase de procesos o nodos
  #atributos
  def __init__(self, Id, operacion, tme):  
    self.Id = Id
    self.operacion = operacion
    self.tme = tme
    self.next = None  # Inicializar el apuntador al siguiente nodo como None

  @staticmethod
  def getOperacion():
    operadores = ['+', '-', '*', '/', '%']  # Lista de operadores matemáticos
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)

    operador = random.choice(operadores)

    if num2 == 0 and operador == '/' or operador == '%':
      num2 = random.randint(1, 9)

    operacion = f"{num1} {operador} {num2}"

    return operacion
              
  @staticmethod
  def getTME():
    tme = random.randint(5, 18) # Tiempo de ejecución aleatorio entre 5 y 18 segundos
    return tme

class LL:  #clase de estructura de datos Linked list
  def __init__(self):  #apuntadores
    self.head = None
    self.tail = None

  #métodos
  def agregarTail(self, Id, operacion, tme):  #agregar al final
    nuevoProceso = Procesos(Id, operacion, tme)
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
  
  def mostrarLista(self):  #mostrar los procesos
    temp = self.head
    while temp is not None:
      print(f'\nNúmero de proceso: {temp.Id}')
      print(f"Resultado: {eval(temp.operacion)}")
      print(f"Tiempo de ejecución: {temp.tme}")
      temp = temp.next

  def mostrarProceso(self, proceso):  #mostrar un proceso
    print(f'Número de proceso: {proceso.Id}')
    print(f"Resultado: {eval(proceso.operacion)}")
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

class Ventana:
  def __init__(self, ventana, listaEspera, listaTerminados):
    self.ventana = ventana
    self.listaEspera = listaEspera
    self.listaTerminados = listaTerminados
    self.ventana.title("Procesamiento por lotes")
    self.tiempo = 0
    self.relojglobal = tk.Label(ventana, text=f"Reloj Global: {self.tiempo}")
    self.relojglobal.grid(row=0, column=4, padx=150)
    self.procesoactual = None
    self.contador = 0
    self.lotes = self.listaEspera.hacerLotes()
    self.lotesp = len(self.lotes) #lotes pendientes
    self.pendientes = tk.Label(ventana, text=f"Número de Lotes pendientes: { self.lotesp }")
    self.pendientes.grid(row=3, column=0, pady=10)

    #label
    etiqueta = tk.Label(ventana, text=f'Número de procesos: {listaEspera.contar()}', font="arial 12")
    etiqueta.grid(row=0, column=0, pady=10)
    estado1 = tk.Label(ventana, text="EN ESPERA", font="arial 12")
    estado1.grid(row=1, column=0, pady=10)
    estado2 = tk.Label(ventana, text="EJECUCIÓN", font="arial 12")
    estado2.grid(row=1, column=2, pady=10)
    estado3 = tk.Label(ventana, text="TERMINADOS", font="arial 12")
    estado3.grid(row=1, column=4, pady=10)

    #procesos en espera
    self.espera = tk.Text(ventana, width=30, borderwidth=4, bg="#FFDDDD", state=tk.DISABLED)
    self.espera.grid(row=2, column=0, padx=30)
    #procesos en ejecución
    self.ejecucion = tk.Text(ventana, width=30, borderwidth=4, bg="lightyellow", state=tk.DISABLED)
    self.ejecucion.grid(row=2, column=2, padx=30)
    #procesos terminados
    self.terminado = tk.Text(ventana, width=30, borderwidth=4, bg="#DDFFDD", state=tk.DISABLED)
    self.terminado.grid(row=2, column=4)

    #botón de inicio
    boton = tk.Button(ventana, text="Iniciar", command=self.iniciar)
    boton.grid(row=3, column=2, pady=10)


  def actualizarEspera(self):  #actualiza la interfaz de espera
    texto = ""

    # Verificar si aún hay lotes disponibles
    if self.contador < len(self.lotes):
      lote_actual = self.lotes[self.contador]  

        # Verificar si el lote actual tiene procesos
      if len(lote_actual) > 0:
        proceso = lote_actual.pop(0)
        # Mostrar el proceso en la interfaz
        for proceso in lote_actual:
          texto += f'{proceso.Id}.- {proceso.operacion}\n TME: {proceso.tme}\n\n'

          # Mostrar cuántos procesos faltan en el lote actual
        texto += f'\nProcesos faltantes del lote: {len(lote_actual)}'
      else:
        # Si el lote actual está vacío, avanzar al siguiente lote
        self.contador += 1
        self.actualizarEspera()  # Llamar recursivamente para actualizar el siguiente lote
        self.actualizarLotes()
        return
    else:
      # Si no quedan más lotes, mostrar que no hay más procesos
      texto = "No hay más procesos en espera."

    # Actualizar la caja de texto para mostrar los procesos en espera
    self.espera.config(state=tk.NORMAL)
    self.espera.delete('1.0', tk.END)
    self.espera.insert(tk.END, texto)
    self.espera.config(state=tk.DISABLED)

  def actualizarEjecucion(self): #actualiza la interfaz de ejecución
    if self.procesoactual is not None:
      self.procesoactual.tme -= 1  
      texto = f'{self.procesoactual.Id}.- {self.procesoactual.operacion}\n TME: {self.procesoactual.tme}'
      
      self.ejecucion.config(state=tk.NORMAL)  
      self.ejecucion.delete('1.0', tk.END)  
      self.ejecucion.insert(tk.END, texto)  
      self.ejecucion.config(state=tk.DISABLED)  

      # Actualizar el reloj global
      self.tiempo += 1
      self.relojglobal.config(text=f"Reloj Global: {self.tiempo}")
      
      # Si el TME llega a 0, pasar al siguiente proceso
      if self.procesoactual.tme == 0:
        self.listaTerminados.agregarTail(self.procesoactual.Id, self.procesoactual.operacion, self.procesoactual.tme)
        self.actualizarTerminados()
        self.listaEspera.borrarHead()
        self.procesoactual = self.listaEspera.peekFront()
        self.actualizarEspera()

      # Continuar actualizando cada segundo
      self.ventana.after(1000, self.actualizarEjecucion)  # Se ejecutará de nuevo en 1 segundo

    else:
      self.listaTerminados.mostrarLista()
      texto = "\nNo hay procesos en ejecución."
      self.ejecucion.config(state=tk.NORMAL)
      self.ejecucion.delete('1.0', tk.END)
      self.ejecucion.insert(tk.END, texto)
      self.ejecucion.config(state=tk.DISABLED)

  def actualizarTerminados(self):  #actualiza la interfaz de terminados
    texto = ""
    temp = self.listaTerminados.head
    while temp is not None:
      texto += f'{temp.Id}.- Resultado de la operación: {eval(temp.operacion)}\n\n\n'
      temp = temp.next
    
    self.terminado.config(state=tk.NORMAL)  
    self.terminado.delete('1.0', tk.END)  
    self.terminado.insert(tk.END, texto)  
    self.terminado.config(state=tk.DISABLED)  
  
  def iniciar(self):
    self.lote_actual = 0
    self.procesoactual = self.listaEspera.peekFront()
    self.actualizarLotes()
    self.actualizarEspera()
    self.actualizarEjecucion()

  def actualizarLotes(self):
    self.lotesp -= 1
    self.pendientes.config(text=f"Número de Lotes pendientes: {self.lotesp}") #lotes pendientes


def main():
  listaEspera = LL()  #Lista de procesos en espera
  listaTerminados = LL()  #Lista de procesos terminados

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
  
  #hacer autocremental el Id
  Id = 0
  for _ in range(nprocesos()):
    Id += 1
    listaEspera.agregarTail(Id, Procesos.getOperacion(), Procesos.getTME())

  ventana = tk.Tk()
  app = Ventana(ventana, listaEspera, listaTerminados)
  ventana.mainloop()

if __name__ == "__main__":
  main()
