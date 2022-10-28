from models.SpriteSheet import SpriteSheet

class BlockSpriteSheet(SpriteSheet):
	__SPRITE_TIME_UPDATE = 0.4
	def __init__(self):
		super().__init__("sprites/sprites-super-bomberman3-battle-stage-1.png")
		self.image_index: int = 0
	def get_state_crop(self, all_sprites: bool = False):
		image_rectangles: list[tuple[int,int]] = [
			(0,209,16,16),
			(17,209,16,16),
			(34,209,16,16),
			(51,209,16,16),
			(68,209,16,16),
			(85,209,16,16),
			(102,209,16,16)
		]
		if self.image_index >= len(image_rectangles):
			self.image_index = 0
		image = self.image_at(image_rectangles[int(self.image_index)])
		if all_sprites:
			self.image_index += self.__SPRITE_TIME_UPDATE
		return image