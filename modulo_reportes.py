import tkinter as tk
import json
import os
from fpdf import FPDF, FontFace


def generar_pdf_tickets(tickets, ruta_destino):
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_margins(10, 10, 10)
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(
        0,
        10,
        "Tickets listos para imprimir",
        new_x="LMARGIN",
        new_y="NEXT",
        align="C"
    )
    pdf.ln(3)

    encabezados = ("ID", "Activo", "Descripción", "Técnico", "Estado")
    colores_estado = {
        "Pendiente": (238, 238, 238),
        "En Proceso": (255, 244, 204),
        "Resuelto": (221, 242, 225),
    }

    with pdf.table(
        width=277,
        col_widths=(0.08, 0.13, 0.41, 0.20, 0.18),
        line_height=7,
        padding=2,
        text_align="LEFT",
        headings_style=FontFace(
            emphasis="B",
            color=(255, 255, 255),
            fill_color=(105, 67, 87)
        )
    ) as tabla:
        fila_encabezados = tabla.row()
        for encabezado in encabezados:
            fila_encabezados.cell(encabezado)

        for ticket in tickets:
            estilo_fila = FontFace(
                fill_color=colores_estado.get(
                    ticket.get("estado"),
                    (255, 255, 255)
                )
            )
            fila = tabla.row()
            for clave in ("id", "activo", "descripcion", "tecnico", "estado"):
                fila.cell(str(ticket.get(clave, "")), style=estilo_fila)

    pdf.output(ruta_destino)


def abrir_ventana_reportes():

    # Obtener la ruta de tickets.json
    carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(carpeta, "tickets.json")

    # Crear la ventana
    ventana_reportes = tk.Toplevel()
    ventana_reportes.title("Reportes de tickets")
    ventana_reportes.geometry("400x300")

    # Leer los tickets
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            tickets = json.load(archivo)

    except FileNotFoundError:
        tk.Label(
            ventana_reportes,
            text="No se encontró el archivo tickets.json"
        ).pack(pady=20)
        return

    except json.JSONDecodeError:
        tk.Label(
            ventana_reportes,
            text="El archivo tickets.json contiene un error."
        ).pack(pady=20)
        return

    # Contar los tickets según su estado
    pendientes = 0
    en_proceso = 0
    resueltos = 0

    for ticket in tickets:
        estado = ticket.get("estado", "")

        if estado == "Pendiente":
            pendientes += 1

        elif estado == "En Proceso":
            en_proceso += 1

        elif estado == "Resuelto":
            resueltos += 1

    # Mostrar el reporte
    tk.Label(
        ventana_reportes,
        text="REPORTE DE TICKETS",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    tk.Label(
        ventana_reportes,
        text=f"Total de tickets: {len(tickets)}"
    ).pack(pady=5)

    tk.Label(
        ventana_reportes,
        text=f"Pendientes: {pendientes}",
        bg="lightgray",
        width=30
    ).pack(pady=5)

    tk.Label(
        ventana_reportes,
        text=f"En proceso: {en_proceso}",
        bg="yellow",
        width=30
    ).pack(pady=5)

    tk.Label(
        ventana_reportes,
        text=f"Resueltos: {resueltos}",
        bg="lightgreen",
        width=30
    ).pack(pady=5)

    tk.Button(
        ventana_reportes,
        text="Cerrar",
        bg="#A31A1A",
        fg="white",
        activebackground="#7F1511",
        activeforeground="white",
        command=ventana_reportes.destroy
    ).pack(pady=15)
