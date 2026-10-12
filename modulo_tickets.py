import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os


def _ruta_archivo(nombre_archivo):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre_archivo)


def _cargar_lista_json(nombre_archivo):
    ruta = _ruta_archivo(nombre_archivo)
    if not os.path.exists(ruta):
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump([], archivo, indent=4, ensure_ascii=False)

    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


# -------------------------
# CARGAR TICKETS
# -------------------------
def cargar_tickets():
    return _cargar_lista_json("tickets.json")


def cargar_tecnicos():
    return _cargar_lista_json("tecnicos.json")


def abrir_ventana_tickets():

    ventana = tk.Toplevel() #tipo de ventana
    ventana.title("Tickets")
    ventana.geometry("600x350") #tamaño de ventana

    titulo = tk.Label(
        ventana,
        text="Listado de Tickets",
        font=("Arial", 14))
    titulo.pack(pady=10)

    tickets = cargar_tickets()

    for ticket in tickets:
        estado = ticket["estado"]
        color = "lightgray"

        if estado == "En Proceso":
            color = "yellow"

        elif estado == "Resuelto":
            color = "lightgreen"

        texto = (
            f"Ticket #{ticket['id']} | "
            f"{ticket['activo']} | "
            f"{ticket['estado']}")

        etiqueta = tk.Label(
            ventana,
            text=texto,
            bg=color, #bg es blackground (fondo)
            width=60)

        etiqueta.pack(pady=2)

    boton_cerrar = tk.Button(
        ventana,
        text="Cerrar",
        bg="#A31A1A",
        fg="white",
        activebackground="#7F1511",
        activeforeground="white",
        command=ventana.destroy)

    boton_cerrar.pack(pady=10)


# -------------------------
# GUARDAR TICKETS
# -------------------------

def guardar_tickets(tickets):

    with open(_ruta_archivo("tickets.json"), "w", encoding="utf-8") as archivo:
        json.dump(
            tickets,
            archivo,
            indent=4,
            ensure_ascii=False
        )


def eliminar_tickets(ticket_ids):
    ids_a_eliminar = {str(ticket_id) for ticket_id in ticket_ids}
    if not ids_a_eliminar:
        return 0

    tickets = cargar_tickets()
    tickets_restantes = [
        ticket for ticket in tickets
        if str(ticket.get("id")) not in ids_a_eliminar
    ]
    cantidad_eliminada = len(tickets) - len(tickets_restantes)

    if cantidad_eliminada:
        guardar_tickets(tickets_restantes)

    return cantidad_eliminada


# -------------------------
# MOSTRAR TICKETS
# -------------------------

def mostrar_tickets():
    tickets = cargar_tickets()
    ventana = tk.Toplevel()

    # Título de la ventana
    titulo = tk.Label(
        ventana,
        text="Tickets registrados",
        font=("Arial", 14)
    )

    titulo.pack(pady=10)

    # Contenedor de los tickets
    contenedor = tk.Frame(ventana)

    contenedor.pack()

    for ticket in tickets:

        estado = ticket["estado"]

        # Color según estado
        color = "lightgray"

        if estado == "En Proceso":
            color = "yellow"

        elif estado == "Resuelto":
            color = "lightgreen"

        # Crear un ticket individual
        ticket_frame = tk.Frame(
            contenedor,
            bg=color,
            bd=2,
            relief="solid",
            width=350
        )

        ticket_frame.pack(
            pady=10,
            padx=10,
            fill="x"
        )

        # Número del ticket
        titulo_ticket = tk.Label(
            ticket_frame,
            text=f"TICKET #{ticket['id']}",
            bg=color,
            font=("Arial", 12, "bold")
        )

        titulo_ticket.pack(pady=5)

        # Separador
        separador = tk.Label(
            ticket_frame,
            text="-----------------------------",
            bg=color
        )

        separador.pack()

        # Activo
        activo = tk.Label(
            ticket_frame,
            text=f"ACTIVO: {ticket['activo']}",
            bg=color,
            font=("Arial", 10, "bold")
        )

        activo.pack(anchor="w", padx=10)

        # Descripción
        descripcion = tk.Label(
            ticket_frame,
            text=f"PROBLEMA: {ticket['descripcion']}",
            bg=color,
            wraplength=320,
            justify="left"
        )

        descripcion.pack(
            anchor="w",
            padx=10,
            pady=5
        )

        # Técnico
        tecnico = tk.Label(
            ticket_frame,
            text=f"TÉCNICO: {ticket['tecnico']}",
            bg=color
        )

        tecnico.pack(anchor="w", padx=10)

        # Estado
        estado_label = tk.Label(
            ticket_frame,
            text=f"ESTADO: {ticket['estado']}",
            bg=color,
            font=("Arial", 10, "bold")
        )

        estado_label.pack(
            anchor="w",
            padx=10,
            pady=5
        )

        # Separador inferior
        separador_final = tk.Label(
            ticket_frame,
            text="-----------------------------",
            bg=color
        )

        separador_final.pack(pady=5)

    # Botón cerrar
    boton_cerrar = tk.Button(
        ventana,
        text="Cerrar",
        width=20,
        bg="#A31A1A",
        fg="white",
        activebackground="#7F1511",
        activeforeground="white",
        command=ventana.destroy
    )

    boton_cerrar.pack(pady=10)


