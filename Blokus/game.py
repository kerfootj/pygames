class Game():
	def __init__(self, player):
	
		self.num_players = 1
		self.turn = 0
		self.max_players = 4
		
		self.state = 'waiting'
		self.board = [[0 for y in range(5)] for x in range(5)]
	
	# Add a player to the game
	def add_player(player):
		# Make sure there is space in the game
		if self.num_players < self.max_players:
			players.append(player)
			self.num_players += 1
			return True
		return False
	
	# Return true if the game has started, false if players can still join
	def can_join():
		return self.state == 'waiting'
	
	# Start the game
	def start_game():
		self.state = 'running'
	
	# Place a tile on board	
	def place(self, tile, c, num):
		# Only allow a player to place a tile on their turn
		if self.turn == num:
			# Next players turn 
			self.turn = (self.turn + 1) % self.max_players
			# place the tile
			for piece in tile:
				row, col = piece
				self.board[row][col] = c
				return True
		return False

def main():
	game = Game(1)
	game.place([[0,0]], 1, 0)
	game.place([[1,1]], 2, 0)
	game.place([[2,2]], 3, 1)
	game.place([[3,3]], 4, 0)
	print(str(game.board))

if __name__ == '__main__':
	main()