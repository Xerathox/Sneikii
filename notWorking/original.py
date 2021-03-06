# Snake Game implementando el algoritmo A*
# Renzo Mondragon
# Joaquin Aguirre
# Francesco Bassino

import numpy as np
import random as rnd
import os

rand = rnd.Random()

# Clase Nodo
class Node():
	def __init__(self, parent=None, position=None):
		self.parent = parent
		self.position = position
		self.f, self.g, self.h = 0,0,0

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
		self.inputs	 = ["w","s","a","d"]
		self.directions = [[-1,0],[0,-1],[1,0],[0,1]]
		self.direction  = rnd.Random().choice(self.directions) # Obtener una direccion aleatoria
		self.reverse	= None

		# Serpiente
		self.head  = [self.height//2, self.width//2] # Ubicar la serpiente al medio
		self.snake = [[self.head[0] - i*self.direction[0], self.head[1] - i*self.direction[1]] for i in range(3)] # Obtener coordenadas del cuerpo de la serpiente segun la posicion de la cabeza
		
		# Rellenar Tablero, 0: vacio, -1 : comida, 1 : cuerpo, 2 : cabeza
		for s in self.snake: # Ubicar la serpiente en la matriz 2d tablero
			self.board[s[0],s[1]] = 1 # board[x,y] = board[x][y]
		self.board[self.head[0], self.head[1]] = 2 # Marcar la cabeza de la serpiente en el tablero
		self.food = self.getRandomBlank()
		self.board[self.food[0], self.food[1]] = 3 # Marcar la comida de la serpiente en el tablero

		#### TEST
		self.reversa = 1
		self.temp_head_orig = []

		
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
					stringy += "+"
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
		# Obtener un listado de ubicaciones vacias (=0)
		blanks = [[i, j] for i in range(self.height) for j in range(self.width) if self.board[i, j] == 0]
		# Elegir aleatoriamente de todas las ubicaciones vacias
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
			# Obtuvo comida
			if self.head == self.food: 
				# Aumentar el puntaje	
				self.score += 1
				# Serpiente crece, insertar posicion actual al comienzo de la lista
				self.snake.insert(0, self.head.copy()) 
				# Marcar la posicion anterior de la cabeza como cola
				self.board[self.snake[1][0], self.snake[1][1]] = 1
				# Actualizar la posicion de la cabeza
				self.board[self.head[0], self.head[1]] = 2
				# Generar mas comida obteniendo una posicion vacia aleatoria
				self.food = self.getRandomBlank()
				# Marcar la comida en el tablero
				self.board[self.food[0], self.food[1]] = 3

			# Mover serpiente
			else: 
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
		for i in range(self.height): # Se limpia cualquier camino que se haya trazado anteriormente
			for j in range(self.width):
				if self.board[i][j] == 4:
					self.board[i][j] = 0
		
		# Marcamos el camino en el tablero
		for i in range(1,len(path)-1): # Imprimimos todo el camino excepto el primer y ultimo valor que representa inicio y final
			self.board[path[i][0]][path[i][1]] = mark
			pass
		
		# Devolvemos la direccion del primer paso
		for direction in self.directions:
			if self.head[0]+direction[0]==path[1][0] and self.head[1]+direction[1]==path[1][1]:
				return direction

		# Creamos una nueva matriz resultado con 0 en cada posicion
		#result = [[0 for i in range(self.width)] for j in range(self.height)]
		#for i in range(len(path)):
		#	result[path[i][0]][path[i][1]] = mark # Se marca el camino en la matriz
		#	#mark += 1 # Cada paso se incrementa 1 para se??alar el orden
		#return np.array(result)

	# Busqueda informada de A-star
	def aStar(self, ending = None):
		# Crear nodo de comienzo y final con los valores g,h,f inicializados
		startNode = Node(None, self.head)
		endNode = Node(None, (ending or self.food)) # Revisar si el ending ha sido declarado o no

		# Iniciar las listas de visitado y por visitar
		toVisit = [] # Los que faltan visitar para explorar. Aqui se encuentra el nodo de menor costo para expandir luego
		visited = [] # Los que ya han sido explorados

		toVisit.append(startNode) # Agregamos el nodo inicial
		
		# Loop hasta que encuentre el final
		while len(toVisit) > 0:

			# Obtener el nodo a evaluar
			# Eliminar el nodo de la lista de los que faltan visitar y agregarlo a la lista de los visitados
			currentNode = toVisit.pop(0)
			visited.append(currentNode)

			# Comprobar si se ha alcanzado el destino
			if currentNode == endNode:
				return self.solveAStar(currentNode) # Retornar el camino hasta el nodo actual

			# Generar nodos hijos para todos los cuadrados adyacentes del nodo
			for direction in self.directions: # Iterar por cada direccion (arriba, abajo, derecha, izquierda)
				# Generar la nueva posicion del nodo utilizando una direccion
				nodePosition = [currentNode.position[0] + direction[0], currentNode.position[1] + direction[1]]

				# Comprobar si esta dentro de los limites del tablero
				if (nodePosition[0] > (self.height-1) or 
					nodePosition[0] < 0 or 
					nodePosition[1] > (self.width-1) or 
					nodePosition[1] < 0):
					continue

				# Comprobar si no hay obstaculos
				if self.board[nodePosition[0]][nodePosition[1]] == 1:
					continue

				# Nuevo nodo
				newNode = Node(currentNode, nodePosition)

				# Generar los valores f, g y h
				newNode.g = currentNode.g + self.cost # Aqui se podria utilizar el valor de la arista, si es que existiese
				# Coste de heuristica es calculado aqui, utilizando la distancia euclidiana
				newNode.h = (((newNode.position[0]-endNode.position[0]) ** 2) +  ((newNode.position[1]-endNode.position[1])** 2))**0.5 
				newNode.f = newNode.g + newNode.h

				# Comprobar que el nodo no esta en la lista de los visitados
				if newNode in visited:
					continue
				
				# Comprobar que el nodo no esta en la lista de los que faltan visitar
				if newNode not in toVisit:
					# Agregar el nodo hijo a la lista de los que faltan visitar
					toVisit.insert(0, newNode)
					# Ordenar la lista para que el primer nodo sea el del valor f minimo
					toVisit.sort(key = lambda x: x.f)
					# Revertir la lista para agarrar primero al que tenga el valor f maximo
					if endNode.position != self.food:
						toVisit.reverse()

	# Primera version de a-star
	def aStarSlow(self):
		# Crear nodo de comienzo y final con los valores g,h,f inicializados
		startNode = Node(None, tuple(self.head))
		#startNode.g = startNode.h = startNode.f = 0
		endNode = Node(None, tuple(self.food))
		#endNode.g = endNode.h = endNode.f = 0

		# Iniciar las listas de visitado y por visitar
		toVisit = [] # Los que faltan visitar para explorar. Aqui se encuentra al nodo de menor costo para expandir luego
		visited = [] # Los que ya han sido explorados

		toVisit.append(startNode) # Agregamos el nodo inicial

		# Condiciones de parada
		iterations = 0 # Para evitar loops infinitos y detenerse luego de una cantidad razonable de iteraciones
		maxIterations = (len(self.board) // 2) ** 10 
		
		# Loop hasta que encuentre el final
		while len(toVisit) > 0:
			if iterations % 2500 == 0:
				print(iterations)
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
				if child in visited: #if len([visitedChild for visitedChild in visited if visitedChild == child]) > 0:
					continue

				# Generar los valores f, g y h
				child.g = currentNode.g + self.cost # Aqui se podria utilizar el valor de la arista, si es que existiese
	
				# Coste de heuristica es calculado aqui, utilizando la distancia euclidiana
				child.h = (((child.position[0]-endNode.position[0]) ** 2) +  ((child.position[1]-endNode.position[1])** 2))**0.5 
				child.f = child.g + child.h

				# Comprobar si el nodo hijo ya esta en la lista de los que faltan visitar y si el costo g es ya es mas bajo
				for i in toVisit:
					if child == i and child.g > i.g:
						continue
				#if len([i for i in toVisit if child == i and child.g > i.g]) > 0:
				#	continue

				# Agregar el nodo hijo a la lista de los que faltan visitar
				toVisit.append(child)
	
	def revAStar(self):
		# Iniciar matrices donde se guardaran los espacios en blanco validos
		blanks, visited, toVisit = [], [], []
		# A??adir el nodo inicial a la lista por visitar
		toVisit.append(self.head)
		blanks.append(self.head)
		while len(toVisit) > 0:
			position = toVisit.pop(0)
			visited.append(position)
			for direction in self.directions:
				# Generar la nueva posicion del nodo utilizando una direccion
				newPosition = [position[0] + direction[0], position[1] + direction[1]]
				# Comprobar si esta dentro de los limites del tablero
				if (newPosition[0] > (self.height-1) or 
					newPosition[0] < 0 or 
					newPosition[1] > (self.width-1) or 
					newPosition[1] < 0):
					continue
				# Comprobar si no hay obstaculos
				if self.board[newPosition[0]][newPosition[1]] == 1:
					continue
				# Comprobar que el nodo no esta en la lista de los visitados
				if newPosition in visited:
					continue
				# Comprobar que el nodo no esta en la lista de los que faltan visitar
				if newPosition not in toVisit:
					# Agregar el nodo hijo a la lista de los que faltan visitar
					toVisit.append(newPosition)
					blanks.append(newPosition)
		
		# Escoger el nodo mas cercano a la comida como el destino
		mini, near = 1e9, None
		for i in range(len(blanks)):
			heuristic = ((blanks[i][0]-self.food[0])**2+(blanks[i][1]-self.food[1])**2)**0.5
			if heuristic < mini:
				mini = heuristic
				near = blanks[i].copy()
		
		return self.aStar(near)

	# Encontrar todos los caminos y elegir el mas largo para hacer tiempo
	def buyTime(self):
		# Iniciar matrices donde se guardaran los espacios en blanco validos
		blanks, visited, toVisit = [], [], []
		# A??adir el nodo inicial a la lista por visitar
		toVisit.append(self.head)
		blanks.append(self.head)
		while len(toVisit) > 0:
			position = toVisit.pop(0)
			visited.append(position)
			for direction in self.directions:
				# Generar la nueva posicion del nodo utilizando una direccion
				newPosition = [position[0] + direction[0], position[1] + direction[1]]
				# Comprobar si esta dentro de los limites del tablero
				if (newPosition[0] > (self.height-1) or 
					newPosition[0] < 0 or 
					newPosition[1] > (self.width-1) or 
					newPosition[1] < 0):
					continue
				# Comprobar si no hay obstaculos
				if self.board[newPosition[0]][newPosition[1]] == 1:
					continue
				# Comprobar que el nodo no esta en la lista de los visitados
				if newPosition in visited:
					continue
				# Comprobar que el nodo no esta en la lista de los que faltan visitar
				if newPosition not in toVisit:
					# Agregar el nodo hijo a la lista de los que faltan visitar
					toVisit.append(newPosition)
					blanks.append(newPosition)
				
		# Sortear la lista
		blanks.sort()

		# Convertir a grafo con sus nodos adyacentes
		graph = [[] for i in range(len(blanks))]
		for i in range(len(blanks)):
			for direction in self.directions:
				newPosition = [blanks[i][0] + direction[0], blanks[i][1] + direction[1]]
				if (newPosition[0] > (self.height-1) or 
					newPosition[0] < 0 or 
					newPosition[1] > (self.width-1) or 
					newPosition[1] < 0):
					continue
				if self.board[newPosition[0]][newPosition[1]] == 1:
					continue
				graph[i].append(blanks.index(newPosition))

		## Imprimir
		#for i in range(len(graph)):
		#	print(blanks[i],": ",sep="",end="")
		#	for j in range(len(graph[i])):
		#		print(blanks[graph[i][j]],end=" ")
		#	print()

		# Escoger el nodo mas cercano a la comida como el destino
		mini, near = 1e9, None
		for i in range(len(blanks)):
			heuristic = ((blanks[i][0]-self.food[0])**2+(blanks[i][1]-self.food[1])**2)**0.5
			if heuristic < mini:
				mini = heuristic
				near = blanks[i].copy()
		
		# Encontrar el inicio y final en el grafo
		start, end = None, None
		for i in range(len(graph)):
			for j in range(len(graph[i])):
				if self.head == blanks[graph[i][j]]:
					start = graph[i][j]
				if near == blanks[graph[i][j]]:
					end = graph[i][j]

		# Generar todos los caminos posibles
		visited = [False for i in range(len(graph))]
		path, answer = [], []
		def dfs(graphic, start, end, visited, path, answer):
			visited[start] = True
			path.append(start)
			aux = []
			if start == end:
				aux += path
				answer.append(aux)
			else:
				for v in graphic[start]:
					if visited[v] == False:
						dfs(graphic, v, end, visited, path, answer)
			path.pop()
			visited[start] = False
		dfs(graph,start,end,visited,path,answer)

		# Elegir el camino mas largo de todos los caminos posibles
		maxi, index = 0, 0
		for idx, i in enumerate(answer):
			if len(i) > maxi:
				maxi = len(i)
				index = idx
		answer = answer[index]

		# Reconstruir el camino con las ubicaciones adecuadas
		path = []
		for i in range(len(answer)):
			print(blanks[answer[i]])
			path.append(blanks[answer[i]])

		return path

	# Frany
	def mov_lista(self, movimientos, mov_no_seguros):
		for mov in movimientos:
			temp_head = self.temp_head_orig.copy()
			temp_head[0] += mov[0]
			temp_head[1] += mov[1]

			if temp_head[0] < 0 or temp_head[0] >= self.height:
				mov_no_seguros.append(mov)
			elif temp_head[1] < 0 or temp_head[1] >= self.width:
				mov_no_seguros.append(mov)
			elif temp_head in self.snake: 
				mov_no_seguros.append(mov)

		for mov in mov_no_seguros:
			movimientos.remove(mov)
		
		return movimientos

	def mov_seguros(self, temp_head = None): 
		movimientos = self.directions.copy()
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
		
		d0 = -self.food[0] + self.head[0]
		if d0 != 0:
			dir_comida.append([d0//abs(d0), 0])

		d1 = -self.food[1] + self.head[1]
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

	def busqueda_A_star(self):
		comida_encontrada = False
		no_explorado = []
		explorado = []
		padres = dict()
		
		no_explorado.insert(0,[0,self.head])

		# Explorar los nodos adyacentes y expandir cada uno
		while len(no_explorado) > 0:
			h_th = no_explorado.pop(0)

			## ASTART EXPLORE
			explorado.append(h_th[1])
			movimientos = self.mov_seguros(h_th[1])

			for mov in movimientos:
				head = h_th[1].copy()
				head[0] += mov[0]
				head[1] += mov[1]
				h = ((self.food[0] - head[0])**2 + (self.food[1] - head[1])**2)**0.5

				if str(head) not in padres.keys():
					padres[str(head)] = h_th[1]

				if head in explorado:
					continue

				if self.food[0] == head[0] and self.food[1] == head[1]:
					comida_encontrada = True
					break
					#return 

				if [h, head] not in no_explorado:
					no_explorado.insert(0, [h, head])
					no_explorado.sort()
			## END

			if comida_encontrada:
				break

		if comida_encontrada: # backtrack para moverse
			loc = self.food
			while padres[str(loc)] != self.head:
				loc = padres[str(loc)]
			return [loc[0] - self.head[0], loc[1] - self.head[1]]

		elif len(explorado) > 0: 
			loc = explorado[-1] # ultimo punto
			while padres[str(loc)] != self.head:
				loc = padres[str(loc)]
			return [loc[0] - self.head[0], loc[1] - self.head[1]]

		else: # no hay camino para comida, no hay camino para el punto lejano
			return self.deslizarse() #mov_seguro() # rand.opciones([[1, 0], [-1, 0], [0, 1], [0, -1]])

# # # JUEGO # # #
game = Sneikii(30,30)
while game.gaming:
	#print(game)
	os.system('cls' if os.name == 'nt' else 'clear') # Limpiar consola
	print(game)

	### Mover Manualmente
	#rawInput = input("input:")
	#direccion = game.processInput(rawInput)
	#direccion = game.aStar()
	#if direccion == None:
	#	direccion = game.revAStar()

	direccion = game.busqueda_A_star()
	print("direccion",direccion)

	game.updateDirection(direccion)
	game.updateState()

print("Game Over")
