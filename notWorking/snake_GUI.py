import pygame
import time
import random
from snake_clase import SnakeGame

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

    def run_game(self, player_ai = None):
        actualizar_rate = 1
        fps = 60
        contador = 0
        distancia = self.distancia
        pygame.init()
        myfont = pygame.font.SysFont("monospace", 65)
        self.dibujar_tablero()
        pygame.display.update()
        exit_flag = False

        # Loop principal del juego
        while exit_flag == False and self.game_state == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direccion = [-1, 0]
                    elif event.key == pygame.K_DOWN:
                        direccion = [1, 0]
                    elif event.key == pygame.K_LEFT:
                        direccion = [0, -1]
                    elif event.key == pygame.K_RIGHT:
                        direccion = [0, 1]
                    else:
                        distancia = self.distancia
            time.sleep(1.0/fps)
            contador += 1
            if contador >= actualizar_rate:
                if player_ai != None:
                    direccion = player_ai()
                self.actualizar_distancia(direccion)
                self.actualizar_estado()
                contador = 0
            self.dibujar_tablero()
            pygame.display.update()
        
        # --- perdimos el juego ---
        label = myfont.render(f"Game Over!", 1, self.ROJO)
        self.SCREEN.blit(label, (self.ANCHO + 10, 50))
        pygame.display.update()
        while exit_flag == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True 
        pygame.quit()
