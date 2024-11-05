# Autor: Eduardo Mora
import tkinter as tk
from tkinter import ttk
import threading
from time import sleep
import ProcesosClass as pc
import LLClass as ll

class Ventana:
  def __init__(self, ventana, listaEspera, listaEjecucion, listaBloqueados, listaTerminados, quantum):
    self.ventana = ventana          #atributos
    self.ventana.title("Procesamiento por lotes (First Come First Server)")

    # instancia de la clase LL
    self.listaEspera = listaEspera
    self.listaEjecucion = listaEjecucion
    self.listaBloqueados = listaBloqueados
    self.listaTerminados = listaTerminados
    self.quantum = quantum
    self.procesoactual = None       #inicializa el apuntador al proceso en ejecución
    
    # atributos de ayuda
    self.contador = 0
    self.tiempo = 0
    self.pausado = False
    self.pausaText = tk.Label(self.ventana, text="", font="arial 12")
    self.pausaText.grid(row=0, column=6, pady=10)
    self.relojglobal = tk.Label(ventana, text=f"Reloj Global: {self.tiempo}")
    self.relojglobal.grid(row=0, column=8, padx=150)

    #label
    etiqueta = tk.Label(ventana, text=f'Número de procesos: {listaEspera.contar()}', font="arial 12")
    etiqueta.grid(row=0, column=0, pady=10)
    estado1 = tk.Label(ventana, text="NUEVO", font="arial 12")
    estado1.grid(row=1, column=0, pady=10)
    estado2 = tk.Label(ventana, text="LISTOS", font="arial 12")
    estado2.grid(row=1, column=2, pady=10)
    estado3 = tk.Label(ventana, text="EJECUCIÓN", font="arial 12")
    estado3.grid(row=1, column=4, pady=10)
    estado4 = tk.Label(ventana, text="BLOQUEADO", font="arial 12")
    estado4.grid(row=1, column=6, pady=10)
    estado5 = tk.Label(ventana, text="TERMINADO", font="arial 12")
    estado5.grid(row=1, column=8, pady=10)

    #procesos en nuevo
    self.nuevo = tk.Text(ventana, width=30, borderwidth=4, bg="sky blue", state=tk.DISABLED)
    self.nuevo.grid(row=2, column=0, padx=30)
    #procesos en listos
    self.listos = tk.Text(ventana, width=30, borderwidth=4, bg="pale green", state=tk.DISABLED)
    self.listos.grid(row=2, column=2, padx=30)
    #procesos ejecucion
    self.ejecucion = tk.Text(ventana, width=30, borderwidth=4, bg="light goldenrod", state=tk.DISABLED)
    self.ejecucion.grid(row=2, column=4, padx=30)
    #procesos bloqueados
    self.bloqueados = tk.Text(ventana, width=30, borderwidth=4, bg="tomato", state=tk.DISABLED)
    self.bloqueados.grid(row=2, column=6, padx=30)
    #procesos terminados
    self.terminado = tk.Text(ventana, width=30, borderwidth=4, bg="pale violet red", state=tk.DISABLED)
    self.terminado.grid(row=2, column=8, padx=30)

    #botón de inicio
    self.boton = tk.Button(ventana, text="Iniciar", command=self.iniciar)
    self.boton.grid(row=3, column=4, pady=10)
    self.ventana.bind("<Return>", lambda event: self.ventana.quit()) # Enter para salir


  def actualizarNuevos(self):  #actualiza la interfaz de espera
    texto = ""
    if self.listaEspera.head is not None:
      self.listaEjecucion.agregarTail(self.listaEspera.head.Id, self.listaEspera.head.operacion, self.listaEspera.head.tme, self.listaEspera.head.tiempoTranscurrido)
      self.listaEspera.borrarHead()

    temp = self.listaEspera.head

    while temp is not None:
      texto += f'{temp.Id}.- {temp.operacion}\n TME: {temp.tme}\n\n'
      temp = temp.next
    
    if texto == "":
      texto = "\nNo hay más procesos en espera."  # Si no hay más lotes

    self.actulizarTextArea(self.nuevo, texto)

  def actualizarListos(self):  #actualiza la interfaz de listos
    texto = ""
    
    try:
      temp = self.listaEjecucion.head.next
      while temp is not None:
        temp.tiempoTranscurrido += 1
        texto += f'{temp.Id}.- TME: {temp.tme}\n Tiempo Transcurrido: {temp.tiempoTranscurrido} \n\n'
        temp = temp.next
    except AttributeError:
      pass

    if texto == "":
      texto = "\nNo hay más procesos en listos."
    
    self.actulizarTextArea(self.listos, texto)

  def actualizarEjecucion(self): #actualiza la interfaz de ejecución
    if not self.pausado:
      self.actualizarReloj()

      if self.procesoactual is not None:
        self.procesoactual.tme -= 1  
        texto = f'{self.procesoactual.Id}.- {self.procesoactual.operacion}\n TME: {self.procesoactual.tme} \nTiempo de ejecución: {self.procesoactual.tiempoTranscurrido} segundos\n\n'
        
        self.actulizarTextArea(self.ejecucion, texto)

        self.procesoactual.tiempoTranscurrido += 1
                
        # Si el TME llega a 0, pasar al siguiente proceso
        if self.procesoactual.tme == 0:
            self.listaTerminados.agregarTail(self.procesoactual.Id, eval(self.procesoactual.operacion), self.procesoactual.tme,self.procesoactual.tiempoTranscurrido)
            self.actualizarTerminados()
            self.listaEjecucion.borrarHead()
            self.procesoactual = self.procesoactual.next
            self.actualizarListos()

      else:
        texto = "\nTodos los procesos \nhan terminado."
        self.actulizarTextArea(self.ejecucion, texto)
        return
      
      self.actualizarListos()

      self.ventana.after(1000, self.actualizarEjecucion)  # Se ejecutará de nuevo en 1 segundo
  
  def actualizarBloqueados(self):  #actualiza la interfaz de bloqueados
    texto = ""
    temp = self.listaBloqueados.head

    while temp is not None:
      texto += f'{temp.Id}.- {temp.operacion}\n TME: {temp.tme}\n\n'
      temp = temp.next

    if texto == "":
      texto = "\nNo hay procesos bloqueados."
    
    self.actulizarTextArea(self.bloqueados, texto)

  def actualizarTerminados(self):  #actualiza la interfaz de terminados
    texto = ""
    temp = self.listaTerminados.head

    while temp is not None:
      texto += f'{temp.Id}.- Resultado de la operación: {temp.operacion}\n Tiempo transcurrido -> {temp.tiempoTranscurrido}\n\n\n'
      temp = temp.next
    
    self.actualizarListos()
    self.actualizarNuevos()
    self.actulizarTextArea(self.terminado, texto)
  
  def iniciar(self):
    self.procesoactual = self.listaEspera.peekFront()
    self.boton.config(state=tk.DISABLED)

    self.ventana.bind("<i>", lambda evebt: self.interrupcion())
    self.ventana.bind("<e>", lambda event: self.error())
    self.ventana.bind("<p>", lambda event: self.pausa())
    self.ventana.bind("<c>", lambda event: self.continuar())
    self.ventana.bind('<n>', lambda event: self.crearNuevoproceso())
    self.ventana.bind('<b>', lambda event: self.showBCP())
    
    self.agregarProceso()

    self.actualizarNuevos()
    self.actualizarEjecucion()
  
  def agregarProceso(self):  # Agrega un proceso a la lista de ejecución
    for _ in range(0,4):
      if self.listaEspera.head is not None:
        self.listaEjecucion.agregarTail(self.listaEspera.head.Id, self.listaEspera.head.operacion, self.listaEspera.head.tme, self.listaEspera.head.tiempoTranscurrido)
        self.listaEspera.borrarHead()

  def interrupcion(self): # Mueve el proceso actual a lista de bloqueados
    if self.procesoactual is not None:
      self.listaBloqueados.agregarTail(self.procesoactual.Id, self.procesoactual.operacion, self.procesoactual.tme, self.procesoactual.tiempoTranscurrido + 8)
      self.listaEjecucion.borrarHead()  # Eliminar el proceso de la lista de ejecución
      
      # Pasar al siguiente proceso
      self.procesoactual = self.listaEjecucion.peekFront()
      self.actualizarEjecucion()
      self.actualizarListos()
      self.actualizarBloqueados()
      
      # Desbloquear proceso después de 8 segundos
      def desbloquear():
        sleep(8)
        if self.listaBloqueados.head is not None:
          desbloqueado = self.listaBloqueados.borrarHead()
          self.listaEjecucion.agregarTail(desbloqueado.Id, desbloqueado.operacion, desbloqueado.tme, desbloqueado.tiempoTranscurrido)
          if self.procesoactual is None:
            self.procesoactual = self.listaEjecucion.peekFront()
          self.actualizarEjecucion()
          self.actualizarBloqueados()
          self.actualizarListos()
      
      # Iniciar un hilo separado para manejar el desbloqueo
      threading.Thread(target=desbloquear).start()

  def error(self): # Mueve el proceso actual a lista de terminados con estado de error
    if self.procesoactual is not None:
      self.listaTerminados.agregarTail(self.procesoactual.Id, "ERROR", self.contador, self.procesoactual.tiempoTranscurrido)
      self.contador = 0
      self.actualizarTerminados()
      self.procesoactual = self.procesoactual.next
      self.listaEjecucion.borrarHead()
      self.actualizarListos()

  def pausa(self): # Pausa los procesos
    if not self.pausado:
      self.pausado = True
      self.pausaText.config(text="Procesos pausados.")   
    
  def continuar(self): # Continúa los procesos
    if self.pausado:
      self.pausado = False
      self.pausaText.config(text="")
      self.actualizarEjecucion()

  def crearNuevoproceso(self): # Agrega un nuevo proceso a la lista de espera
    Id = self.listaEspera.tail.Id + 1
    self.listaEspera.agregarTail(Id, pc.Procesos.getOperacion(), pc.Procesos.getTME(), 0)

    texto = ""
    temp = self.listaEspera.head

    while temp is not None:
      texto += f'{temp.Id}.- {temp.operacion}\n TME: {temp.tme}\n\n'
      temp = temp.next
    
    if texto == "":
      texto = "\nNo hay más procesos en espera."  # Si no hay más lotes

    self.actulizarTextArea(self.nuevo, texto)
  
  def showBCP(self): # Muestra el Bloque de Control de Procesos
    self.pausa()
    tabla = tk.Toplevel(self.ventana)
    tabla.title("Bloque de Control de Procesos")
    tabla.geometry("700x400")

    # Crear tabla
    columnas = ("ID", "Operación", "TME", "Tiempo restante", "Tiempo Transcurrido", "Estado")
    tablaBCP = ttk.Treeview(tabla, columns=columnas, show="headings")
    
    tablaBCP.heading("ID", text="ID")
    tablaBCP.heading("Operación", text="Operación")
    tablaBCP.heading("TME", text="TME")
    tablaBCP.heading("Tiempo restante", text="Tiempo restante")
    tablaBCP.heading("Tiempo Transcurrido", text="Tiempo Transcurrido")
    tablaBCP.heading("Estado", text="Estado")

    tablaBCP.column("ID", width=30)
    tablaBCP.column("Operación", width=100)
    tablaBCP.column("TME", width=50)
    tablaBCP.column("Tiempo restante", width=100)
    tablaBCP.column("Tiempo Transcurrido", width=100)
    tablaBCP.column("Estado", width=100)

    tablaBCP.pack(fill="both", expand=True)

    # Función para añadir filas a la tabla BCP
    def agregar_filas(lista, estado):
      temp = lista.head
      while temp is not None:
        if temp == self.listaEjecucion.head:
          tablaBCP.insert("", "end", values=(temp.Id, temp.operacion, temp.tme, temp.tme, temp.tiempoTranscurrido, "Ejecución"))
        elif estado == "Nuevo":
          tablaBCP.insert("", "end", values=(temp.Id, temp.operacion, temp.tme, 'NULL', 'NULL', estado))
        elif estado == "Terminado":
          tablaBCP.insert("", "end", values=(temp.Id, temp.operacion, temp.tme, 0, temp.tiempoTranscurrido, estado))
        else:
          tablaBCP.insert("", "end", values=(temp.Id, temp.operacion, temp.tme, temp.tme, temp.tiempoTranscurrido, estado))
        temp = temp.next

    # Llenar la tabla BCP con los procesos de cada estado
    agregar_filas(self.listaEjecucion, "Espera")
    agregar_filas(self.listaEspera, "Nuevo")
    agregar_filas(self.listaBloqueados, "Bloqueado")
    agregar_filas(self.listaTerminados, "Terminado")


  def actualizarReloj(self):
    self.tiempo += 1
    self.relojglobal.config(text=f"Reloj Global: {self.tiempo} segundos")
  
  def actulizarTextArea(self, widget, texto):
    widget.config(state=tk.NORMAL)
    widget.delete('1.0', tk.END)
    widget.insert(tk.END, texto)
    widget.config(state=tk.DISABLED)

def main():
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
    listaEspera.agregarTail(Id, pc.Procesos.getOperacion(), pc.Procesos.getTME(), 0)
  
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
  app = Ventana(ventana, listaEspera, listaEjecucion, listaBloqueados, listaTerminados, quantum)
  ventana.mainloop()

if __name__ == "__main__":
  main()
