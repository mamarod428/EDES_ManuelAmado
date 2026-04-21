import csv
import EDES_ManuelAmado.T4_Act7.database as database
from tkinter import messagebox, filedialog

def exportar_clientes_csv():
    # Abrimos diálogo para que el usuario elija dónde guardar el archivo
    ruta_archivo = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Archivos CSV", "*.csv")],
        title="Guardar listado de clientes"
    )

    if ruta_archivo:
        try:
            conexion = database.conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM clientes")
            filas = cursor.fetchall()
            conexion.close()

            with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                # Escribimos las cabeceras
                escritor.writerow(["ID", "Nombre", "Teléfono", "Email", "Empresa", "Fecha Alta"])
                # Escribimos los datos
                for fila in filas:
                    escritor.writerow(fila)
                    
            messagebox.showinfo("Exportación", "Clientes exportados correctamente al archivo CSV.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al exportar: {str(e)}")