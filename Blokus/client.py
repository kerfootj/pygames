import socket, sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('184.71.29.94', int(sys.argv[1]))
sock.connect(server_address)

try:
	message = 'This is a test message'
	sock.sendall(message)
	
	amount_received = 0
	amount_expected = len(message)
	
	while amount_received < amount_expected:
		data = sock.recv(16)
		amount_received += len(data)
		print >>sys.stderr, 'received "%s"' % data
		
finally:
	print >>sys.stderr, 'closing socket'
	sock.close()