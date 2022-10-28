import pygame
from models.Cell import Cell

class ItemImage:
	def __init__(self, width: float, height: float):
		self.__surface = pygame.Surface((width, height))
	@property
	def size(self):
		return self.__surface.get_rect().size
	def transform(self, image: pygame.Surface):
		return pygame.transform.scale(image, self.size)
	def position(self, cell: Cell) -> tuple[int,int]:
		return (
			cell.left + (cell.width-self.size[0])//2,
			cell.top + (cell.height-self.size[1])//2
		)