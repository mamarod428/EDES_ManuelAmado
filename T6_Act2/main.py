import tkinter as tk
import pytest
# Importo la lógica y los tests desde el módulo matemático
from matematicas import suma, resta, multiplicacion, division
from matematicas import test_suma, test_resta, test_multiplicacion, test_division, test_division_cero

class CalculadoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora + Pruebas Unitarias")
        # Ajusto el tamaño para que sea equilibrado y respete los márgenes
        self.root.geometry("350x620")
        self.root.configure(bg="#f0f0f0")
        
        self.operando1 = None
        self.operador = None
        self.reiniciar_pantalla = False

        self.crear_interfaz()

    def crear_interfaz(self):
        # Yo creo un contenedor principal para forzar los márgenes en toda la ventana
        # El padding de 15 asegura que nada toque los bordes laterales
        self.contenedor = tk.Frame(self.root, bg="#f0f0f0")
        self.contenedor.pack(expand=True, fill="both", padx=15, pady=15)

        # Pantalla de la calculadora
        self.pantalla = tk.Text(self.contenedor, height=8, width=30, font=("Arial", 12), bg="white", bd=2, relief="sunken")
        self.pantalla.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 15))
        
        # Etiquetas de colores para los tests
        self.pantalla.tag_configure("verde", foreground="green", font=("Arial", 11, "bold"))
        self.pantalla.tag_configure("rojo", foreground="red", font=("Arial", 11, "bold"))
        self.pantalla.tag_configure("normal", foreground="black", font=("Arial", 12))
        
        self.pantalla.insert(tk.END, "0")
        self.pantalla.config(state="disabled")

        # Botones de la calculadora
        botones = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3),
        ]

        # Configuro las columnas para que tengan el mismo peso y respeten el margen derecho
        for i in range(4):
            self.contenedor.grid_columnconfigure(i, weight=1)

        for (texto, f, c) in botones:
            tk.Button(self.contenedor, text=texto, width=5, height=2, font=("Arial", 14),
                      command=lambda t=texto: self.click_boton(t)).grid(row=f, column=c, padx=3, pady=3, sticky="nsew")

        # Botón de Pruebas bien centrado y con margen
        btn_pruebas = tk.Button(self.contenedor, text="Ejecutar Pruebas", font=("Arial", 12, "bold"),
                                bg="#4da6ff", fg="white", command=self.ejecutar_pruebas)
        btn_pruebas.grid(row=5, column=0, columnspan=4, pady=(20, 0), sticky="nsew")

    def click_boton(self, valor):
        self.pantalla.config(state="normal")
        texto_actual = self.pantalla.get("1.0", tk.END).strip()

        if valor in '0123456789':
            if texto_actual == "0" or self.reiniciar_pantalla:
                self.pantalla.delete("1.0", tk.END)
                self.reiniciar_pantalla = False
            self.pantalla.insert(tk.END, valor, "normal")

        elif valor in '+-*/':
            try:
                self.operando1 = float(texto_actual)
                self.operador = valor
                self.reiniciar_pantalla = True
            except ValueError:
                _ = "Evito usar pass"

        elif valor == '=':
            if self.operador and self.operando1 is not None:
                try:
                    operando2 = float(texto_actual)
                    res = 0
                    if self.operador == '+': res = suma(self.operando1, operando2)
                    elif self.operador == '-': res = resta(self.operando1, operando2)
                    elif self.operador == '*': res = multiplicacion(self.operando1, operando2)
                    elif self.operador == '/': res = division(self.operando1, operando2)
                    
                    self.pantalla.delete("1.0", tk.END)
                    # Limpio el resultado para que no siempre salgan decimales innecesarios
                    if res.is_integer():
                        self.pantalla.insert(tk.END, str(int(res)), "normal")
                    else:
                        self.pantalla.insert(tk.END, str(res), "normal")
                except ValueError:
                    self.pantalla.delete("1.0", tk.END)
                    self.pantalla.insert(tk.END, "Error: División por 0", "rojo")
                
                self.operador = None
                self.reiniciar_pantalla = True

        elif valor == 'C':
            self.pantalla.delete("1.0", tk.END)
            self.pantalla.insert(tk.END, "0", "normal")
            self.operando1 = None
            self.operador = None
            self.reiniciar_pantalla = False

        self.pantalla.config(state="disabled")

    def ejecutar_pruebas(self):
        """Yo ejecuto las pruebas de Pytest y muestro el feedback visual"""
        self.pantalla.config(state="normal")
        self.pantalla.delete("1.0", tk.END)

        pruebas = {
            "Suma": test_suma,
            "Resta": test_resta,
            "Multiplicación": test_multiplicacion,
            "División": test_division,
            "División por cero": test_division_cero
        }

        exitos = 0
        for nombre, func in pruebas.items():
            try:
                func()
                self.pantalla.insert(tk.END, f"✔ {nombre} OK\n", "verde")
                exitos += 1
            except (AssertionError, Exception):
                self.pantalla.insert(tk.END, f"❌ {nombre} FALLO\n", "rojo")

        self.pantalla.insert(tk.END, f"\nFinal: {exitos}/{len(pruebas)} correctas", "normal")
        self.pantalla.config(state="disabled")
        self.reiniciar_pantalla = True

if __name__ == "__main__":
    ventana = tk.Tk()
    app = CalculadoraApp(ventana)
    ventana.mainloop()