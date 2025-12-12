# ============================================================
# EJERCICIO 3: SIMULADOR VISUAL (TKINTER)
# Reutiliza las clases del Ejercicio 2
# ============================================================

import tkinter as tk
# Importamos las clases definidas en el archivo anterior
from ModeloEspacial import Planeta, SateliteNatural, SateliteArtificial, Cohete

class SimuladorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Espacial - Ejercicio 3")
        self.root.geometry("800x600")

        # Panel lateral para controles e info
        self.panel = tk.Frame(root, width=200, bg="#dddddd")
        self.panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.lbl_info = tk.Label(self.panel, text="Info: Selecciona objeto", bg="#dddddd", wraplength=180)
        self.lbl_info.pack(pady=20)

        # Botones de control
        tk.Button(self.panel, text="Avanzar 1 Paso", command=self.avanzar_paso).pack(pady=5)
        
        self.btn_animar = tk.Button(self.panel, text="Iniciar Animación", command=self.toggle_animacion)
        self.btn_animar.pack(pady=5)

        # Canvas (Zona de dibujo)
        self.canvas = tk.Canvas(root, bg="#000022", width=600, height=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Estado de la simulación
        self.objetos = []
        self.graficos = {} # Diccionario: objeto -> id_dibujo_canvas
        self.animando = False
        
        self.inicializar_simulacion()

    def inicializar_simulacion(self):
        # Creamos objetos con posiciones visibles (0-600)
        p1 = Planeta("Tierra", "Solar", 100, 300, 300, 0, 0, 50, 1, True)
        l1 = SateliteNatural("Luna", "Solar", 10, 450, 300, 0, 3, "Tierra", 150)
        
        c1 = Cohete("Falcon", "SpaceX", "USA", "Lanzamiento", 100, 500, 2, -2, 5000, 2000)
        s1 = SateliteArtificial("ISS", "NASA", "Int", "Orbita", 200, 100, 3, 1, "Tierra", 400, "Lab")

        self.objetos = [p1, l1, c1, s1]
        self.dibujar_objetos()

    def dibujar_objetos(self):
        for obj in self.objetos:
            x, y = obj.x, obj.y
            
            # Definir apariencia según el tipo de clase
            if isinstance(obj, Planeta):
                color, r = "blue", 20
            elif isinstance(obj, SateliteNatural):
                color, r = "gray", 8
            elif isinstance(obj, Cohete):
                color, r = "red", 10 # Cuadrado representado como circulo rojo
            else:
                color, r = "green", 6

            # Crear el dibujo en el canvas
            item_id = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="white")
            
            # Guardar referencia para poder moverlo después
            self.graficos[obj] = item_id
            
            # Evento click para mostrar información
            self.canvas.tag_bind(item_id, "<Button-1>", lambda event, o=obj: self.mostrar_info(o))

    def mostrar_info(self, obj):
        # Muestra el __str__ del objeto en el panel lateral
        self.lbl_info.config(text=str(obj))

    def avanzar_paso(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        for obj in self.objetos:
            # 1. Lógica Física: Mover objeto
            obj.avanzar_tiempo(dt=1)

            # Rebote simple en los bordes para que no desaparezcan
            if obj.x <= 0 or obj.x >= w: obj.vx *= -1
            if obj.y <= 0 or obj.y >= h: obj.vy *= -1

            # 2. Lógica Visual: Actualizar coordenadas en el canvas
            item_id = self.graficos[obj]
            
            # Obtenemos radio aproximado visual para centrar
            coords = self.canvas.coords(item_id)
            r = (coords[2] - coords[0]) / 2 
            
            self.canvas.coords(item_id, obj.x-r, obj.y-r, obj.x+r, obj.y+r)

    def toggle_animacion(self):
        self.animando = not self.animando
        if self.animando:
            self.btn_animar.config(text="Detener Animación")
            self.bucle_animacion()
        else:
            self.btn_animar.config(text="Iniciar Animación")

    def bucle_animacion(self):
        if self.animando:
            self.avanzar_paso()
            # Llamarse a sí mismo en 50 milisegundos
            self.root.after(50, self.bucle_animacion)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = SimuladorGUI(ventana)
    ventana.mainloop()