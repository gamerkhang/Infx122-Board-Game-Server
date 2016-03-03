from socket import *
from threading import Thread

def recieveData(s, conn): # function to recieve data
    data = conn.recv(1024) # conn.recv(1024) waits for data of 1024 or less bytes and stores it in data
    print "Received Message", repr(data)
    print(conn, data, "\n") # print the connection and data sent
    return data; # returns the contents of data

def broadcastData(s, conn, data): # function to send Data
	print  conn  , "sending to conn= "
	print s , " socket=  "
	conn.sendall(data)  # sends data received to connection
	print("Data sent to all clients \n")  # print to inform data was went


socks = []
conns = []

def clientHandler(): 	
	conn, addr = s.accept() 
	global conns
	conns += [conn]
	print addr, "is Connected"
	print conn, "conn is Connected" 
	while 1: 
		data = recieveData(s,conn)
		if not data: 
			break
		for i in range(len(conns)):
			print i
			broadcastData(s,conns[i], data)



HOST = '' #localhost
PORT = 8000

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print "Server is running......"

for i in range(5): 
	Thread(target=clientHandler).start()

s.close()
