from models.SpriteSheet import SpriteSheet

class BombSpriteSheet(SpriteSheet):
	__SPRITE_TIME_UPDATE = 0.2
	def __init__(self):
		super().__init__("sprites/spirtes-super-bomberman3-bombs-and-items.png")
		self.image_index: int = 0
	def get_state_crop(self):
		colorkey = (112,136,88,255)
		image_rectangles: list[tuple[int,int]] = [
			(4,7,16,16),
			(21,7,15,16),
			(38,7,14,16),
			(21,7,15,16)
		]
		if self.image_index >= len(image_rectangles):
			self.image_index = 0
		image = self.image_at(image_rectangles[int(self.image_index)],colorkey)
		self.image_index += self.__SPRITE_TIME_UPDATE
		return image