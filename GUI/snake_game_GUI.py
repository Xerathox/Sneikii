from snake_game import SnakeGame
import pygame
# import time
import random

rand = random.Random()

class SnakeGameGUI(SnakeGame):
    
    def __init__(self, headless_mode = False):
        super().__init__()
        self.AZUL = (0, 0, 255)
        self.MORADO = (255, 0, 255)
        self.NEGRO = (0, 0, 0)
        self.ROJO = (255, 0, 0)
        self.TAMAÑO_CUADRADO = 10
        self.ANCHO = self.TAMAÑO_CUADRADO*self.ancho
        self.ALTO = self.TAMAÑO_CUADRADO*self.alto
        self.TAMAÑO = (self.ANCHO + 400, self.ALTO)

        if headless_mode == False:
            self.SCREEN = pygame.display.set_mode(self.TAMAÑO)
            pygame.init()

    def dibujar_tablero(self):
        myfont = pygame.font.SysFont("monospace", 50)
        self.SCREEN.fill(self.NEGRO)
        for i in range(self.alto):
            for j in range(self.alto):
                # check for head, body, food
                if self.tablero[i, j] == 1:
                    tam_loc = (j*self.TAMAÑO_CUADRADO, i*self.TAMAÑO_CUADRADO, self.TAMAÑO_CUADRADO, self.TAMAÑO_CUADRADO)
                    pygame.draw.rect(self.SCREEN, self.AZUL, tam_loc)
                elif self.tablero[i, j] == 2:
                    tam_loc = (j*self.TAMAÑO_CUADRADO, i*self.TAMAÑO_CUADRADO, self.TAMAÑO_CUADRADO, self.TAMAÑO_CUADRADO)
                    pygame.draw.rect(self.SCREEN, self.MORADO, tam_loc)
                elif self.tablero[i, j] == -1:
                    loc = (int((j+0.5)*self.TAMAÑO_CUADRADO), int((i+0.5)*self.TAMAÑO_CUADRADO))
                    pygame.draw.circle(self.SCREEN, self.ROJO, loc, self.TAMAÑO_CUADRADO//2)
        
        label = myfont.render(f"Score: {self.puntaje}", 1, self.MORADO)
        self.SCREEN.blit(label, (self.ANCHO + 10,10))
        tam_loc = (self.ANCHO, 0, 3, self.ALTO)
        pygame.draw.rect(self.SCREEN, (255, 255, 255), tam_loc)
        pygame.display.update()
