class ScreenSettings:
	def __init__(self, width: int, height: int, background_color: tuple[int, int, int]):
		self.__width = width
		self.__height = height
		self.__background_color = background_color
	@property
	def width(self):
		return self.__width
	@property
	def height(self):
		return self.__height
	@property
	def background_color(self):
		return self.__background_color


class GameSettings:
	def __init__(self, screen_width: int, screen_height: int, screen_bg_color: tuple[int, int, int]):
		self.__screen = ScreenSettings(screen_width,screen_height,screen_bg_color)
		self.background_color = (0, 0, 0)
	@property
	def screen(self):
		return self.__screen