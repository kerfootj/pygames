import socket, sys, threading, re, pygame

class Server():
	
	def __init__(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.port = int(sys.argv[1]) if len(sys.argv) == 2 else 9999
		self.s.bind(('', self.port))
		self.s.listen(5)
		
		self.players = []
		self.state = 'wating'
		self.turn = 0
		self.total = [4,0]
		
		self.board = []
				
	def listen(self):
		
		print('Server Online...\nConnect on Port: %s' % (self.port))
		
		while len(self.players) < self.total[0]:
			
			print('len ' + str(len(self.players)) + '\t' + str(self.total))
			# Connect client to the server
			conn, addr = self.s.accept()
			conn.settimeout(None)
			
			# Add the player to the list
			self.players.append((conn, addr))
			
			# Spawn a new thread for the player
			thread = threading.Thread(target = self.client_thread)
			thread.start()
		
		if self.state != 'running':
			self.update_game_state('running')
		
		print('Game Started')
		
	
	def client_thread(self):
		
		player_num = len(self.players) - 1 
		conn = self.players[player_num][0]
		msg = '%s' % (player_num)
		conn.sendall(msg.encode())
		
		print('Player %s connected from: %s' % (player_num+1, self.players[player_num][1][0]))
		
		while True:
			
			sys.stdout.flush()
			data = conn.recv(2048).decode()
			
			if data is not None:
				if player_num == self.turn:
					self.parse_data(data)
			
			data = None
		
		print('All players connected...\nStarting the game')
		self.state = 'running'
				
		print('Closed connection from: ' + str(addr))
		conn.close()
		
	def parse_data(self, data):
		
		print(data)
		
		cmd = ''
		arg = ''
		
		if data.startswith('/'):
			
			cmd = data.split(' ', 1)[0]
			arg = data.split(' ', 1)[1]
			
			if cmd == '/state':
				self.update_game_state(arg)
			if cmd == '/players' and not self.total[1]:
				self.total = [arg, 1]
				print('Game created for ' + str(arg) + ' players')
	
	def update_game_state(self, state):
		self.state = state
		
def main():
		
	print('Setting up game...')
	pygame.init()
	
	print('Starting Server')
	server = Server()
	server.listen()
	
if __name__ == '__main__':
	main()
