import pygame
from pygame.locals import *

GREEN = (76, 155, 0)

class Platform(pygame.sprite.Sprite):

	def __init__(self, width, height, color=GREEN):
		
		super().__init__()
		
		self.image = pygame.Surface([width, height])
		self.image.fill(color)

		self.rect = self.image.get_rect()
		
	def collide(self, player):
		if self.rect.top == player.rect.bottom:
				if player.rect.centerx in range(self.rect.left, self.rect.right):
				 return True