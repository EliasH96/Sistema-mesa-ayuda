import json
import tkinter as tk
import os


def abrir_ventana_tecnicos():

    ventana_tecnicos = tk.Toplevel()
    ventana_tecnicos.title("Técnicos")
    ventana_tecnicos.geometry("400x300")

    ruta = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "tecnicos.json"
    )

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            tecnicos = json.load(archivo)

    except (FileNotFoundError, json.JSONDecodeError):
        tk.Label(
            ventana_tecnicos,
            text="No se pudo leer tecnicos.json"
        ).pack(pady=20)
        return

    tk.Label(
        ventana_tecnicos,
        text="LISTADO DE TÉCNICOS",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    for tecnico in tecnicos:
        tk.Label(
            ventana_tecnicos,
            text=f'{tecnico["id"]} - {tecnico["nombre"]}'
        ).pack(pady=5)

    tk.Button(
        ventana_tecnicos,
        text="Cerrar",
        bg="#A31A1A",
        fg="white",
        activebackground="#7F1511",
        activeforeground="white",
        command=ventana_tecnicos.destroy
    ).pack(pady=15)
