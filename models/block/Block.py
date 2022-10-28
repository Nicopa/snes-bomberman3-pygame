import time
from models.Cell import Cell
from models.road.Road import Road
from models.Screen import Screen
from models.block.BlockImage import BlockImage
from models.block.BlockSpriteSheet import BlockSpriteSheet

class Block(Cell):
	__COLLAPSING_DURATION = 0.5
	def __init__(self, road: Road):
		super().__init__(road.left, road.top, road.width, road.height)
		self.__road = road
		self.__spritesheet = BlockSpriteSheet()
		self.__destroying = False
		self.__destroyed_at = 0
		self.__image = BlockImage(road.width,road.height)
	@property
	def road(self):
		return self.__road
	@property
	def destroyed(self):
		return self.__destroying and self.__destroyed_at <= time.time()
	def destroy(self):
		self.__destroying = True
		self.__destroyed_at = time.time()+self.__COLLAPSING_DURATION
	def blitme(self, screen: Screen):
		image = self.__image.transform(
			self.__spritesheet.get_state_crop(self.__destroyed_at > 0)
		)
		screen.surface.blit(
			image,
			self.__image.position(self.__road)
		)