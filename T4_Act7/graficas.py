import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import EDES_ManuelAmado.T4_Act7.database as database

class PanelGraficas:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.frame, text="Panel de Análisis de Dirección", font=("Arial", 16, "bold")).pack(pady=10)

        # Contenedor para alinear los gráficos uno al lado del otro
        self.graficos_frame = tk.Frame(self.frame)
        self.graficos_frame.pack(fill=tk.BOTH, expand=True)

        self.mostrar_grafica_pedidos_estado()
        self.mostrar_grafica_clientes_empresa()

    def mostrar_grafica_pedidos_estado(self):
        conexion = database.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT estado, COUNT(*) FROM pedidos GROUP BY estado")
        datos = cursor.fetchall()
        conexion.close()

        estados = []
        cantidades = []
        for fila in datos:
            estados.append(fila[0])
            cantidades.append(fila[1])

        figura, ax = plt.subplots(figsize=(5, 4))
        if len(estados) > 0:
            ax.pie(cantidades, labels=estados, autopct='%1.1f%%', startangle=90)
            ax.set_title("Pedidos por Estado")
        else:
            ax.text(0.5, 0.5, 'No hay datos de pedidos', horizontalalignment='center', verticalalignment='center')

        canvas = FigureCanvasTkAgg(figura, master=self.graficos_frame)
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def mostrar_grafica_clientes_empresa(self):
        conexion = database.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT empresa, COUNT(*) FROM clientes WHERE empresa != '' GROUP BY empresa")
        datos = cursor.fetchall()
        conexion.close()

        empresas = []
        cantidades = []
        for fila in datos:
            empresas.append(fila[0])
            cantidades.append(fila[1])

        figura, ax = plt.subplots(figsize=(5, 4))
        if len(empresas) > 0:
            ax.bar(empresas, cantidades, color='skyblue')
            ax.set_title("Clientes por Empresa")
            ax.set_ylabel("Cantidad de Clientes")
            ax.tick_params(axis='x', rotation=45)
            figura.tight_layout()
        else:
            ax.text(0.5, 0.5, 'No hay datos de empresas', horizontalalignment='center', verticalalignment='center')

        canvas = FigureCanvasTkAgg(figura, master=self.graficos_frame)
        canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)