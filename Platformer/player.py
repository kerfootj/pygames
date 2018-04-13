import pygame
from pygame.locals import *

WINDOW_HEIGHT = 600

TILE_SIZE = 40

# Colors
RED = ( 190,  20,  20)

class Player(pygame.sprite.Sprite):
	
	def __init__(self):
		super().__init__()
		
		# Create Player Image
		width = TILE_SIZE
		height = TILE_SIZE
		self.image = pygame.Surface([width, height])
		self.image.fill(RED)
		
		# Image Reference 
		self.rect = self.image.get_rect()
		
		# Player Speed
		self.speed = 6
		self.change_x = 0
		self.change_y = 0
		
		jumps = 0
		
		self.level = None
		
	def update(self):
		# Gravity
		self.calc_grav()
		
		# Move left/right
		self.rect.x += self.change_x
		
		# Check for collisions
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		for block in block_hit_list:
			# Moving right
			if self.change_x > 0:
				self.rect.right = block.rect.left
			# Moving left
			elif self.change_x < 0:
				self.rect.left = block.rect.right
				
		# Move up/down
		self.rect.y += self.change_y
		
		# Check for collisions
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		for block in block_hit_list:
			# Moving down
			if self.change_y > 0:
				self.rect.bottom = block.rect.top
				self.change_y = 0
			elif self.change_y < 0:
				self.rect.top = block.rect.bottom
	
	def calc_grav(self):
		
		if self.change_y == 0:
			self.change_y = 0.2
		else:
			self.change_y += .35
			
		# See if we are on the ground.
		if self.rect.y >= WINDOW_HEIGHT - self.rect.height and self.change_y >= 0:
			self.change_y = 0
			self.rect.y = WINDOW_HEIGHT - self.rect.height
			
	def jump(self):
		
		# Check player is on a surface
		self.rect.y += 2
		platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		self.rect.y -= 2
		
		# If player is on a surface ie not falling
		if len(platform_hit_list) > 0 or self.rect.bottom >= WINDOW_HEIGHT:
			self.change_y = -10
			self.jumps = 1
		
		# Double jump
		elif self.jumps == 1:
			self.change_y = -6.5
			self.jumps = 0
		
	# Player movement 
	def go_right(self):
		self.change_x = self.speed
		
	def go_left(self):
		self.change_x = -1 * self.speed
		
	def stop(self):
		self.change_x = 0
		