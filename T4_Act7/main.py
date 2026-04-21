import tkinter as tk
from tkinter import ttk
import EDES_ManuelAmado.T4_Act7.database as database
from EDES_ManuelAmado.T4_Act7.login import VentanaLogin
from EDES_ManuelAmado.T4_Act7.clientes import PanelClientes
from EDES_ManuelAmado.T4_Act7.pedidos import PanelPedidos
from EDES_ManuelAmado.T4_Act7.graficas import PanelGraficas
from EDES_ManuelAmado.T4_Act7.exportacion import exportar_clientes_csv

class AppPrincipal:
    def __init__(self, root, rol_usuario):
        self.root = root
        self.root.title(f"Sistema de Gestión - Perfil: {rol_usuario}")
        self.root.geometry("800x600")
        
        # Pestañas (Notebook)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        if rol_usuario == "Administrador":
            # Pestaña Clientes
            tab_clientes = ttk.Frame(self.notebook)
            self.notebook.add(tab_clientes, text="Gestión de Clientes")
            PanelClientes(tab_clientes)

            # Pestaña Pedidos
            tab_pedidos = ttk.Frame(self.notebook)
            self.notebook.add(tab_pedidos, text="Gestión de Pedidos")
            PanelPedidos(tab_pedidos)
            
            # Botón de exportación en la parte inferior para Administradores
            frame_inferior = tk.Frame(root)
            frame_inferior.pack(fill=tk.X, pady=10)
            tk.Button(frame_inferior, text="Exportar Clientes a CSV", command=exportar_clientes_csv, bg="green", fg="white").pack()

        elif rol_usuario == "CEO":
            # Pestaña Análisis CEO (Solo lectura y gráficas)
            tab_analisis = ttk.Frame(self.notebook)
            self.notebook.add(tab_analisis, text="Panel de Análisis")
            PanelGraficas(tab_analisis)

def iniciar_aplicacion(rol):
    root = tk.Tk()
    app = AppPrincipal(root, rol)
    root.mainloop()

def main():
    # Inicializamos la base de datos y creamos usuarios si no existen
    database.inicializar_db()
    
    # Creamos la ventana temporal para el Login
    root_login = tk.Tk()
    app_login = VentanaLogin(root_login, iniciar_aplicacion)
    root_login.mainloop()

if __name__ == "__main__":
    main()