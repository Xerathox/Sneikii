# Snake Game implementando el algoritmo A*
# Renzo Mondragon
# Joaquin Aguirre
# Francesco Bassino

import numpy as np
import random as rnd
import os

rand = rnd.Random()

class Sneikii():
	def __init__(self, height=15, width=15):
		# Estado de Juego
		self.gaming = True # Falso cuando es Game Over

		# Tablero
		self.height = height
		self.width  = width
		self.board  = np.zeros([self.height, self.width])
		self.score  = 0

		# Direcciones
		self.inputs     = ["w","s","a","d"]
		self.directions = [[-1,0],[1,0],[0,-1],[0,1]]
		self.direction  = rnd.Random().choice(self.directions) # Obtener una direccion aleatoria
		self.reverse    = None

		# Serpiente
		self.head  = [self.height//2, self.width//2] # Ubicar la serpiente al medio
		self.snake = [[self.head[0] - i*self.direction[0], self.head[1] - i*self.direction[1]] for i in range(3)] # Obtener coordenadas del cuerpo de la serpiente segun la posicion de la cabeza
		
		# Rellenar Tablero, 0: vacio, -1 : comida, 1 : cuerpo, 2 : cabeza
		for s in self.snake: # Ubicar la serpiente en la matriz 2d tablero
			self.board[s[0],s[1]] = 1 # board[x,y] = board[x][y]
		self.board[self.head[0], self.head[1]] = 2 # Marcar la cabeza de la serpiente en el tablero
		self.food = self.getRandomBlank()
		self.board[self.food[0], self.food[1]] = -1 # Marcar la comida de la serpiente en el tablero

		
	# Imprimir el tablero con la serpiente
	def __str__(self):
		os.system('cls' if os.name == 'nt' else 'clear') # Limpiar consola
		b_str = " " + "_"*self.width + "\n"
		for i in range(self.height):
			b_str += "|"
			for j in range(self.width):
				if self.board[i, j] == 2: # cabeza
					b_str += "X"
				elif self.board[i, j] == 1: # cuerpo
					b_str += "x"
				elif self.board[i, j] == -1: # comida
					b_str += "O"
				elif self.board[i, j] == 0: # vacio
					b_str += " "
			b_str += "|\n"
		b_str += u" \u0305"*self.width + "\n" # guion arriba
		b_str += f"Score: {self.score}" + "\n"
		b_str += f"Pos: {self.head[0]}:{self.head[1]}" + "\n"
		b_str += f"Pos2: {self.snake}" + "\n"
		return b_str
	
	# Busca espacios en desocupados y devuelve una coordenada aleatoria 
	def getRandomBlank(self):
		blanks = [[i, j] for i in range(self.height) for j in range(self.width) if self.board[i, j] == 0]
		return rnd.Random().choices(blanks)[0]
	
	# Actualizar la direccion
	def updateDirection(self, direction):
		tempHead = [self.head[0] + direction[0], self.head[1] + direction[1]]
		if tempHead != self.snake[1]: # se asegura que no es una parte del cuerpo previa
			self.direction = direction
	
	# Procesar entradas de movimiento
	def processInput(self,rawInput):
		for i, move in enumerate(self.inputs):
			if rawInput == move:
				return self.directions[i]
		return self.direction
	
	# Actualizar el estado del juego
	def updateState(self):
		self.head[0] += self.direction[0]
		self.head[1] += self.direction[1]
		# Limite vertical
		if self.head[0] < 0 or self.head[0] >= self.height:
			self.head = self.snake[0].copy() # movimiento invalido
			self.gaming = False
		# Limite horizontal
		elif self.head[1] < 0 or self.head[1] >= self.width:
			self.head = self.snake[0].copy() # movimiento invalido
			self.gaming = False
		# Choca con su propio cuerpo
		elif self.head in self.snake[2::]: # serpiente en cuerpo y no hay vuelta en U
			self.head = self.snake[0].copy() # movimiento invalido
			self.gaming = False
		# Movimiento valido
		elif self.head not in self.snake:
			if self.head == self.food: # Obtuvo comida
				self.score += 1
				self.snake.insert(0, self.head.copy()) # Serpiente crece
				self.board[self.snake[1][0], self.snake[1][1]] = 1
				self.board[self.head[0], self.head[1]] = 2
				self.food = self.getRandomBlank() # Generar mas comida
				self.board[self.food[0], self.food[1]] = -1

			else: # Mover serpiente
				self.snake.insert(0, self.head.copy())
				self.board[self.snake[1][0], self.snake[1][1]] = 1
				self.board[self.head[0], self.head[1]] = 2
				rem = self.snake.pop()
				self.board[rem[0], rem[1]] = 0
		# Movimiento invalido
		else:
			self.head = self.snake[0].copy()
	
	# MOVIMIENTO AUTONOMO # Bassino

	

# # # JUEGO # # #
game = Sneikii(15,30)
while game.gaming:
	print(game)

	### Mover Manualmente
	rawInput = input("Movimiento: ")
	direccion = game.processInput(rawInput)
	
	### Mover automaticamente
	# Correr a-star
	# Obtener una lista de movimientos
	# Pop a esa lista de movimientos -> dir
	# Cuando el score cambie, correr a-start nuevamente

	#print(game.busqueda_A_star()) #default

	game.updateDirection(direccion)
	game.updateState()

print("Game Over")