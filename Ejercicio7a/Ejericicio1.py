#   CLASES BASE

class Capitan:
    def __init__(self, nombre, rango):
        self.nombre = nombre
        self.rango = rango

    def __str__(self):
        return f"{self.rango} {self.nombre}"


class SistemaArmas:
    def __init__(self, nombre, potencia):
        self.nombre = nombre
        self.potencia = potencia

    def __str__(self):
        return f"{self.nombre} (Potencia: {self.potencia})"


class Sensor:
    def __init__(self, tipo, alcance):
        self.tipo = tipo
        self.alcance = alcance

    def __str__(self):
        return f"{self.tipo} (Alcance: {self.alcance} km)"


#   CLASE PLATAFORMA BASE

class PlataformaNaval:
    def __init__(self, nombre, desplazamiento, integridad=100):
        self.nombre = nombre
        self.desplazamiento = desplazamiento
        self.integridad = integridad
        self.capitan = None
        self.sistemas_armas = []
        self.sensores = []

    # Asociación
    def asumir_mando(self, capitan):
        self.capitan = capitan

    # Composición
    def agregar_sistema_arma(self, arma):
        self.sistemas_armas.append(arma)

    def agregar_sensor(self, sensor):
        self.sensores.append(sensor)

    def navegar(self, rumbo, velocidad):
        print(f"{self.nombre} navega en rumbo {rumbo}° a {velocidad} nudos.")

    def recibir_danio(self, cantidad):
        self.integridad -= cantidad
        if self.integridad < 0:
            self.integridad = 0
        print(f"{self.nombre} ha recibido {cantidad}% de daño. Integridad actual: {self.integridad}%")

    def esta_operativa(self):
        return self.integridad > 0

    def mostrar_info(self):
        print(f"\nPlataforma: {self.nombre}")
        print(f"Desplazamiento: {self.desplazamiento} toneladas")
        print(f"Integridad: {self.integridad}%")
        print(f"Capitán: {self.capitan}")
        print("Sistemas de armas:")
        for arma in self.sistemas_armas:
            print(" -", arma)
        print("Sensores:")
        for sensor in self.sensores:
            print(" -", sensor)


#   CLASES DERIVADAS

class Fragata(PlataformaNaval):
    def __init__(self, nombre, desplazamiento, helicopteros=1):
        super().__init__(nombre, desplazamiento)
        self.helicopteros = helicopteros

    def despegar_helicoptero(self):
        if self.helicopteros > 0:
            self.helicopteros -= 1
            print(f"{self.nombre} ha despegado un helicóptero. Helicópteros restantes: {self.helicopteros}")
        else:
            print(f"{self.nombre} no tiene helicópteros disponibles.")

class Corbeta(PlataformaNaval):
    def __init__(self, nombre, desplazamiento, velocidad_max):
        super().__init__(nombre, desplazamiento)
        self.velocidad_max = velocidad_max


class Submarino(PlataformaNaval):
    def __init__(self, nombre, desplazamiento, profundidad_max):
        super().__init__(nombre, desplazamiento)
        self.profundidad_max = profundidad_max
        self.profundidad_actual = 0

    def sumergirse(self, metros):
        if metros <= self.profundidad_max:
            self.profundidad_actual = metros
            print(f"{self.nombre} se sumerge a {metros} metros.")
        else:
            print(f"No puede superar su profundidad máxima de {self.profundidad_max} metros.")


#   CLASE FLOTA

class Flota:
    def __init__(self, nombre):
        self.nombre = nombre
        self.plataformas = []  # Agregación

    def agregar_plataforma(self, plataforma):
        self.plataformas.append(plataforma)

    def ordenar_ataque(self):
        print(f"La flota {self.nombre} ordena ataque general.")

    def mostrar_info(self):
        print(f"\n{self.nombre.upper()}")
        for p in self.plataformas:
            p.mostrar_info()

#   PROGRAMA PRINCIPAL

# Crear capitanes
cap1 = Capitan("Ramírez", "Capitán de navío")
cap2 = Capitan("Torres", "Capitán de fragata")
cap3 = Capitan("López", "Teniente de navío")

# Crear plataformas
fragata = Fragata("F-101 Álvaro de Bazán", 5800)
corbeta = Corbeta("C-35 Descubierta", 1700, velocidad_max=28)
submarino = Submarino("S-80 Isaac Peral", 3000, profundidad_max=300)

# Asignar capitanes
fragata.asumir_mando(cap1)
corbeta.asumir_mando(cap2)
submarino.asumir_mando(cap3)

# Crear sistemas de armas
arma1 = SistemaArmas("Misiles Harpoon", 85)
arma2 = SistemaArmas("Cañón naval de 127 mm", 70)
arma3 = SistemaArmas("Torpedos pesados", 90)

# Crear sensores
sens1 = Sensor("Radar SPY-1", 200)
sens2 = Sensor("Sonar activo", 50)
sens3 = Sensor("Sensor infrarrojo", 30)

# Asignar sistemas a plataformas
fragata.agregar_sistema_arma(arma1)
fragata.agregar_sensor(sens1)

corbeta.agregar_sistema_arma(arma2)
corbeta.agregar_sensor(sens3)

submarino.agregar_sistema_arma(arma3)
submarino.agregar_sensor(sens2)

# Crear flota
flota = Flota("Flota del Atlántico")
flota.agregar_plataforma(fragata)
flota.agregar_plataforma(corbeta)
flota.agregar_plataforma(submarino)

# Mostrar información inicial
flota.mostrar_info()

# Simulación
print("\nSIMULACIÓN")
flota.ordenar_ataque()

corbeta.navegar(90, 20)
fragata.recibir_danio(30)
submarino.sumergirse(200)
fragata.despegar_helicoptero()

# Estado operativo
print("\nESTADO OPERATIVO")
for p in flota.plataformas:
    print(f"{p.nombre} operativo: {p.esta_operativa()}")

# Información final
flota.mostrar_info()
