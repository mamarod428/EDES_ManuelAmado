from alojamiento import Alojamiento

class Apartamento(Alojamiento):
    def __init__(self, codigo, direccion, ciudad, precio_por_noche, espacio_principal, numero_planta, tiene_ascensor):
        super().__init__(codigo, direccion, ciudad, precio_por_noche, espacio_principal)
        self.numero_planta = numero_planta
        self.tiene_ascensor = tiene_ascensor

    def mostrar_info(self):
        print("--- TIPO: APARTAMENTO ---")
        super().mostrar_info() 
        
        if self.tiene_ascensor:
            ascensor_txt = "Sí"
        else:
            ascensor_txt = "No"
            
        print(f"    Detalles: Planta {self.numero_planta}, Ascensor: {ascensor_txt}")