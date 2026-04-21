import tkinter as tk
from tkinter import messagebox
import requests
import time
import cProfile
import pstats
import io
from datetime import datetime

# Variable global para almacenar el historial de datos y hacer los cálculos
historial_iss = []

def fetch_iss_data():
    """
    Obtiene los datos actuales de la Estación Espacial Internacional (ISS).
    Si la red falla o está bloqueada por un firewall, genera datos simulados 
    para garantizar que la aplicación y la comparativa de rendimiento no se congelen.

    Retorna:
        dict: Un diccionario con los datos de altitud y velocidad.
    """
    url = "https://api.wheretheiss.at/v1/satellites/25544"
    try:
        # Bajamos el timeout a 2 segundos para evitar que Tkinter se quede bloqueado
        respuesta = requests.get(url, timeout=2)
        if respuesta.status_code == 200:
            return respuesta.json()
    except Exception as error:
        # Imprimimos el fallo en la terminal como aviso para el desarrollador
        print(f"Aviso de red: No se pudo conectar a la API ({error}). Usando datos de respaldo.")
    
    # --- SISTEMA DE RESPALDO (MOCK DATA) ---
    # Si la ejecución llega hasta aquí, significa que la API falló.
    # Generamos datos con rangos realistas de la ISS.
    import random
    return {
        "altitude": random.uniform(410.0, 425.0),
        "velocity": random.uniform(27500.0, 27700.0)
    }

def process_unoptimized(data_list):
    """
    Calcula la altitud media y velocidad máxima del historial usando técnicas NO optimizadas.
    Emplea bucles repetitivos y uso ineficiente de memoria al duplicar listas.

    Parámetros:
        data_list (list): Lista de diccionarios con el histórico de posiciones de la ISS.

    Retorna:
        tuple: Contiene dos valores numéricos (altitud_media, velocidad_maxima).
    """
    if not data_list:
        return 0, 0
        
    altitudes = []
    # Bucle innecesario para extraer datos
    for d in data_list:
        altitudes.append(d['altitude'])
        
    total_alt = 0
    # Cálculo manual en lugar de usar sum()
    for a in altitudes:
        total_alt = total_alt + a
        
    avg_alt = total_alt / len(altitudes)
    
    max_vel = 0
    # Bucle repetido sobre la misma estructura en lugar de hacerlo todo junto
    for d in data_list:
        if d['velocity'] > max_vel:
            max_vel = d['velocity']
            
    # Simulamos un pequeño sobrecoste temporal extra por la ineficiencia
    lista_basura = [x * 2 for x in range(10000)]
            
    return avg_alt, max_vel

def process_optimized(data_list):
    """
    Calcula la altitud media y velocidad máxima del historial usando técnicas optimizadas.
    Emplea funciones nativas de C (sum, max) y generadores para no saturar la memoria.

    Parámetros:
        data_list (list): Lista de diccionarios con el histórico de posiciones de la ISS.

    Retorna:
        tuple: Contiene dos valores numéricos (altitud_media, velocidad_maxima).
    """
    if not data_list:
        return 0, 0
        
    # Uso de generadores y funciones integradas en una sola línea
    avg_alt = sum(d['altitude'] for d in data_list) / len(data_list)
    max_vel = max(d['velocity'] for d in data_list)
    
    return avg_alt, max_vel

def profile_function(func, *args):
    """
    Ejecuta una función bajo la supervisión de cProfile para extraer sus estadísticas de rendimiento.

    Parámetros:
        func (callable): La función que se va a evaluar.
        *args: Argumentos posicionales que requiere la función.

    Retorna:
        tuple: (resultado_de_la_funcion, string_con_estadisticas_cprofile)
    """
    pr = cProfile.Profile()
    pr.enable()
    resultado = func(*args)
    pr.disable()
    
    flujo_salida = io.StringIO()
    ps = pstats.Stats(pr, stream=flujo_salida).sort_stats('cumulative')
    ps.print_stats(5) # Extraemos solo el top 5 de líneas más lentas
    
    return resultado, flujo_salida.getvalue()


