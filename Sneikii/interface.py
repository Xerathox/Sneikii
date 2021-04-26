# Snake Game implementando el algoritmo A*
# Renzo Mondragon
# Joaquin Aguirre
# Francesco Bassino

import pygame
import time
from astar import Node, Board

class Game():
	def __init__(self, height=30, width=30):	
		# Iniciamos el tablero
		self.gameBoard = Board(height,width)

		self.blue = (0, 0, 255)
		self.purple = (255, 0, 255)
		self.black = (0, 0, 0)
		self.red = (255, 0, 0)
		self.yellow = (255,255,0)
		self.sizeSquared = 20
		self.height = self.sizeSquared * self.gameBoard.height
		self.width = self.sizeSquared * self.gameBoard.width
		self.size = (self.width + 400, self.height)

		self.screen = pygame.display.set_mode(self.size)
		pygame.init()
	
	def drawBoard(self):
		myFont = pygame.font.SysFont("monospace", 50)
		self.screen.fill(self.black)
		for i in range(self.gameBoard.height):
			for j in range(self.gameBoard.width):
				# check for head, body, food
				if self.gameBoard.board[i, j] == 1:
					temp = (j*self.sizeSquared, i*self.sizeSquared, self.sizeSquared, self.sizeSquared)
					pygame.draw.rect(self.screen, self.blue, temp)
				elif self.gameBoard.board[i, j] == 2:
					temp = (j*self.sizeSquared, i*self.sizeSquared, self.sizeSquared, self.sizeSquared)
					pygame.draw.rect(self.screen, self.purple, temp)
				elif self.gameBoard.board[i, j] == 3:
					temp = (int((j+0.5)*self.sizeSquared), int((i+0.5)*self.sizeSquared))
					pygame.draw.circle(self.screen, self.red, temp, self.sizeSquared//2)
				elif self.gameBoard.board[i, j] == 4:
					temp = (j*self.sizeSquared, i*self.sizeSquared, self.sizeSquared, self.sizeSquared)
					pygame.draw.rect(self.screen, self.yellow, temp)
		
		label = myFont.render(f"Score: {self.gameBoard.score}", 1, self.purple)
		self.screen.blit(label, (self.width + 10,10))
		tam_loc = (self.width, 0, 3, self.height)
		pygame.draw.rect(self.screen, (255, 255, 255), tam_loc)
		pygame.display.update()

	def runGame(self, ai=True):
		fps = 40
		pygame.init()
		myFont = pygame.font.SysFont("monospace", 65)
		self.drawBoard()

		pygame.display.update()
		exitPressed = False
		
		# Loop principal del juego
		while exitPressed == False and self.gameBoard.gaming == True:

			# Input del usuario
			move = self.gameBoard.direction
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exitPressed = True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						move = [-1, 0]			
					elif event.key == pygame.K_DOWN:
						move = [1, 0]
					elif event.key == pygame.K_LEFT:
						move = [0, -1]
					elif event.key == pygame.K_RIGHT:
						move = [0, 1]
			
			# Si la IA esta activada
			if ai:
				move = self.gameBoard.aStar() or self.gameBoard.revAStar()

			# Controlar la rapidez
			time.sleep(1.0/fps)

			# Procesar el movimiento
			self.gameBoard.updateDirection(move)
			self.gameBoard.updateState()	
			self.drawBoard()
			pygame.display.update()
				
		# --- perdimos el juego ---
		label = myFont.render(f"Game Over!", 1, self.red)
		self.screen.blit(label, (self.width + 10, 50))
		pygame.display.update()
		while exitPressed == False:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exitPressed = True 
		pygame.quit()



# Probando el juego
if __name__ == "__main__":
	Sneikii = Game()
	Sneikii.runGame()