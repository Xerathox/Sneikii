import numpy as np
import random as rnd

rand = rnd.Random()

class SnakeGame():
	def __init__(self, height=15, width=15):
		self.game_state = True # False cuando es Game Over
		self.height = height
		self.width = width
		self.size = [self.height, self.width]
		self.board = np.zeros(self.size)
		self.score = 0
		self.head = [self.height//2, self.width//2]  
		self.direccion = rand.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])
		self.snake = [[self.head[0] - i*self.direccion[0], self.head[1] - i*self.direccion[1]] for i in range(3)]
		for s in self.snake:
			self.board[s[0], s[1]] = 1
		self.board[self.head[0], self.head[1]] = 2
		self.food = self.comida_aleatoria()
		self.board[self.food[0], self.food[1]] = -1
		
		self.reverse = None

	
	def __str__(self): # Para la impresion
		b_str = " " + "_"*self.width + f"  Score: {self.score}\n"
		for i in range(self.height):
			b_str += "|"
			for j in range(self.width):
				if self.board[i, j] == 2: # if [i, j] == self.head
					b_str += "X"
				elif self.board[i, j] == 1: # elif [i, j] in self.snake:
					b_str += "x"
				elif self.board[i, j] == -1: # elif [i, j] == self.food:
					b_str += "O"
				else:
					b_str += " "
			b_str += "|\n"
		b_str += u" \u0305"*self.width 
		return b_str

	def input_movimiento(self,move):
		moves = ["w","s","a","d"]
		dirs = [[-1,0],[1,0],[0,-1],[0,1]]

		for i, v in enumerate(moves):
			if move == v:
				return dirs[i]
		
		return self.direccion


	def comida_aleatoria(self):
		espacios_vacios = [[i, j] for i in range(self.height) for j in range(self.width) if self.board[i, j] == 0]
		return rand.choices(espacios_vacios)[0]
	
	def actualizar_direccion(self, direccion):
		temp_head = [self.head[0] + direccion[0], self.head[1] + direccion[1]]
		if temp_head != self.snake[1]: # make sure it's not previous body part
			self.direccion = direccion

	def actualizar_estado(self):
		self.head[0] += self.direccion[0]
		self.head[1] += self.direccion[1]

		if self.head[0] < 0 or self.head[0] >= self.height:
			self.head = self.snake[0].copy() # did not enter valid move
			self.game_state = False
		elif self.head[1] < 0 or self.head[1] >= self.width:
			self.head = self.snake[0].copy() # did not enter valid move
			self.game_state = False
		elif self.head in self.snake[2::]: # snake in body and no u-turn
			self.head = self.snake[0].copy() # did not enter valid move
			self.game_state = False 
		elif self.head not in self.snake: # snake moved
			if self.head == self.food: # ate food, grow snake, gen food
				self.score += 1
				self.snake.insert(0, self.head.copy())
				self.board[self.snake[1][0], self.snake[1][1]] = 1
				self.board[self.head[0], self.head[1]] = 2
				self.food = self.comida_aleatoria()
				self.board[self.food[0], self.food[1]] = -1
			else: # move snake
				self.snake.insert(0, self.head.copy())
				self.board[self.snake[1][0], self.snake[1][1]] = 1
				self.board[self.head[0], self.head[1]] = 2
				rem = self.snake.pop()
				self.board[rem[0], rem[1]] = 0
		else:
			self.head = self.snake[0].copy() # did not enter valid move
	
	def ver_comida(self, loc):
		if self.food[0] == loc[0] and self.food[1] == loc[1]:
			return True
		else:
			return False

	def espacio_vacio(self):
		return [[i, j] for i in range(self.height) for j in range(self.width) if self.board[i, j] == 0 or self.board[i, j] == -1]

	def mov_no_seguro(self, moves, no_seguros):
		for move in moves:
			temp_head = self.head.copy()
			temp_head[0] += move[0]
			temp_head[1] += move[1]

			if temp_head[0] < 0 or temp_head[0] >= self.height:
				no_seguros.append(move)
			elif temp_head[1] < 0 or temp_head[1] >= self.width:
				no_seguros.append(move)
			elif temp_head in self.snake:
				no_seguros.append(move)
		
		for move in no_seguros:
			moves.remove(move)
		
		return moves

	def moverse_lejos(self):
		moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
		no_seguros = []
		direc_food = []
		
		d0 = -self.food[0] + self.head[0]
		if d0 != 0:
			direc_food.append([d0 // abs(d0), 0])

		d1 = -self.food[1] + self.head[1]
		if d1 != 0:
			direc_food.append([0, d1 // abs(d1)])

		# eliminar movimientos no seguros
		moves = self.mov_no_seguro(moves, no_seguros)

		# moverse hacia la comida primer
		self.reverse *= -1 # para ir cambiando de direccion
		for move in moves[::self.reverse]:
			if move in direc_food:
				return move
			
		if len(moves) == 0: # no hay movimientos seguros
			return [1, 0]
		else:
			return rand.choice(moves)

	def heuristica(self, head):
		# distancia Manhattan
		d0 = self.food[0] - head[0]
		d1 = self.food[1] - head[1]
		return np.sqrt(d0**2 + d1**2)
	
	def get_movimiento_seguro(self, temp_head = None):
		moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
		no_seguro = []
		if temp_head == None:
			temp_head_orig = self.head.copy()
		else:
			temp_head_orig = temp_head.copy()
		# quitar movimientos no seguros
		moves = self.mov_no_seguro(moves, no_seguro)
		
		return moves

	def movimiento_seguro(self):
		moves = self.get_movimiento_seguro()
		if len(moves) == 0:
			moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
		return rand.choice(moves)

	def A_star(self, temp_head):
		self.food_found = False
		self.not_explored = []
		self.explored = []
		self.parents = dict()
		self.explored.append(temp_head)
		moves = self.get_movimiento_seguro(temp_head)

		for move in moves:
			head = temp_head.copy()
			head[0] += move[0]
			head[1] += move[1]
			h = self.heuristica(head) # aplicamos la heuristica

			if str(head) not in self.parents.keys():
				self.parents[str(head)] = temp_head
			
			if head in self.explored:
				continue
			
			if self.ver_comida(head):
				self.food_found = True
				return
			
			if [h, head] not in self.not_explored:
				self.not_explored.insert(0, [h, head])
				self.not_explored.sort()

	def busqueda_A_star(self, temp_head = None):
		self.food_found = False
		self.not_explored = []
		self.explored = []
		self.parents = dict()
		if temp_head == None:
			temp_head = self.head.copy()
		orig_head = temp_head.copy()

		moves = self.get_movimiento_seguro(temp_head)

		for move in moves:
			head = temp_head.copy()
			head[0] += move[0]
			head[1] += move[1]
			h = self.heuristica(head)
			if str(head) not in self.parents.keys():
				self.parents[str(head)] = temp_head
			if self.ver_comida(head):
				return move
			else:
				self.not_explored.insert(0, [h, head])
				self.not_explored.sort()
		
		while len(self.not_explored) > 0:
			h_th = self.not_explored.pop(0)
			self.A_star(h_th[0])
			if self.food_found:
				break
		
		if self.food_found:
			location = self.food
			while self.parents[str(location)] != orig_head:
				location = self.parents[str(location)]
			return [location[0] - orig_head[0], location[1] - orig_head[1]]
		elif len(self.explored) > 0:
			location = self.explored[-1]
			while self.parents[str(location)] != orig_head:
				location = self.parents[str(location)]
			return [location[0] - orig_head[0], location[1] - orig_head[1]]
		else:
			return self.moverse_lejos()


## MAIN
				
game = SnakeGame(15,30)
while game.game_state:
	print(game)

	### Mover Manualmente
	move = input("Enter move: ")
	dire = game.input_movimiento(move)
	
	### Mover automaticamente
	# Correr a-star
	# Obtener una lista de movimientos
	# Pop a esa lista de movimientos -> dir
	# Cuando el score cambie, correr a-start nuevamente

	print(game.busqueda_A_star()) #default

	game.actualizar_direccion(dire)
	game.actualizar_estado()
