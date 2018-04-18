import pygame
from pygame.locals import *
from levels.level import Level
from blocks import *

class Level_01(Level):
	def __init__(self, player):
		# Parent constructor
		Level.__init__(self, player)
		self.level_limit = -1500
		
		# Platforms in the level
		level = [[210, 70, 500, 500],
                 [210, 70, 800, 400],
                 [210, 70, 1000, 500],
                 [210, 70, 1120, 280],
                 ]
				 
		for platform in level:
			block = Platform(platform[0], platform[1])
			block.rect.x = platform[2]
			block.rect.y = platform[3]
			block.player = self.player
			self.platform_list.add(block)
			
		# Add a custom moving platform
		block = MovingPlatform(70, 40)
		block.rect.x = 1350
		block.rect.y = 280
		block.boundary_left = 1350
		block.boundary_right = 1600
		block.change_x = 1
		block.player = self.player
		block.level = self
		self.platform_list.add(block)
		
		block = BreakablePlatform(60,60, (139,69,19))
		block.rect.x = 0
		block.rect.y = 450
		block.player = self.player
		block.level = self
		self.platform_list.add(block)