class Cliente:
    def __init__(self, nombre, dni, telefono):
        self.nombre = nombre
        self.dni = dni
        self.telefono = telefono
        self.alojamiento_actual = None 
    def mostrar_info(self):
        print(f"Cliente: {self.nombre} (DNI: {self.dni}, Tlf: {self.telefono})")

    def reservar(self, alojamiento):
        self.alojamiento_actual = alojamiento
        print(f"--> {self.nombre} ha reservado el alojamiento {alojamiento.codigo}")

    def cancelar_reserva(self):
        self.alojamiento_actual = None
        print(f"--> {self.nombre} ha cancelado su reserva.")

    def mostrar_reserva(self):
        if self.alojamiento_actual:
            print(f"Reserva actual de {self.nombre}:")
            self.alojamiento_actual.mostrar_info()
        else:
            print(f"{self.nombre} no tiene ninguna reserva activa.")