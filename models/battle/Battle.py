from time import time
import pygame
from models.battle.BattleMap import BattleMap
from models.Consumer import Consumer
from models.Direction import Direction
from models.road.Road import Road
from models.battle.BattleEvents import BattleEvents
from models.block.Block import Block
from models.bomb.Bomb import Bomb
from GameSettings import GameSettings
from models.explosion.Explosion import Explosion
from models.item.Item import Item
from models.player.Player import Player
from models.player.PlayerDeath import PlayerDeath
from models.player.PlayerSpriteSheet import PlayerSpriteSheet
from models.Screen import Screen
class Battle:
	def __init__(self, settings: GameSettings):
		self.__music = pygame.mixer.Sound("sound/music/battle.mp3")
		self.__music.set_volume(0.7)
		self.__music.play(-1)
		self.__map = BattleMap(
			width=settings.screen.width,
			height=settings.screen.height,
			image=pygame.image.load("sprites/sprites-super-bomberman3-battle-stage-1.png")
		)
		self.__blocks = [Block(road) for road in self.__map.block_roads]
		self.__items: list[Item] = self.__map.generate_items()
		self.__player: Player | None = Player(
			id=1,
			cell=self.__map.player_start_road,
			spritesheet=PlayerSpriteSheet()
		)
		self.__bombs: list[Bomb] = []
		self.__explosions: list[Explosion] = []
		self.__deaths: list[PlayerDeath] = []
		self.__ended: bool = False
	@property
	def map(self):
		return self.__map
	@property
	def player(self):
		return self.__player
	@property
	def ended(self):
		return self.__ended
	@property
	def consumers(self):
		return [
			Consumer(pygame.KEYDOWN,self.__place_bomb,pygame.K_SPACE)
		]
	def __kill_player(self):
		self.__deaths.append(PlayerDeath(self.__player.cell))
		self.__player = None
	def __destroy_block(self, block: Block):
		block.destroy()
	def __destroy_item(self, item: Item):
		item.destroy()
	def __player_can_place_bomb(self, road: Road) -> bool:
		player_bombs = list(filter(lambda __bomb:
			__bomb.owner == self.__player.id
		, self.__bombs))
		if len(player_bombs) >= self.__player.bomb_quantity:
			return False
		for bomb in self.__bombs:
			if bomb.road == road:
				return False
		return True
	def __place_bomb(self):
		road = self.__map.get_closest_road(self.__player.cell.center)
		if self.__player_can_place_bomb(road):
			bomb = Bomb(road, self.__player.bomb_force, self.__player.id)
			self.__bombs.append(bomb)
			self.__player.bomb_passable = bomb
	def __make_explosion(self, bomb: Bomb):
		bomb.explode()
		self.__bombs.remove(bomb)
		self.__explosions.append(
			Explosion(bomb.road,bomb.force)
		)
		self.__explode_adjacent_roads(bomb.road, bomb.force)
	def __explode_adjacent_roads(self, center_road: Road, force: int):
		adjacent_roads = self.__map.get_adjacent_roads(center_road)
		for road in adjacent_roads:
			if (road.top < center_road.top):
				self.__extend_explosion(road,force,Direction.UP)
			elif (road.left < center_road.left):
				self.__extend_explosion(road,force,Direction.LEFT)
			elif (road.right > center_road.right):
				self.__extend_explosion(road,force,Direction.RIGHT)
			elif (road.bottom > center_road.bottom):
				self.__extend_explosion(road,force,Direction.DOWN)
	def __extend_explosion(self, road: Road, force: int, direction: Direction):
		if self.__player and self.__player.cell.colliderect(road):
			return self.__kill_player()
		next_bomb = next((bomb for bomb in self.__bombs if bomb.road == road), None)
		if next_bomb:
			return next_bomb.set_explosion_time(time()+0.2)
		block = next((block for block in self.__blocks if block.road == road), None)
		if block:
			return self.__destroy_block(block)
		item = next((item for item in self.__items if item.road == road), None)
		if item:
			return self.__destroy_item(item)
		self.__explosions.append(
			Explosion(road, force, direction)
		)
		if force > 1:
			new_road = self.__map.get_next_road(road, direction)
			if new_road:
				self.__extend_explosion(new_road, force - 1, direction)	
	def __end_battle(self):
		pygame.event.Event(BattleEvents.BATTLE_ENDED)
		self.__music.stop()
	def update(self, time_diff: int):
		if self.__player:
			self.__player.update(time_diff,[*self.__map.walls,*self.__blocks],self.__bombs,self.__items)
		for bomb in self.__bombs:
			if (bomb.has_to_explode()):
				self.__make_explosion(bomb)
		for explosion in self.__explosions:
			if (explosion.ended()):
				self.__explosions.remove(explosion)
		for block in self.__blocks:
			if block.destroyed:
				self.__blocks.remove(block)
		for item in self.__items:
			if (item.destroyed):
				self.__items.remove(item)
		for death in self.__deaths:
			if (death.ended()):
				self.__deaths.remove(death)
				self.__end_battle()
	def draw(self, screen: Screen):
		self.__map.draw(screen)
		for item in self.__items:
			item.blitme(screen)
		for block in self.__blocks:
			block.blitme(screen)
		for bomb in self.__bombs:
			bomb.blitme(screen)
		for explosion in self.__explosions:
			explosion.blitme(screen)
		if self.__player:
			self.__player.blitme(screen)
		for death in self.__deaths:
			death.blitme(screen)
