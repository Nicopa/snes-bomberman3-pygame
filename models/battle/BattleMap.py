import random
import pygame
from models.Cell import Cell
from models.Direction import Direction
from models.road.Road import Road
from models.Screen import Screen
from models.battle.wall.Wall import Wall
from models.item.Item import Item
from utils.Colors import GRAY, PINK

class BattleMap:
	_rows = 15
	_columns = 13
	_blockless_road_indexes = [0, 1, 9, 10, 11, 16, 96, 101, 102, 103, 111, 112]
	_max_empty_roads = 8
	_max_items = {
		"bomb": 5,
		"bomb_force": 5
	}
	def __init__(self, width: int, height: int, image: pygame.Surface):
		self.__cell = Cell(0,0,width // self._rows, height // self._columns)
		cropped_image = image.subsurface((0,0,240,208))
		self.__image = pygame.transform.scale(cropped_image, (width,height))
		self.__walls: list[Wall] = self.__load_walls()
		self.__roads: list[Road] = self.__load_roads()
		self.__player_start_road = self.__roads[0]
		self.__block_roads = [road for road in self.__roads if self.__roads.index(road) not in self._blockless_road_indexes]
		self.__leave_random_empty_roads()
	@property
	def cell(self):
		return self.__cell
	@property
	def player_start_road(self):
		return self.__player_start_road
	@property
	def block_roads(self):
		return self.__block_roads
	@property
	def walls(self):
		return self.__walls
	def __leave_random_empty_roads(self):
		total = 0
		for road in self.__block_roads:
			should_remove = random.random() < 0.15
			if (should_remove and total < self._max_empty_roads):
				self.block_roads.remove(road)
				total += 1
	def __load_walls(self):
		walls: list[Wall] = []
		for row in range(self._rows):
			for column in range(self._columns):
				if (row == 0
					or column == 0
					or row == self._rows-1
					or column == self._columns-1
					or (row > 0 and column > 0 and row % 2 == 0 and column % 2 == 0)
					):
					walls.append(
						Wall(
							left=row*self.__cell.width,
							top=column*self.__cell.height,
							width=self.__cell.width,
							height=self.__cell.height
						)
					)
		return walls
	def __load_roads(self):
		roads: list[Road] = []
		for row in range(self._rows):
			for column in range(self._columns):
				if (
					(row % 2 > 0 or column % 2 > 0)
					and (row > 0 and column > 0)
					and (row + 1 < self._rows and column + 1 < self._columns)
				):
					roads.append(
						Road(
							left=row*self.__cell.width,
							top=column*self.__cell.height,
							width=self.__cell.width,
							height=self.__cell.height
						)
					)
		return roads
	def get_closest_road(self, coordinate: tuple[int, int]):
		for road in self.__roads:
			if road.collidepoint(coordinate[0], coordinate[1]):
				return road
		return None
	def get_adjacent_roads(self, road: Road):
		results = filter(lambda __road: 
			(__road.right == road.left and __road.top == road.top) or
			(__road.left == road.right and __road.top == road.top) or
			(__road.bottom == road.top and __road.left == road.left) or
			(__road.top == road.bottom and __road.left == road.left)
		, self.__roads)
		return list(results)
	def get_next_road(self, road: Road, direction: Direction) -> Road | None:
		results = filter(lambda __road: 
			(direction == Direction.UP and __road.bottom == road.top and __road.left == road.left) or
			(direction == Direction.RIGHT and __road.left == road.right and __road.top == road.top) or
			(direction == Direction.DOWN and __road.top == road.bottom and __road.left == road.left) or
			(direction == Direction.LEFT and __road.right == road.left and __road.top == road.top)
		, self.__roads)
		roads = list(results)
		return roads[0] if len(roads) else None
	def get_random_block_road(self) -> Road:
		while True:
			random_road = self.__roads[random.randrange(len(self.__roads))]
			if random_road in self.__block_roads:
				return random_road
	def generate_items(self) -> list[Item]:
		items: list[Item] = []
		for type in self._max_items:
			total = 0
			while total < self._max_items[type]:
				random_road = self.get_random_block_road()
				road_has_item: bool = False
				for item in items:
					if item.road == random_road:
						road_has_item = True
				if not road_has_item:
					items.append(Item(random_road, type))
					total += 1
		return items
	def draw(self, screen: Screen):
		screen.surface.blit(self.__image, (0,0))
		#for road in self.__roads:
			#pygame.draw.rect(screen.surface,PINK, (road.center[0]-2,road.center[1]-2,4,4))
		#for wall in self.__walls:
			#pygame.draw.rect(screen.surface,GRAY, (wall.topleft,wall.size))
		