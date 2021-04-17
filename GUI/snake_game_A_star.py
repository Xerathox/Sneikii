from snake_game_GUI import SnakeGameGUI
import pygame
import time
import random
import numpy as np

rand = random.Random()

class SnakeGameAStar(SnakeGameGUI):
    
    def __init__(self, headless_mode = False):
        super().__init__(headless_mode)
        # self.path2food = []
        self.reversa = 1
        self.temp_head_orig = []
    
    def movimiento_no_seguro(self, movimientos, mov_no_seguros):
        for mov in movimientos:
            temp_head = self.head.copy()
            temp_head[0] += mov[0]
            temp_head[1] += mov[1]

            if temp_head[0] < 0 or temp_head[0] >= self.alto:
                mov_no_seguros.append(mov)
            elif temp_head[1] < 0 or temp_head[1] >= self.ancho:
                mov_no_seguros.append(mov)
            elif temp_head in self.snake: 
                mov_no_seguros.append(mov)

        for mov in mov_no_seguros:
            movimientos.remove(mov)
        
        return movimientos

    def mov_seguros(self, temp_head = None): 
        movimientos = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        mov_no_seguros = []

        if temp_head == None:
            self.temp_head_orig = self.head.copy()
        else:
            self.temp_head_orig = temp_head.copy()
        # remove unsafe moves
        for mov in movimientos:
            temp_head = self.temp_head_orig.copy()
            temp_head[0] += mov[0]
            temp_head[1] += mov[1]

            if temp_head[0] < 0 or temp_head[0] >= self.alto:
                mov_no_seguros.append(mov)
            elif temp_head[1] < 0 or temp_head[1] >= self.ancho:
                mov_no_seguros.append(mov)
            elif temp_head in self.snake: 
                mov_no_seguros.append(mov)

        for mov in mov_no_seguros:
            movimientos.remove(mov)
        
        return movimientos

    def wiggle_away(self):
        movimientos = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        mov_no_seguros = []
        dir_comida = []
        
        d0 = -self.comida[0] + self.head[0]
        if d0 != 0:
            dir_comida.append([d0//abs(d0), 0])
        d1 = -self.comida[1] + self.head[1]
        if d1 != 0:
            dir_comida.append([0, d1//abs(d1)])

        # remove unsafe moves
        for mov in movimientos:
            temp_head = self.temp_head_orig.copy()
            temp_head[0] += mov[0]
            temp_head[1] += mov[1]

            if temp_head[0] < 0 or temp_head[0] >= self.alto:
                mov_no_seguros.append(mov)
            elif temp_head[1] < 0 or temp_head[1] >= self.ancho:
                mov_no_seguros.append(mov)
            elif temp_head in self.snake: 
                mov_no_seguros.append(mov)

        for mov in mov_no_seguros:
            movimientos.remove(mov)
                
        # move towards food first
        self.reversa *= -1 # to alternate turning direction
        for mov in movimientos[::self.reversa]:
        # for move in moves:
            if mov in dir_comida:
                return mov
            
        if len(movimientos) == 0: # no safe moves
            return [1, 0]
        else:
            return rand.choice(movimientos)

    def verificar_comida(self, loc):
        if self.comida[0] == loc[0] and self.comida[1] == loc[1]:
            return True
        else:
            return False

    def heuristica(self, head):
        # distancia euclidania para la heuristica
        d0 = self.comida[0] - head[0]
        d1 = self.comida[1] - head[1]
        return np.sqrt(d0**2 + d1**2)

    def astar_explorar(self, temp_head):
        self.explorado.append(temp_head)
        movimientos = self.mov_seguros(temp_head)

        for mov in movimientos:
            head = temp_head.copy()
            head[0] += mov[0]
            head[1] += mov[1]
            h = self.heuristica(head)

            if str(head) not in self.padres.keys():
                self.padres[str(head)] = temp_head

            if head in self.explorado:
                continue

            if self.verificar_comida(head):
                self.comida_encontrada = True
                return 
            if [h, head] not in self.no_explorado:
                self.no_explorado.insert(0, [h, head])
                self.no_explorado.sort()

    def busqueda_A_star(self, temp_head = None):
        self.comida_encontrada = False
        self.no_explorado = []
        self.explorado = []
        self.padres = dict()

        if temp_head == None:
            temp_head = self.head.copy()
        orig_head = temp_head.copy()

        moves = self.mov_seguros(temp_head)

        for move in moves:
            head = temp_head.copy()
            head[0] += move[0]
            head[1] += move[1]
            h = self.heuristica(head)
            if str(head) not in self.padres.keys():
                self.padres[str(head)] = temp_head
            if self.verificar_comida(head):
                return move
            else:
                self.no_explorado.insert(0, [h, head])
                self.no_explorado.sort()
        
        while len(self.no_explorado) > 0:
            h_th = self.no_explorado.pop(0)
            self.astar_explorar(h_th[1])
            if self.comida_encontrada:
                break

        if self.comida_encontrada: # back track to move
            loc = self.comida
            while self.padres[str(loc)] != orig_head:
                loc = self.padres[str(loc)]
            return [loc[0] - orig_head[0], loc[1] - orig_head[1]]

        elif len(self.explorado) > 0: 
            loc = self.explorado[-1] # last point
            while self.padres[str(loc)] != orig_head:
                loc = self.padres[str(loc)]
            return [loc[0] - orig_head[0], loc[1] - orig_head[1]]

        else: # no path to food, no path to far point
            return self.wiggle_away() #safe_move() # rand.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])

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
        while exit_flag == False and self.game_state == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        vel = [-1, 0]
                    elif event.key == pygame.K_DOWN:
                        vel = [1, 0]
                    elif event.key == pygame.K_LEFT:
                        vel = [0, -1]
                    elif event.key == pygame.K_RIGHT:
                        vel = [0, 1]
                    else:
                        distancia = self.distancia
            
            time.sleep(1.0/fps)
            contador += 1
            if contador >= actualizar_rate:
                if player_ai != None:
                    vel = player_ai()
                self.actualizar_distancia(vel)
                self.actualizar_estado()
                contador = 0
            self.dibujar_tablero()
            pygame.display.update()
        label = myfont.render(f"Game Over!", 1, self.ROJO)
        self.SCREEN.blit(label, (self.ANCHO+10,50))
        pygame.display.update()
        while exit_flag == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True 
        pygame.quit()


def main():
    my_game = SnakeGameAStar()
    my_game.run_game(my_game.busqueda_A_star)

if __name__ == "__main__":
    main()