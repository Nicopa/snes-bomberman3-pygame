import pygame

from models.Consumer import Consumer
from models.Event import Event

class EventController:
	def __init__(self):
		self.__consumers: list[Consumer] = []
	def subscribe(self, consumer: Consumer):
		self.__consumers.append(consumer)
	def __check(self, event: Event):
		for consumer in self.__consumers:
			if event.type == consumer.type:
				if not consumer.key:
					consumer.callback()
				elif consumer.key == event.key:
					consumer.callback()
	def run(self, event_list: list[Event]):
		for event in event_list:
			self.__check(event)