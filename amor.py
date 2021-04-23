import numpy as np
import random as rnd

# Clase Nodo
class Node():
	def __init__(self, parent=None, position=None):
		self.parent = parent
		self.position = position
		self.g, self.h, self.f = 0,0,0

	
	def __eq__(self, other):
		return self.position == other.position

# Clase Board
class Board():
	def __init__(self, height=10, width=10):
		self.height = height
		self.width = width
		self.board = np.zeros([self.height, self.width], dtype=int)
		self.cost = 1
		self.directions = [[-1,0],[0,-1],[1,0],[0,1]]

		self.start, self.end = None, None

	def __str__(self):
		stringy = ""
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				stringy += str(self.board[i][j]) + " "
			stringy += "\n"
		return stringy
	
	def populate(self):
		self.start = [rnd.randint(0,self.width-1),rnd.randint(0,self.height-1)]
		self.end = [rnd.randint(0,self.width-1),rnd.randint(0,self.height-1)]

		#self.start = [5,5]
		#self.end = [5,6] 

		count = 0
		while count < 30:
			x = rnd.randint(0,self.width-1)
			y = rnd.randint(0,self.height-1)

			if [x,y] != self.start and [x,y] != self.end:
				self.board[x][y] = 1 # wall
				count += 1
		
		
		self.board[self.start[0]][self.start[1]] = 2 # start
		self.board[self.end[0]][self.end[1]] = 3 # food



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
			if self.start[0]+direction[0]==path[1][0] and self.start[1]+direction[1]==path[1][1]:
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
		startNode = Node(None, tuple(self.start))
		startNode.g = startNode.h = startNode.f = 0
		endNode = Node(None, tuple(self.end))
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

tablero = Board()
tablero.populate()

print(tablero)

move = tablero.aStar()
print(tablero)
print(move)