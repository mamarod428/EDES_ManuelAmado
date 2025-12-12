# ============================================================
# EJERCICIO 2: MODELO DE DOMINIO ESPACIAL
# Incluye: HERENCIA, COMPOSICIÓN, AGREGACIÓN y ASOCIACIÓN
# ============================================================

import math

# ============================================================
# HERENCIA:
# Clase padre: ObjetoEspacial
# Todos los objetos del simulador comparten posición y velocidad
# ============================================================

class ObjetoEspacial:
    def __init__(self, x, y, vx, vy):
        # Atributos físicos comunes
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def avanzar_tiempo(self, dt=1):
        # Actualiza posición según velocidad (física básica)
        self.x += self.vx * dt
        self.y += self.vy * dt

    def __str__(self):
        return f"Pos: ({self.x}, {self.y}) Vel: ({self.vx}, {self.vy})"


# ============================================================
# HERENCIA:
# Rama de Cuerpos Naturales (Planetas, Lunas, etc.)
# Heredan de ObjetoEspacial
# ============================================================

class CuerpoNatural(ObjetoEspacial):
    def __init__(self, nombre, tipo, sistema_origen, masa, x, y, vx, vy):
        # Llamamos al constructor del padre
        super().__init__(x, y, vx, vy)
        self.nombre = nombre
        self.tipo = tipo
        self.sistema_origen = sistema_origen
        self.masa = masa

    def __str__(self):
        texto = f"[{self.tipo}] {self.nombre} (Sistema: {self.sistema_origen})\n"
        texto += f"   {super().__str__()}"
        return texto

class Planeta(CuerpoNatural):
    def __init__(self, nombre, sistema_origen, masa, x, y, vx, vy, radio, max_sat, atmosfera):
        super().__init__(nombre, "Planeta", sistema_origen, masa, x, y, vx, vy)
        self.radio_medio = radio
        self.max_satelites = max_sat
        self.tiene_atmosfera = atmosfera

class SateliteNatural(CuerpoNatural):
    def __init__(self, nombre, sistema_origen, masa, x, y, vx, vy, orbitando_a, dist_media):
        super().__init__(nombre, "Satélite Natural", sistema_origen, masa, x, y, vx, vy)
        self.orbitando_a = orbitando_a
        self.distancia_media = dist_media

class Cometa(CuerpoNatural):
    def __init__(self, nombre, sistema_origen, masa, x, y, vx, vy, periodo, cola_visible):
        super().__init__(nombre, "Cometa", sistema_origen, masa, x, y, vx, vy)
        self.periodo_orbital = periodo
        self.cola_visible = cola_visible


# ============================================================
# COMPOSICIÓN:
# Sistemas internos de las naves (Propulsión, Comunicaciones)
# Si la nave se destruye, estos sistemas dejan de existir.
# ============================================================

class SistemaPropulsion:
    def __init__(self, tipo_combustible, cantidad, empuje_max):
        self.tipo_combustible = tipo_combustible
        self.cantidad_combustible = cantidad
        self.empuje_max = empuje_max

    def consumir(self, cantidad):
        if self.cantidad_combustible >= cantidad:
            self.cantidad_combustible -= cantidad
            return True
        return False

    def __str__(self):
        return f"Motor {self.tipo_combustible}: {self.cantidad_combustible}L restantes"

class SistemaComunicaciones:
    def __init__(self, potencia, frecuencias):
        self.potencia_max = potencia
        self.frecuencias = frecuencias
        self.operativo = True

    def enviar_mensaje(self, msg):
        if self.operativo:
            print(f"   >>> [RADIO] Tx: {msg}")
        else:
            print(f"   >>> [RADIO] Error: Sistema averiado")


# ============================================================
# ASOCIACIÓN:
# Centro de Control dirige la misión.
# La nave tiene un centro asignado, pero NO es dueña del centro.
# ============================================================

class CentroControl:
    def __init__(self, nombre, pais, operadores):
        self.nombre = nombre
        self.pais = pais
        self.operadores = operadores

    def enviar_orden(self, estructura, orden):
        print(f"[Centro {self.nombre}] envía orden a '{estructura.id_mision}': {orden}")


# ============================================================
# HERENCIA + COMPOSICIÓN + ASOCIACIÓN:
# Rama de Estructuras Artificiales (Naves, Satélites)
# ============================================================

