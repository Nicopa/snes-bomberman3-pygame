class Event:
	def __init__(self, type: int, key: int | None = None):
		self.__type = type
		self.__key = key
	@property
	def type(self):
		return self.__type
	@property
	def key(self):
		return self.__key