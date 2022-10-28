import pygame
import time
from models.Cell import Cell
from models.road.Road import Road
from models.Screen import Screen
from models.item.ItemImage import ItemImage
from models.item.ItemSpriteSheet import ItemSpriteSheet
from utils.Colors import ORANGE

class Item(Cell):
	__COLLAPSING_DURATION = 0.5
	def __init__(self, road: Road, type: str):
		super().__init__(road.left, road.top, road.width, road.height)
		self.__destroying = False
		self.__destroyed_at = 0
		self.__road = road
		self.__type = type
		self.__spritesheet = ItemSpriteSheet(type)
		self.__image = ItemImage(road.width,road.height)
	@property
	def road(self):
		return self.__road
	@property
	def type(self):
		return self.__type
	@property
	def destroyed(self):
		return self.__destroying and self.__destroyed_at <= time.time()
	def destroy(self):
		self.__destroying = True
		self.__destroyed_at = time.time()
	def blitme(self, screen: Screen):
		image = self.__image.transform(
			self.__spritesheet.get_state_crop()
		)
		screen.surface.blit(
			image,
			self.__image.position(self.__road)
		)