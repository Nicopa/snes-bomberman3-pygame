import pygame
class SpriteSheet:
	def __init__(self, filename):
		try:
			self.sheet = pygame.image.load(filename).convert()
		except pygame.error as e:
			print(f"Unable to load spritesheet image: {filename}")
			raise SystemExit(e)
	def image_at(self, space: tuple[int, int, int, int], colorkey: tuple[int, int, int, int] | None = None):
		_space = pygame.Rect(space)
		image = pygame.Surface(_space.size).convert()
		image.blit(self.sheet, (0,0), _space)
		if colorkey is not None:
			if colorkey == -1:
				colorkey = image.get_at((0,0))
			image.set_colorkey(colorkey, pygame.RLEACCEL)
		return image