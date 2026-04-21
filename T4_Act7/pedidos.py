import tkinter as tk
from tkinter import ttk, messagebox
import EDES_ManuelAmado.T4_Act7.database as database
import EDES_ManuelAmado.T4_Act7.validaciones as validaciones
import datetime

class PanelPedidos:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # ---- ZONA DE FORMULARIO ----
        form_frame = tk.LabelFrame(self.frame, text="Datos del Pedido")
        form_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(form_frame, text="ID Cliente:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id_cliente = tk.Entry(form_frame)
        self.entry_id_cliente.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Importe (€):").grid(row=0, column=2, padx=5, pady=5)
        self.entry_importe = tk.Entry(form_frame)
        self.entry_importe.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Estado:").grid(row=1, column=0, padx=5, pady=5)
        self.combo_estado = ttk.Combobox(form_frame, values=["pendiente", "en preparación", "enviado", "entregado", "cancelado"], state="readonly")
        self.combo_estado.grid(row=1, column=1, padx=5, pady=5)
        if len(self.combo_estado['values']) > 0:
            self.combo_estado.current(0)

        tk.Label(form_frame, text="Descripción:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_descripcion = tk.Entry(form_frame)
        self.entry_descripcion.grid(row=1, column=3, padx=5, pady=5)

        # ---- ZONA DE BOTONES ----
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(btn_frame, text="Guardar Nuevo", command=self.guardar_pedido).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Actualizar Seleccionado", command=self.actualizar_pedido).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Eliminar Seleccionado", command=self.eliminar_pedido).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Limpiar Cajas", command=self.limpiar_formulario).pack(side=tk.LEFT, padx=5)

        # ---- ZONA DE TABLA (TREEVIEW) ----
        columnas = ("ID", "ID Cliente", "Fecha", "Importe", "Estado", "Descripción")
        self.tree = ttk.Treeview(self.frame, columns=columnas, show="headings")
        
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
            
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.seleccionar_pedido)

        self.pedido_id_seleccionado = None
        self.cargar_datos()

    def cargar_datos(self):
        for elemento in self.tree.get_children():
            self.tree.delete(elemento)

        conexion = database.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM pedidos")
        filas = cursor.fetchall()
        conexion.close()

        for fila in filas:
            self.tree.insert("", tk.END, values=fila)

    def limpiar_formulario(self):
        self.entry_id_cliente.delete(0, tk.END)
        self.entry_importe.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        if len(self.combo_estado['values']) > 0:
            self.combo_estado.current(0)
        self.pedido_id_seleccionado = None

    def comprobar_cliente_existe(self, id_cliente):
        conexion = database.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM clientes WHERE id=?", (id_cliente,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado is not None

    def recopilar_y_validar(self):
        id_cliente = self.entry_id_cliente.get()
        importe = self.entry_importe.get()
        estado = self.combo_estado.get()
        descripcion = self.entry_descripcion.get()
        
        es_valido = True
        mensaje_error = ""

        if not validaciones.validar_campos_llenos([id_cliente, importe, estado]):
            es_valido = False
            mensaje_error = "ID Cliente, Importe y Estado son obligatorios."
        elif not id_cliente.isdigit():
            es_valido = False
            mensaje_error = "El ID del cliente debe ser un número entero."
        elif not self.comprobar_cliente_existe(id_cliente):
            es_valido = False
            mensaje_error = "El ID de cliente indicado no existe en la base de datos."
        else:
            try:
                importe_float = float(importe)
            except ValueError:
                es_valido = False
                mensaje_error = "El importe debe ser un número válido (ej: 150.50)."

        return es_valido, mensaje_error, id_cliente, importe, estado, descripcion

    def guardar_pedido(self):
        es_valido, mensaje, id_cliente, importe, estado, descripcion = self.recopilar_y_validar()
        fecha = datetime.date.today().strftime("%Y-%m-%d")

        if es_valido:
            conexion = database.conectar()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO pedidos (id_cliente, fecha, importe, estado, descripcion) VALUES (?, ?, ?, ?, ?)",
                           (id_cliente, fecha, importe, estado, descripcion))
            conexion.commit()
            conexion.close()
            
            self.limpiar_formulario()
            self.cargar_datos()
            messagebox.showinfo("Éxito", "Pedido registrado correctamente.")
        else:
            messagebox.showerror("Error", mensaje)

    def seleccionar_pedido(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            valores = self.tree.item(seleccion[0], "values")
            self.limpiar_formulario()
            
            self.pedido_id_seleccionado = valores[0]
            self.entry_id_cliente.insert(0, valores[1])
            self.entry_importe.insert(0, valores[3])
            self.combo_estado.set(valores[4])
            self.entry_descripcion.insert(0, valores[5])

    def actualizar_pedido(self):
        if self.pedido_id_seleccionado:
            es_valido, mensaje, id_cliente, importe, estado, descripcion = self.recopilar_y_validar()

            if es_valido:
                conexion = database.conectar()
                cursor = conexion.cursor()
                cursor.execute("UPDATE pedidos SET id_cliente=?, importe=?, estado=?, descripcion=? WHERE id=?",
                               (id_cliente, importe, estado, descripcion, self.pedido_id_seleccionado))
                conexion.commit()
                conexion.close()
                
                self.limpiar_formulario()
                self.cargar_datos()
                messagebox.showinfo("Éxito", "Pedido actualizado.")
            else:
                messagebox.showerror("Error", mensaje)
        else:
            messagebox.showwarning("Atención", "Seleccione un pedido de la lista.")

    def eliminar_pedido(self):
        if self.pedido_id_seleccionado:
            if messagebox.askyesno("Confirmar", "¿Eliminar este pedido?"):
                conexion = database.conectar()
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM pedidos WHERE id=?", (self.pedido_id_seleccionado,))
                conexion.commit()
                conexion.close()
                
                self.limpiar_formulario()
                self.cargar_datos()
                messagebox.showinfo("Éxito", "Pedido eliminado.")
        else:
            messagebox.showwarning("Atención", "Seleccione un pedido para eliminar.")