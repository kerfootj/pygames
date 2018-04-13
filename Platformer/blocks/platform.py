import pygame
from pygame.locals import *

GREEN = (76, 155, 0)

class Platform(pygame.sprite.Sprite):

	def __init__(self, width, height):
		
		super().__init__()
		
		self.image = pygame.Surface([width, height])
		self.image.fill(GREEN)

		self.rect = self.image.get_rect()