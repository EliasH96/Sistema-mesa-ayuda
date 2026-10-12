import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from fpdf.errors import FPDFException

import modulo_activos
import modulo_tecnicos
import modulo_tickets
import modulo_reportes

# -------------------------
# VENTANA PRINCIPAL
# -------------------------

ventana = tk.Tk()

ventana.title("Sistema Help Desk")
ventana.geometry("1200x600")
ventana.minsize(850, 400)
ventana.configure(bg="#FAF7F8")

estilo = ttk.Style(ventana)
estilo.theme_use("clam")
estilo.configure(
    "Pastel.Vertical.TScrollbar",
    background="#694357",
    troughcolor="#F8E8EF",
    bordercolor="#F8E8EF",
    lightcolor="#F8E8EF",
    darkcolor="#F8E8EF",
    arrowcolor="#694357"
)
# -------------------------
# BARRA SUPERIOR
# -------------------------

barra_menu = tk.Frame(
    ventana,
    bg="#F8E8EF",
    height=50)

barra_menu.pack(fill="x")
barra_menu.pack_propagate(False)


# Nombre del sistema
titulo = tk.Label(
    barra_menu,
    text="Gestión de soporte técnico",
    bg="#F8E8EF",
    fg="#694357",
    font=("Arial", 14, "bold")
)

titulo.pack(side="left", padx=15)


# -------------------------
# MENU VER
# -------------------------

menu_ver = tk.Menu(
    ventana,
    tearoff=0,
    bg="#F8E8EF",
    fg="#694357",
    activebackground="#EBCFD9",
    activeforeground="#694357"
)

menu_ver.add_command(
    label="Ver activos",
    command=modulo_activos.abrir_ventana_activos
)

menu_ver.add_command(
    label="Ver técnicos",
    command=modulo_tecnicos.abrir_ventana_tecnicos
)

def mostrar_menu_ver():
    try:
        menu_ver.tk_popup(
            boton_ver.winfo_rootx(),
            boton_ver.winfo_rooty() + boton_ver.winfo_height()
        )
    finally:
        menu_ver.grab_release()


# Botón para mostrar las opciones de consulta
boton_ver = tk.Button(
    barra_menu,
    text="Ver ▼",
    bg="#F8E8EF",
    fg="#694357",
    activebackground="#EBCFD9",
    activeforeground="#694357",
    font=("Arial", 10),
    relief="flat",
    command=mostrar_menu_ver,
    padx=12,
    pady=5
)

boton_ver.pack(side="left", padx=3)


# -------------------------
# Botón de acción directa para abrir el formulario
boton_crear = tk.Button(
    barra_menu,
    text="Crear ticket",
    bg="#81C784",
    fg="white",
    activebackground="#388E3C",
    activeforeground="white",
    font=("Arial", 10),
    relief="flat",
    command=lambda: modulo_tickets.crear_ticket(on_update=actualizar_grilla),
    padx=12,
    pady=5
)

boton_crear.pack(side="left", padx=3)

# -------------------------
# PANELES DE TICKETS
# -------------------------

panel_principal = tk.Frame(
    ventana,
    bg="#FAF7F8",
)
panel_principal.pack(fill="both", expand=True, padx=20, pady=20)

tabla_contenedor = tk.Frame(panel_principal, bg="#FAF7F8")
tabla_contenedor.pack(fill="both", expand=True)

tabla_canvas = tk.Canvas(
    tabla_contenedor,
    bg="#FAF7F8",
    highlightthickness=0
)
barra_vertical = ttk.Scrollbar(
    tabla_contenedor,
    orient="vertical",
    command=tabla_canvas.yview,
    style="Pastel.Vertical.TScrollbar"
)
tabla_canvas.configure(
    yscrollcommand=barra_vertical.set
)

tabla_canvas.grid(row=0, column=0, sticky="nsew")
barra_vertical.grid(row=0, column=1, sticky="ns")
tabla_contenedor.grid_rowconfigure(0, weight=1)
tabla_contenedor.grid_columnconfigure(0, weight=1)

tabla = tk.Frame(tabla_canvas, bg="#FAF7F8")
tabla_canvas.create_window((0, 0), window=tabla, anchor="nw")


