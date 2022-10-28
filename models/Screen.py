import pygame

class Screen:
	def __init__(self, width: int, height: int):
		self._surface = pygame.display.set_mode(
			(width, height)
		)
		pygame.display.set_caption("BombermanPyGame")
	@property
	def surface(self):
		return self._surface