import time
from models.Direction import Direction
from models.road.Road import Road
from models.Screen import Screen
from models.bomb.Bomb import Bomb
from models.explosion.ExplosionImage import ExplosionImage
from models.explosion.ExplosionSpriteSheet import ExplosionSpriteSheet
from utils.Colors import RED

class Explosion():
	__DURATION = 0.45
	def __init__(self, road: Road,force: int, direction: Direction | None = None):
		self.__road = road
		self.__ends_at = time.time()+self.__DURATION
		self.__spritesheet = ExplosionSpriteSheet(force, direction)
		self.__image = ExplosionImage(self.__road.width,self.__road.height)
	def ended(self):
		return self.__ends_at <= time.time()
	def blitme(self, screen: Screen):
		image = self.__image.transform(
			self.__spritesheet.get_state_crop()
		)
		screen.surface.blit(
			image,
			self.__image.position(self.__road)
		)