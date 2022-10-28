from models.SpriteSheet import SpriteSheet

class PlayerDeathSpriteSheet(SpriteSheet):
	__SPRITE_TIME_UPDATE = 0.3
	def __init__(self):
		super().__init__("sprites/sprites-super-bomberman3-bomberman.png")
		self.image_index: int = 0
	def get_state_crop(self):
		colorkey = (0,162,232,255)
		image_rectangles: list[tuple[int,int]] = [
			(3,216,15,22),
			(20,216,15,22),
			(37,216,15,22),
			(54,216,19,22),
			(75,216,21,22),
			(98,217,22,21),
			(122,218,22,20)
		]
		if self.image_index >= len(image_rectangles):
			self.image_index = 0
		image = self.image_at(image_rectangles[int(self.image_index)],colorkey)
		self.image_index += self.__SPRITE_TIME_UPDATE
		return image