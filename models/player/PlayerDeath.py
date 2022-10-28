import time
from models.Cell import Cell
from models.player.PlayerDeathSpriteSheet import PlayerDeathSpriteSheet
from models.player.PlayerImage import PlayerImage
from models.Screen import Screen

class PlayerDeath:
	__DURATION = 0.5
	def __init__(self, cell: Cell):
		self.__cell = cell
		self.__ends_at = time.time()+self.__DURATION
		self.__spritesheet = PlayerDeathSpriteSheet()
		self.__image = PlayerImage(cell.width//10*9,cell.height*2//10*9)
	def ended(self):
		return self.__ends_at <= time.time()
	def blitme(self, screen: Screen):
		image = self.__image.transform(
			self.__spritesheet.get_state_crop()
		)
		screen.surface.blit(
			image,
			self.__image.position(self.__cell)
		)

