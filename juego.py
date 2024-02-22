import pygame
import sys
import time
import random

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la pantalla
ANCHO = 800
ALTO = 600

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Atrapando comida!")

# Cargar imágenes
try:
    jugador_imagen = pygame.image.load("jugador.png")
    comida_imagen = pygame.image.load("comida.png")
    super_comida_imagen = pygame.image.load("super_comida.png")
    fondo_imagen = pygame.image.load("fondo.jpg")
except pygame.error as err:
    print("Error al cargar imágenes:", err)

# Redimensionar imágenes
jugador_imagen = pygame.transform.scale(jugador_imagen, (50, 50))
comida_imagen = pygame.transform.scale(comida_imagen, (30, 30))
super_comida_imagen = pygame.transform.scale(super_comida_imagen, (30, 30))
fondo_imagen = pygame.transform.scale(fondo_imagen, (ANCHO, ALTO))

# Crear el reloj del juego
reloj_juego = pygame.time.Clock()

# Crear fuente para el tiempo restante
fuente_tiempo = pygame.font.Font(None, 36)

# Función para mostrar la pantalla de inicio
def mostrar_pantalla_inicio():
    # Definir botones
    boton_play = pygame.Rect(300, 200, 200, 50)
    boton_opciones = pygame.Rect(300, 300, 200, 50)
    boton_salir = pygame.Rect(300, 400, 200, 50)

    # Loop de la pantalla de inicio
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar si se hizo clic en alguno de los botones
                if boton_play.collidepoint(event.pos):
                    print("¡Comenzar juego!")
                    mostrar_ready()
                    contar_regresivo()
                    iniciar_juego()
                elif boton_opciones.collidepoint(event.pos):
                    print("Abrir opciones")
                    # Aquí puedes llamar a la función que muestra las opciones
                elif boton_salir.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Limpiar pantalla
        pantalla.fill(NEGRO)

        # Dibujar botones
        pygame.draw.rect(pantalla, BLANCO, boton_play)
        pygame.draw.rect(pantalla, BLANCO, boton_opciones)
        pygame.draw.rect(pantalla, BLANCO, boton_salir)

        # Texto de los botones
        font = pygame.font.Font(None, 36)
        texto_play = font.render("Play Game", True, NEGRO)
        texto_opciones = font.render("Opciones", True, NEGRO)
        texto_salir = font.render("Salir", True, NEGRO)

        # Posicionar textos en los botones
        pantalla.blit(texto_play, (boton_play.x + 50, boton_play.y + 10))
        pantalla.blit(texto_opciones, (boton_opciones.x + 50, boton_opciones.y + 10))
        pantalla.blit(texto_salir, (boton_salir.x + 70, boton_salir.y + 10))

        # Actualizar pantalla
        pygame.display.flip()

# Función para mostrar "Ready"
def mostrar_ready():
    pantalla.fill(NEGRO)
    font = pygame.font.Font(None, 72)
    texto_ready = font.render("Ready", True, BLANCO)
    pantalla.blit(texto_ready, (ANCHO // 2 - 80, ALTO // 2))
    pygame.display.flip()
    time.sleep(1)  # Esperar un segundo antes de mostrar el conteo regresivo

# Función para mostrar el conteo regresivo
def contar_regresivo():
    for i in range(3, 0, -1):
        pantalla.fill(NEGRO)
        font = pygame.font.Font(None, 72)
        texto_cuenta = font.render(str(i), True, BLANCO)
        pantalla.blit(texto_cuenta, (ANCHO // 2 - 20, ALTO // 2))
        pygame.display.flip()
        time.sleep(1)

# Clase para representar al jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = jugador_imagen
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.velocidad_x = 0

    def update(self):
        # Mover el jugador horizontalmente
        self.rect.x += self.velocidad_x
        # Mantener al jugador dentro de la pantalla
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        elif self.rect.left < 0:
            self.rect.left = 0

# Clase para representar la comida
class Comida(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Hay una probabilidad del 10% de que la comida sea una super comida
        if random.random() < 0.1:
            self.image = super_comida_imagen
            self.valor = 5  # Valor de la super comida
        else:
            self.image = comida_imagen
            self.valor = 1  # Valor de la comida normal
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidad_y = random.randint(1, 5)

    def update(self):
        # Mover la comida hacia abajo
        self.rect.y += self.velocidad_y
        # Si la comida sale de la pantalla, reiniciar su posición
        if self.rect.top > ALTO:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.velocidad_y = random.randint(1, 5)

# Función para iniciar el juego
def iniciar_juego():
    # Crear grupos de sprites
    todos_los_sprites = pygame.sprite.Group()
    jugadores = pygame.sprite.Group()
    comidas = pygame.sprite.Group()

    # Crear el jugador
    jugador = Jugador()
    todos_los_sprites.add(jugador)
    jugadores.add(jugador)

    # Crear las comidas iniciales
    for _ in range(8):
        comida = Comida()
        todos_los_sprites.add(comida)
        comidas.add(comida)

    # Tiempo de juego en segundos
    tiempo_juego = 60
    tiempo_inicial = pygame.time.get_ticks()

    # Puntuación del jugador
    puntaje = 0

    # Loop principal del juego
    jugando = True
    while jugando:
        # Controlar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    jugador.velocidad_x = -5
                elif event.key == pygame.K_RIGHT:
                    jugador.velocidad_x = 5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    jugador.velocidad_x = 0

        # Actualizar sprites
        todos_los_sprites.update()

        # Verificar colisiones entre el jugador y la comida
        colisiones = pygame.sprite.spritecollide(jugador, comidas, True)
        for colision in colisiones:
            puntaje += colision.valor
            comida = Comida()
            todos_los_sprites.add(comida)
            comidas.add(comida)

        # Verificar si se acaba el tiempo
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - tiempo_inicial) // 1000
        tiempo_restante = max(tiempo_juego - tiempo_transcurrido, 0)
        if tiempo_restante <= 0:
            jugando = False

        # Limpiar pantalla
        pantalla.fill(NEGRO)

        # Dibujar fondo
        pantalla.blit(fondo_imagen, (0, 0))

        # Dibujar sprites en la pantalla
        todos_los_sprites.draw(pantalla)

        # Mostrar puntaje
        texto_puntaje = fuente_tiempo.render("Puntaje: " + str(puntaje), True, BLANCO)
        pantalla.blit(texto_puntaje, (10, 10))

        # Mostrar tiempo restante
        texto_tiempo = fuente_tiempo.render("Tiempo: " + str(tiempo_restante), True, BLANCO)
        pantalla.blit(texto_tiempo, (ANCHO - 150, 10))

        # Actualizar pantalla
        pygame.display.flip()

        # Controlar velocidad de actualización
        reloj_juego.tick(60)

    # Mostrar "Game Over"
    font_game_over = pygame.font.Font(None, 72)
    texto_game_over = font_game_over.render("Game Over", True, BLANCO)
    pantalla.blit(texto_game_over, (ANCHO // 2 - 150, ALTO // 2))
    pygame.display.flip()
    time.sleep(3)  # Mostrar "Game Over" durante 3 segundos

    # Volver a la pantalla de inicio después de "Game Over"
    mostrar_pantalla_inicio()

# Llamar a la función de la pantalla de inicio
mostrar_pantalla_inicio()
