import pygame
import time
from models.Cell import Cell
from models.road.Road import Road
from models.Screen import Screen
from models.bomb.BombImage import BombImage
from models.bomb.BombSpriteSheet import BombSpriteSheet
from utils.Colors import RED
class Bomb(Cell):
	def __init__(self, road: Road, force: int, owner: int):
		super().__init__(road.left, road.top, road.width, road.height)
		self.__road = road
		self.__force = force
		self.__owner = owner
		self.__explodes_at = time.time()+4
		self.__spritesheet = BombSpriteSheet()
		self.__image = BombImage(road.width,road.height)
		self.__explosion_sound = pygame.mixer.Sound("sound/effect/bomb_explodes1.wav")
		pygame.mixer.Sound("sound/effect/bomb_setup1.wav").play()
	@property
	def road(self):
		return self.__road
	@property
	def force(self):
		return self.__force
	@property
	def owner(self):
		return self.__owner
	def set_explosion_time(self, time: float):
		self.__explodes_at = time
	def has_to_explode(self):
		return self.__explodes_at <= time.time()
	def explode(self):
		self.__explosion_sound.play()
	def blitme(self, screen: Screen):
		image = self.__image.transform(
			self.__spritesheet.get_state_crop()
		)
		screen.surface.blit(
			image,
			self.__image.position(self.__road)
		)

