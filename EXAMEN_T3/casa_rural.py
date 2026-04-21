from alojamiento import Alojamiento

class CasaRural(Alojamiento):
    def __init__(self, codigo, direccion, ciudad, precio_por_noche, espacio_principal, metros_jardin, tiene_chimenea):
        super().__init__(codigo, direccion, ciudad, precio_por_noche, espacio_principal)
        self.metros_jardin = metros_jardin
        self.tiene_chimenea = tiene_chimenea

    def mostrar_info(self):
        print("--- TIPO: CASA RURAL ---")
        super().mostrar_info()
        
        if self.tiene_chimenea:
            chimenea_txt = "Sí"
        else:
            chimenea_txt = "No"
            
        print(f"    Detalles: Jardín {self.metros_jardin} m2, Chimenea: {chimenea_txt}")