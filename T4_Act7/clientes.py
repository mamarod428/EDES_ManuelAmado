import tkinter as tk
from tkinter import ttk, messagebox
import EDES_ManuelAmado.T4_Act7.database as database
import EDES_ManuelAmado.T4_Act7.validaciones as validaciones
import datetime

class PanelClientes:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # ---- ZONA DE FORMULARIO ----
        form_frame = tk.LabelFrame(self.frame, text="Datos del Cliente")
        form_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(form_frame)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Teléfono:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_telefono = tk.Entry(form_frame)
        self.entry_telefono.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_email = tk.Entry(form_frame)
        self.entry_email.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Empresa:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_empresa = tk.Entry(form_frame)
        self.entry_empresa.grid(row=1, column=3, padx=5, pady=5)

        # ---- ZONA DE BOTONES ----
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(btn_frame, text="Guardar Nuevo", command=self.guardar_cliente).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Actualizar Seleccionado", command=self.actualizar_cliente).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Eliminar Seleccionado", command=self.eliminar_cliente).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Limpiar Cajas", command=self.limpiar_formulario).pack(side=tk.LEFT, padx=5)

        # ---- ZONA DE TABLA (TREEVIEW) ----
        columnas = ("ID", "Nombre", "Teléfono", "Email", "Empresa", "Fecha Alta")
        self.tree = ttk.Treeview(self.frame, columns=columnas, show="headings")
        
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
            
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Evento: Al hacer doble clic en una fila, cargar datos en el formulario
        self.tree.bind("<Double-1>", self.seleccionar_cliente)

        self.cliente_id_seleccionado = None
        self.cargar_datos()

    def cargar_datos(self):
        # Vaciamos la tabla antes de rellenarla
        elementos = self.tree.get_children()
        for elemento in elementos:
            self.tree.delete(elemento)

        conexion = database.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes")
        filas = cursor.fetchall()
        conexion.close()

        # Insertamos los datos de SQLite en el Treeview
        for fila in filas:
            self.tree.insert("", tk.END, values=fila)

    def limpiar_formulario(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_empresa.delete(0, tk.END)
        self.cliente_id_seleccionado = None

    def recopilar_y_validar(self):
        # Función auxiliar para no repetir código en Guardar y Actualizar
        nombre = self.entry_nombre.get()
        telefono = self.entry_telefono.get()
        email = self.entry_email.get()
        empresa = self.entry_empresa.get()
        
        es_valido = True
        mensaje_error = ""

        if not validaciones.validar_campos_llenos([nombre, telefono, email]):
            es_valido = False
            mensaje_error = "Nombre, teléfono y email son obligatorios."
        elif not validaciones.validar_telefono(telefono):
            es_valido = False
            mensaje_error = "El teléfono debe tener exactamente 9 números."
        elif not validaciones.validar_email(email):
            es_valido = False
            mensaje_error = "El formato del email es incorrecto."

        return es_valido, mensaje_error, nombre, telefono, email, empresa

    def guardar_cliente(self):
        es_valido, mensaje, nombre, telefono, email, empresa = self.recopilar_y_validar()
        fecha_alta = datetime.date.today().strftime("%Y-%m-%d")

        if es_valido:
            conexion = database.conectar()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO clientes (nombre, telefono, email, empresa, fecha_alta) VALUES (?, ?, ?, ?, ?)",
                           (nombre, telefono, email, empresa, fecha_alta))
            conexion.commit()
            conexion.close()
            
            self.limpiar_formulario()
            self.cargar_datos()
            messagebox.showinfo("Éxito", "Cliente guardado correctamente.")
        else:
            messagebox.showerror("Error de Validación", mensaje)

    def seleccionar_cliente(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            # Obtenemos los valores de la fila seleccionada
            valores = self.tree.item(seleccion[0], "values")
            self.limpiar_formulario()
            
            self.cliente_id_seleccionado = valores[0]
            self.entry_nombre.insert(0, valores[1])
            self.entry_telefono.insert(0, valores[2])
            self.entry_email.insert(0, valores[3])
            self.entry_empresa.insert(0, valores[4])

    def actualizar_cliente(self):
        if self.cliente_id_seleccionado:
            es_valido, mensaje, nombre, telefono, email, empresa = self.recopilar_y_validar()

            if es_valido:
                conexion = database.conectar()
                cursor = conexion.cursor()
                cursor.execute("UPDATE clientes SET nombre=?, telefono=?, email=?, empresa=? WHERE id=?",
                               (nombre, telefono, email, empresa, self.cliente_id_seleccionado))
                conexion.commit()
                conexion.close()
                
                self.limpiar_formulario()
                self.cargar_datos()
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
            else:
                messagebox.showerror("Error de Validación", mensaje)
        else:
            messagebox.showwarning("Atención", "Seleccione un cliente de la lista para actualizar.")

    def eliminar_cliente(self):
        if self.cliente_id_seleccionado:
            respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?")
            if respuesta:
                conexion = database.conectar()
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM clientes WHERE id=?", (self.cliente_id_seleccionado,))
                conexion.commit()
                conexion.close()
                
                self.limpiar_formulario()
                self.cargar_datos()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
        else:
            messagebox.showwarning("Atención", "Seleccione un cliente de la lista para eliminar.")