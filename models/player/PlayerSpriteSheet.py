from models.Direction import Direction
from models.SpriteSheet import SpriteSheet

class PlayerSpriteSheet(SpriteSheet):
	__SPRITE_TIME_UPDATE = 0.6
	def __init__(self):
		super().__init__("sprites/sprites-super-bomberman3-bomberman.png")
		self.image_index: int = 0
	def get_state_crop(self, moving: bool, direction: Direction):
		colorkey = (0,162,232,255)
		image_rectangles: dict[str,list[tuple[int,int]]] = {
			"STOPPED_DOWN": [(6,9,15,23)],
			"STOPPED_UP": [(6,34,15,23)],
			"STOPPED_LEFT": [(6,59,17,23)],
			"STOPPED_RIGHT": [(4,84,17,23)],
			"MOVING_DOWN": [(6,9,15,23),(23,9,15,23),(6,9,15,23),(40,9,14,23)],
			"MOVING_UP": [(6,34,15,23),(23,34,15,23),(6,34,15,23),(40,34,15,23)],
			"MOVING_LEFT": [(6,59,17,23),(24,59,16,23),(6,59,17,23),(41,59,16,23)],
			"MOVING_RIGHT": [(4,84,17,23),(23,84,14,23),(4,84,17,23),(39,84,14,23)]
		}
		state = ("STOPPED" if not moving else "MOVING") + "_" + direction.value
		if self.image_index >= len(image_rectangles[state]):
			self.image_index = 0
		image = self.image_at(image_rectangles[state][int(self.image_index)],colorkey)
		self.image_index += self.__SPRITE_TIME_UPDATE
		return image