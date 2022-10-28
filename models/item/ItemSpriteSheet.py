from models.SpriteSheet import SpriteSheet

class ItemSpriteSheet(SpriteSheet):
	__SPRITE_TIME_UPDATE = 0.2
	def __init__(self, type: str):
		super().__init__("sprites/spirtes-super-bomberman3-bombs-and-items.png")
		self.image_index: int = 0
		self.__type = type
	def get_state_crop(self):
		colorkey = (112,136,88,255)
		image_rectangles: list[tuple[int,int]] = [
			(48,86,16,16),
			(88,86,16,16),
		]
		if self.__type == "bomb":
			self.image_index = 1
		else:
			self.image_index = 0
		image = self.image_at(image_rectangles[int(self.image_index)],colorkey)
		return image