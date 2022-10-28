import pygame

class Cell(pygame.Rect):
	def __init__(self, left: int, top: int, width: int, height: int):
		super().__init__(left, top, width, height)
	def move(self, x: float, y: float):
		rectangle = super().move(x,y)
		return Cell(rectangle.left,rectangle.top,rectangle.width,rectangle.height)
		