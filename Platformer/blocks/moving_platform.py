import pygame
from pygame.locals import *
from blocks.platform import Platform

class MovingPlatform(Platform):
	
	change_x = 0
	change_y = 0

	boundary_top = 0
	boundary_bottom = 0
	boundary_left = 0
	boundary_right = 0

	player = None
	level = None
	
	def update(self):

		# Move left/right
		self.rect.x += self.change_x
		
		# Check for collision with player
		if self.change_x != 0:
			if self.rect.top == self.player.rect.bottom:
				if self.player.rect.centerx in range(self.rect.left, self.rect.right):
					
					# Move the player on the platform
					self.player.rect.centerx += self.change_x
					self.player.change_y = 0
	
		# Move up/down
		self.rect.y += self.change_y

		# Check for collision when moving down
		if self.change_y > 0:
			if self.rect.top -1 == self.player.rect.bottom:
				if self.player.rect.left in range(self.rect.left, self.rect.right) or self.player.rect.right in range(self.rect.left, self.rect.right):
					self.player.rect.bottom = self.rect.top
					self.player.change_y = 0
			elif self.player.rect.top in range(self.rect.top, self.rect.bottom):
				if self.player.rect.left in range(self.rect.left, self.rect.right) or self.player.rect.right in range(self.rect.left, self.rect.right):
					self.player.rect.top = self.rect.bottom
					self.player.change_y = self.change_y

		# Check for collision when moving up
		if self.change_y < 0:
			if self.rect.top +1 == self.player.rect.bottom:
				if self.player.rect.left in range(self.rect.left, self.rect.right) or self.player.rect.right in range(self.rect.left, self.rect.right):
					self.player.rect.bottom = self.rect.top
					self.player.change_y = 0

		# Check the boundaries and see if we need to reverse
		# direction.
		if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
			self.change_y *= -1

		cur_pos = self.rect.x - self.level.world_shift
		if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
			self.change_x *= -1
	
