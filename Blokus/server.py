import socket, sys, threading, json
class Server():
	
	def __init__(self):
		self.s = socket.socket()
		self.host = socket.gethostname()
		self.port = 9999 if sys.argv[1] == None else int(sys.argv[1])
		self.address = (self.host, self.port)
		self.s.bind(('', self.port))
		self.s.listen(5)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
	def parseinput(self, message, clientAddress, clientSocket):
		print(message)
		
	def listen(self):
		
		print('Server Online...\nConnect on Port: %s' % (self.port))
		
		while True:
			clientSocket, clientAddress = self.s.accept()
			print("Found a new connection")
			clientSocket.settimeout(None)
			print("Spawning a thread")
			
			thread = threading.Thread(target = self.control, args = (clientSocket, clientAddress))
			thread.start()
			
	def control(self, clientSocket, clientAddress):
		while True:
			sys.stdout.flush()
			instruction = clientSocket.recv(4096)
			
			if instruction is not None:
				self.parseinput(message, clientAddress, clientSocket)
				

def main():
	
	server = Server()
	server.listen()
	
if __name__ == '__main__':
	main()