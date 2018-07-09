import pygame
import os

import constants

class SpriteSheet(object):

	def __init__(self, file_name):

		self.sprite_sheet = pygame.image.load(os.path.join('data', file_name)).convert()

	def get_image(self, x, y, width, height):

		image = pygame.Surface([width, height]).convert()
		image.set_colorkey((255,0,255))

		image.blit(self.sprite_sheet, (0,0), (x, y, width, height))
		
		return image