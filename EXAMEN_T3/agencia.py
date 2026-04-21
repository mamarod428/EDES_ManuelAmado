class Agencia:
    def __init__(self, nombre, correo_contacto):
        self.nombre = nombre
        self.correo_contacto = correo_contacto
        self.lista_alojamientos = [] 
    def agregar_alojamiento(self, alojamiento):
        self.lista_alojamientos.append(alojamiento)

    def quitar_alojamiento(self, codigo):
        encontrado = None
        for aloj in self.lista_alojamientos:
            if aloj.codigo == codigo:
                encontrado = aloj
                break
        
        if encontrado:
            self.lista_alojamientos.remove(encontrado)
            print(f"Alojamiento {codigo} eliminado correctamente.")
        else:
            print(f"No se encontró el alojamiento {codigo}.")

    def contar_alojamientos(self):
        return len(self.lista_alojamientos)

    def mostrar_info(self):
        print(f"\n=== AGENCIA: {self.nombre} ({self.correo_contacto}) ===")
        print(f"Total alojamientos: {self.contar_alojamientos()}")
        for aloj in self.lista_alojamientos:
            print("---------------------------------------")
            aloj.mostrar_info()