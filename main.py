import time
import tkinter as Tk
from tkinter import Button, Entry, Frame, Label, StringVar, Toplevel, messagebox, Tk, Radiobutton, LabelFrame
from tkinter.ttk import Treeview

clientes = [["Franco Avendaño", 4, "Con Reserva"], ["Logan", 2, "Sin Reserva"]]
raiz = Tk()
raiz.title("Reservaciones")
raiz.resizable(0,0)
raiz.geometry("800x400")
raiz.configure(bg="lightblue")

tiempo = Label(raiz)
tiempo.pack()
tiempo.place(x=2, y=15)
tiempo.configure(bg="lavender", font=("Arial", 8, "bold"))

def actualizar_hora():
    tiempo.configure(text=time.strftime("%H:%M:%S"))
    tiempo.after(1000, actualizar_hora)

opciones_frame = LabelFrame(raiz, text="Opciones", bg="lavender")
opciones_frame.pack()
listado_frame = LabelFrame(raiz, text="Clientes", bg="lavender")
listado_frame.pack()

mesas = [
    {"id": 1, "capacidad": 2, "ocupado": False},
    {"id": 2, "capacidad": 2, "ocupado": False},
    {"id": 3, "capacidad": 2, "ocupado": False},
    {"id": 4, "capacidad": 3, "ocupado": False},
    {"id": 5, "capacidad": 3, "ocupado": False},
    {"id": 6, "capacidad": 3, "ocupado": False},
    {"id": 7, "capacidad": 4, "ocupado": False},
    {"id": 8, "capacidad": 4, "ocupado": False},
    {"id": 9, "capacidad": 4, "ocupado": False},
    {"id": 10, "capacidad": 5, "ocupado": False},
    {"id": 11, "capacidad": 5, "ocupado": False},
    {"id": 12, "capacidad": 5, "ocupado": False},
]

mesas_frame = LabelFrame(raiz, text="Mesas", bg="lavender")
mesas_frame.pack(fill='both', expand=True)