# -------------------------
# CREAR TICKET
# -------------------------

def crear_ticket(on_update=None):

    tickets = cargar_tickets()

    # Cargar los activos
    activos = _cargar_lista_json("activos.json")

    ventana = tk.Toplevel()
    ventana.title("Crear Ticket")
    ventana.geometry("400x300")

    # Título
    titulo = tk.Label(
        ventana,
        text="Crear nuevo ticket",
        font=("Arial", 14)
    )
    titulo.pack(pady=10)

    # Texto para seleccionar activo
    etiqueta_activo = tk.Label(
        ventana,
        text="Seleccione el activo:"
    )
    etiqueta_activo.pack()

    # Lista de activos
    opciones_activos = []

    for activo in activos:
        opciones_activos.append(
            activo["id"] + " - " + activo["nombre"]
        )

    combo_activo = ttk.Combobox(
        ventana,
        values=opciones_activos,
        state="readonly",
        width=35
    )

    combo_activo.pack(pady=5)

    # Texto para descripción
    etiqueta_descripcion = tk.Label(
        ventana,
        text="Describa el problema:"
    )
    etiqueta_descripcion.pack(pady=5)

    # Caja para escribir la descripción
    entrada_descripcion = tk.Entry(
        ventana,
        width=40
    )
    entrada_descripcion.pack()

    # Función para guardar el ticket
    def guardar_nuevo_ticket():

        activo_seleccionado = combo_activo.get()
        descripcion = entrada_descripcion.get()

        if activo_seleccionado == "":
            messagebox.showerror(
                "Error",
                "Debe seleccionar un activo"
            )
            return

        if descripcion == "":
            messagebox.showerror(
                "Error",
                "Debe escribir una descripción"
            )
            return

        # Obtener solamente el ID del activo
        activo_id = activo_seleccionado.split(" - ")[0]

        # Generar nuevo ID
        nuevo_id = 1

        if len(tickets) > 0:
            nuevo_id = int(tickets[-1]["id"]) + 1

        nuevo_ticket = {
            "id": nuevo_id,
            "activo": activo_id,
            "descripcion": descripcion,
            "tecnico": "",
            "estado": "Pendiente"
        }

        tickets.append(nuevo_ticket)

        guardar_tickets(tickets)

        messagebox.showinfo(
            "Éxito",
            f"Ticket #{nuevo_id} creado correctamente"
        )

        ventana.destroy()
        if on_update is not None:
            on_update()

    # Botón guardar
    boton_guardar = tk.Button(
        ventana,
        text="Crear Ticket",
        width=20,
        bg="#81C784",
        fg="white",
        activebackground="#388E3C",
        activeforeground="white",
        command=guardar_nuevo_ticket
    )
    boton_guardar.pack(pady=15)

    # Botón cancelar
    boton_cancelar = tk.Button(
        ventana,
        text="Cancelar",
        width=20,
        bg="#A31A1A",
        fg="white",
        activebackground="#7F1511",
        activeforeground="white",
        command=ventana.destroy
    )
    boton_cancelar.pack()
    
# -------------------------
# ASIGNAR TÉCNICO
# -------------------------

