import numpy as np
import random

rand = random.Random()

class SnakeGame():
    
    def __init__(self):
        self.game_state = True # False when Game Over
        self.alto = 30
        self.ancho = 30
        self.tamaño = [self.alto, self.ancho]
        self.tablero = np.zeros(self.tamaño)
        self.puntaje = 0
        self.head = [self.alto//2, self.ancho//2]  
        self.distancia = rand.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])
        self.snake = [[self.head[0] - i*self.distancia[0], self.head[1] - i*self.distancia[1]] for i in range(3)]
        for s in self.snake:
            self.tablero[s[0], s[1]] = 1
        self.tablero[self.head[0], self.head[1]] = 2
        self.comida = self.comida_aleatoria()
        self.tablero[self.comida[0], self.comida[1]] = -1
    
    def __str__(self):
        b_str = " " + "_"*self.ancho + f"  Score: {self.puntaje}\n"
        for i in range(self.alto):
            b_str += "|"
            for j in range(self.ancho):
                if self.tablero[i, j] == 2:
                # if [i, j] == self.head:
                    b_str += "X"
                elif self.tablero[i, j] == 1:
                # elif [i, j] in self.snake:
                    b_str += "x"
                elif self.tablero[i, j] == -1:
                # elif [i, j] == self.food:
                    b_str += "O"
                else:
                    b_str += " "
            b_str += "|\n"
        b_str += u" \u0305"*self.ancho 
        return b_str

    def comida_aleatoria(self):
        espacios_vacios = [[i, j] for i in range(self.alto) for j in range(self.ancho) if self.tablero[i, j] == 0]
        return rand.choices(espacios_vacios)[0]
    
    def actualizar_distancia(self, distancia):
        temp_head = [self.head[0] + distancia[0], self.head[1] + distancia[1]]
        if temp_head != self.snake[1]: # make sure it's not previous body part
            self.distancia = distancia

    def actualizar_estado(self):
        self.head[0] += self.distancia[0]
        self.head[1] += self.distancia[1]

        if self.head[0] < 0 or self.head[0] >= self.alto:
            self.head = self.snake[0].copy() # did not enter valid move
            self.game_state = False

        elif self.head[1] < 0 or self.head[1] >= self.ancho:
            self.head = self.snake[0].copy() # did not enter valid move
            self.game_state = False

        elif self.head in self.snake[2::]: # snake in body and no u-turn
            self.head = self.snake[0].copy() # did not enter valid move
            self.game_state = False 

        elif self.head not in self.snake: # snake moved
            if self.head == self.comida: # ate food, grow snake, gen food
                self.puntaje += 1
                self.snake.insert(0, self.head.copy())
                self.tablero[self.snake[1][0], self.snake[1][1]] = 1
                self.tablero[self.head[0], self.head[1]] = 2
                self.comida = self.comida_aleatoria()
                self.tablero[self.comida[0], self.comida[1]] = -1

            else: # move snake
                self.snake.insert(0, self.head.copy())
                self.tablero[self.snake[1][0], self.snake[1][1]] = 1
                self.tablero[self.head[0], self.head[1]] = 2
                rem = self.snake.pop()
                self.tablero[rem[0], rem[1]] = 0
                
        else:
            self.head = self.snake[0].copy() # did not enter valid move
