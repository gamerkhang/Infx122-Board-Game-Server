from socket import *
from threading import Thread
import select
import sys

HOST = '' # define our host
PORT = 8000 # define our port

s = socket(AF_INET, SOCK_STREAM) # creates a TCP socket
s.connect((HOST, PORT)) # connects to our host and port
# while True:

# 	message = raw_input("Enter message: ") # takes input for what to send

# 	if message == "quit": # check to see if user quits
# 		s.close() # closes socket is user quicks
# 		break; # breaks out of looop and exits program
# 	s.send(message) # allows client to send data to Server
# 	data = s.recv(1024) # waits for a reply from Server
# 	print(data) # print reply from Server


def sendReceive():
	global s
	while True:
		socket_list = [sys.stdin, s]

		message = raw_input("Enter message: ") # takes input for what to send

		if message == "quit": # check to see if user quits
			s.close() # closes socket is user quicks
			break; # breaks out of looop and exits program
		s.send(message) # allows client to send data to Server
		data = s.recv(1024) # waits for a reply from Server
		print(data) # print reply from Server
	



sendReceive()
# for i in range(5):
# 	Thread(target=sendReceive).start()