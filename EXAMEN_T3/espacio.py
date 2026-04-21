class Espacio:
    def __init__(self, nombre, metros_cuadrados, tiene_ventanas):
        self.nombre = nombre
        self.metros_cuadrados = metros_cuadrados
        self.tiene_ventanas = tiene_ventanas

    def mostrar_info(self):
        if self.tiene_ventanas:
            ventanas_txt = "Sí"
        else:
            ventanas_txt = "No"
        print(f"    - Espacio: {self.nombre} ({self.metros_cuadrados} m2, Ventanas: {ventanas_txt})")