def asignar_tecnico(ticket_id=None, tecnico_id=None, on_update=None):

    if ticket_id is not None:
        if not tecnico_id:
            messagebox.showerror("Error", "Debe seleccionar un técnico")
            return

        tecnicos = cargar_tecnicos()
        if tecnico_id not in {tecnico["id"] for tecnico in tecnicos}:
            messagebox.showerror("Error", "El técnico seleccionado no existe")
            return

        tickets = cargar_tickets()
        ticket = next(
            (item for item in tickets if str(item.get("id")) == str(ticket_id)),
            None
        )
        if ticket is None:
            messagebox.showerror("Error", "No se encontró el ticket seleccionado")
            return

        ticket["tecnico"] = tecnico_id
        ticket["estado"] = "En Proceso"
        guardar_tickets(tickets)
        messagebox.showinfo("Éxito", "Técnico asignado correctamente")

        if on_update is not None:
            on_update()
        return

    tickets = cargar_tickets()

    # Cargar los técnicos desde el JSON
    tecnicos = cargar_tecnicos()

    # Crear ventana
    ventana = tk.Toplevel()
    ventana.title("Asignar Técnico")
    ventana.geometry("450x300")

    # Título
    titulo = tk.Label(
        ventana,
        text="Asignar Técnico a Ticket",
        font=("Arial", 14)
    )
    titulo.pack(pady=10)

    # -------------------------
    # SELECCIONAR TICKET
    # -------------------------

    etiqueta_ticket = tk.Label(
        ventana,
        text="Seleccione el ticket:"
    )
    etiqueta_ticket.pack()

    opciones_tickets = []

    for ticket in tickets:

        texto = (
            f"Ticket #{ticket['id']} - "
            f"{ticket['activo']} - "
            f"{ticket['estado']}"
        )

        opciones_tickets.append(texto)

    combo_ticket = ttk.Combobox(
        ventana,
        values=opciones_tickets,
        state="readonly",
        width=40
    )

    combo_ticket.pack(pady=5)

    # -------------------------
    # SELECCIONAR TÉCNICO
    # -------------------------

    etiqueta_tecnico = tk.Label(
        ventana,
        text="Seleccione el técnico:"
    )
    etiqueta_tecnico.pack(pady=5)

    opciones_tecnicos = []

    for tecnico in tecnicos:

        texto = (
            f"{tecnico['id']} - "
            f"{tecnico['nombre']}"
        )

        opciones_tecnicos.append(texto)

    combo_tecnico = ttk.Combobox(
        ventana,
        values=opciones_tecnicos,
        state="readonly",
        width=40
    )

    combo_tecnico.pack(pady=5)

    # -------------------------
    # ASIGNAR
    # -------------------------

    def guardar_asignacion():

        ticket_seleccionado = combo_ticket.get()
        tecnico_seleccionado = combo_tecnico.get()

        # Verificar que se haya seleccionado un ticket
        if ticket_seleccionado == "":
            messagebox.showerror(
                "Error",
                "Debe seleccionar un ticket"
            )
            return

        # Verificar que se haya seleccionado un técnico
        if tecnico_seleccionado == "":
            messagebox.showerror(
                "Error",
                "Debe seleccionar un técnico"
            )
            return

        # Obtener el ID del ticket
        parte_ticket = ticket_seleccionado.split(" - ")[0]

        ticket_id = parte_ticket.replace("Ticket #", "")

        # Obtener el ID del técnico
        tecnico_id = tecnico_seleccionado.split(" - ")[0]

        # Buscar el ticket
        for ticket in tickets:

            if str(ticket["id"]) == ticket_id:

                ticket["tecnico"] = tecnico_id

                # Al asignar técnico pasa a estar en proceso
                ticket["estado"] = "En Proceso"

                break

        # Guardar los cambios
        guardar_tickets(tickets)

        messagebox.showinfo(
            "Éxito",
            "Técnico asignado correctamente"
        )

        ventana.destroy()

    # Botón asignar
    boton_asignar = tk.Button(
        ventana,
        text="Asignar Técnico",
        width=20,
        command=guardar_asignacion
    )

    boton_asignar.pack(pady=15)

    # Botón cancelar
    boton_cancelar = tk.Button(
        ventana,
        text="Cancelar",
        width=20,
        bg="#A31A1A",
        fg="white",
        activebackground="#7F1511",
        activeforeground="white",
        command=ventana.destroy
    )

    boton_cancelar.pack()


# -------------------------
# CAMBIAR ESTADO
# -------------------------

