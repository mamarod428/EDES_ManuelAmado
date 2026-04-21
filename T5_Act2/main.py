import random
import time

# Generamos los datos base de las 100.000 fincas (entre 50 y 500 kg)
datos_fincas = [random.randint(50, 500) for _ in range(100000)]

# 1. LISTAS TRADICIONALES
inicio_tradicional = time.time()
lista_tradicional = []
for peso in datos_fincas:
    lista_tradicional.append(peso * 1.10)
total_tradicional = sum(lista_tradicional)
fin_tradicional = time.time()
tiempo_tradicional = fin_tradicional - inicio_tradicional

# 2. LISTAS CON COMPRENSIÓN (LIST COMPREHENSION)
inicio_comprension = time.time()
lista_comprension = [peso * 1.10 for peso in datos_fincas]
total_comprension = sum(lista_comprension)
fin_comprension = time.time()
tiempo_comprension = fin_comprension - inicio_comprension

# 3. GENERADORES
inicio_generador = time.time()
# Se usan paréntesis en lugar de corchetes para crear la expresión generadora
generador = (peso * 1.10 for peso in datos_fincas)
total_generador = sum(generador)
fin_generador = time.time()
tiempo_generador = fin_generador - inicio_generador

# SALIDA POR PANTALLA
print("=== LISTA TRADICIONAL ===")
print(f"Total: {total_tradicional:.2f} kg")
print(f"Tiempo: {tiempo_tradicional:.6f} segundos\n")

print("=== LIST COMPREHENSION ===")
print(f"Total: {total_comprension:.2f} kg")
print(f"Tiempo: {tiempo_comprension:.6f} segundos\n")

print("=== GENERADOR ===")
print(f"Total: {total_generador:.2f} kg")
print(f"Tiempo: {tiempo_generador:.6f} segundos")