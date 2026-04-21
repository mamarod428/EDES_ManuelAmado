import random
import time

class Pixel:
    def __init__(self, id_pixel, face, intensidad):
        self.id = id_pixel
        self.face = face
        self.intensidad = intensidad

    def __hash__(self):
        # Generamos el hash basándonos en los atributos críticos de búsqueda
        return hash((self.face, self.intensidad))

    def __eq__(self, other):
        # Dos píxeles se consideran iguales para el set si comparten la misma cara e intensidad
        if isinstance(other, Pixel):
            return (self.face == other.face) and (self.intensidad == other.intensidad)
        return False

# --- 1. Creación de datos ---
lista_pixeles = []
conjunto_pixeles = set()

# Elegimos aleatoriamente la posición (ID) del único objeto que cumplirá la condición
id_objetivo = random.randint(1, 10000)

for i in range(1, 10001):
    if i == id_objetivo:
        f = True
        int_val = 1.0
    else:
        f = random.choice([True, False])
        # Usamos uniform hasta 0.99 para asegurar que ningún otro objeto tenga intensidad 1.0
        int_val = random.uniform(0.0, 0.99)
        
    nuevo_pixel = Pixel(i, f, int_val)
    lista_pixeles.append(nuevo_pixel)
    conjunto_pixeles.add(nuevo_pixel)

# --- 2. Búsqueda y Medición en LISTA ---
tiempo_inicio_lista = time.perf_counter()

# Búsqueda secuencial (más lenta, complejidad O(N))
contador_lista = 0
for p in lista_pixeles:
    if p.face == True and p.intensidad == 1.0:
        contador_lista += 1

tiempo_fin_lista = time.perf_counter()
tiempo_lista = tiempo_fin_lista - tiempo_inicio_lista

encontrado_lista = contador_lista > 0
unico_lista = (contador_lista == 1)

# --- 3. Búsqueda y Medición en SET ---
# Creamos un objeto "señuelo" con los atributos que buscamos para aprovechar la búsqueda rápida
objetivo_busqueda = Pixel(-1, True, 1.0)

tiempo_inicio_set = time.perf_counter()

# Búsqueda instantánea (más rápida, complejidad O(1))
encontrado_set = objetivo_busqueda in conjunto_pixeles

# Como un Set de Python matemáticamente no admite elementos duplicados (según el método __eq__),
# si el elemento está presente, obligatoriamente es único dentro de la estructura.
unico_set = encontrado_set 

tiempo_fin_set = time.perf_counter()
tiempo_set = tiempo_fin_set - tiempo_inicio_set

# --- 4. Salida por pantalla ---
print("=== LISTA ===")
print(f"Encontrado: {encontrado_lista}")
print(f"Tiempo: {tiempo_lista:.6f} segundos")
if unico_lista:
    print("Único objeto")
else:
    print("El objeto no cumple la condición de ser único")

print("\n=== SET ===")
print(f"Encontrado: {encontrado_set}")
print(f"Tiempo: {tiempo_set:.6f} segundos")
if unico_set:
    print("Único objeto")
else:
    print("El objeto no cumple la condición de ser único")

# --- 5. Condición Especial ---
# Es muy probable que la lista tarde más de 0.0001s en recorrer 10.000 objetos, activando este mensaje.
if tiempo_lista > 0.0001 or tiempo_set > 0.0001:
    print("\nPEATÓN MUERTO")