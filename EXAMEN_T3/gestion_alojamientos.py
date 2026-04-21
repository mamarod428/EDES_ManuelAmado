from espacio import Espacio
from apartamento import Apartamento
from casa_rural import CasaRural
from agencia import Agencia
from cliente import Cliente

if __name__ == "__main__":
    print("=== ALOJAMIENTOS TURÍSTICOS ===\n")

    espacio_apt = Espacio("Salón", 22.5, True)
    apt1 = Apartamento("APT-01", "Calle Amiel 7", "Cádiz", 80.0, espacio_apt, 3, True)

    espacio_casa = Espacio("Estudio", 18.0, True)
    casa1 = CasaRural("RUR-99", "Camino del Bosque", "Granada", 120.0, espacio_casa, 50, True)


    mi_agencia = Agencia("Viajes DAW", "contacto@gmail.com")
    mi_agencia.agregar_alojamiento(apt1)
    mi_agencia.agregar_alojamiento(casa1)


    cliente1 = Cliente("Manuel Amado", "12345678Z", "600999888")
    
    print("--- GESTIÓN DE RESERVAS ---")
    cliente1.reservar(apt1)
    cliente1.mostrar_reserva()
    
    print("\n-- Cambiando reserva...")
    cliente1.reservar(casa1)
    cliente1.mostrar_reserva()

    print("\n--- ACTUALIZACIÓN DE PRECIOS ---")
    apt1.cambiar_precio(95.0)
    print(f"Nuevo precio APT-01: {apt1.get_precio()} euros")
    
    casa1.aumentar_precio_porcentaje(10) 
    print(f"Nuevo precio RUR-99 +10%: {casa1.get_precio()} euros")

    mi_agencia.mostrar_info()

    print("\n--- ELIMINACIÓN DE ALOJAMIENTO ---")
    mi_agencia.quitar_alojamiento("APT-01")
    
    mi_agencia.mostrar_info()