class SpaceApp:
    """
    Clase principal de la interfaz gráfica que controla los paneles de la aplicación y la actualización periódica.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor ISS - Optimización vs Ineficiencia")
        self.root.geometry("1100x600")
        self.root.configure(bg="#2e3440")
        
        self.construir_interfaz()
        self.actualizar_datos_periodicamente()

    def construir_interfaz(self):
        """
        Construye la estructura visual dividiendo la ventana en un panel izquierdo y uno derecho.
        """
        # --- Contenedor Principal ---
        self.main_frame = tk.Frame(self.root, bg="#2e3440")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # --- Panel Izquierdo (NO Optimizado) ---
        self.frame_izq = tk.Frame(self.main_frame, bg="#bf616a", bd=2, relief=tk.SUNKEN)
        self.frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(self.frame_izq, text="❌ VERSIÓN NO OPTIMIZADA", font=("Arial", 14, "bold"), bg="#bf616a", fg="white").pack(pady=10)
        
        self.lbl_hora_izq = tk.Label(self.frame_izq, text="Última actualización: --:--:--", bg="#bf616a", fg="white")
        self.lbl_hora_izq.pack()
        
        self.lbl_datos_izq = tk.Label(self.frame_izq, text="Esperando datos...", bg="#bf616a", fg="white", font=("Arial", 12))
        self.lbl_datos_izq.pack(pady=15)
        
        self.lbl_tiempo_izq = tk.Label(self.frame_izq, text="Tiempo ejecución: 0.0000s", bg="#bf616a", fg="white", font=("Arial", 10, "bold"))
        self.lbl_tiempo_izq.pack()
        
        tk.Label(self.frame_izq, text="Análisis cProfile (Top 5 func):", bg="#bf616a", fg="white").pack(pady=(10, 0))
        self.txt_profile_izq = tk.Text(self.frame_izq, height=12, width=55, bg="#3b4252", fg="#eceff4")
        self.txt_profile_izq.pack(padx=10, pady=5)
        
        tk.Button(self.frame_izq, text="Help (Docstrings)", command=lambda: self.mostrar_help(process_unoptimized)).pack(pady=10)

        # --- Panel Derecho (Optimizado) ---
        self.frame_der = tk.Frame(self.main_frame, bg="#a3be8c", bd=2, relief=tk.SUNKEN)
        self.frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(self.frame_der, text="✔ VERSIÓN OPTIMIZADA", font=("Arial", 14, "bold"), bg="#a3be8c", fg="#2e3440").pack(pady=10)
        
        self.lbl_hora_der = tk.Label(self.frame_der, text="Última actualización: --:--:--", bg="#a3be8c", fg="#2e3440")
        self.lbl_hora_der.pack()
        
        self.lbl_datos_der = tk.Label(self.frame_der, text="Esperando datos...", bg="#a3be8c", fg="#2e3440", font=("Arial", 12))
        self.lbl_datos_der.pack(pady=15)
        
        self.lbl_tiempo_der = tk.Label(self.frame_der, text="Tiempo ejecución: 0.0000s", bg="#a3be8c", fg="#2e3440", font=("Arial", 10, "bold"))
        self.lbl_tiempo_der.pack()
        
        tk.Label(self.frame_der, text="Análisis cProfile (Top 5 func):", bg="#a3be8c", fg="#2e3440").pack(pady=(10, 0))
        self.txt_profile_der = tk.Text(self.frame_der, height=12, width=55, bg="#3b4252", fg="#eceff4")
        self.txt_profile_der.pack(padx=10, pady=5)
        
        tk.Button(self.frame_der, text="Help (Docstrings)", command=lambda: self.mostrar_help(process_optimized)).pack(pady=10)

    def mostrar_help(self, funcion):
        """
        Abre una ventana emergente para mostrar la documentación oficial de la función indicada.
        """
        docstring = funcion.__doc__ if funcion.__doc__ else "Sin documentación disponible."
        messagebox.showinfo(f"Documentación: {funcion.__name__}", docstring.strip())

    def actualizar_datos_periodicamente(self):
        """
        Consulta la API de la ISS, procesa los datos en ambas versiones, actualiza la UI y
        se programa a sí misma para volver a ejecutarse usando root.after.
        """
        nuevo_dato = fetch_iss_data()
        if nuevo_dato:
            historial_iss.append(nuevo_dato)
            
            hora_actual = datetime.now().strftime("%H:%M:%S")
            
            # --- Ejecución NO optimizada ---
            inicio_izq = time.perf_counter()
            (alt_media_izq, vel_max_izq), profile_izq = profile_function(process_unoptimized, historial_iss)
            tiempo_total_izq = time.perf_counter() - inicio_izq
            
            # --- Ejecución Optimizada ---
            inicio_der = time.perf_counter()
            (alt_media_der, vel_max_der), profile_der = profile_function(process_optimized, historial_iss)
            tiempo_total_der = time.perf_counter() - inicio_der
            
            # --- Actualizar Textos UI Izquierda ---
            self.lbl_hora_izq.config(text=f"Actualización: {hora_actual}")
            self.lbl_datos_izq.config(text=f"Registros analizados: {len(historial_iss)}\nAltitud media: {alt_media_izq:.2f} km\nVelocidad Max: {vel_max_izq:.2f} km/h")
            self.lbl_tiempo_izq.config(text=f"Tiempo ejecución: {tiempo_total_izq:.6f}s")
            
            self.txt_profile_izq.delete("1.0", tk.END)
            self.txt_profile_izq.insert(tk.END, profile_izq)
            
            # --- Actualizar Textos UI Derecha ---
            self.lbl_hora_der.config(text=f"Actualización: {hora_actual}")
            self.lbl_datos_der.config(text=f"Registros analizados: {len(historial_iss)}\nAltitud media: {alt_media_der:.2f} km\nVelocidad Max: {vel_max_der:.2f} km/h")
            self.lbl_tiempo_der.config(text=f"Tiempo ejecución: {tiempo_total_der:.6f}s")
            
            self.txt_profile_der.delete("1.0", tk.END)
            self.txt_profile_der.insert(tk.END, profile_der)

        # Reprogramar la ejecución de esta misma función dentro de 3 segundos (3000ms)
        self.root.after(3000, self.actualizar_datos_periodicamente)


if __name__ == "__main__":
    # Arrancamos la aplicación
    root = tk.Tk()
    app = SpaceApp(root)
    root.mainloop()