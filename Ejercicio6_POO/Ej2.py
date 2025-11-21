import tkinter as tk
from tkinter import messagebox
import pygame
import math
import time
import threading

# -------------------------------------------------------------------------
# CLASES
# -------------------------------------------------------------------------

class Caja:
    def __init__(self, peso):
        self.peso = float(peso)

    def __str__(self):
        return f"Caja ({self.peso} kg)"


class Camion:
    def __init__(self, matricula, modelo, velocidad=0, rumbo=0, cajas=None):
        if not (0 <= rumbo < 360):
            raise ValueError("El rumbo debe estar entre 0 y 359.")

        self.matricula = matricula
        self.modelo = modelo
        self.velocidad = float(velocidad)
        self.rumbo = float(rumbo)
        self.x = 100
        self.y = 100

        self.width = 40
        self.height = 20

        if cajas is None:
            self.cajas = []
        else:
            self.cajas = list(cajas)

    def add_caja(self, caja):
        self.cajas.append(caja)

    def total_carga(self):
        return sum(c.peso for c in self.cajas)

    def mover(self):
        ang_rad = math.radians(self.rumbo)
        self.x += math.cos(ang_rad) * self.velocidad
        self.y -= math.sin(ang_rad) * self.velocidad

    def __str__(self):
        return (f"CAMIÓN {self.matricula}\n"
                f"Modelo: {self.modelo}\n"
                f"Velocidad: {self.velocidad}\n"
                f"Rumbo: {self.rumbo}°\n"
                f"Nº cajas: {len(self.cajas)}\n"
                f"Peso total: {self.total_carga()} kg\n"
                f"Pos: ({int(self.x)}, {int(self.y)})")


