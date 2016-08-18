import socket, select, string, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)

try:
	s.connect(("waleska.nvg.im",4949))
except:
	print 'Unable to connect' 
	sys.exit()

print 'Connected...' 

while 1:
		  socket_list = [sys.stdin, s]

		  # Get the list sockets which are readable
		  read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

		  for sock in read_sockets:
				#incoming message from remote server
				if sock == s:
					data = sock.recv(4096)
					if not data:
						print 'Connection closed' 
						sys.exit()
			  		else:
				st



  		#print data
				  		sys.stdout.write(data)
				else:
					msg = "list"
					s.send(msg)


s.close()
