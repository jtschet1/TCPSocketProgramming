from socket import * #import socket module
import sys # In order to terminate the program
import errno
import os

#create socket if sufficient args given
if len(sys.argv) < 2:
	sys.exit("Usage: 'python3 Webserver.py portnumber'")
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = int(sys.argv[1])

try:
	serverSocket.bind(('', serverPort))
	serverSocket.listen(1)
except PermissionError as e:
	sys.exit("No permission to use port " + str(serverPort) + ". " + str(e))
while True:
	#Establish the connection
	print('Ready to serve...')
	try:
		connectionSocket, addr = serverSocket.accept()
		try:
			message = connectionSocket.recv(1024).decode()
			print(message, flush=True)
			filename = message.split()[1]
			#Exit if filename is stop
			if any(x in filename[1:] for x in ["Stop", "stop"]):
				raise ValueError("Recieved stop from client.\r\n")
			'''
			for x in filename[1:]:
				if x.lower() == "stop":
					raise ValueError("Received stop from client.\r\n")
			'''
			f = open(filename[1:])
			outputdata = f.read()
			#Send one HTTP header line into socket
			connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
			#Send the content of the requested file to the client
			for i in range(0, len(outputdata)):
				connectionSocket.send(outputdata[i].encode())
			connectionSocket.send("\r\n".encode())
			connectionSocket.close()
		except IOError:
			#Send response message for file not found
			connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
			#Close client socket 
			connectionSocket.close()
		except ValueError as e:
			connectionSocket.close()
			sys.exit(e.args)
	except KeyboardInterrupt:
		sys.exit("\nKilled gracefully")
		
serverSocket.close()
sys.exit()