def desplazar_con_rueda(evento):
    widget = evento.widget
    while widget is not None and widget is not tabla_canvas:
        widget = getattr(widget, "master", None)

    if widget is None:
        return

    if getattr(evento, "num", None) == 4:
        unidades = -1
    elif getattr(evento, "num", None) == 5:
        unidades = 1
    else:
        delta = getattr(evento, "delta", 0)
        unidades = -int(delta / 120) if abs(delta) >= 120 else (-1 if delta > 0 else 1)

    tabla_canvas.yview_scroll(unidades, "units")
    return "break"


ventana.bind_all("<MouseWheel>", desplazar_con_rueda)
ventana.bind_all("<Button-4>", desplazar_con_rueda)
ventana.bind_all("<Button-5>", desplazar_con_rueda)

encabezados_datos = (
    ("ID", 5),
    ("Activo", 10),
    ("Descripción", 35),
    ("Técnico", 12),
    ("Estado", 11),
)

seleccionados_ids: set[str] = set()
anchos_columnas = [60, 120, 420, 150, 130]

colores_estado = {
    "Pendiente": "#EEEEEE",
    "En Proceso": "#FFF4CC",
    "Resuelto": "#DDF2E1",
}


def crear_grilla_filas(
    parent,
    tickets,
    grupos_columnas,
    seleccionable=False,
    al_seleccionar=None
):
    columnas = ("ID", "Activo", "Descripción", "Técnico", "Estado")
    celdas_por_columna = [[] for _ in columnas]
    celdas_por_ticket = {}

    for columna in range(len(columnas)):
        parent.grid_columnconfigure(
            columna,
            minsize=anchos_columnas[columna],
            weight=1 if columna == 2 else 0
        )

    for columna, titulo_columna in enumerate(columnas):
        encabezado = tk.Label(
            parent,
            text=titulo_columna,
            bg="#EBCFD9",
            fg="#694357",
            font=("Arial", 10, "bold"),
            anchor="w",
            padx=5,
            pady=7,
            width=1,
            cursor="sb_h_double_arrow"
        )
        encabezado.grid(row=0, column=columna, sticky="nsew", padx=1, pady=1)
        celdas_por_columna[columna].append(encabezado)

        def comenzar_ajuste(evento, indice=columna):
            if evento.x >= evento.widget.winfo_width() - 6:
                evento.widget._ajuste_columna = indice
                evento.widget._x_inicio_ajuste = evento.x_root
                evento.widget._ancho_inicio_ajuste = anchos_columnas[indice]

        def ajustar_columna(evento, encabezado_widget=encabezado):
            indice = getattr(encabezado_widget, "_ajuste_columna", None)
            if indice is None:
                return
            ancho = max(
                50,
                encabezado_widget._ancho_inicio_ajuste
                + evento.x_root
                - encabezado_widget._x_inicio_ajuste
            )
            anchos_columnas[indice] = ancho
            for grupo in grupos_columnas:
                grupo[0].master.grid_columnconfigure(indice, minsize=ancho)
                for celda in grupo[indice]:
                    if indice == 2:
                        celda.configure(wraplength=max(50, ancho - 12))
            encabezado_widget._ancho_inicio_ajuste = ancho
            encabezado_widget._x_inicio_ajuste = evento.x_root

        def finalizar_ajuste(evento):
            if hasattr(evento.widget, "_ajuste_columna"):
                del evento.widget._ajuste_columna

        encabezado.bind("<Button-1>", comenzar_ajuste)
        encabezado.bind("<B1-Motion>", ajustar_columna)
        encabezado.bind("<ButtonRelease-1>", finalizar_ajuste)

    for fila, ticket in enumerate(tickets, start=1):
        ticket_id = str(ticket.get("id", ""))
        color_fila = colores_estado.get(ticket.get("estado"), "#FFFFFF")
        valores = (
            ticket.get("id", "-"),
            ticket.get("activo", "-"),
            ticket.get("descripcion", "-"),
            ticket.get("tecnico") or "Sin asignar",
            ticket.get("estado", "-"),
        )

        for columna, valor in enumerate(valores):
            celda = tk.Label(
                parent,
                text=valor,
                bg=color_fila,
                fg="#493B43",
                anchor="w",
                justify="left",
                wraplength=max(50, anchos_columnas[columna] - 12)
                if columna == 2 else 0,
                padx=5,
                pady=6,
                width=1
            )
            celda.grid(row=fila, column=columna, sticky="nsew", padx=1, pady=1)
            celdas_por_columna[columna].append(celda)
            celdas_por_ticket.setdefault(ticket_id, []).append(celda)

            if seleccionable and al_seleccionar is not None:
                def alternar(evento, actual_id=ticket_id):
                    al_seleccionar(actual_id, evento)
                    return "break"

                celda.bind("<Button-1>", alternar)

        if seleccionable and ticket_id in seleccionados_ids:
            for celda in celdas_por_ticket[ticket_id]:
                celda.configure(bg="#DCCBD6")

    grupos_columnas.append(celdas_por_columna)
    return celdas_por_ticket


