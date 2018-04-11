import pygame, time
from pygame.locals import *

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
BLOCK_SIZE = 100
BUFFER = WINDOW_HEIGHT - WINDOW_WIDTH
assert WINDOW_WIDTH % BLOCK_SIZE == 0
assert WINDOW_HEIGHT % BLOCK_SIZE == 0

WHITE = 	(255, 255, 255)
GRAY =		(120, 120, 120)
DGRAY = 	( 80,  80,  80)
LGRAY = 	(130, 130, 130)
BLACK = 	(  0,   0,   0)
BEIGE =  	(205, 205, 180)
PINK = 		(255, 105, 180)
RED = 		(255, 	0,   0)
ORANGE = 	(255, 140,   0)
DORANGE = 	(255,  99,  71)
LORANGE = 	(255, 165,   0)
YELLOW = 	(255, 255, 102)
DYELLOW = 	(255, 255,   0)
LYELLOW = 	(255, 255, 153)
GOLD = 		(255, 215,   0)
LGOLD =		(255, 223,   0)
LBLUE = 	( 30, 144, 255)		

BGCOLOR = GRAY
COLORS = {0: LGRAY, 2: WHITE, 4: BEIGE, 8: LORANGE, 16: ORANGE, 32: DORANGE, 64: RED,
		  128: LYELLOW, 256: YELLOW, 512: DYELLOW, 1024: LGOLD, 2048: GOLD, 4096: PINK}

def text_objects(text, font, color=BLACK):
	
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()
	
def drawTitle(DISPLAY):
	
	x=y = 15
	w=h = 125
	pygame.draw.rect(DISPLAY, GOLD, (x,y,w,h))
	titleFont = pygame.font.Font('freesansbold.ttf', 48)
	textSurf, textRect = text_objects('2048', titleFont, WHITE)
	textRect.center = (x+(w/2), y+(h/2))
	DISPLAY.blit(textSurf, textRect)

def drawScore(DISPLAY, score):
	
	textFont = pygame.font.Font('freesansbold.ttf', 18)
	textSurf, textRect = text_objects('Score', textFont, WHITE)
	textRect.topright = (WINDOW_WIDTH - 12, 10)
	DISPLAY.blit(textSurf, textRect)
	
	textFont = pygame.font.Font('freesansbold.ttf', 32)
	textSurf, textRect = text_objects(str(score), textFont, WHITE)
	textRect.topright = (WINDOW_WIDTH - 12, 32)
	DISPLAY.blit(textSurf, textRect)

def drawTime(DISPLAY, t):
	
	textFont = pygame.font.Font('freesansbold.ttf', 18)
	textSurf, textRect = text_objects('Time', textFont, WHITE)
	textRect.topright = (WINDOW_WIDTH - 12, 80)
	DISPLAY.blit(textSurf, textRect)
	
	elapsed = int(time.time()-t)
	if elapsed < 60:
		et = time.strftime('%S', time.gmtime(elapsed))
	else:
		et = time.strftime('%M:%S', time.gmtime(elapsed))
	
	textFont = pygame.font.Font('freesansbold.ttf', 32)
	textSurf, textRect = text_objects(et, textFont, WHITE)
	textRect.topright = (WINDOW_WIDTH - 12, 102)
	DISPLAY.blit(textSurf, textRect)
	
def drawBoard(DISPLAY, board):
	
	offset = 6 
	for i in range(0, len(board)):
		for j in range(0, len(board[i])):
			tile = pygame.Rect(i*BLOCK_SIZE+offset, j*BLOCK_SIZE+BUFFER+offset, BLOCK_SIZE-2*offset, BLOCK_SIZE-2*offset)
			val = board[i][j]
			pygame.draw.rect(DISPLAY, COLORS[val], tile)
			if val != 0:
				tileFont = pygame.font.Font('freesansbold.ttf', 18)
				textSurf, textRect = text_objects(str(val), tileFont)
				textRect.center = (i*BLOCK_SIZE+BLOCK_SIZE/2, j*BLOCK_SIZE+BUFFER+BLOCK_SIZE/2)
				DISPLAY.blit(textSurf, textRect)
	
def showGameEndScreen(DISPLAY, result):
	
	top = 'You' if result else 'GAME'
	bottom = 'WIN!' if result else 'OVER'
	fillColor = (255,255,102,100) if result else (80,80,80,180)
	textColor = DGRAY if result else WHITE
		
	rect = pygame.Surface((400,400), pygame.SRCALPHA)
	rect.fill(fillColor)                  
	
	gameOverFont = pygame.font.Font('freesansbold.ttf', 50)
	
	topSurf, topRect = text_objects(top, gameOverFont, textColor)
	btmSurf, btmRect = text_objects(bottom, gameOverFont, textColor)
	topRect.midbottom = (WINDOW_WIDTH/2, (WINDOW_HEIGHT+BUFFER)/2 - 6)
	btmRect.midtop = (WINDOW_WIDTH/2, (WINDOW_HEIGHT+BUFFER)/2 + 6)
	
	DISPLAY.blit(rect,(0, BUFFER))	
	DISPLAY.blit(topSurf, topRect)
	DISPLAY.blit(btmSurf, btmRect)