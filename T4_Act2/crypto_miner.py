import pygame
import random
import sys
import os

# --- CONFIGURACIÓN GENERAL ---
ANCHO = 1300
ALTO = 800
FPS = 60
NOMBRE_ALUMNO = "Manuel Amado"

# Colores
NEGRO = (10, 10, 10)
VERDE_MATRIX = (0, 255, 65)
DORADO = (255, 215, 0)   
ROJO_HACIENDA = (200, 0, 0)
AZUL_CUERO = (0, 100, 200) # Azul tipo cartera de piel
AZUL_OSCURO = (0, 50, 120) # Para la solapa

# =========================================================
# HERRAMIENTAS DE CARGA
# =========================================================
def cargar_imagen(nombre, w, h, color_backup, tipo=None):
    ruta = os.path.join(os.path.dirname(__file__), nombre)
    try:
        img = pygame.image.load(ruta).convert_alpha()
        img = pygame.transform.scale(img, (w, h))
        return img
    except FileNotFoundError:
        surf = pygame.Surface((w, h), pygame.SRCALPHA) # Fondo transparente
        
        if tipo == "cartera":
            pygame.draw.rect(surf, color_backup, (0, h//3, w, h*2//3), border_radius=10)
            pygame.draw.rect(surf, AZUL_OSCURO, (0, 0, w, h//2), border_bottom_left_radius=10, border_bottom_right_radius=10)
            pygame.draw.circle(surf, DORADO, (w//2, h//2), 6)
            
        elif tipo == "hacienda":
            surf.fill(color_backup)
            pygame.draw.rect(surf, (255,255,255), surf.get_rect(), 2)
            font = pygame.font.SysFont("Arial", 40, bold=True)
            text = font.render("H", True, (255, 255, 255))
            surf.blit(text, (w//2 - 12, h//2 - 22))
            
        else:
            if nombre == "btc.png":
                pygame.draw.circle(surf, DORADO, (w//2, h//2), w//2)
                font = pygame.font.SysFont("Arial", 30, bold=True)
                text = font.render("B", True, (255, 255, 255))
                surf.blit(text, (w//2 - 8, h//2 - 18))
            else:
                surf.fill(color_backup)
        
        return surf

def cargar_sonido(nombre):
    if pygame.mixer.get_init() is None: return None  
    ruta = os.path.join(os.path.dirname(__file__), nombre)
    try: return pygame.mixer.Sound(ruta)
    except: return None

# =========================================================
# CLASES
# =========================================================

class Cartera(pygame.sprite.Sprite):
    """ El jugador: Ahora es una Cartera Azul """
    def __init__(self):
        super().__init__()
        self.image = cargar_imagen("cartera.png", 80, 60, AZUL_CUERO, tipo="cartera")
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 20
        self.velocidad = 12 

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidad
        
        if self.rect.right > ANCHO: self.rect.right = ANCHO
        if self.rect.left < 0: self.rect.left = 0

class Bitcoin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cargar_imagen("btc.png", 50, 50, DORADO, tipo="bitcoin")
        self.rect = self.image.get_rect()
        self.reset_pos()

    def reset_pos(self):
        self.rect.x = random.randrange(0, ANCHO - self.rect.width)
        self.rect.y = random.randrange(-150, -50)
        self.velocidad_y = random.randrange(4, 9)

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top > ALTO:
            self.reset_pos()

class AgenciaTributaria(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cargar_imagen("aet.png", 60, 60, ROJO_HACIENDA, tipo="hacienda")
        self.rect = self.image.get_rect()
        self.reset_pos()

    def reset_pos(self):
        self.rect.x = random.randrange(0, ANCHO - self.rect.width)
        self.rect.y = random.randrange(-300, -100) 
        self.velocidad_y = random.randrange(6, 12)

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top > ALTO:
            self.reset_pos()

class JuegoCrypto:
    def __init__(self):
        pygame.init()
        try: pygame.mixer.init()
        except: print("Modo silencio activado")

        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(f"MI CARTERA vs HACIENDA - {NOMBRE_ALUMNO}")
        
        self.reloj = pygame.time.Clock()
        self.corriendo = True
        self.wallet = 0 
        self.fuente_ui = pygame.font.SysFont("Consolas", 30, bold=True)

        self.fondo = None
        ruta_fondo = os.path.join(os.path.dirname(__file__), "circuito.jpg")
        if os.path.exists(ruta_fondo):
            try:
                img = pygame.image.load(ruta_fondo).convert()
                self.fondo = pygame.transform.scale(img, (ANCHO, ALTO))
            except: pass

        self.sfx_cash = cargar_sonido("coin.mp3") 
        self.sfx_multa = cargar_sonido("error.mp3") 

        self.sprites = pygame.sprite.Group()
        self.monedas = pygame.sprite.Group()
        self.hacienda_group = pygame.sprite.Group()

        self.jugador = Cartera()
        self.sprites.add(self.jugador)

        for _ in range(6):
            b = Bitcoin()
            self.sprites.add(b)
            self.monedas.add(b)

        for _ in range(3):
            m = AgenciaTributaria()
            self.sprites.add(m)
            self.hacienda_group.add(m)

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.corriendo = False

    def logica(self):
        self.sprites.update()

        hits_monedas = pygame.sprite.spritecollide(self.jugador, self.monedas, True)
        for hit in hits_monedas:
            self.wallet += 100
            if self.sfx_cash: self.sfx_cash.play()
            b = Bitcoin()
            self.sprites.add(b)
            self.monedas.add(b)

        hits_hacienda = pygame.sprite.spritecollide(self.jugador, self.hacienda_group, True)
        for hit in hits_hacienda:
            self.wallet -= 300
            if self.sfx_multa: self.sfx_multa.play()
            m = AgenciaTributaria()
            self.sprites.add(m)
            self.hacienda_group.add(m)

    def dibujar(self):
        if self.fondo: self.pantalla.blit(self.fondo, (0, 0))
        else: self.pantalla.fill(NEGRO)

        self.sprites.draw(self.pantalla)

        texto_wallet = self.fuente_ui.render(f"FONDOS: ${self.wallet}", True, VERDE_MATRIX)
        self.pantalla.blit(texto_wallet, (20, 20))
        
        texto_info = self.fuente_ui.render("¡Esquiva a HACIENDA!", True, ROJO_HACIENDA)
        self.pantalla.blit(texto_info, (ANCHO - 400, 20))

        pygame.display.flip()

    def ejecutar(self):
        while self.corriendo:
            self.manejar_eventos()
            self.logica()
            self.dibujar()
            self.reloj.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    JuegoCrypto().ejecutar()