def actualizar_grilla():
    for widget in tabla.winfo_children():
        widget.destroy()

    columnas_datos = len(encabezados_datos)

    try:
        tickets = modulo_tickets.cargar_tickets()
        tecnicos = modulo_tickets.cargar_tecnicos()
    except (OSError, ValueError) as error:
        tk.Label(
            tabla,
            text=f"No se pudieron cargar los tickets o técnicos: {error}",
            bg="#FAF7F8",
            fg="#A31A1A",
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        return

    tk.Label(
        tabla,
        text="Todos los tickets",
        bg="#FAF7F8",
        fg="#493B43",
        font=("Arial", 16, "bold")
    ).grid(row=0, column=0, sticky="w", pady=(4, 8))

    tabla_todos = tk.Frame(tabla, bg="#FAF7F8")
    tabla_todos.grid(row=1, column=0, sticky="w")

    encabezados_todos = encabezados_datos + (("Acción", 14),)
    for columna, (texto, ancho) in enumerate(encabezados_todos):
        tk.Label(
            tabla_todos,
            text=texto,
            width=ancho,
            bg="#EBCFD9",
            fg="#493B43",
            font=("Arial", 10, "bold"),
            anchor="w",
            padx=5,
            pady=7
        ).grid(row=0, column=columna, sticky="nsew", padx=1, pady=1)

    tickets_incompletos = [
        ticket for ticket in tickets
        if not str(ticket.get("tecnico", "")).strip()
    ]

    if tickets:
        for fila, ticket in enumerate(tickets, start=1):
            color_fila = colores_estado.get(ticket.get("estado"), "#FFFFFF")
            valores = (
                ticket.get("id", "-"),
                ticket.get("activo", "-"),
                ticket.get("descripcion", "-"),
                ticket.get("tecnico") or "Sin asignar",
                ticket.get("estado", "-"),
            )

            for columna, valor in enumerate(valores):
                tk.Label(
                    tabla_todos,
                    text=valor,
                    width=encabezados_datos[columna][1],
                    bg=color_fila,
                    fg="#493B43",
                    anchor="w",
                    justify="left",
                    wraplength=240,
                    padx=5,
                    pady=6
                ).grid(row=fila, column=columna, sticky="nsew", padx=1, pady=1)

            tk.Button(
                tabla_todos,
                text="Cambiar estado",
                width=14,
                bg=color_fila,
                activebackground=color_fila,
                command=lambda current_id=ticket.get("id"): modulo_tickets.cambiar_estado(
                    ticket_id=current_id,
                    on_update=actualizar_grilla
                )
            ).grid(row=fila, column=columnas_datos, padx=4, pady=3)
    else:
        tk.Label(
            tabla_todos,
            text="No hay tickets registrados.",
            bg="#FAF7F8",
            fg="#6F646A",
            anchor="w",
            padx=8,
            pady=12
        ).grid(
            row=1,
            column=0,
            columnspan=len(encabezados_todos),
            sticky="w"
        )

    tk.Label(
        tabla,
        text="Tickets nuevos sin técnico asignado",
        bg="#FAF7F8",
        fg="#493B43",
        font=("Arial", 16, "bold")
    ).grid(row=2, column=0, sticky="w", pady=(24, 8))

    tabla_asignacion = tk.Frame(tabla, bg="#FAF7F8")
    tabla_asignacion.grid(row=3, column=0, sticky="w")

    encabezados_asignacion = encabezados_datos + (
        ("Asignar técnico", 18),
        ("Acción", 8),
    )
    for columna, (texto, ancho) in enumerate(encabezados_asignacion):
        tk.Label(
            tabla_asignacion,
            text=texto,
            width=ancho,
            bg="#EBCFD9",
            fg="#493B43",
            font=("Arial", 10, "bold"),
            anchor="w",
            padx=5,
            pady=7
        ).grid(row=0, column=columna, sticky="nsew", padx=1, pady=1)

    if not tickets_incompletos:
        tk.Label(
            tabla_asignacion,
            text="No hay tickets pendientes de asignación.",
            bg="#FAF7F8",
            fg="#6F646A",
            anchor="w",
            padx=8,
            pady=12
        ).grid(row=1, column=0, columnspan=len(encabezados_asignacion), sticky="w")

    opciones_tecnicos = [
        f"{tecnico['id']} - {tecnico['nombre']}"
        for tecnico in tecnicos
    ]

    for fila, ticket in enumerate(tickets_incompletos, start=1):
        valores = (
            ticket.get("id", "-"),
            ticket.get("activo", "-"),
            ticket.get("descripcion", "-"),
            ticket.get("tecnico") or "Sin asignar",
            ticket.get("estado", "-"),
        )

        for columna, valor in enumerate(valores):
            tk.Label(
                tabla_asignacion,
                text=valor,
                width=encabezados_datos[columna][1],
                bg="white",
                fg="#493B43",
                anchor="w",
                justify="left",
                wraplength=240,
                padx=5,
                pady=6
            ).grid(row=fila, column=columna, sticky="nsew", padx=1, pady=1)

        selector_tecnico = ttk.Combobox(
            tabla_asignacion,
            values=opciones_tecnicos,
            state="readonly",
            width=18
        )
        selector_tecnico.grid(row=fila, column=columnas_datos, padx=4, pady=3)

        tk.Button(
            tabla_asignacion,
            text="Asignar",
            width=8,
            command=lambda current_id=ticket.get("id"), selector=selector_tecnico: modulo_tickets.asignar_tecnico(
                ticket_id=current_id,
                tecnico_id=selector.get().split(" - ", 1)[0] if selector.get() else "",
                on_update=actualizar_grilla
            )
        ).grid(row=fila, column=columnas_datos + 1, padx=4, pady=3)

    encabezado_reporte = tk.Frame(tabla, bg="#FAF7F8")
    encabezado_reporte.grid(row=4, column=0, sticky="ew", pady=(24, 8))
    tk.Label(
        encabezado_reporte,
        text="Reporte de todos los tickets",
        bg="#FAF7F8",
        fg="#493B43",
        font=("Arial", 16, "bold")
    ).pack(side="left")
    tk.Button(
        encabezado_reporte,
        text="Ver resumen",
        command=modulo_reportes.abrir_ventana_reportes
    ).pack(side="right")

    grupos_columnas = []
    tabla_reporte = tk.Frame(tabla, bg="white")
    tabla_reporte.grid(row=5, column=0, sticky="w")
    crear_grilla_filas(tabla_reporte, tickets, grupos_columnas)

    encabezado_listos = tk.Frame(tabla, bg="#FAF7F8")
    encabezado_listos.grid(row=6, column=0, sticky="ew", pady=(24, 8))
    tk.Label(
        encabezado_listos,
        text="Tickets listos",
        bg="#FAF7F8",
        fg="#493B43",
        font=("Arial", 16, "bold")
    ).pack(side="left")

    tickets_listos = [
        ticket for ticket in tickets
        if all(
            str(ticket.get(clave, "")).strip()
            for clave in ("id", "activo", "descripcion", "tecnico", "estado")
        )
    ]
    ids_listos = {str(ticket["id"]) for ticket in tickets_listos}
    seleccionados_ids.intersection_update(ids_listos)

    boton_imprimir = tk.Button(
        encabezado_listos,
        text="\U0001F5A8 Imprimir",
        state="disabled",
        bg="#EEEEEE",
        fg="black",
        disabledforeground="black",
        activebackground="#C8C8C8",
        activeforeground="black",
        command=lambda: None
    )
    boton_imprimir.pack(side="right")

    boton_eliminar = tk.Button(
        encabezado_listos,
        text="Eliminar",
        state="disabled",
        bg="#A31A1A",
        fg="white",
        disabledforeground="white",
        activebackground="#7F1511",
        activeforeground="white",
        command=lambda: None
    )
    boton_eliminar.pack(side="right", padx=(0, 8))

    tk.Label(
        tabla,
        text="Usa Ctrl + clic izquierdo para seleccionar varios tickets.",
        bg="#FAF7F8",
        fg="#6F646A",
        font=("Arial", 9)
    ).grid(row=7, column=0, sticky="w", pady=(0, 4))

    def sincronizar_seleccion():
        hay_seleccion = bool(seleccionados_ids)
        boton_imprimir.configure(
            state="normal" if hay_seleccion else "disabled",
            bg="#C8C8C8" if hay_seleccion else "#EEEEEE",
            fg="black",
            activebackground="#AFAFAF" if hay_seleccion else "#EEEEEE"
        )
        boton_eliminar.configure(
            state="normal" if hay_seleccion else "disabled"
        )

    def alternar_seleccion_manual(ticket_id, evento):
        control_presionado = bool(evento.state & 0x0004)

        if control_presionado:
            if ticket_id in seleccionados_ids:
                seleccionados_ids.remove(ticket_id)
            else:
                seleccionados_ids.add(ticket_id)
        elif ticket_id in seleccionados_ids:
            seleccionados_ids.remove(ticket_id)
        else:
            seleccionados_ids.clear()
            seleccionados_ids.add(ticket_id)

        for ticket in tickets_listos:
            actual_id = str(ticket["id"])
            color_fila = colores_estado.get(ticket.get("estado"), "#FFFFFF")
            color = "#DCCBD6" if actual_id in seleccionados_ids else color_fila
            for celda in celdas_listos[actual_id]:
                celda.configure(bg=color)
        sincronizar_seleccion()

    def imprimir_tickets_seleccionados():
        if not seleccionados_ids:
            return

        ruta_pdf = filedialog.asksaveasfilename(
            title="Guardar tickets listos como PDF",
            defaultextension=".pdf",
            initialfile="tickets_listos.pdf",
            filetypes=(("Documento PDF", "*.pdf"),)
        )
        if not ruta_pdf:
            return

        try:
            tickets_actualizados = modulo_tickets.cargar_tickets()
            tickets_seleccionados = [
                ticket for ticket in tickets_actualizados
                if str(ticket.get("id")) in seleccionados_ids
                and all(
                    str(ticket.get(clave, "")).strip()
                    for clave in ("id", "activo", "descripcion", "tecnico", "estado")
                )
            ]
            if not tickets_seleccionados:
                messagebox.showerror(
                    "Error",
                    "Los tickets seleccionados ya no están completos."
                )
                actualizar_grilla()
                return

            modulo_reportes.generar_pdf_tickets(tickets_seleccionados, ruta_pdf)
        except (OSError, ValueError, FPDFException) as error:
            messagebox.showerror("Error al generar el PDF", str(error))
            return

        messagebox.showinfo(
            "PDF generado",
            f"Se guardó el PDF para imprimir en:\n{ruta_pdf}"
        )

    def eliminar_tickets_seleccionados():
        if not seleccionados_ids:
            return

        ids_a_eliminar = sorted(seleccionados_ids)
        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Eliminar los tickets seleccionados?\n\n"
            f"ID: {', '.join(ids_a_eliminar)}\n\n"
            "Esta acción no se puede deshacer."
        )
        if not confirmacion:
            return

        try:
            cantidad_eliminada = modulo_tickets.eliminar_tickets(ids_a_eliminar)
        except (OSError, ValueError) as error:
            messagebox.showerror("Error al eliminar tickets", str(error))
            return

        if not cantidad_eliminada:
            messagebox.showerror(
                "Error",
                "No se encontró ninguno de los tickets seleccionados."
            )
            actualizar_grilla()
            return

        seleccionados_ids.clear()
        messagebox.showinfo(
            "Tickets eliminados",
            f"Se eliminaron {cantidad_eliminada} ticket(s)."
        )
        actualizar_grilla()

    tabla_listos = tk.Frame(tabla, bg="white")
    tabla_listos.grid(row=8, column=0, sticky="w")
    celdas_listos = crear_grilla_filas(
        tabla_listos,
        tickets_listos,
        grupos_columnas,
        seleccionable=True,
        al_seleccionar=alternar_seleccion_manual
    )
    boton_imprimir.configure(command=imprimir_tickets_seleccionados)
    boton_eliminar.configure(command=eliminar_tickets_seleccionados)
    sincronizar_seleccion()

    tabla.update_idletasks()
    tabla_canvas.configure(scrollregion=tabla_canvas.bbox("all"))


actualizar_grilla()


# -------------------------
# CERRAR APLICACION
# -------------------------

ventana.protocol(
    "WM_DELETE_WINDOW",
    ventana.destroy)

# Iniciar el programa
ventana.mainloop()