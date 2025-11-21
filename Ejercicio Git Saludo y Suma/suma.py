# El fichero suma.py pedirá al usuario dos números y mostrará la suma.

def suma(a,b):
    suma = a + b
    return suma

a = int(input("Introduce el primer número: "))
b = int(input("Introduce el segundo número: "))
print(f"La suma de {a} y {b} es {suma(a,b)}.")