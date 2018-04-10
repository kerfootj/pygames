import pygame, time, random, sys
from pygame.locals import *

FPS = 20

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
BLOCK_SIZE = 100
BUFFER = WINDOW_HEIGHT - WINDOW_WIDTH
assert WINDOW_WIDTH % BLOCK_SIZE == 0
assert WINDOW_HEIGHT % BLOCK_SIZE == 0
SIDE_TILES = 4

WIN = 2048
MOVES = []

WHITE = 	(255, 255, 255)
GRAY =		(120, 120, 120)
DGRAY = 	( 80,  80,  80)
LGRAY = 	(130, 130, 130)
BLACK = 	(  0,   0,   0)
BEIGE =  	(205, 205, 180)
PINK = 		(255, 105, 180)
RED = 		(255, 	0,   0)
ORANGE = 	(255, 140,	 0)
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

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():

	global CLOCK, DISPLAY, FONT, SCORE
	
	pygame.init()
				 
	CLOCK = pygame.time.Clock()
	DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	FONT = pygame.font.Font('freesansbold.ttf', 18)
	pygame.display.set_caption('2048')
	
	while True:
		result = runGame()
		if result != 'reset':
			showGameEndScreen(result)
		
def runGame():
	
	board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	direction = None
	
	global SCORE
	SCORE = 0
	
	board = addRandomTile(board)
	board = addRandomTile(board)
	
	t = time.time()
		
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if (event.key == K_LEFT or event.key == K_a):
					direction = LEFT
				elif (event.key == K_RIGHT or event.key == K_d):
					direction = RIGHT
				elif (event.key == K_UP or event.key == K_w):
					direction = UP
				elif (event.key == K_DOWN or event.key == K_s):
					direction = DOWN
				elif event.key == K_ESCAPE:
					terminate()
		
		if direction != None:
			board,new = updateBoard(board, direction)
			direction = None
			state = checkState(board)
			if state != 'not over':
				drawGame(board, t)
				return state
			if new:
				board = addRandomTile(board)
				
		drawGame(board, t)
		
		if button('Reset', 15, BUFFER-35, 70, 25, DGRAY, RED):
			return 'reset'
		if button('Undo', WINDOW_WIDTH-85, BUFFER-35, 70, 25, DGRAY, LBLUE):
			board = undo(board)
			
		pygame.display.update()
		CLOCK.tick(FPS)
			
def checkState(board):
	
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == WIN:
				return 'win'
				
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == 0:
				return 'not over'
	
	for i in range(len(board)-1): 
		for j in range(len(board[i])-1): 
			if board[i][j] == board[i+1][j] or board[i][j] == board[i][j+1]:
				return 'not over'
	
	for k in range(len(board)-1):
		if board[len(board)-1][k] == board[len(board)-1][k+1]:
			return 'not over'
	
	for j in range(len(board)-1):
		if board[j][len(board)-1] == board[j+1][len(board)-1]:
			return 'not over'
	
	return 'game over'
			
def updateBoard(board, direction):
	
	global SCORE
	MOVES.append((board,SCORE))
	if len(MOVES) > 5:
		del MOVES[0]
	
	if direction == RIGHT:
		board = reverseBoard(transposeBoard(board))
	elif direction == LEFT:
		board = transposeBoard(board)
	elif direction == DOWN:
		board = reverseBoard(board)
	
	board,done = colletTiles(board)
	temp = mergeTiles(board)
	board = temp[0]
	done = done or temp[1]
	board = colletTiles(board)[0]
	
	if not done:
		del MOVES[len(MOVES)-1]
		
	if direction == RIGHT:
		board = transposeBoard(reverseBoard(board))
	elif direction == LEFT:
		board = transposeBoard(board)
	elif direction == DOWN:
		board = reverseBoard(board)		
	
	return (board,done)

def colletTiles(board):
	
	new = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	done = False
	
	for i in range(SIDE_TILES):
		count = 0
		for j in range(SIDE_TILES):
			if board[i][j] != 0:
				new[i][count] = board[i][j]
				if j!=count:
					done = True
				count += 1
					
	return (new,done)
		
def mergeTiles(board):
	global SCORE
	done = False
	
	for i in range(SIDE_TILES):
		for j in range(SIDE_TILES-1):
			if board[i][j] != 0 and board[i][j] == board[i][j+1]:
				board[i][j] *= 2
				board[i][j+1] = 0
				SCORE += board[i][j]
				done = True
	return (board,done)

