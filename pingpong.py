import pygame
import cv2 as cv
import numpy as np
from pygame.locals import *
import os
import threading
import sys

# -----------
# Constantes
# -----------

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
IMG_DIR = "imagenes"
SONIDO_DIR = "sonidos"

red = [255, 0, 0]

font_name = pygame.font.match_font('Agency FB')

# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------
y = 200
y2 = 200

score1 = 0
score2 = 0

def scale(i, inMin, inMax, outMin, outMax): #50 - 700  : 50 - 430
    return ((i - inMin) * (outMax - outMin) / (inMax - inMin) + outMin)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, red)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)



def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print("Error, no se puede cargar la imagen: " + ruta)
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha is True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image


def load_sound(nombre, dir_sonido):
    ruta = os.path.join(dir_sonido, nombre)
    # Intentar cargar el sonido
    try:
        sonido = pygame.mixer.Sound(ruta)
    except (pygame.error) as message:
        print("No se pudo cargar el sonido:" + ruta)
        sonido = None
    return sonido

# -----------------------------------------------
# Creamos los sprites (clases) de los objetos del juego:


class Pelota(pygame.sprite.Sprite):
    "La bola y su comportamiento en la pantalla"

    def __init__(self, sonido_golpe):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("bola.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.centery = SCREEN_HEIGHT / 2
        self.speed = [12, 12]
        self.sonido_golpe = sonido_golpe


    def update(self):
        global score1
        global score2
        if self.rect.left < 0: 
            score1 += 1
            self.speed[0] = -self.speed[0]
            self.rect.centerx = SCREEN_WIDTH / 2
            self.rect.centery = SCREEN_HEIGHT / 2
        elif self.rect.right > SCREEN_WIDTH:
            score2 += 1
            self.speed[0] = -self.speed[0]
            self.rect.centerx = SCREEN_WIDTH / 2
            self.rect.centery = SCREEN_HEIGHT / 2
        elif self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed[1] = -self.speed[1]
        self.rect.move_ip((self.speed[0], self.speed[1]))

    def colision(self, objetivo):
        if self.rect.colliderect(objetivo.rect):
            self.speed[0] = -self.speed[0]
            self.sonido_golpe.play()  # Reproducir sonido de rebote


class Paleta(pygame.sprite.Sprite):
    "Define el comportamiento de las paletas de ambos jugadores"

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("paleta.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = SCREEN_HEIGHT / 2

    def humano(self):
        # Controlar que la paleta no salga de la pantalla
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.top <= 0:
            self.rect.top = 0

    def cpu(self, pelota):
        self.speed = [0, 2.5]
        if pelota.speed[0] >= 0 and pelota.rect.centerx >= SCREEN_WIDTH / 2:
            if self.rect.centery > pelota.rect.centery:
                self.rect.centery -= self.speed[1]
            if self.rect.centery < pelota.rect.centery:
                self.rect.centery += self.speed[1]


# ------------------------------
# Funcion principal del juego
# ------------------------------


def main():
    global y
    global y2
    global score1
    global score2
    cap = cv.VideoCapture(0)
    #hilo1 = threading.Thread(target=deteccion)
    #hilo1.start()
    j1 = input("JUGADOR 1:")

    j2 = input("JUGADOR 2:")


    pygame.init()
    pygame.mixer.init()
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PingPong RobotistasMX")

    # cargamos los objetos
    fondo = load_image("fondo2.jpg", IMG_DIR, alpha=False)
    sonido_golpe = load_sound("tennis.ogg", SONIDO_DIR)

    bola = Pelota(sonido_golpe)
    jugador1 = Paleta(40)
    jugador2 = Paleta(SCREEN_WIDTH - 40)

    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 25)  # Activa repeticion de teclas
    pygame.mouse.set_visible(False)

    screen.blit(fondo, (0, 0))
    draw_text(screen, j1 + ":", 48,  ((SCREEN_WIDTH / 2) - (len(j1)) - 200), 0)
    draw_text(screen, str(score1), 48, (SCREEN_WIDTH / 2) + 40 , 0)
    draw_text(screen, str(score2), 48, (SCREEN_WIDTH / 2) - 40 , 0)
    draw_text(screen,  ":" + j2 , 48,  ((SCREEN_WIDTH / 2) + (len(j2)) + 200), 0)
    draw_text(screen,  "PRESIONA LA BARRA ESPACIADORA PARA COMENZAR", 60,  SCREEN_WIDTH / 2, SCREEN_HEIGHT/2 + 250)
    todos = pygame.sprite.RenderPlain(bola, jugador1, jugador2)
    todos.draw(screen)
    pygame.display.flip()
    
    wait = False
    while wait == False:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                wait = True
            elif event.type == pygame.QUIT:
                sys.exit(0)    
    # el bucle principal del juego

    while True:
        clock.tick(60)

        # Actualizamos los obejos en pantalla
        jugador1.humano()
        jugador2.humano()
        bola.update()


        # Comprobamos si colisionan los objetos
        bola.colision(jugador1)
        bola.colision(jugador2)

        ny =  scale(y, 100, 350, 60, 500)
        ny2 = scale(y2, 100, 350, 60, 500)

        #print(ny)

        

        _ , frame = cap.read()
        #_ , frame2 = cap.read()
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        #hsv2 = cv.cvtColor(frame2, cv.COLOR_BGR2HSV)

        lower_blue = np.array([51,114,144])
        upper_blue = np.array([255, 203,255])

        lower_red = np.array([0,52,172])
        upper_red = np.array([60,255,255])

        mask = cv.inRange(hsv, lower_blue,upper_blue )
        mask2 = cv.inRange(hsv, lower_red,upper_red )

        filtro1 = cv.erode(mask, cv.getStructuringElement(cv.MORPH_RECT,(3,3)), iterations=1)
        filtro2 = cv.erode(filtro1, cv.getStructuringElement(cv.MORPH_RECT,(5,5)), iterations=1)

        filtro3 = cv.erode(mask2, cv.getStructuringElement(cv.MORPH_RECT,(3,3)), iterations = 1)
        filtro4 = cv.erode(filtro3, cv.getStructuringElement(cv.MORPH_RECT,(5,5)), iterations = 1)

        try:
            objct = cv.moments(filtro2)
            if objct['m00'] > 50000:
                cx = int(objct['m10']/objct['m00']+1)
                cy = int(objct['m01']/objct['m00']+1)
                cv.circle(frame, (cx,cy), 10, (0,0,255), 4) 
                y = cy

            objct2 = cv.moments(filtro4)
            if objct2['m00'] > 50000:
                cx2 = int(objct2['m10']/objct2['m00']+1)
                cy2 = int(objct2['m01']/objct2['m00']+1)
                cv.circle(frame, (cx2,cy2), 10, (0,0,255), 4)
                y2 = cy2
        except:
            print("error")

        #cv.imshow('original', frame2)
        #cv.imshow('azul', filtro4)

        jugador1.rect.centery = ny
        jugador2.rect.centery = ny2
        for event in pygame.event.get():


            if event.type == pygame.QUIT:
                sys.exit(0)


        # actualizamos la pantalla
        screen.blit(fondo, (0, 0))
        draw_text(screen, j1 + ":", 48,  ((SCREEN_WIDTH / 2) - (len(j1)) - 200), 0)
        draw_text(screen, str(score1), 48, (SCREEN_WIDTH / 2) - 40 , 0)
        draw_text(screen, str(score2), 48, (SCREEN_WIDTH / 2) + 40 , 0)
        draw_text(screen,  ":" + j2 , 48,  ((SCREEN_WIDTH / 2) + (len(j2)) + 200), 0)
        todos = pygame.sprite.RenderPlain(bola, jugador1, jugador2)
        todos.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