def crear_grilla_mesas():
    columnas = 4
    for i, mesa in enumerate(mesas):
        color = "forestgreen" if not mesa["ocupado"] else "red3"
        etiqueta_mesa = Label(mesas_frame, text=f"Mesa {mesa['id']}", bg=color, width=15)
        etiqueta_mesa.grid(row=i//columnas, column=i%columnas, padx=5, pady=5, sticky="nsew")
    for columna in range(columnas): mesas_frame.columnconfigure(columna, weight=1)

crear_grilla_mesas()

def actualizar_grilla_mesas():
    for boton_mesa in mesas_frame.winfo_children():
        boton_mesa.destroy()
    crear_grilla_mesas()

def agregar_reservacion():
    def aceptar_modal():
        nombre_entry = nombre.get()
        cantidad_entry = int(cantidad_personas.get())
        opcion_entry = opcion.get()
        if nombre_entry and cantidad_entry and opcion_entry:
            nuevoCliente = [nombre_entry, cantidad_entry, opcion_entry]
            
            if nuevoCliente[2] == "Con Reserva":
                i = 0
                while i < len(clientes) and clientes[i][2] == "Con Reserva":
                    i +=1
                    
                clientes.insert(i, nuevoCliente)
                tabla.insert(parent='',index=i,values=(nuevoCliente[0],nuevoCliente[1],nuevoCliente[2]))
            else:
                clientes.append(nuevoCliente)
                tabla.insert(parent='',index="end",values=(nuevoCliente[0],nuevoCliente[1],nuevoCliente[2]))

            modal.destroy()
            messagebox.showinfo("Valor ingresado", "La reservacion se realizo con exito")
            
        else:
            messagebox.showinfo("Advertencia", "Por favor ingresa un valor.")
        
        
    modal = Toplevel(opciones_frame)
    modal.title("Agregar Reservacion")
    modal.resizable(0,0)
    modal.geometry("300x250")
    modal.grab_set()
    modal.protocol("WM_DELETE_WINDOW", lambda: None)
    modal.configure(bg="lavender")
    
    
    
    label_nombre = Label(modal,text="Nombre:", bg="lavender", font=("Arial", 10, "bold"))
    label_nombre.grid(column=0,row=0,ipady=10)
    
    nombre = Entry(modal)
    nombre.grid(column=1,row=0)
    
    label_personas = Label(modal,text="Cantidad de Personas", bg="lavender", font=("Arial", 10, "bold"))
    label_personas.grid(column=0,row=1,ipady=10)
    
    cantidad_personas = Entry(modal)
    cantidad_personas.grid(column=1,row=1)
    
    
    selecionar_opcion = Label(modal, text="Seleccione una Opcion", bg="lavender", font=("Arial", 10, "bold"))
    selecionar_opcion.grid(column=0, row=2,ipady=10)
    
    # Variable para almacenar la opción seleccionada
    opcion = StringVar(value="")  # Valor inicial vacío
    opciones = ["Con Reserva", "Sin Reserva"]
    for i,texto in enumerate(opciones):
        opciones_reserva = Radiobutton(modal,text=texto,variable=opcion,value=texto)
        opciones_reserva.grid(column=1,row=i+2)
        
    
    boton_modal_cancelar = Button(modal,text="Cancelar", bg="lavender", command=modal.destroy,width=15)
    boton_modal_cancelar.grid(column=0,row=5,pady=25,padx=20)
    
    boton_modal_aceptar = Button(modal, text="Aceptar", bg="lavender", command=aceptar_modal,width=15)
    boton_modal_aceptar.grid(column=1,row=5,pady=25)
    

def atender_cliente():
    if clientes:
        cliente = clientes.pop(0)
        for mesa in mesas:
            if not mesa["ocupado"] and mesa["capacidad"] >= int(cliente[1]):
                mesa["ocupado"] = True
                messagebox.showinfo("Mesa asignada",f"Mesa {mesa['id']} asignada a {cliente[0]}")
                for usuario in tabla.get_children():
                    if tabla.item(usuario)["values"][0] == cliente[0]:
                        tabla.delete(usuario)
                        break
                actualizar_grilla_mesas()
                return
        messagebox.showinfo("Sin mesas","No hay mesas disponibles para el cliente actual.")
    else:
        messagebox.showinfo("Sin clientes","No hay clientes en la lista de espera.")

def buscar_reservacion():
    def realizar_busqueda():
        nombre_buscar = nombre_entry.get()
        if not nombre_buscar:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un nombre para buscar.")
            return

        # Buscar el cliente en la lista de clientes
        resultados = [cliente for cliente in clientes if cliente[0].lower() == nombre_buscar.lower()]
        if resultados:
            cliente = resultados[0]
            messagebox.showinfo("Reservación encontrada", f"Nombre: {cliente[0]}\nPersonas: {cliente[1]}\nTipo: {cliente[2]}")
        else:
            messagebox.showinfo("Sin resultados", "No se encontró una reservación con ese nombre.")

        buscar_modal.destroy()
    buscar_modal = Toplevel(opciones_frame)
    buscar_modal.title("Buscar Reservación")
    buscar_modal.resizable(0, 0)
    buscar_modal.geometry("300x150")
    buscar_modal.grab_set()
    buscar_modal.configure(bg="lavender")

    label_nombre = Label(buscar_modal, text="Nombre:", bg="lavender", font=("Arial", 10, "bold"))
    label_nombre.pack(pady=10)
    
    nombre_entry = Entry(buscar_modal)
    nombre_entry.pack(pady=5)
    
    boton_buscar = Button(buscar_modal, text="Buscar", bg="lavender", command=realizar_busqueda)
    boton_buscar.pack(pady=10)

    boton_cancelar = Button(buscar_modal, text="Cancelar", bg="lavender", command=buscar_modal.destroy)
    boton_cancelar.pack()

def cancelar_reservacion():
    pass

def modificar_reservacion():
    #Seleciona la fila que desea cambiar
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Por favor, selecciona una reservación para modificar.")
        return

    item_id = seleccion[0]
    index = tabla.index(item_id)
    cliente = clientes[index]

    def aceptar_cambios():
        nuevo_nombre = nombre_entry.get()
        nueva_cantidad = int(cantidad_personas_entry.get())
        if nueva_cantidad <= 0:
            messagebox.showerror("Error", "Cantidad de personas debe ser mayor que cero")
            return
        if nueva_cantidad > 5:
            messagebox.showerror("Error", "Cantidad de personas debe ser un menor de 5 personas.")
            return

        nuevo_tipo_reserva = opcion.get()

        if nuevo_nombre and nuevo_tipo_reserva:
            
            cliente_anterior = clientes[index]
            tipo_reserva_anterior = cliente_anterior[2]
        
            
            cliente_actualizado = [nuevo_nombre, nueva_cantidad, nuevo_tipo_reserva]
        
            
            if tipo_reserva_anterior == "Con Reserva" and nuevo_tipo_reserva == "Sin Reserva":
                
                clientes.pop(index)
                
                clientes.append(cliente_actualizado)
            elif tipo_reserva_anterior == "Sin Reserva" and nuevo_tipo_reserva == "Con Reserva":
                
                clientes.pop(index)
                
                clientes.insert(0, cliente_actualizado)
            else:
                
                clientes[index] = cliente_actualizado

            # Actualizar la tabla para reflejar los cambios
            tabla.delete(*tabla.get_children())
            for cliente in clientes:
                tabla.insert(parent='', index="end", values=(cliente[0], cliente[1], cliente[2]))
            messagebox.showinfo("Modificación Exitosa", "La reservación se modificó correctamente.")
            modificar.destroy()
        else:
             messagebox.showwarning("Advertencia", "Por favor, ingresa todos los valores.")

    modificar = Toplevel(raiz)
    modificar.title("Modificar Reservación")
    modificar.resizable(0,0)
    modificar.geometry("300x250")
    modificar.grab_set()
    modificar.configure(bg="lavender")

    Label(modificar, text="Nombre:",bg="lavender", font=("Arial", 10, "bold")).grid(column=0, row=0,ipady=10)
    nombre_entry = Entry(modificar)
    nombre_entry.grid(column=1, row=0)
    nombre_entry.insert(0, cliente[0])

    Label(modificar, text="Cantidad de Personas:", bg="lavender", font=("Arial", 10, "bold")).grid(column=0, row=1,ipady=10)
    cantidad_personas_entry = Entry(modificar)
    cantidad_personas_entry.grid(column=1, row=1)
    cantidad_personas_entry.insert(0, cliente[1])

    Label(modificar, text="Tipo de Reserva:", bg="lavender", font=("Arial", 10, "bold")).grid(column=0, row=2,ipady=10)
    opcion = StringVar(value=cliente[2])
    opciones = ["Con Reserva", "Sin Reserva"]
    for i, texto in enumerate(opciones):
        Radiobutton(modificar, text=texto, variable=opcion, value=texto).grid(column=1, row=i+2)

    Button(modificar, text="Cancelar", bg="lavender", command=modificar.destroy,width=15).grid(column=0, row=5,pady=25,padx=20)
    Button(modificar, text="Aceptar", bg="lavender", command=aceptar_cambios,width=15).grid(column=1, row=5,pady=25)

def liberar_mesas():
    for mesa in mesas:
        mesa["ocupado"] = False
    actualizar_grilla_mesas()

def eliminar_cliente():
    if clientes:
        cliente = clientes.pop(0)  # Elimina al cliente atendido de la lista
        messagebox.showinfo("Cliente eliminado", f"Cliente {cliente[0]} eliminado de la lista.")
        for usuario in tabla.get_children():
            if tabla.item(usuario)["values"][0] == cliente[0]:
                tabla.delete(usuario)
                break
    else:
        messagebox.showinfo("Sin clientes", "No hay clientes para eliminar.")

# UI PRINCIPAL
boton_agregar = Button(opciones_frame,text="Agregar Reservacion", bg="lavender", font=("Arial", 10, "bold"), command=agregar_reservacion)
boton_agregar.grid(column=0,row=0)
#boton_agregar.pack(pady=10)

boton_atender = Button(opciones_frame,text="Atender Cliente", bg="lavender", font=("Arial", 10, "bold"), command=atender_cliente)
boton_atender.grid(column=1,row=0)
#boton_atender.pack(pady=10)

boton_buscar = Button(opciones_frame,text="Buscar Reservacion", bg="lavender", font=("Arial", 10, "bold"), command=buscar_reservacion)
boton_buscar.grid(column=2,row=0)
#boton_buscar.pack(pady=10)

boton_liberarmesas = Button(opciones_frame, text="Liberar Mesas", bg="lavender", font=("Arial", 10, "bold"), command=liberar_mesas)
boton_liberarmesas.grid(column=3,row=0)

boton_eliminar = Button(opciones_frame, text="Eliminar Cliente", bg="lavender", font=("Arial", 10, "bold"), command=eliminar_cliente)
boton_eliminar.grid(column=4, row=0)  # Ajusta la columna según sea necesario

boton_modificar = Button(opciones_frame, text="Modificar Reservación", bg="lavender", font=("Arial", 10, "bold"), command=modificar_reservacion)
boton_modificar.grid(column=5, row=0)


tabla = Treeview(listado_frame,columns=('Nombre', 'Cantidad Clientes', 'Tipo Reserva'),show='headings')
tabla.heading('Nombre', text="Nombre")
tabla.heading('Cantidad Clientes',text='Cantidad Clientes')
tabla.heading('Tipo Reserva',text='Tipo Reserva')
tabla.pack(fill='both',expand=True)

for i in range(len(clientes)):
    
    tabla.insert(parent='',index="end",values=(clientes[i][0],clientes[i][1],clientes[i][2]))
"""
# LISTADO
fila = 1
for i, cliente in enumerate(clientes):
    columna = 0
    for j, dato in enumerate(cliente):
        label_cliente = Label(raiz,text=dato)
        label_cliente.grid(column=columna,row=fila)
        columna += 1
    boton_cancelar = Button(text="Cancelar Reservacion")
    boton_cancelar.grid(column=columna,row=fila)
    fila += 1
    
boton_cancelar = Button(text="Cancelar Reservacion", height=2, width=25)
#boton_cancelar.pack(pady=10)

boton_modificar = Button(text="Modificar Reservacion", height=2, width=25)
#boton_modificar.pack(pady=10)
"""
actualizar_hora()
raiz.mainloop()