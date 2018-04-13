import pygame
from pygame.locals import *

from player import *
from levels import *

# Window Dimension 
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

TILE_SIZE = 40

def main():
	pygame.init()
	
	# Set the height and width of the display
	size = [WINDOW_WIDTH, WINDOW_HEIGHT]
	screen = pygame.display.set_mode(size)
	
	pygame.display.set_caption('Platformer')
	
	player = Player()
	
	# Create all the levels
	level_list = []
	level_list.append(Level_01(player))
	
	# Set the current level
	current_level_no = 0
	current_level = level_list[current_level_no]
	
	active_sprite_list = pygame.sprite.Group()
	player.level = current_level

	player.rect.x = 340
	player.rect.y = WINDOW_HEIGHT - player.rect.height
	active_sprite_list.add(player)
	
	# Run until the user closes the game
	done = False

    # Used to manage how fast the display updates
	clock = pygame.time.Clock()
	
	# Main game loop
	while not done:
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT: # If user clicked close
				done = True
				
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					player.go_left()
				if event.key == pygame.K_RIGHT:
					player.go_right()
				if event.key == pygame.K_UP:
					player.jump()
				
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT and player.change_x < 0:
					player.stop()
				if event.key == pygame.K_RIGHT and player.change_x > 0:
					player.stop()
					
		# Update the player
		active_sprite_list.update()

		 # Update items in the level
		current_level.update()
		
		# If the player gets near the right side, shift the world left (-x)
		if player.rect.right >= 500:
			diff = player.rect.right - 500
			player.rect.right = 500
			current_level.shift_world(-diff)
 
        # If the player gets near the left side, shift the world right (+x)
		if player.rect.left <= 120:
			diff = 120 - player.rect.left
			player.rect.left = 120
			current_level.shift_world(diff)
			
		 # If the player gets to the end of the level, go to the next level
		current_position = player.rect.x + current_level.world_shift
		if current_position < current_level.level_limit:
			if current_level_no < len(level_list)-1:
				player.rect.x = 120
				current_level_no += 1
				current_level = level_list[current_level_no]
				player.level = current_level
			else:
				done = True
				
		# Update the display
		current_level.draw(screen)
		active_sprite_list.draw(screen)
		
		pygame.display.flip()
		
		clock.tick(60)

if __name__ == '__main__':
	main()