import pygame
from pygame.locals import *
from blocks.platform import Platform

class BreakablePlatform(Platform):
	
	player = None
	level = None
	
	def update(self):
		
		if super().collide(self.player) and self.player.plunging() == 1:
			self.level.platform_list.remove(self)