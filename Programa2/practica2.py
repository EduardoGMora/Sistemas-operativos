import random
import tkinter as tk
import ProcesosClass as pc
import LLClass as ll

class Ventana:
  def __init__(self, ventana, listaEspera, listaTerminados):
    self.ventana = ventana          #atributos
    self.ventana.title("Procesamiento por lotes")

    # instancia de la clase LL
    self.listaEspera = listaEspera
    self.listaTerminados = listaTerminados
    self.procesoactual = None       #inicializa el apuntador al proceso actual
    
    # atributos de ayuda
    self.contador = 0
    self.tiempo = 0
    self.procesoLote = 1
    self.relojglobal = tk.Label(ventana, text=f"Reloj Global: {self.tiempo}")
    self.relojglobal.grid(row=0, column=4, padx=150)
    self.lotes = self.listaEspera.hacerLotes()
    self.lotesp = len(self.lotes)   #lotes pendientes
    self.pendientes = tk.Label(ventana, text=f"Número de Lotes pendientes: { self.lotesp }")
    self.pendientes.grid(row=3, column=0, pady=10)
    self.lote_actual = 0
    self.lote_enespera = self.lotes[self.lote_actual]
    self.pausado = False

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
    self.ventana.bind("<space>", lambda event: self.iniciar())  # Espacio para iniciar
    self.boton = tk.Button(ventana, text="Iniciar", command=self.iniciar)
    self.boton.grid(row=3, column=2, pady=10)
    self.ventana.bind("<Return>", lambda event: self.ventana.quit()) # Enter para salir


  def actualizarEspera(self):  #actualiza la interfaz de espera
    texto = ""
    if self.lote_actual < len(self.lotes):
        self.lote_enespera = self.lotes[self.lote_actual]

        for proceso in self.lote_enespera:
            if proceso != self.procesoactual and not proceso.ejecutado:
                texto += f'{proceso.Id}.- {proceso.operacion}\n TME: {proceso.tme}\n\n'
        
    else:
        texto = "No hay más procesos en espera."  # Si no hay más lotes

    self.espera.config(state=tk.NORMAL)
    self.espera.delete('1.0', tk.END)
    self.espera.insert(tk.END, texto)
    self.espera.config(state=tk.DISABLED)

  def actualizarEjecucion(self): #actualiza la interfaz de ejecución
    if not self.pausado:
      self.actualizarReloj()

      if self.procesoactual is not None:
        self.procesoactual.tme -= 1  
        texto = f'{self.procesoactual.Id}.- {self.procesoactual.operacion}\n TME: {self.procesoactual.tme} \nTiempo de ejecución: {self.contador} segundos\n\n'
        
        self.ejecucion.config(state=tk.NORMAL)  
        self.ejecucion.delete('1.0', tk.END)  
        self.ejecucion.insert(tk.END, texto)  
        self.ejecucion.config(state=tk.DISABLED)  

        self.contador += 1
                
        # Si el TME llega a 0, pasar al siguiente proceso
        if self.procesoactual.tme == 0:
            resultado = eval(self.procesoactual.operacion)
            self.listaTerminados.agregarTail(self.procesoactual.Id, resultado, self.contador)
            self.actualizarTerminados()
            self.listaEspera.borrarHead()
            self.contador = 0
            self.procesoactual.ejecutado = True
            self.procesoactual = self.procesoactual.next

      else:
        texto = "\nTodos los procesos han terminado."
        self.ejecucion.config(state=tk.NORMAL)
        self.ejecucion.delete('1.0', tk.END)
        self.ejecucion.insert(tk.END, texto)
        self.ejecucion.config(state=tk.DISABLED)
        return

    self.ventana.after(1000, self.actualizarEjecucion)  # Se ejecutará de nuevo en 1 segundo


  def actualizarTerminados(self):  #actualiza la interfaz de terminados
    texto = ""
    temp = self.listaTerminados.head

    while temp is not None:
      texto += f'{temp.Id}.- Resultado de la operación: {temp.operacion}\n\n\n'
      temp = temp.next
    
    self.procesoLote += 1
    if self.procesoLote == 5:
        self.lote_actual += 1
        self.procesoLote = 0
    
    self.actualizarEspera()
    
    self.terminado.config(state=tk.NORMAL)  
    self.terminado.delete('1.0', tk.END)  
    self.terminado.insert(tk.END, texto)  
    self.terminado.config(state=tk.DISABLED)  
  
  def iniciar(self):
    self.lote_actual = 0
    self.procesoactual = self.listaEspera.peekFront()
    self.boton.config(state=tk.DISABLED)

    # Entradas del teclado
    self.ventana.bind("<i>", lambda event: self.interrupcion())
    self.ventana.bind("<e>", lambda event: self.error())
    self.ventana.bind("<p>", lambda event: self.pausa())
    self.ventana.bind("<c>", lambda event: self.continuar())

    self.actualizarLotes()
    self.actualizarEspera()
    self.actualizarEjecucion()

  def interrupcion(self):
    # Mueve el proceso actual al final del lote
    if self.procesoactual.next is not None:
      self.listaEspera.switch(len(self.lote_enespera)-1)
      self.procesoactual = self.listaEspera.peekFront()
      self.actualizarEspera()
      self.actualizarEjecucion()
    else:
      return

  def error(self):
    if self.procesoactual is not None:
      # Agregar el proceso actual a la lista de terminados con estado de ERROR
      self.listaTerminados.agregarTail(self.procesoactual.Id, "ERROR", self.contador)
      self.contador = 0
      self.actualizarTerminados()
      self.procesoactual.ejecutado = True
      self.procesoactual = self.procesoactual.next
      self.listaEspera.borrarHead()
      self.actualizarEspera()

  def pausa(self):
    while self.pausado == False:
      # Pausa la ejecución de los procesos
      self.pausado = True
      print("Pausando procesos.")
      
    
  def continuar(self):
    if self.pausado:
      # Continuar la ejecución de los procesos
      print("Continuando procesos.")
      self.pausado = False
      self.actualizarEjecucion()

  def actualizarReloj(self):
    # Incrementa el tiempo y actualiza la etiqueta
    self.tiempo += 1
    self.relojglobal.config(text=f"Reloj Global: {self.tiempo} segundos")

  def actualizarLotes(self):
    if self.lotesp > 0:
      self.lotesp -= 1
      self.pendientes.config(text=f"Número de Lotes pendientes: {self.lotesp}") #lotes pendientes

def main():
  listaEspera = ll.LL()  #Lista de procesos en espera
  listaTerminados = ll.LL()  #Lista de procesos terminados

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
    listaEspera.agregarTail(Id, pc.Procesos.getOperacion(), pc.Procesos.getTME())

  ventana = tk.Tk()
  app = Ventana(ventana, listaEspera, listaTerminados)
  ventana.mainloop()

if __name__ == "__main__":
  main()
