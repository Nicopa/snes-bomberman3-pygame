import sys
import pygame
from GameSettings import GameSettings
from controllers.EventController import EventController
from models.battle.Battle import Battle
from models.Consumer import Consumer
from models.Event import Event
from models.Screen import Screen
from models.battle.BattleEvents import BattleEvents
from utils.Colors import BLACK

class BombermanGame:
	__FRAMES_PER_SECOND = 30
	def __init__(self):
		pygame.init()
		self.__settings = GameSettings(720,624,BLACK)
		self.__screen = Screen(self.__settings.screen.width,self.__settings.screen.height)
		self.__event_controller = EventController()
		self.__clock = pygame.time.Clock()
		self.__battle = Battle(self.__settings)
		self.__pause_sound = pygame.mixer.Sound("sound/effect/pause.wav")
	def __quit_game(self):
		pygame.quit()
		sys.exit()
	def __check_events(self, time_diff: int):
		events: list[Event] = []
		for event in pygame.event.get():
			events.append(Event(event.type,getattr(event,"key",None)))
			""" if self.__battle.ended:
				self.__paused = True
				self.__pause_loop()
				pygame.quit()
				sys.exit() """
		self.__event_controller.run(events)
	def __update_objects(self, time_diff: int):
		self.__battle.update(time_diff)
	def __pause_loop(self):
		paused = True
		self.__pause_sound.play()
		while paused:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					self.__quit_game()
				if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
					paused = False
					self.__pause_sound.play()
	def __update_screen(self):
		self.__screen.surface.fill(self.__settings.background_color)
		self.__battle.draw(self.__screen)
		pygame.display.flip()
	def run_game(self):
		self.__event_controller.subscribe(Consumer(pygame.QUIT,self.__quit_game))
		self.__event_controller.subscribe(Consumer(pygame.KEYDOWN,self.__quit_game,pygame.K_ESCAPE))
		self.__event_controller.subscribe(Consumer(pygame.KEYDOWN,self.__pause_loop,pygame.K_p))
		self.__event_controller.subscribe(Consumer(BattleEvents.BATTLE_ENDED,self.__pause_loop))
		for consumer in self.__battle.consumers:
			self.__event_controller.subscribe(consumer)
		while True:
			time_diff = self.__clock.tick(self.__FRAMES_PER_SECOND)
			self.__check_events(time_diff)
			self.__update_objects(time_diff)
			self.__update_screen()