from models.Direction import Direction
from models.SpriteSheet import SpriteSheet

class ExplosionSpriteSheet(SpriteSheet):
	__SPRITE_TIME_UPDATE = 0.5
	def __init__(self, force: int, direction: Direction | None = None):
		super().__init__("sprites/spirtes-super-bomberman3-bombs-and-items.png")
		self.__force = force
		self.__direction = direction
		self.image_index: int = 0
	def get_state_crop(self):
		colorkey = (112,136,88,255)
		image_rectangles: dict[str,list[tuple[int,int]]] = {
			"CENTER": [
				(656,72,16,16),
				(538,72,16,16),
				(415,72,16,16),
				(293,72,16,16),
				(415,72,16,16),
				(538,72,16,16),
				(656,72,16,16)
			],
			"UP_MIDDLE": [
				(657,51,14,16),
				(539,49,14,16),
				(415,51,16,16),
				(293,50,16,16),
				(415,51,16,16),
				(539,49,14,16),
				(657,51,14,16)
			],
			"UP_END": [
				(656,32,14,15),
				(539,24,14,16),
				(415,29,16,16),
				(293,31,16,15),
				(415,29,16,16),
				(539,24,14,16),
				(656,32,14,15)
			],
			"RIGHT_MIDDLE": [
				(678,73,16,14),
				(562,72,16,14),
				(438,72,16,16),
				(316,72,16,16),
				(438,72,16,16),
				(562,72,16,14),
				(678,73,16,14)
			],
			"RIGHT_END": [
				(700,73,15,14),
				(584,72,16,14),
				(461,72,16,16),
				(338,72,16,16),
				(461,72,16,16),
				(584,72,16,14),
				(700,73,15,14)
			],
			"DOWN_MIDDLE": [
				(657,93,14,16),
				(539,94,14,16),
				(415,92,16,16),
				(293,94,16,16),
				(415,92,16,16),
				(539,94,14,16),
				(657,93,14,16)
			],
			"DOWN_END": [
				(656,113,15,15),
				(539,116,14,16),
				(415,113,16,16),
				(293,115,16,16),
				(415,113,16,16),
				(539,116,14,16),
				(656,113,15,15)
			],
			"LEFT_MIDDLE": [
				(633,73,16,14),
				(513,72,16,14),
				(391,72,16,16),
				(270,72,16,16),
				(391,72,16,16),
				(513,72,16,14),
				(633,73,16,14)
			],
			"LEFT_END": [
				(609,73,15,14),
				(488,72,16,14),
				(370,72,16,16),
				(247,72,16,16),
				(370,72,16,16),
				(488,72,16,14),
				(609,73,15,14)
			]
		}
		state = "CENTER"
		if self.__direction:
			state = self.__direction.value
			state += "_MIDDLE" if self.__force > 1 else "_END"
		if self.image_index >= len(image_rectangles[state]):
			self.image_index = 0
		image = self.image_at(image_rectangles[state][int(self.image_index)],colorkey)
		self.image_index += self.__SPRITE_TIME_UPDATE
		return image