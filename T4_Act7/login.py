import tkinter as tk
from tkinter import messagebox
import EDES_ManuelAmado.T4_Act7.database as database

class VentanaLogin:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("300x250")
        self.root.resizable(False, False)
        
        # Guardamos la función que se ejecutará si el login es correcto
        self.on_login_success = on_login_success

        # Elementos de la interfaz
        tk.Label(root, text="Gestión Empresarial", font=("Arial", 14, "bold")).pack(pady=15)

        tk.Label(root, text="Usuario:").pack(pady=5)
        self.entry_username = tk.Entry(root)
        self.entry_username.pack()

        tk.Label(root, text="Contraseña:").pack(pady=5)
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack()

        tk.Button(root, text="Iniciar Sesión", command=self.iniciar_sesion, bg="blue", fg="white").pack(pady=20)

    def iniciar_sesion(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        conexion = database.conectar()
        cursor = conexion.cursor()
        # Buscamos si existe la combinación usuario y contraseña
        cursor.execute("SELECT rol FROM usuarios WHERE username=? AND password=?", (username, password))
        resultado = cursor.fetchone()
        conexion.close()

        if resultado:
            rol = resultado[0]
            messagebox.showinfo("Acceso Correcto", f"Bienvenido, perfil: {rol}")
            self.root.destroy() # Cerramos la ventana de login
            self.on_login_success(rol) # Llamamos al programa principal pasándole el rol
        else:
            messagebox.showerror("Error de Acceso", "Usuario o contraseña incorrectos")