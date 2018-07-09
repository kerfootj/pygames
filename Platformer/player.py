import pygame
import constants
from spritesheet_functions import SpriteSheet
from pygame.locals import *

WINDOW_HEIGHT = 600

TILE_SIZE = 40

# Colors
RED = ( 190,  20,  20)

class Player(pygame.sprite.Sprite):
	
	def __init__(self):
		super().__init__()

		self.walking_frames_l = []
		self.walking_frames_r = []

		self.direction = 'R'	

		# Load Sprites
		sprite_sheet = SpriteSheet("p1_walking.png")

		image = sprite_sheet.get_image(0, 192, 64, 64)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(64, 192, 64, 64)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(128, 192, 64, 64)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(192, 192, 64, 64)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(256, 192, 64, 64)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(320, 192, 64, 64)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(384, 192, 64, 64)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(448, 192, 64, 64)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(512, 192, 64, 64)
		self.walking_frames_r.append(image)

		image = sprite_sheet.get_image(0, 64, 64, 64)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(64, 64, 64, 64)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(128, 64, 64, 64)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(192, 64, 64, 64)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(256, 64, 64, 64)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(320, 64, 64, 64)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(384, 64, 64, 64)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(448, 64, 64, 64)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(512, 64, 64, 64)
		self.walking_frames_l.append(image)

		# Starting image
		self.image = self.walking_frames_r[0]

		self.rect = self.image.get_rect()

		# Player Speed
		self.speed = 6
		self.change_x = 0
		self.change_y = 0
		
		jumps = 0
		double_jump = 0
		plunge = 0
		
		self.level = None
		
	def update(self):
		# Gravity
		self.calc_grav()
		
		# Move left/right
		self.rect.x += self.change_x
		pos = self.rect.x + self.level.world_shift

		# Update sprite animation
		if self.direction == 'R':
			frame = (pos // 30) % len(self.walking_frames_r)
			self.image = self.walking_frames_r[frame]
		else:
			frame = (pos // 30) % len(self.walking_frames_l)
			self.image = self.walking_frames_l[frame]

		# Check for collisions
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		for block in block_hit_list:
			
			# Reset movement flags
			self.jumps = 0
			self.double_jump = 0
			self.plunge = 0
			
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
				self.change_y = 0
	
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
			self.double_jump = 1
			self.jumps = 2
			
	def smash(self):
		
		if self.jumps != 0 or self.double_jump != 0:
			self.change_y = 15
			self.plunge = 1
			
	def plunging(self):
		return self.plunge == 1
		
	# Player movement 
	def go_right(self):
		self.change_x = self.speed
		self.direction = 'R'
		
	def go_left(self):
		self.change_x = -1 * self.speed
		self.direction = 'L'
		
	def stop(self):
		self.change_x = 0
		