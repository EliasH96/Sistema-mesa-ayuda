import json
import os
import tkinter as tk


def abrir_ventana_activos():
    ventana_activos = tk.Toplevel()
    ventana_activos.title("Activos")
    ventana_activos.geometry("400x300")

    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "activos.json")

    if not os.path.exists(ruta):
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump([], archivo, indent=4, ensure_ascii=False)

    with open(ruta, "r", encoding="utf-8") as archivo:
        activos = json.load(archivo)

    tk.Label(
        ventana_activos,
        text="LISTADO DE ACTIVOS",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    if not activos:
        tk.Label(
            ventana_activos,
            text="No hay activos registrados."
        ).pack(pady=10)

    for activo in activos:
        tk.Label(
            ventana_activos,
            text=f'{activo["id"]} - {activo["nombre"]}'
        ).pack(pady=5)

    tk.Button(
        ventana_activos,
        text="Cerrar",
        bg="#A31A1A",
        fg="white",
        activebackground="#7F1511",
        activeforeground="white",
        command=ventana_activos.destroy
    ).pack(pady=10)