class EstructuraArtificial(ObjetoEspacial):
    def __init__(self, id_mision, agencia, pais, estado, x, y, vx, vy):
        super().__init__(x, y, vx, vy)
        self.id_mision = id_mision
        self.agencia = agencia
        self.pais = pais
        self.estado_operativo = estado

        # COMPOSICIÓN: La estructura crea sus propios sistemas internos
        self.propulsion = SistemaPropulsion("Químico", 1000, 5000)
        self.comunicaciones = SistemaComunicaciones(100, ["UHF"])

        # ASOCIACIÓN: Referencia al centro de control (inicialmente None)
        self.centro_control = None

    def asignar_centro(self, centro):
        # Establecemos la asociación
        self.centro_control = centro

    def __str__(self):
        texto = f"[Misión] {self.id_mision} ({self.estado_operativo})\n"
        texto += f"   {super().__str__()}\n"
        texto += f"   - {self.propulsion}\n"
        if self.centro_control:
            texto += f"   - Controlado por: {self.centro_control.nombre}"
        else:
            texto += f"   - Sin centro de control asignado"
        return texto

class SateliteArtificial(EstructuraArtificial):
    def __init__(self, id_mision, agencia, pais, estado, x, y, vx, vy, orbitando_a, altura, funcion):
        super().__init__(id_mision, agencia, pais, estado, x, y, vx, vy)
        self.orbitando_a = orbitando_a
        self.altura_orbita = altura
        self.funcion = funcion

class Cohete(EstructuraArtificial):
    def __init__(self, id_mision, agencia, pais, estado, x, y, vx, vy, empuje, capacidad):
        super().__init__(id_mision, agencia, pais, estado, x, y, vx, vy)
        self.empuje_total = empuje
        self.capacidad_carga = capacidad
        self.lanzamientos_realizados = 0


# ============================================================
# AGREGACIÓN:
# Agrupaciones (Sistemas Planetarios, Constelaciones)
# Contienen objetos, pero si la agrupación se borra, los objetos siguen.
# ============================================================

class SistemaPlanetario:
    def __init__(self, nombre, estrella):
        self.nombre = nombre
        self.estrella = estrella
        self.cuerpos = [] # Lista de agregación

    def agregar_cuerpo(self, cuerpo):
        self.cuerpos.append(cuerpo)

    def __str__(self):
        texto = f"\n=== SISTEMA PLANETARIO: {self.nombre} ===\n"
        for c in self.cuerpos:
            texto += str(c) + "\n"
        return texto

class Constelacion:
    def __init__(self, nombre, tipo_orbita):
        self.nombre = nombre
        self.tipo_orbita = tipo_orbita
        self.satelites = [] # Lista de agregación

    def agregar_satelite(self, sat):
        self.satelites.append(sat)

    def __str__(self):
        texto = f"\n=== CONSTELACIÓN: {self.nombre} ===\n"
        for s in self.satelites:
            texto += f" - {s.id_mision}\n"
        return texto


# ============================================================
# EJECUCIÓN DEL EJERCICIO 2 (Main)
# ============================================================

if __name__ == "__main__":
    print("--- INICIANDO SIMULACIÓN DE CONSOLA ---\n")

    # 1. Crear Sistema Planetario (Agregación)
    sistema_solar = SistemaPlanetario("Sistema Solar", "Sol")
    
    # Crear cuerpos (Herencia)
    tierra = Planeta("Tierra", "Sistema Solar", 5.97e24, 0, 0, 0, 0, 6371, 1, True)
    luna = SateliteNatural("Luna", "Sistema Solar", 7.34e22, 10, 0, 0, 1, "Tierra", 384400)
    
    # Agregar al sistema
    sistema_solar.agregar_cuerpo(tierra)
    sistema_solar.agregar_cuerpo(luna)

    # 2. Crear Centro de Control y Misiones (Asociación y Composición)
    centro_houston = CentroControl("Houston", "USA", 50)
    
    cohete = Cohete("Falcon 9", "SpaceX", "USA", "Lanzamiento", 0, 0, 2, 5, 7600, 22000)
    cohete.asignar_centro(centro_houston) # Asociación

    satelite = SateliteArtificial("Starlink-1", "SpaceX", "USA", "En órbita", 50, 50, 1, 1, "Tierra", 550, "Internet")
    satelite.asignar_centro(centro_houston)

    constelacion = Constelacion("Starlink", "LEO")
    constelacion.agregar_satelite(satelite)

    # 3. Imprimir Estado Inicial
    print(sistema_solar)
    print("--- ESTRUCTURAS ARTIFICIALES ---")
    print(cohete)
    print(satelite)

    # 4. Modificar Estados (Simulación)
    print("\n--- EJECUTANDO CAMBIOS ---")
    print(">>> El cohete consume combustible y asciende...")
    cohete.propulsion.consumir(200) # Usamos el objeto compuesto
    cohete.avanzar_tiempo(dt=10)    # Método heredado
    
    print(">>> Cambiando estado del satélite...")
    satelite.estado_operativo = "Mantenimiento"
    centro_houston.enviar_orden(satelite, "Reiniciar sistemas")

    # 5. Imprimir Estado Final
    print("\n--- ESTADO FINAL COHETE ---")
    print(cohete)
    print("\n--- ESTADO FINAL SATÉLITE ---")
    print(satelite)