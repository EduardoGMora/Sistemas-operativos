import os
import sys
import time
import threading
import random
import tkinter as tk

class Procesos:  #clase de procesos o nodos
    #atributos
    def __init__(self, n, nombre, operacion, tme):  
        self.n = n
        self.nombre = nombre
        self.operacion = operacion
        self.tme = tme
        self.resultado = eval(operacion)
        self.next = None

    @staticmethod
    def getNombre():
        nombre = str(input("Ingrese el nombre del proceso -> "))
        return nombre

    @staticmethod
    def getOperacion():  #métodos
        operadores = ['+', '-', '*', '/']
        num1 = random.randint(0, 9)
        num2 = random.randint(0, 9)

        operador = random.choice(operadores)

        if num2 == 0 and operador == '/':
            num2 = random.randint(1, 9)

        operacion = f"{num1} {operador} {num2}"

        return operacion
    
    @staticmethod
    def getTME():
        tme = int(input('Ingrese el tiempo de ejecución del proceso -> '))
        return tme



class LL:  #clase de estructura de datos Linked list

    def __init__(self):  #apuntadores
        self.head = None
        self.tail = None

    #métodos
    def agregartail(self, n, nombre, operacion, tme):  #agregar al final
        nuevoProceso = Procesos(n, nombre, operacion, tme)
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
    self.pendientes = tk.Label(
        ventana, text=f"Número de Lotes pendientes: {self.lotesp}")
    self.pendientes.grid(row=3, column=0, pady=10)

    #label
    etiqueta = tk.Label(ventana, text="Número de Procesos:", font="arial 12")
    etiqueta.grid(row=0, column=0, pady=10)
    estado1 = tk.Label(ventana, text="EN ESPERA", font="arial 12")
    estado1.grid(row=1, column=0, pady=10)
    estado2 = tk.Label(ventana, text="EJECUCIÓN", font="arial 12")
    estado2.grid(row=1, column=2, pady=10)
    estado3 = tk.Label(ventana, text="TERMINADOS", font="arial 12")
    estado3.grid(row=1, column=4, pady=10)

    #text#
    espera = tk.Text(self.ventana,
                     width=30,
                     borderwidth=4,
                     bg="#FFDDDD",
                     state=tk.DISABLED)
    espera.grid(row=2, column=0, padx=30)
    ejecucion = tk.Text(self.ventana,
                        width=30,
                        borderwidth=4,
                        bg="lightyellow",
                        state=tk.DISABLED)
    ejecucion.grid(row=2, column=2, padx=10)
    terminado = tk.Text(ventana,
                        width=30,
                        borderwidth=4,
                        bg="#DDFFDD",
                        state=tk.DISABLED)
    terminado.grid(row=2, column=4)

    #botones
    botonProcesos = tk.Button(ventana,
                              text="GENERAR",
                              command=self.generarprocesos)
    botonProcesos.grid(row=0, column=2)

    self.Listaligada = LL()  #objeto de la lista
    self.listaterminados = LL()

    botonResultado = tk.Button(ventana,
                               text="OBTENER RESULTADOS",
                               command=self.listaterminados.guardarresultados)
    botonResultado.grid(row=3, column=4, pady=10)

  def actualizarEspera(self):  #actualiza la interfaz de espera
    texto = " "
    procesoejecutado = self.Listaligada.peekfront()
    procesosfaltantes = self.Listaligada.contar() - 2

    if procesoejecutado is not None and procesoejecutado != self.Listaligada.tail:
      procesonext = procesoejecutado.next
      texto += f'{procesonext.n}.- {procesonext.nombre} \n {procesonext.operacion}\n TME: {procesonext.tme}\n\n\n\n Procesos faltantes: {procesosfaltantes}'
    else:
      # Si no hay procesos en espera, muestra un mensaje
      texto = "No hay procesos en espera."

    espera = tk.Text(self.ventana,
                     width=30,
                     borderwidth=4,
                     bg="#FFDDDD",
                     state=tk.DISABLED)
    espera.grid(row=2, column=0, padx=30)
    espera.config(state=tk.NORMAL)
    espera.delete('1.0', tk.END)
    espera.insert(tk.END, texto)
    espera.config(state=tk.DISABLED)
    self.actualizarLotes()

  def actualizarEjecucion(self):  #actualiza la interfaz de ejecución
    texto = " "
    proceso_actual = self.Listaligada.peekfront()

    if proceso_actual is None:
      self.borrarinterfaz()
      return
    if proceso_actual is self.Listaligada.tail:
      self.borrarespera()

    texto = f'{proceso_actual.n}.- {proceso_actual.nombre} \n {proceso_actual.operacion} \n TME: {proceso_actual.tme} \n '
    ejecucion = tk.Text(self.ventana,
                        width=30,
                        borderwidth=4,
                        bg="lightyellow",
                        state=tk.DISABLED)
    ejecucion.grid(row=2, column=2, padx=10)
    ejecucion.config(state=tk.NORMAL)
    ejecucion.delete('1.0', tk.END)
    ejecucion.insert(tk.END, texto)
    ejecucion.config(state=tk.DISABLED)

    proceso_actual.tme -= 1  # Disminuye el TME cada segundo

    if proceso_actual.tme >= 0:
      self.ventana.after(1000, self.actualizarTiempo)

    if proceso_actual.tme == 0:
      resultado = eval(proceso_actual.operacion)
      proceso_actual.resultado = resultado
      self.Listaligada.moverTerminados(self.listaterminados)
      self.actualizarTerminado()

      if proceso_actual.next is not None:
        self.Listaligada.head = proceso_actual.next

      if self.Listaligada.peekfront() is not None:
        self.actualizarEspera()
        self.actualizarEjecucion()

  def actualizarTerminado(self):  #actualiza la interfaz de terminado
    # Limpia la interfaz "TERMINADOS"
    terminado = tk.Text(self.ventana,
                        width=30,
                        borderwidth=4,
                        bg="#DDFFDD",
                        state=tk.DISABLED)
    terminado.grid(row=2, column=4)
    terminado.config(state=tk.NORMAL)
    terminado.delete('1.0', tk.END)

    # Recorre la lista enlazada y agrega los procesos terminados a la interfaz
    proceso_actual = self.listaterminados.peekfront()
    while proceso_actual:
      if proceso_actual.tme == 0:
        texto = f'{proceso_actual.n}.- {proceso_actual.nombre} \n {proceso_actual.operacion} \n Resultado: {proceso_actual.resultado}\n'
        terminado.insert(tk.END, texto)

      proceso_actual = proceso_actual.next

    terminado.config(state=tk.DISABLED)

  def borrarinterfaz(self):  #borrar interfaz

    ejecucion = tk.Text(self.ventana,
                        width=30,
                        borderwidth=4,
                        bg="lightyellow",
                        state=tk.DISABLED)
    ejecucion.grid(row=2, column=2, padx=10)
    ejecucion.config(state=tk.NORMAL)
    ejecucion.delete('1.0', tk.END)
    ejecucion.config(state=tk.DISABLED)

  def borrarespera(self):  #borra la interfaz de espera
    texto = "No hay procesos en espera."
    espera = tk.Text(self.ventana,
                     width=30,
                     borderwidth=4,
                     bg="#FFDDDD",
                     state=tk.DISABLED)
    espera.grid(row=2, column=0, padx=30)
    espera.config(state=tk.NORMAL)
    espera.delete('1.0', tk.END)
    espera.insert(tk.END, texto)
    espera.config(state=tk.DISABLED)

  def actualizarTiempo(self):  # cambia el tiempo de espera y el reloj global
    self.tiempo += 1
    self.relojglobal.config(text=f"Reloj Global: {self.tiempo}")
    self.actualizarEjecucion()

  def actualizarLotes(self):
    num_procesos = self.Listaligada.contar()
    lotes_pendientes = num_procesos // 5  # Cada 5 procesos forman un lote
    if num_procesos % 5 != 0:
      lotes_pendientes += 1  # Si hay procesos adicionales que no forman un lote completo, suma 1
    self.pendientes.config(text=f'Lotes pendientes: {lotes_pendientes - 1}')


def main():
  ventana = tk.Tk()
  app = Ventana(ventana)
  ventana.mainloop()

if __name__ == "__main__":
    main()