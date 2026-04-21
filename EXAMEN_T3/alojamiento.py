class Alojamiento:
    def __init__(self, codigo, direccion, ciudad, precio_por_noche, espacio_principal):
        self.codigo = codigo
        self.direccion = direccion
        self.ciudad = ciudad
        self.precio_por_noche = precio_por_noche
        self.espacio_principal = espacio_principal

    def mostrar_info(self):
        print(f"[{self.codigo}] {self.direccion} ({self.ciudad}) - {self.precio_por_noche}€/noche")
        self.espacio_principal.mostrar_info()

    def cambiar_precio(self, nuevo_precio):
        if nuevo_precio > 0:
            self.precio_por_noche = nuevo_precio

    def aumentar_precio_porcentaje(self, porcentaje):
        if porcentaje >= 0:
            aumento = self.precio_por_noche * (porcentaje / 100)
            self.precio_por_noche += aumento

    def get_precio(self):
        return self.precio_por_noche