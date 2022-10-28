from typing import Callable

class Consumer:
	def __init__(self, type: int, callback: Callable, key: int | None = None):
		self.__type = type
		self.__callback = callback
		self.__key = key
	@property
	def type(self):
		return self.__type
	@property
	def callback(self):
		return self.__callback
	@property
	def key(self):
		return self.__key