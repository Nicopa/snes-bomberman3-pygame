import pygame
from models.bomb.Bomb import Bomb
from models.Cell import Cell
from models.Direction import Direction
from models.Screen import Screen
from models.item.Item import Item
from models.player.PlayerImage import PlayerImage
from models.player.PlayerSpriteSheet import PlayerSpriteSheet
from utils.Colors import BLUE

class Player:
	__SLIDE_PIXELS = 14
	def __init__(self, id: int, cell: Cell, spritesheet: PlayerSpriteSheet):
		self.__id = id
		self.__state = {
			"moving": False,
			"direction": Direction.DOWN
		}
		self.__bomb_force = 2
		self.__bomb_quantity = 1
		self.__cell = cell
		self.__bomb_passable: bool | Bomb | None = None
		self.__spritesheet = spritesheet
		self.__image = PlayerImage(cell.width//10*9,cell.height*2//10*9)
		self.__x_speed, self.__y_speed = 0.2, 0.2
		self.__get_item_sound = pygame.mixer.Sound("sound/effect/get_item.wav")
	@property
	def id(self):
		return self.__id
	@property
	def cell(self):
		return self.__cell
	@property
	def bomb_force(self):
		return self.__bomb_force
	@property
	def bomb_quantity(self):
		return self.__bomb_quantity
	@property
	def bomb_passable(self):
		return self.__bomb_passable
	@bomb_passable.setter
	def bomb_passable(self, value: bool | Bomb | None):
		self.__bomb_passable = value
	def __get_impassable_bombs(self, bombs: list[Bomb]):
		return [bomb for bomb in bombs if self.__bomb_passable != bomb]
	def __move_up(self, time_diff: int, obstacles: list[Cell]):
		new_cell = self.__cell.move(0, -(self.__y_speed * time_diff))
		self.__state["moving"] = True
		self.__state["direction"] = Direction.UP
		collision = new_cell.collidelist(obstacles)
		if collision < 0:
			self.__cell = new_cell
		# if the move is greater than the left space, go next to the collision object
		elif obstacles[collision].bottom != self.__cell.top:
			self.__cell.top = obstacles[collision].bottom
		# correction to avoid perfect pixel player positioning restriction
		# right up
		elif obstacles[collision].right - new_cell.left < self.__SLIDE_PIXELS:
			new_cell.left = obstacles[collision].right
			collision = new_cell.collidelist(obstacles)
			if collision < 0:
				self.__cell = new_cell
		# left up
		elif new_cell.right - obstacles[collision].left < self.__SLIDE_PIXELS:
			new_cell.right = obstacles[collision].left
			collision = new_cell.collidelist(obstacles)
			if collision < 0:
				self.__cell = new_cell
	def __move_right(self, time_diff: int, obstacles: list[Cell]):
		new_cell = self.__cell.move(self.__x_speed * time_diff, 0)
		self.__state["moving"] = True
		self.__state["direction"] = Direction.RIGHT
		collision = new_cell.collidelist(obstacles)
		if collision < 0:
			self.__cell = new_cell
		elif obstacles[collision].left != self.__cell.right:
			self.__cell.right = obstacles[collision].left
		# correction to avoid perfect pixel player positioning restriction
		# up right
		elif new_cell.bottom - obstacles[collision].top < self.__SLIDE_PIXELS:
			new_cell.bottom = obstacles[collision].top
			collision = new_cell.collidelist(obstacles)
			if collision < 0:
				self.__cell = new_cell
		# down right
		elif obstacles[collision].bottom - new_cell.top < self.__SLIDE_PIXELS:
			new_cell.top = obstacles[collision].bottom
			collision = new_cell.collidelist(obstacles)
			if collision < 0:
				self.__cell = new_cell
	def __move_down(self, time_diff: int, obstacles: list[Cell]):
		new_cell = self.__cell.move(0, self.__y_speed * time_diff)
		self.__state["moving"] = True
		self.__state["direction"] = Direction.DOWN
		collision = new_cell.collidelist(obstacles)
		if collision < 0:
			self.__cell = new_cell
		elif obstacles[collision].top != self.__cell.bottom:
			self.__cell.bottom = obstacles[collision].top
		# correction to avoid perfect pixel player positioning restriction
		# right down
		elif obstacles[collision].right - new_cell.left < self.__SLIDE_PIXELS:
			new_cell.left = obstacles[collision].right
			collision = new_cell.collidelist(obstacles)
			if collision < 0:
				self.__cell = new_cell
		# left down
		elif new_cell.right - obstacles[collision].left < self.__SLIDE_PIXELS:
			new_cell.right = obstacles[collision].left
			collision = new_cell.collidelist(obstacles)
			if collision < 0:
				self.__cell = new_cell
	def __move_left(self, time_diff: int, obstacles: list[Cell]):
		new_cell = self.__cell.move(-(self.__x_speed * time_diff), 0)
		self.__state["moving"] = True
		self.__state["direction"] = Direction.LEFT
		collision = new_cell.collidelist(obstacles)
		if collision < 0:
			self.__cell = new_cell
		elif obstacles[collision].right != self.__cell.left:
			self.__cell.left = obstacles[collision].right
		# correction to avoid perfect pixel player positioning restriction
		# up left
		elif new_cell.bottom - obstacles[collision].top < self.__SLIDE_PIXELS:
			new_cell.bottom = obstacles[collision].top
			collision = new_cell.collidelist(obstacles)
			if collision < 0:
				self.__cell = new_cell
		# down left
		elif obstacles[collision].bottom - new_cell.top < self.__SLIDE_PIXELS:
			new_cell.top = obstacles[collision].bottom
			collision = new_cell.collidelist(obstacles)
			if collision < 0:
				self.__cell = new_cell
	def check_items_on_road(self, items: list[Item]):
		collision = self.__cell.collidelist(items)
		if collision >= 0:
			if items[collision].type == "bomb":
				self.__bomb_quantity += 1
			else:
				self.__bomb_force += 1
			self.__get_item_sound.play()
			items[collision].destroy()
	def update(self, time_diff: int, obstacles: list[Cell], bombs: list[Bomb], items: list[Item]):
		pressed_keys = pygame.key.get_pressed()
		if isinstance(self.__bomb_passable, Bomb):
			if not self.__cell.colliderect(self.__bomb_passable):
				self.__bomb_passable = None
		if pressed_keys[pygame.K_UP]:
			obstacle_bombs = self.__get_impassable_bombs(bombs)
			self.__move_up(time_diff, [*obstacles,*obstacle_bombs])
		elif pressed_keys[pygame.K_RIGHT]:
			obstacle_bombs = self.__get_impassable_bombs(bombs)
			self.__move_right(time_diff, [*obstacles,*obstacle_bombs])
		elif pressed_keys[pygame.K_DOWN]:
			obstacle_bombs = self.__get_impassable_bombs(bombs)
			self.__move_down(time_diff, [*obstacles,*obstacle_bombs])
		elif pressed_keys[pygame.K_LEFT]:
			obstacle_bombs = self.__get_impassable_bombs(bombs)
			self.__move_left(time_diff, [*obstacles,*obstacle_bombs])
		else:
			self.__state["moving"] = False
			pass
		self.check_items_on_road(items)
	def blitme(self,screen: Screen):
		image = self.__image.transform(
			self.__spritesheet.get_state_crop(
				moving=self.__state["moving"],
				direction=self.__state["direction"]
			)
		)
		screen.surface.blit(
			image,
			self.__image.position(self.__cell)
		)

