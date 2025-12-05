import tkinter as tk
from tkinter import ttk, messagebox

#   CLASES LÓGICAS

class Capitan:
    def __init__(self, nombre, rango):
        self.nombre = nombre
        self.rango = rango

    def __str__(self):
        return f"{self.rango} {self.nombre}"


class PlataformaNaval:
    def __init__(self, nombre, desplazamiento, x, y):
        self.nombre = nombre
        self.desplazamiento = desplazamiento
        self.integridad = 100
        self.capitan = None
        self.x = x
        self.y = y

    def asumir_mando(self, capitan):
        self.capitan = capitan

    def navegar(self, dx, dy):
        self.x += dx
        self.y += dy

    def recibir_danio(self, d):
        self.integridad = max(0, self.integridad - d)

    def esta_operativa(self):
        return self.integridad > 0


class Fragata(PlataformaNaval):
    def __init__(self, n, d, x, y):
        super().__init__(n, d, x, y)
        self.helicopteros = 1

    def despegar_helicoptero(self):
        if self.helicopteros > 0:
            self.helicopteros -= 1
        else:
            print("No quedan helicópteros.")


class Corbeta(PlataformaNaval):
    def __init__(self, n, d, x, y):
        super().__init__(n, d, x, y)
        self.velocidad_max = 28


class Submarino(PlataformaNaval):
    def __init__(self, n, d, x, y):
        super().__init__(n, d, x, y)
        self.profundidad = 0

    def sumergirse(self, m):
        self.profundidad = m

#   INTERFAZ GRÁFICA CON TKINTER

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Naval")

        # --- Canvas para mostrar la flota ---
        self.canvas = tk.Canvas(root, width=700, height=500, bg="lightblue")
        self.canvas.grid(row=0, column=0, rowspan=10)

        # Lista de plataformas
        self.plataformas = []
        self.iconos = {}  # Mapa: plataforma -> id de objeto en canvas
        self.plataforma_activa = None

        # Interfaz lateral
        self.crear_panel_lateral()

        # Cargar datos iniciales
        self.crear_escenario()

        # Vincular clic del mouse
        self.canvas.bind("<Button-1>", self.detectar_click)

        # Dibujar plataformas
        self.actualizar_canvas()

    # PANEL LATERAL
    def crear_panel_lateral(self):
        ttk.Label(self.root, text="Plataforma activa:").grid(row=0, column=1)
        self.selector = ttk.Combobox(self.root, state="readonly")
        self.selector.grid(row=1, column=1)
        self.selector.bind("<<ComboboxSelected>>", self.cambiar_plataforma)

        # Movimiento
        ttk.Label(self.root, text="Mover: dx, dy").grid(row=2, column=1)
        self.dx = tk.Entry(self.root, width=5)
        self.dy = tk.Entry(self.root, width=5)
        self.dx.grid(row=3, column=1, sticky="w")
        self.dy.grid(row=3, column=1, sticky="e")
        ttk.Button(self.root, text="Mover", command=self.mover).grid(row=4, column=1)

        # Daño
        ttk.Label(self.root, text="Recibir daño (%)").grid(row=5, column=1)
        self.danio = tk.Entry(self.root, width=5)
        self.danio.grid(row=6, column=1)
        ttk.Button(self.root, text="Aplicar daño", command=self.aplicar_danio).grid(row=7, column=1)

        # Acciones especiales
        ttk.Button(self.root, text="Sumergir (Submarino)", command=self.sumergir).grid(row=8, column=1)
        ttk.Button(self.root, text="Despegar Helicóptero (Fragata)", command=self.despegar_helicoptero).grid(row=9, column=1)

    # ESCENARIO INICIAL
    def crear_escenario(self):
        f = Fragata("Fragata F-101", 5800, 100, 100)
        c = Corbeta("Corbeta C-35", 1700, 300, 200)
        s = Submarino("Submarino S-80", 3000, 200, 350)

        self.plataformas = [f, c, s]
        self.selector["values"] = [p.nombre for p in self.plataformas]

    # DIBUJAR PLATAFORMAS
    def actualizar_canvas(self):
        self.canvas.delete("all")
        self.iconos.clear()

        for p in self.plataformas:
            if isinstance(p, Fragata):
                color = "green"
                r = 18
            elif isinstance(p, Corbeta):
                color = "yellow"
                r = 14
            else:
                color = "gray"
                r = 16

            obj = self.canvas.create_oval(
                p.x - r, p.y - r, p.x + r, p.y + r,
                fill=color
            )
            self.canvas.create_text(p.x, p.y - r - 10, text=p.nombre)
            self.iconos[obj] = p

    # SELECCIÓN CON EL RATÓN
    def detectar_click(self, event):
        obj = self.canvas.find_closest(event.x, event.y)[0]
        if obj in self.iconos:
            self.plataforma_activa = self.iconos[obj]
            self.selector.set(self.plataforma_activa.nombre)

    # SELECCIÓN POR COMBOBOX
    def cambiar_plataforma(self, event):
        nombre = self.selector.get()
        for p in self.plataformas:
            if p.nombre == nombre:
                self.plataforma_activa = p

    # ACCIONES
    def mover(self):
        if not self.plataforma_activa:
            messagebox.showwarning("Aviso", "No hay plataforma seleccionada.")
            return

        try:
            dx = int(self.dx.get())
            dy = int(self.dy.get())
        except ValueError:
            messagebox.showerror("Error", "dx y dy deben ser números.")
            return

        self.plataforma_activa.navegar(dx, dy)
        self.actualizar_canvas()

    def aplicar_danio(self):
        if not self.plataforma_activa:
            return
        
        try:
            d = int(self.danio.get())
        except ValueError:
            messagebox.showerror("Error", "Introduce un número válido.")
            return

        self.plataforma_activa.recibir_danio(d)
        self.actualizar_canvas()

    def sumergir(self):
        if isinstance(self.plataforma_activa, Submarino):
            self.plataforma_activa.sumergirse(200)
            messagebox.showinfo("Acción", "Submarino sumergido a 200m.")

    def despegar_helicoptero(self):
        if isinstance(self.plataforma_activa, Fragata):
            self.plataforma_activa.despegar_helicoptero()
            messagebox.showinfo("Acción", "Helicóptero despegado.")


#   EJECUCIÓN DEL PROGRAMA

root = tk.Tk()
app = App(root)
root.mainloop()
