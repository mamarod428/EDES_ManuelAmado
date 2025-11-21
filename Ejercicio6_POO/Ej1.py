# Crea un programa en Python que haga uso de una clase llamado Camióncon los siguientes atributos:
# + matricula - tipo string
# + conductor - tipo string
# + capacidad_kg - tipo float. Capacidad máxima de carga
# + descripcion_carga - tipo string
# + rumbo. Una cantidad entre 1 y 359 grados. Tipo entero
# + velocidad. Tipo entero
# + cajas. Será una lista de objetos tipo Caja. Tendrá también los siguientes métodos: · peso_total() → float: suma de pesos de las cajas cargadas. · ·add_caja(caja: Caja): añade una caja si no supera capacidad_kg.· Si supera, no la añade y muestra un aviso/lanza excepción (a tu elección). · __str__: texto con todos los atributos del camión (incluyendo nº de cajasypeso total). + setVelocidad, que establecerá una nueva velocidad
# + setRumbo, que establecerá un nuevo rumbo. + claxon. Imprimirá un mensaje “piiiiiii” en el terminal.
# La clase Caja tendrá los siguientes atributos:
# + codigo - tipo string
# + peso_kg - tipo float
# + descripcion_carga - tipo string
# + largo - tipo float
# + ancho - tipo float
# + altura - tipo float
# Esta clase tendrá como único método, además del constructor, el método__str__, que imprimirá todos los atributos de la caja, en un formato a eleccióndel alumno. El programa debe crear 2 objetos tipo Camión, con 3 cajas cada uno deellos. A continuación se debe imprimir toda la información de cada camión,
# incluyendo sus cajas. Posteriormente se añadirán 2 cajas al primer camión y 3 cajas al segundo. Se variarán las velocidades y los rumbos de los dos camiones. El segundo camión tocará el claxón. El programa terminará volviendo a imprimir toda la información de los
# camiones, para ver los cambios.


class Caja:
    def __init__(self, codigo, peso_kg, descripcion_carga, largo, ancho, altura):
        self.codigo = codigo
        self.peso_kg = float(peso_kg)
        self.descripcion_carga = descripcion_carga
        self.largo = float(largo)
        self.ancho = float(ancho)
        self.altura = float(altura)

    def __str__(self):
        return (f"{self.codigo} - {self.descripcion_carga} "
                f"({self.peso_kg} kg, {self.largo}x{self.ancho}x{self.altura} m)")


class Camion:
    def __init__(self, matricula, conductor, capacidad_kg, descripcion_carga, rumbo, velocidad, cajas=None):

        if capacidad_kg <= 0:
            raise ValueError("La capacidad debe ser positiva.")

        if not (1 <= rumbo <= 359):
            raise ValueError("El rumbo debe estar entre 1 y 359 grados.")

        self.matricula = matricula
        self.conductor = conductor
        self.capacidad_kg = float(capacidad_kg)
        self.descripcion_carga = descripcion_carga
        self.rumbo = int(rumbo)
        self.velocidad = int(velocidad)

        # agregación
        self.cajas = list(cajas) if cajas is not None else []

    def peso_total(self):
        return sum(c.peso_kg for c in self.cajas)

    def add_caja(self, caja):
        """Intenta añadir una caja. Devuelve True si se añade."""
        if self.peso_total() + caja.peso_kg <= self.capacidad_kg:
            self.cajas.append(caja)
            return True
        else:
            print(f"No se pudo añadir la caja {caja.codigo}: "
                  f"capacidad excedida ({self.peso_total()}/{self.capacidad_kg} kg).")
            return False

    def setVelocidad(self, nueva_velocidad):
        self.velocidad = int(nueva_velocidad)

    def setRumbo(self, nuevo_rumbo):
        if 1 <= nuevo_rumbo <= 359:
            self.rumbo = int(nuevo_rumbo)
        else:
            print("Aviso: rumbo fuera de rango (1-359 grados).")

    def claxon(self):
        print("piiiiiii")

    def __str__(self):
        if self.cajas:
            listado = "\n    " + "\n    ".join(str(c) for c in self.cajas)
        else:
            listado = " — sin cajas —"

        texto = (
            f"Camión {self.matricula} — Conductor: {self.conductor}\n"
            f"  Velocidad: {self.velocidad} km/h   Rumbo: {self.rumbo}°\n"
            f"  Capacidad: {self.capacidad_kg} kg  Cargado: {self.peso_total()} kg\n"
            f"  Descripción general: {self.descripcion_carga}\n"
            f"  Cajas:{listado}"
        )
        return texto


def imprimir_estado(titulo, lista_camiones):
    print(f"\n=== {titulo} ===")
    for c in lista_camiones:
        print(c)
        print("-" * 60)


if __name__ == "__main__":

    # Crear cajas independientes
    c1 = Caja("C001", 2000, "Frutas", 2.0, 1.5, 1.0)
    c2 = Caja("C002", 3000, "Verduras", 2.5, 1.5, 1.2)
    c3 = Caja("C003", 1500, "Lácteos", 2.0, 1.0, 1.0)

    c4 = Caja("C004", 2500, "Televisores", 2.0, 1.5, 1.0)
    c5 = Caja("C005", 2000, "Computadoras", 2.5, 1.5, 1.2)
    c6 = Caja("C006", 1000, "Teléfonos", 1.5, 1.0, 0.5)

    # Crear camiones con 3 cajas cada uno
    camion1 = Camion("1234ABC", "Juan Pérez", 10000, "Transporte de alimentos",
                     rumbo=90, velocidad=80, cajas=[c1, c2, c3])

    camion2 = Camion("5678DEF", "María López", 8000, "Electrónica",
                     rumbo=180, velocidad=70, cajas=[c4, c5, c6])

    flota = [camion1, camion2]

    # Estado inicial
    imprimir_estado("ESTADO INICIAL", flota)

    # Nuevas cajas
    n1 = Caja("C007", 4000, "Bebidas", 3.0, 2.0, 1.5)
    n2 = Caja("C008", 2500, "Snacks", 2.0, 1.5, 1.0)

    n3 = Caja("C009", 3000, "Cámaras", 2.5, 1.5, 1.2)
    n4 = Caja("C010", 1500, "Accesorios", 1.5, 1.0, 0.5)
    n5 = Caja("C011", 2000, "Consolas", 2.0, 1.5, 1.0)

    # Añadir cajas
    camion1.add_caja(n1)
    camion1.add_caja(n2)

    camion2.add_caja(n3)
    camion2.add_caja(n4)
    camion2.add_caja(n5)

    # Cambios de velocidad/rumbo
    camion1.setVelocidad(90)
    camion1.setRumbo(120)

    camion2.setVelocidad(80)
    camion2.setRumbo(200)

    # Claxon del segundo camión
    camion2.claxon()

    # Estado final
    imprimir_estado("ESTADO FINAL", flota)