# -------------------------------------------------------------------------
# APLICACIÓN
# -------------------------------------------------------------------------

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Camiones")

        # -------- GRID RESPONSIVE --------
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)

        for i in range(30):
            self.root.rowconfigure(i, weight=1)

        # -------- AUDIO --------
        try:
            pygame.mixer.init(devicename=None)
        except:
            print("Audio no disponible.")

        # -------- LISTA --------
        self.camiones = []
        self.camion_activo = None

        # -------- CANVAS --------
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=30, sticky="nsew")

        self.iconos_canvas = {}

        # -------- PANEL LATERAL --------
        panel = tk.Frame(root)
        panel.grid(row=0, column=1, rowspan=30, sticky="nsew")
        panel.columnconfigure(0, weight=1)

        tk.Label(panel, text="Camiones").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.lista = tk.Listbox(panel, height=6)
        self.lista.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.lista.bind("<<ListboxSelect>>", self.seleccionar_camion)

        tk.Label(panel, text="Velocidad:").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.vel_entry = tk.Entry(panel)
        self.vel_entry.grid(row=3, column=0, sticky="we", padx=10, pady=2)

        tk.Label(panel, text="Rumbo (0-359):").grid(row=4, column=0, sticky="w", padx=10, pady=2)
        self.rumbo_entry = tk.Entry(panel)
        self.rumbo_entry.grid(row=5, column=0, sticky="we", padx=10, pady=2)

        tk.Button(panel, text="Actualizar", command=self.actualizar_camion)\
            .grid(row=6, column=0, sticky="we", padx=10, pady=5)

        tk.Label(panel, text="Peso de nueva caja:").grid(row=7, column=0, sticky="w", padx=10, pady=2)
        self.caja_entry = tk.Entry(panel)
        self.caja_entry.grid(row=8, column=0, sticky="we", padx=10, pady=2)

        tk.Button(panel, text="Añadir Caja", command=self.agregar_caja)\
            .grid(row=9, column=0, sticky="we", padx=10, pady=5)

        tk.Label(panel, text="--- NUEVO CAMIÓN ---").grid(row=10, column=0, padx=10, pady=10)

        tk.Label(panel, text="Matrícula:").grid(row=11, column=0, sticky="w", padx=10)
        self.matricula_n = tk.Entry(panel)
        self.matricula_n.grid(row=12, column=0, sticky="we", padx=10, pady=2)

        tk.Label(panel, text="Modelo:").grid(row=13, column=0, sticky="w", padx=10)
        self.modelo_n = tk.Entry(panel)
        self.modelo_n.grid(row=14, column=0, sticky="we", padx=10, pady=2)

        tk.Button(panel, text="Crear Camión", command=self.crear_camion)\
            .grid(row=15, column=0, sticky="we", padx=10, pady=5)

        tk.Button(panel, text="Mostrar Información", command=self.mostrar_info)\
            .grid(row=16, column=0, sticky="we", padx=10, pady=5)

        tk.Button(panel, text="Tocar Claxon", command=self.claxon)\
            .grid(row=17, column=0, sticky="we", padx=10, pady=5)

        # ---------- ANIMACIÓN ----------
        self.animando = True
        threading.Thread(target=self.animar, daemon=True).start()

    # ---------------------------------------------------------------------
    # FUNCIONES
    # ---------------------------------------------------------------------

    def crear_camion(self):
        matricula = self.matricula_n.get().strip()
        modelo = self.modelo_n.get().strip()
        if not matricula or not modelo:
            messagebox.showerror("Error", "Debe introducir matrícula y modelo.")
            return

        nuevo = Camion(matricula, modelo, velocidad=0, rumbo=0)
        self.camiones.append(nuevo)
        self.lista.insert(tk.END, matricula)

        self.crear_icono(nuevo)

        self.matricula_n.delete(0, tk.END)
        self.modelo_n.delete(0, tk.END)

    def seleccionar_camion(self, event=None):
        if not self.lista.curselection():
            return
        idx = self.lista.curselection()[0]
        self.camion_activo = self.camiones[idx]

        self.vel_entry.delete(0, tk.END)
        self.vel_entry.insert(0, self.camion_activo.velocidad)

        self.rumbo_entry.delete(0, tk.END)
        self.rumbo_entry.insert(0, self.camion_activo.rumbo)

    def actualizar_camion(self):
        if not self.camion_activo:
            return
        try:
            self.camion_activo.velocidad = float(self.vel_entry.get())
            rumbo = float(self.rumbo_entry.get())
            if not (0 <= rumbo < 360):
                raise ValueError
            self.camion_activo.rumbo = rumbo
        except:
            messagebox.showerror("Error", "Valores inválidos.")

    def agregar_caja(self):
        if not self.camion_activo:
            return
        try:
            peso = float(self.caja_entry.get())
            self.camion_activo.add_caja(Caja(peso))
            self.caja_entry.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "Peso inválido.")

    def mostrar_info(self):
        if not self.camion_activo:
            return
        messagebox.showinfo("Información", str(self.camion_activo))

    def claxon(self):
        try:
            pygame.mixer.music.load("claxon.mp3")
            pygame.mixer.music.play()
        except:
            messagebox.showerror("Error", "No se pudo reproducir claxon.mp3.")

    # ---------------------------------------------------------------------
    # CANVAS Y REBOTE
    # ---------------------------------------------------------------------

    def crear_icono(self, camion):
        rect = self.canvas.create_rectangle(camion.x, camion.y,
                                            camion.x + camion.width,
                                            camion.y + camion.height,
                                            fill="blue")
        self.iconos_canvas[camion] = rect

    def mover_icono(self, camion):
        self.canvas.coords(self.iconos_canvas[camion],
                           camion.x, camion.y,
                           camion.x + camion.width, camion.y + camion.height)

    # ---------------------------------------------------------------------
    # ANIMACIÓN
    # ---------------------------------------------------------------------

    def animar(self):
        while self.animando:
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()

            for camion in self.camiones:
                camion.mover()

                # Rebote horizontal
                if camion.x <= 0 or camion.x + camion.width >= w:
                    camion.rumbo = (180 - camion.rumbo) % 360

                # Rebote vertical
                if camion.y <= 0 or camion.y + camion.height >= h:
                    camion.rumbo = (-camion.rumbo) % 360

                self.mover_icono(camion)

            time.sleep(0.03)


# -------------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------------
root = tk.Tk()
app = App(root)
root.mainloop()
