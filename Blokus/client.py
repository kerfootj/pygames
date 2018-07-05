import socket, sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(sys.argv[1]) if len(sys.argv) == 2 else 9999

server_address = ('localhost', port)
sock.connect(server_address)

try:
	message = '/players 3'.encode()
	sock.sendall(message)
	
	amount_received = 0
	amount_expected = len(message)
	
	while amount_received < amount_expected:
		data = sock.recv(16)
		amount_received += len(data)
		print('received "%s"' % data.decode())
		
finally:
	print('closing socket')
	sock.close()