def cambiar_estado(ticket_id=None, on_update=None):

    tickets = cargar_tickets()
    ticket_actual = None
    if ticket_id is not None:
        ticket_actual = next(
            (item for item in tickets if str(item.get("id")) == str(ticket_id)),
            None
        )
        if ticket_actual is None:
            messagebox.showerror("Error", "No se encontró el ticket seleccionado")
            return

    # Crear ventana
    ventana = tk.Toplevel()
    ventana.title("Cambiar Estado")
    ventana.geometry("450x300")

    # Título
    titulo = tk.Label(
        ventana,
        text="Cambiar Estado del Ticket",
        font=("Arial", 14)
    )
    titulo.pack(pady=10)

    # -------------------------
    # SELECCIONAR TICKET
    # -------------------------

    if ticket_actual is None:
        etiqueta_ticket = tk.Label(
            ventana,
            text="Seleccione el ticket:"
        )
        etiqueta_ticket.pack()

        opciones_tickets = []

        for ticket in tickets:
            texto = (
                f"Ticket #{ticket['id']} - "
                f"{ticket['activo']} - "
                f"{ticket['estado']}"
            )
            opciones_tickets.append(texto)

        combo_ticket = ttk.Combobox(
            ventana,
            values=opciones_tickets,
            state="readonly",
            width=40
        )

        combo_ticket.pack(pady=5)
    else:
        tk.Label(
            ventana,
            text=f"Ticket #{ticket_actual['id']} - {ticket_actual['activo']}"
        ).pack(pady=5)
        combo_ticket = None

    # -------------------------
    # SELECCIONAR ESTADO
    # -------------------------

    etiqueta_estado = tk.Label(
        ventana,
        text="Seleccione el nuevo estado:"
    )
    etiqueta_estado.pack(pady=5)

    opciones_estados = [
        "Pendiente",
        "En Proceso",
        "Resuelto"
    ]

    combo_estado = ttk.Combobox(
        ventana,
        values=opciones_estados,
        state="readonly",
        width=30
    )

    combo_estado.pack(pady=5)

    # -------------------------
    # GUARDAR CAMBIO
    # -------------------------

    def guardar_estado():

        nuevo_estado = combo_estado.get()

        # Verificar ticket
        if ticket_actual is None and combo_ticket.get() == "":
            messagebox.showerror(
                "Error",
                "Debe seleccionar un ticket"
            )
            return

        # Verificar estado
        if nuevo_estado == "":
            messagebox.showerror(
                "Error",
                "Debe seleccionar un estado"
            )
            return

        # Obtener ID del ticket
        if ticket_actual is None:
            parte_ticket = combo_ticket.get().split(" - ")[0]
            id_ticket_seleccionado = parte_ticket.replace("Ticket #", "")
        else:
            id_ticket_seleccionado = str(ticket_actual["id"])

        # Buscar y modificar ticket
        for ticket in tickets:

            if str(ticket["id"]) == id_ticket_seleccionado:

                ticket["estado"] = nuevo_estado

                break

        # Guardar cambios
        guardar_tickets(tickets)

        messagebox.showinfo(
            "Éxito",
            "Estado actualizado correctamente"
        )

        ventana.destroy()
        if on_update is not None:
            on_update()

    # Botón guardar
    boton_guardar = tk.Button(
        ventana,
        text="Guardar Estado",
        width=20,
        bg="#81C784",
        fg="white",
        activebackground="#388E3C",
        activeforeground="white",
        command=guardar_estado
    )

    boton_guardar.pack(pady=15)

    # Botón cancelar
    boton_cancelar = tk.Button(
        ventana,
        text="Cancelar",
        width=20,
        bg="#A31A1A",
        fg="white",
        activebackground="#7F1511",
        activeforeground="white",
        command=ventana.destroy
    )

    boton_cancelar.pack()

# -------------------------
# VENTANA PRINCIPAL TICKETS
# -------------------------

def abrir_ventana_tickets():

    ventana = tk.Toplevel()

    ventana.title("Gestión de Tickets")
    ventana.geometry("350x350")

    titulo = tk.Label(
        ventana,
        text="Módulo de Tickets",
        font=("Arial", 14))

    titulo.pack(pady=10)

    boton_mostrar = tk.Button(
        ventana,
        text="Mostrar Tickets",
        width=25,
        command=mostrar_tickets)

    boton_mostrar.pack(pady=5)

    boton_crear = tk.Button(
        ventana,
        text="Crear Ticket",
        width=25,
        bg="#81C784",
        fg="white",
        activebackground="#388E3C",
        activeforeground="white",
        command=crear_ticket)

    boton_crear.pack(pady=5)

    boton_asignar = tk.Button(
        ventana,
        text="Asignar Técnico",
        width=25,
        command=asignar_tecnico)

    boton_asignar.pack(pady=5)

    boton_estado = tk.Button(
        ventana,
        text="Cambiar Estado",
        width=25,
        command=cambiar_estado)

    boton_estado.pack(pady=5)

    boton_cerrar = tk.Button(
        ventana,
        text="Cerrar",
        width=25,
        bg="#A31A1A",
        fg="white",
        activebackground="#7F1511",
        activeforeground="white",
        command=ventana.destroy)

    boton_cerrar.pack(pady=15)