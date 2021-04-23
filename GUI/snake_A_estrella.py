from snake_game_GUI import SnakeGameGUI
import pygame
import random
import numpy as np

rand = random.Random()

class SnakeGameAStar(SnakeGameGUI):
    
    def __init__(self, headless_mode = False):
        super().__init__(headless_mode)
        self.reversa = 1
        self.temp_head_orig = []

    def mov_lista(self, movimientos, mov_no_seguros):
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

    def mov_seguros(self, temp_head = None): 
        movimientos = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        mov_no_seguros = []

        if temp_head == None:
            self.temp_head_orig = self.head.copy()
        else:
            self.temp_head_orig = temp_head.copy()
        
        return self.mov_lista(movimientos, mov_no_seguros)

    def deslizarse(self):
        movimientos = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        mov_no_seguros = []
        dir_comida = []
        
        d0 = -self.comida[0] + self.head[0]
        if d0 != 0:
            dir_comida.append([d0//abs(d0), 0])

        d1 = -self.comida[1] + self.head[1]
        if d1 != 0:
            dir_comida.append([0, d1//abs(d1)])

        # remover movimientos no seguros
        movimientos = self.mov_lista(movimientos, mov_no_seguros)
                
        # moverse primero hacia la comida
        self.reversa *= -1 # para alterar cambio de direccion
        for mov in movimientos[::self.reversa]:
        # for move in moves:
            if mov in dir_comida:
                return mov
            
        if len(movimientos) == 0: # no hay mov seguross
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

        if self.comida_encontrada: # backtrack para moverse
            loc = self.comida
            while self.padres[str(loc)] != orig_head:
                loc = self.padres[str(loc)]
            return [loc[0] - orig_head[0], loc[1] - orig_head[1]]

        elif len(self.explorado) > 0: 
            loc = self.explorado[-1] # ultimo punto
            while self.padres[str(loc)] != orig_head:
                loc = self.padres[str(loc)]
            return [loc[0] - orig_head[0], loc[1] - orig_head[1]]

        else: # no hay camino para comida, no hay camino para el punto lejano
            return self.deslizarse() #mov_seguro() # rand.opciones([[1, 0], [-1, 0], [0, 1], [0, -1]])


def main():
    my_game = SnakeGameAStar()
    my_game.run_game(my_game.busqueda_A_star)

if __name__ == "__main__":
    main()