def reverseBoard(board):
	new = []
	for i in range(len(board)):
		new.append([])
		for j in range(len(board[0])):
			new[i].append(board[i][len(board[0])-j-1])
	return new
	
def transposeBoard(board):
	new = []
	for i in range(len(board[0])):
		new.append([])
		for j in range(len(board)):
			new[i].append(board[j][i])
	return new
			
def addRandomTile(board):

	val = 2
	r = random.randint(1,12)
	
	if r % 12 == 0:
		val = 4

	# Could be improved
	while True:
		x = random.randint(0,3)
		y = random.randint(0,3)
		
		if board[x][y] == 0:
			board[x][y] = val
			return board

def undo(board):
	
	global SCORE
	pygame.time.wait(200)
	
	if len(MOVES) > 0:
		temp = MOVES[len(MOVES)-1][0]
		SCORE = MOVES[len(MOVES)-1][1]
		del MOVES[len(MOVES)-1]
		if temp != None:
			return temp
	return board

def drawGame(board,t):
	DISPLAY.fill(BGCOLOR)
	drawTitle()
	drawBoard(board)
	drawScore()
	drawTime(t)

def drawTitle():
	x=y = 15
	w=h = 125
	pygame.draw.rect(DISPLAY, GOLD, (x,y,w,h))
	titleFont = pygame.font.Font('freesansbold.ttf', 48)
	textSurf, textRect = text_objects('2048', titleFont, WHITE)
	textRect.center = (x+(w/2), y+(h/2))
	DISPLAY.blit(textSurf, textRect)
	
def drawBoard(board):
	offset = 6 
	for i in range(0, len(board)):
		for j in range(0, len(board[i])):
			tile = pygame.Rect(i*BLOCK_SIZE+offset, j*BLOCK_SIZE+BUFFER+offset, BLOCK_SIZE-2*offset, BLOCK_SIZE-2*offset)
			val = board[i][j]
			pygame.draw.rect(DISPLAY, COLORS[val], tile)
			if val != 0:
				textSurf, textRect = text_objects(str(val), FONT)
				textRect.center = (i*BLOCK_SIZE+BLOCK_SIZE/2, j*BLOCK_SIZE+BUFFER+BLOCK_SIZE/2)
				DISPLAY.blit(textSurf, textRect)
			
def drawScore():
	global SCORE
	
	textSurf, textRect = text_objects('Score', FONT, WHITE)
	textRect.topright = (WINDOW_WIDTH - 12, 10)
	DISPLAY.blit(textSurf, textRect)
	
	textFont = pygame.font.Font('freesansbold.ttf', 32)
	textSurf, textRect = text_objects(str(SCORE), textFont, WHITE)
	textRect.topright = (WINDOW_WIDTH - 12, 32)
	DISPLAY.blit(textSurf, textRect)

def drawTime(t):
	textSurf, textRect = text_objects('Time', FONT, WHITE)
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
	
def button(msg, x, y, w, h, ic, ac):
	
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	clicked = False
	
	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(DISPLAY, ac,(x,y,w,h), 2)

		if click[0] == 1:
			 clicked = True    
	
	else:
		pygame.draw.rect(DISPLAY, ic,(x,y,w,h), 2)

	textSurf, textRect = text_objects(msg, FONT)
	textRect.center = ( (x+(w/2)), (y+(h/2)) )
	DISPLAY.blit(textSurf, textRect)
	
	return clicked

def text_objects(text, font, color=BLACK):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()
	
def showGameEndScreen(result):
	
	top = 'You'
	bottom = 'WIN!'
	fillColor = (255,255,102,100)
	textColor = DGRAY
	
	if result == 'game over':
		top = 'Game'
		bottom = 'Over'
		fillcolor = (80,80,80,128)
		textColor = WHITE
		
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
	
	pygame.display.update()
	pygame.time.wait(500)
	checkForKeyPress()
	
	while True:
		if checkForKeyPress():
			pygame.event.get()
			print('here')
			return
			
def checkForKeyPress():
	if len(pygame.event.get(QUIT)) > 0:
		terminate()
		
	keyUpEvents = pygame.event.get(KEYUP)
	if len(keyUpEvents) == 0:
		return None 
	if keyUpEvents[0].key == K_ESCAPE:
		terminate()
	return keyUpEvents[0].key
	
def terminate():
	pygame.quit()
	sys.exit()
	
if __name__ == '__main__':
	main()