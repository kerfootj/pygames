import pygame
from pygame.locals import *

BLACK    = (0, 0, 0)

# Generic super class level used to make other levels
class Level():
	
	# Lists of sprites used in the levels
	platform_list = None
	enemy_list = None
	
	# How far this world has been scrolled left/right
	world_shift = 0
	
	def __init__(self, player):
		self.platform_list = pygame.sprite.Group()
		self.enemy_list = pygame.sprite.Group()
		self.player = player
	
	# Update everything in the level
	def update(self):
		self.platform_list.update()
		self.enemy_list.update()
		
	def draw(self, display):
		
		# Background
		display.fill(BLACK)
		
		# Draw all the sprites
		self.platform_list.draw(display)
		self.enemy_list.draw(display)
		
	# Scroll everything when the player moves left or right
	def shift_world(self, shift_x):
		
		self.world_shift += shift_x
		
		# Shift the sprites
		for platform in self.platform_list:
			platform.rect.x += shift_x
		for enemy in self.enemy_list:
			enemy.rect.x += shift_x