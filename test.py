import pygame, sys, random
from pygame.locals import *

FPS = 10

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BLOCK_SIZE = 20
assert WINDOW_WIDTH % BLOCK_SIZE == 0
assert WINDOW_HEIGHT % BLOCK_SIZE == 0
WIDTH = int(WINDOW_WIDTH / BLOCK_SIZE)
HEIGHT = int(WINDOW_HEIGHT / BLOCK_SIZE)

WHITE = 	(255, 255, 255)
BLACK = 	(  0,   0,   0)
GRAY =		(128, 128, 128)
DARKGRAY =  ( 40,  40,  40)
BLUE = 		(  0,   0, 205)
DARKBLUE =  (  0,   0, 110)
RED = 		(135,   0,  30)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0

def main():
	
	global CLOCK, DISPLAY, FONT
	
	pygame.init()
	
	CLOCK = pygame.time.Clock()
	DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	FONT = pygame.font.Font('freesansbold.ttf', 18)
	pygame.display.set_caption('Snake!')
		
	showStartScreen()
	while True:
		runGame()
		showGameOverScreen()
		
def runGame():
	
	startX = random.randint(5, WIDTH - 6)	
	startY = random.randint(5, WIDTH - 6)
	
	snake = [{'x': startX, 'y': startY}, {'x': startX-1, 'y': startY}, {'x': startX-2, 'y': startY}]
	direction = RIGHT
	apple = getRandomLocation()
	
	score = 0
	speed = 0
		
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
					direction = LEFT
				elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
					direction = RIGHT
				elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
					direction = UP
				elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
					direction = DOWN
				elif event.key == K_ESCAPE:
					terminate()
			
		if snake[HEAD]['x'] == -1 or snake[HEAD]['x'] == WIDTH or snake[HEAD]['y'] == -1 or snake[HEAD]['y'] == HEIGHT:
		   return
		for block in snake[1:]:
			if block['x'] == snake[HEAD]['x'] and block['y'] == snake[HEAD]['y']:
				return
		
		if snake[HEAD]['x'] == apple['x'] and snake[HEAD]['y'] == apple['y']:
			apple = getRandomLocation()
			score = len(snake) - 2
			if score != 0 and score % 5 == 0:
				speed += 3
		else:
			del snake[-1]
		
		if direction == UP:
			newHead = {'x': snake[HEAD]['x'], 'y': snake[HEAD]['y']-1}
		elif direction == DOWN:
			newHead = {'x': snake[HEAD]['x'], 'y': snake[HEAD]['y']+1}
		elif direction == LEFT:
			newHead = {'x': snake[HEAD]['x']-1, 'y': snake[HEAD]['y']}
		elif direction == RIGHT:
			newHead = {'x': snake[HEAD]['x']+1, 'y': snake[HEAD]['y']}
				
		snake.insert(0, newHead)
		DISPLAY.fill(BGCOLOR)
		drawBoarders()
		drawSnake(snake)
		drawApple(apple)
		drawScore(score)
		pygame.display.update()
		CLOCK.tick(FPS + speed)	
			
def getRandomLocation():
	return {'x': random.randint(0, WIDTH - 1), 'y': random.randint(0, HEIGHT - 1)}

def checkForKeyPress():
	if len(pygame.event.get(QUIT)) > 0:
		terminate()
		
	keyUpEvents = pygame.event.get(KEYUP)
	if len(keyUpEvents) == 0:
		return None 
	if keyUpEvents[0].key == K_ESCAPE:
		terminate()
	return keyUpEvents[0].key
	
def drawPressKeyMsg():
	pressKeySurf = FONT.render('Press any key to play.', True, DARKGRAY)
	pressKeyRect = pressKeySurf.get_rect()
	pressKeyRect.topleft = (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 30)
	DISPLAY.blit(pressKeySurf, pressKeyRect)
	
def drawScore(score):
	scoreSurf = FONT.render('Score: %s' % (score), True, WHITE)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (WINDOW_WIDTH - 120, 10)
	DISPLAY.blit(scoreSurf, scoreRect)

def drawSnake(snake):
	for coord in snake:
		x = coord['x'] * BLOCK_SIZE
		y = coord['y'] * BLOCK_SIZE
		snakeSegmentRect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
		pygame.draw.rect(DISPLAY, BLUE, snakeSegmentRect)
		snakeSegmentRect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
		pygame.draw.rect(DISPLAY, DARKBLUE, snakeSegmentRect, 1)
		
	
def drawApple(coord):
	x = coord['x'] * BLOCK_SIZE #+ 0.5 * BLOCK_SIZE
	y = coord['y'] * BLOCK_SIZE #+ 0.5 * BLOCK_SIZE
	appleRect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
	pygame.draw.rect(DISPLAY, RED, appleRect)
	
def drawBoarders():
	pygame.draw.line(DISPLAY, GRAY, (0, 0), (WINDOW_WIDTH, 0), 2)
	pygame.draw.line(DISPLAY, GRAY, (0, 0), (0, WINDOW_HEIGHT), 2)
	pygame.draw.line(DISPLAY, GRAY, (WINDOW_WIDTH, WINDOW_HEIGHT), (WINDOW_WIDTH, 0), 5)
	pygame.draw.line(DISPLAY, GRAY, (WINDOW_WIDTH, WINDOW_HEIGHT), (0, WINDOW_HEIGHT), 5)
	

def showStartScreen():
	titleFont = pygame.font.Font('freesansbold.ttf', 100)
	titleSurf1 = titleFont.render('SNAKE!', True, WHITE, DARKBLUE)
	titleSurf2 = titleFont.render('SNAKE!', True, BLUE)
	
	degrees1 = 0
	degrees2 = 0
	
	while True:
		DISPLAY.fill(BGCOLOR)
		rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
		rotatedRect1 = rotatedSurf1.get_rect()
		rotatedRect1.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
		DISPLAY.blit(rotatedSurf1, rotatedRect1)
		
		rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
		rotatedRect2 = rotatedSurf2.get_rect()
		rotatedRect2.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
		DISPLAY.blit(rotatedSurf2, rotatedRect2)
		
		drawPressKeyMsg()
		
		if checkForKeyPress():
			pygame.event.get()
			pygame.display.update()
			CLOCK.tick(FPS)
			return
		
		pygame.display.update()
		CLOCK.tick(FPS)
		degrees1 += 3
		degrees2 += 7
		
def showGameOverScreen():
	gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
	gameSurf = gameOverFont.render('Game', True, WHITE)
	overSurf = gameOverFont.render('Over', True, WHITE)
	gameRect = gameSurf.get_rect()
	overRect = overSurf.get_rect()
	gameRect.midtop = (WINDOW_WIDTH / 2, 10)
	overRect.midtop = (WINDOW_WIDTH / 2, gameRect.height + 10 + 25)
	
	FPS = 10
	
	DISPLAY.blit(gameSurf, gameRect)
	DISPLAY.blit(overSurf, overRect)
	drawPressKeyMsg()
	pygame.display.update()
	pygame.time.wait(500)
	checkForKeyPress()
	
	while True:
		if checkForKeyPress():
			pygame.event.get()
			return
	
def terminate():
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()