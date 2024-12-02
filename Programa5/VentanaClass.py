import tkinter as tk
from tkinter import ttk
from time import sleep
import threading
import ProcesosClass as pc


class Ventana:
  def __init__(self, ventana, listaNuevos, listaEspera, listaEjecucion, listaBloqueados, listaTerminados, quantum):
    self.ventana = ventana          #atributos
    self.ventana.title("Procesamiento por lotes (First Come First Server)")

    # instancia de la clase LL
    self.listaNuevos = listaNuevos
    self.listaEspera = listaEspera
    self.listaEjecucion = listaEjecucion
    self.listaBloqueados = listaBloqueados
    self.listaTerminados = listaTerminados
    self.quantum = quantum
    self.procesoactual = None       #inicializa el apuntador al proceso en ejecución
    
    # atributos de ayuda
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
    if self.listaNuevos.head is not None:
      # Id, operacion, tme, tiemporestante, tiemposervicio = 0, tiempollegada = 0, tiemporetorno = 0, tiempoespera = 0
      self.listaEspera.agregarTail(self.listaNuevos.head.Id, self.listaNuevos.head.operacion, self.listaNuevos.head.tme, self.listaNuevos.head.tiemporestante, 0, self.tiempo, 0, 0)
      self.listaNuevos.borrarHead()

    temp = self.listaNuevos.head

    while temp is not None:
      texto += f'{temp.Id}.- {temp.operacion}\n TME: {temp.tme}\n\n'
      temp = temp.next
    
    if texto == "":
      texto = "\nNo hay más procesos en espera."  # Si no hay más lotes

    self.actualizarTextArea(self.nuevo, texto)

  def actualizarListos(self):  #actualiza la interfaz de listos
    texto = ""

    try:
      temp = self.listaEspera.head
      while temp is not None:
        temp.tiempoespera += 1
        texto += f'{temp.Id}.- TME: {temp.tme}\n Tiempo de espera: {temp.tiempoespera} \n\n'
        temp = temp.next
    except AttributeError:
      pass

    if texto == "":
      texto = "\nNo hay más procesos en listos."
    
    self.actualizarTextArea(self.listos, texto)

  def actualizarEjecucion(self): #actualiza la interfaz de ejecución
    if not self.pausado:
      self.actualizarReloj()

      if self.procesoactual is not None:
        self.procesoactual.tiemporestante -= 1  
        texto = f'{self.procesoactual.Id}.- {self.procesoactual.operacion}\n TME: {self.procesoactual.tme} \nTiempo de ejecución: {self.procesoactual.tiemposervicio} segundos\n\n'
        
        self.actualizarTextArea(self.ejecucion, texto)

        self.procesoactual.tiemposervicio += 1
                
        # Si el TME llega a 0, pasar al siguiente proceso
        if self.procesoactual.tiemposervicio == self.procesoactual.tme:
          tiemporetorno = self.tiempo - self.procesoactual.tiempollegada + 1
          tiempoespera = tiemporetorno - self.procesoactual.tme + 1
          self.listaTerminados.agregarTail(self.procesoactual.Id, eval(self.procesoactual.operacion), self.procesoactual.tme, 0, self.procesoactual.tme, self.procesoactual.tiempollegada, tiemporetorno, tiempoespera)
          self.listaEjecucion.borrarHead()
          self.listaEjecucion.agregarTail(self.listaEspera.head.Id, self.listaEspera.head.operacion, self.listaEspera.head.tme, self.listaEspera.head.tiemporestante)
          self.listaEspera.borrarHead()
          threading.Thread(target=self.actualizarTerminados).start()
          self.procesoactual = self.listaEjecucion.peekFront()
          self.actualizarListos()

      else:
        texto = "\nTodos los procesos \nhan terminado."
        self.actualizarTextArea(self.ejecucion, texto)
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
    
    self.actualizarTextArea(self.bloqueados, texto)

  def actualizarTerminados(self):  #actualiza la interfaz de terminados
    texto = ""
    temp = self.listaTerminados.head

    while temp is not None:
      texto += f'{temp.Id}.- Resultado de la operación: {temp.operacion}\n Tiempo restante -> {temp.tiemporestante} \n Tiempo de Servicio -> {temp.tiemposervicio}\n Tiempo de llegada -> {temp.tiempollegada} \n Tiempo de espera -> {temp.tiempoespera}\n Tiempo de retorno -> {temp.tiemporetorno} \n\n\n'
      temp = temp.next
    
    threading.Thread(target=self.actualizarListos).start()
    self.actualizarNuevos()
    self.actualizarTextArea(self.terminado, texto)
  
  def iniciar(self):
    self.boton.config(state=tk.DISABLED)

    self.ventana.bind("<i>", lambda evebt: self.interrupcion())
    self.ventana.bind("<e>", lambda event: self.error())
    self.ventana.bind("<p>", lambda event: self.pausa())
    self.ventana.bind("<c>", lambda event: self.continuar())
    self.ventana.bind('<n>', lambda event: self.crearNuevoproceso())
    self.ventana.bind('<b>', lambda event: self.showBCP())


    self.agregarProceso()
    
    # Id, operacion, tme, tiemporestante, tiemposervicio = 0, tiempollegada = 0, tiemporetorno = 0, tiempoespera = 0
    self.listaEjecucion.agregarTail(self.listaEspera.head.Id, self.listaEspera.head.operacion, self.listaEspera.head.tme, self.listaEspera.head.tiemporestante)
    self.procesoactual = self.listaEjecucion.peekFront()
    self.listaEspera.borrarHead()

    self.actualizarNuevos()
    self.actualizarEjecucion()

  def agregarProceso(self): # Agrega un proceso a la lista de espera
    for _ in range(0,4):
      if self.listaNuevos.head is not None:
        # Id, operacion, tme, tiemporestante, tiemposervicio = 0, tiempollegada = 0, tiemporetorno = 0, tiempoespera = 0
        self.listaEspera.agregarTail(self.listaNuevos.head.Id, self.listaNuevos.head.operacion, self.listaNuevos.head.tme, self.listaNuevos.head.tiemporestante)
        self.listaNuevos.borrarHead()
      else:
        break

  def interrupcion(self): # Mueve el proceso actual a lista de bloqueados
    if self.procesoactual is not None:
      self.listaBloqueados.agregarTail(self.procesoactual.Id, self.procesoactual.operacion, self.procesoactual.tme, self.procesoactual.tiemporestante, self.procesoactual.tiemposervicio, self.procesoactual.tiempollegada, self.procesoactual.tiemporetorno + 8,self.procesoactual.tiempoespera)
      
      # Pasar al siguiente proceso
      self.listaEjecucion.borrarHead()  # Eliminar el proceso de la lista de ejecución
      self.listaEjecucion.agregarTail(self.listaEspera.head.Id, self.listaEspera.head.operacion, self.listaEspera.head.tme, self.listaEspera.head.tiemporestante)
      self.listaEspera.borrarHead()
      self.procesoactual = self.listaEjecucion.peekFront()
      self.actualizarEjecucion()
      self.actualizarBloqueados()
      threading.Thread(target=self.actualizarListos).start()
      
      # Desbloquear proceso después de 8 segundos
      def desbloquear():
        sleep(8)
        desbloqueado = self.listaBloqueados.borrarHead()
        self.listaEspera.agregarTail(desbloqueado.Id, desbloqueado.operacion, desbloqueado.tme, desbloqueado.tiempoTranscurrido)
        if self.procesoactual is None:
          self.procesoactual = self.listaEjecucion.peekFront()
        self.actualizarBloqueados()
        self.actualizarEjecucion()
        self.actualizarListos()
      
      # Iniciar un hilo separado para manejar el desbloqueo
      threading.Thread(target=desbloquear).start()

  def error(self): # Mueve el proceso actual a lista de terminados con estado de error
    if self.procesoactual is not None:
      tiemporetorno = self.tiempo - self.procesoactual.tiempollegada + 1
      tiempoespera = tiemporetorno - self.procesoactual.tme + self.procesoactual.tiemporestante + 1
      self.listaTerminados.agregarTail(self.procesoactual.Id, "ERROR", self.procesoactual.tme, self.procesoactual.tiemporestante, self.procesoactual.tiemposervicio, self.procesoactual.tiempollegada, tiemporetorno, tiempoespera)
      threading.Thread(target=self.actualizarTerminados).start()
      self.listaEjecucion.borrarHead()
      self.listaEjecucion.agregarTail(self.listaEspera.head.Id, self.listaEspera.head.operacion, self.listaEspera.head.tme, self.listaEspera.head.tiemporestante)
      self.procesoactual = self.listaEjecucion.peekFront()
      self.listaEspera.borrarHead()
      threading.Thread(target=self.actualizarNuevos).start()

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
    if self.listaNuevos.head is None:
      temp = self.listaEspera.head
      Id = temp.Id
      while temp is not None:
        if temp.Id > Id:
          Id = temp.Id
        temp = temp.next
      Id += 1
    else: Id = self.listaNuevos.tail.Id + 1
    
    tme = pc.Procesos.getTME()
    # Id, operacion, tme, tiemporestante, tiemposervicio = 0, tiempollegada = 0, tiemporetorno = 0, tiempoespera = 0
    self.listaNuevos.agregarTail(Id, pc.Procesos.getOperacion(), tme, tme)

    texto = ""
    temp = self.listaNuevos.head

    while temp is not None:
      texto += f'{temp.Id}.- {temp.operacion}\n TME: {temp.tme}\n\n'
      temp = temp.next
    
    if texto == "":
      texto = "\nNo hay más procesos en espera."  # Si no hay más lotes
    self.actualizarTextArea(self.nuevo, texto)
  
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
  
  def actualizarTextArea(self, widget, texto):
    widget.config(state=tk.NORMAL)
    widget.delete('1.0', tk.END)
    widget.insert(tk.END, texto)
    widget.config(state=tk.DISABLED)