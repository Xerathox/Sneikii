# Snake Game implementando el algoritmo A*
# Renzo Mondragon
# Joaquin Aguirre
# Francesco Bassino

import numpy as np
import random as rnd
import os

# Clase Nodo
class Node():
	def __init__(self, parent=None, position=None):
		self.parent = parent
		self.position = position
		self.g, self.h, self.f = 0,0,0

	def __eq__(self, other):
		return self.position == other.position

class Sneikii():
	def __init__(self, height=15, width=15):
		# Estado de Juego
		self.gaming = True # Falso cuando es Game Over

		# Tablero
		self.height = height
		self.width  = width
		self.board  = np.zeros([self.height, self.width], dtype=int)
		self.score  = 0
		self.cost = 1

		# Direcciones
		self.inputs     = ["w","s","a","d"]
		self.directions = [[-1,0],[0,-1],[1,0],[0,1]]
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
		self.board[self.food[0], self.food[1]] = 3 # Marcar la comida de la serpiente en el tablero

		
	# Imprimir el tablero con la serpiente
	def __str__(self):
		os.system('cls' if os.name == 'nt' else 'clear') # Limpiar consola
		stringy = " " + "_"*self.width + "\n"
		for i in range(self.height):
			stringy += "|"
			for j in range(self.width):
				if self.board[i, j] == 2: # cabeza
					stringy += "X"
				elif self.board[i, j] == 1: # cuerpo
					stringy += "x"
				elif self.board[i, j] == 3: # comida
					stringy += "O"
				elif self.board[i, j] == 4: # camino
					stringy += "*"
				elif self.board[i, j] == 0: # vacio
					stringy += " "
			stringy += "|\n"
		stringy += u" \u0305"*self.width + "\n" # guion arriba
		stringy += f"Score: {self.score}" + "\n"
		#stringy += f"Pos: {self.head[0]}:{self.head[1]}" + "\n"
		#stringy += f"Pos2: {self.snake}" + "\n"
		return stringy
	
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
				self.board[self.food[0], self.food[1]] = 3

			else: # Mover serpiente
				self.snake.insert(0, self.head.copy())
				self.board[self.snake[1][0], self.snake[1][1]] = 1
				self.board[self.head[0], self.head[1]] = 2
				rem = self.snake.pop()
				self.board[rem[0], rem[1]] = 0
		# Movimiento invalido
		else:
			self.head = self.snake[0].copy()
	
	# Retorna el camino completo de la busqueda de A-star
	def solveAStar(self, currentNode):
		# Se explora el nodo final pasando por cada padre
		path = [] # Lista donde se guardara el camino
		current = currentNode
		while current is not None: # Hasta que ya no haya nodos padre (nodo de inicio)
			path.append(current.position)
			current = current.parent
		path = path[::-1] # Se invierte el camino porque se necesita mostrar de comienzo a final

		# El valor con el que se marcara el camino
		mark = 4

		# Marcamos el camino en el tablero
		for i in range(1,len(path)-1): # Imprimimos todo el camino excepto el primer y ultimo valor que representa inicio y final
			self.board[path[i][0]][path[i][1]] = mark
		
		# Devolvemos la direccion del primer paso
		for direction in self.directions:
			if self.head[0]+direction[0]==path[1][0] and self.head[1]+direction[1]==path[1][1]:
				return direction

		# Creamos una nueva matriz resultado con 0 en cada posicion
		#result = [[0 for i in range(self.width)] for j in range(self.height)]
		#for i in range(len(path)):
		#	result[path[i][0]][path[i][1]] = mark # Se marca el camino en la matriz
		#	#mark += 1 # Cada paso se incrementa 1 para señalar el orden
		#result = np.array(result)
		#return result

	# Busqueda informada de A-star
	def aStar(self):
		# Crear nodo de comienzo y final con los valores g,h,f inicializados
		startNode = Node(None, tuple(self.head))
		startNode.g = startNode.h = startNode.f = 0
		endNode = Node(None, tuple(self.food))
		endNode.g = endNode.h = endNode.f = 0

		# Iniciar las listas de visitado y por visitar
		toVisit = [] # Los que faltan visitar para explorar. Aqui se encuentra el nodo de menor costo para expandir luego
		visited = [] # Los que ya han sido explorados

		toVisit.append(startNode) # Agregamos el nodo inicial

		# Condiciones de parada
		iterations = 0 # Para evitar loops infinitos y detenerse luego de una cantidad razonable de iteraciones
		maxIterations = (len(self.board) // 2) ** 10 
		
		# Loop hasta que encuentre el final
		while len(toVisit) > 0:
			# Cada ves que un nodo es referido de la lista de toVisit, el contador de iteraciones incrementa
			iterations += 1	

			# Obtener el nodo a evaluar
			currentNode = toVisit[0]
			currentIndex = 0
			for index, item in enumerate(toVisit):
				if item.f < currentNode.f: # Obtener el nodo que tenga el valor f minimo
					currentNode = item
					currentIndex = index
					
			# Si se llega a este punto, existe una alta probabilidad que no haya solucion
			if iterations > maxIterations:
				print ("Muchas iteraciones, cancelando el proceso de busqueda.")
				return self.solveAStar(currentNode) # Se retorna el camino del ultimo nodo evaluado

			# Eliminar el nodo de la lista de los que faltan visitar y agregarlo a la lista de los visitados
			toVisit.pop(currentIndex)
			visited.append(currentNode)

			# Comprobar si se ha alcanzado el destino
			if currentNode == endNode:
				return self.solveAStar(currentNode) # Retornar el camino hasta el nodo actual

			# Generar nodos hijos para todos los cuadrados adyacentes del nodo
			children = []
			for direction in self.directions: # Iterar por cada direccion (arriba, abajo, derecha, izquierda)
				# Generar la nueva posicion del nodo utilizando una direccion
				nodePosition = (currentNode.position[0] + direction[0], currentNode.position[1] + direction[1])

				# Comprobar si esta dentro de los limites del tablero
				if (nodePosition[0] > (self.height - 1) or 
					nodePosition[0] < 0 or 
					nodePosition[1] > (self.width -1) or 
					nodePosition[1] < 0):
					continue

				# Comprobar si no hay obstaculos
				if self.board[nodePosition[0]][nodePosition[1]] not in [0,2,3,4]:
					continue

				# Nuevo nodo
				newNode = Node(currentNode, nodePosition)
				children.append(newNode) # Agregar a la lista de nodos hijos

			# Iterar a traves de los nodos hijos
			for child in children:
				
				# Comprobar que el nodo hijo no esta en la lista de los visitados
				if len([visited_child for visited_child in visited if visited_child == child]) > 0:
					continue

				# Generar los valores f, g y h
				child.g = currentNode.g + self.cost # Aqui se podria utilizar el valor de la arista, si es que existiese
	
				# Coste de heuristica es calculado aqui, utilizando la distancia euclidiana
				child.h = (((child.position[0]-endNode.position[0]) ** 2) +  ((child.position[1]-endNode.position[1])** 2))**0.5 
				child.f = child.g + child.h

				# Comprobar si el nodo hijo ya esta en la lista de los que faltan visitar y si es costo g es ya es mas bajo
				if len([i for i in toVisit if child == i and child.g > i.g]) > 0:
					continue

				# Agregar el nodo hijo a la lista de los que faltan visitar
				toVisit.append(child)
	

# # # JUEGO # # #
game = Sneikii(15,30)
while game.gaming:
	print(game)

	### Mover Manualmente
	rawInput = input("enter: ")
	#print(rawInput)
	#direccion = game.processInput(rawInput)
	direccion = game.aStar()
	print(direccion)

	game.updateDirection(direccion)
	game.updateState()

print("Game Over")