from socket import *
from threading import Thread
import select
import sys

HOST = 'localhost' # define our host
PORT = 8000 # define our port

s = socket(AF_INET, SOCK_STREAM) # creates a TCP socket
s.connect((HOST, PORT)) # connects to our host and port


def sendReceive():
  global s

  message = eval(input("Enter 1 or 2: "))

  if message == 1:
        play = True

        while True:

          if play:

                message = input("Enter message: ") # takes input for what to send

                if message == "quit": # check to see if user quits
                  s.close() # closes socket is user quicks
                  break; # breaks out of looop and exits program
                
                s.sendto(message.encode(),(HOST, PORT)) # allows client to send data to Server
                data = s.recv(1024) # waits for a reply from Server
                print(data) # print reply from Server
                if data != "quit":
                  play = False
                else:
                  play = True

          else:
                data = s.recv(1024) # waits for a reply from Server
                print(data) # print reply from Server
                play = True

  else:

        play = False

        while True:

          if play:
                message = input("Enter message: ") # takes input for what to send

                if message == "quit": # check to see if user quits
                  s.close() # closes socket is user quicks
                  break; # breaks out of looop and exits program
                
                s.sendto(message.encode(),(HOST, PORT)) # allows client to send data to Server
                data = s.recv(1024) # waits for a reply from Server
                print(data) # print reply from Server
                play = False

          else:
                data = s.recv(1024) # waits for a reply from Server
                print(data) # print reply from Server
                play = True
  print('here')



  while True:

    message = eval(input("Enter message: ")) # takes input for what to send

    if message == "quit": # check to see if user quits
      s.close() # closes socket is user quicks
      break; # breaks out of looop and exits program
    s.send(message) # allows client to send data to Server
    data = s.recv(1024) # waits for a reply from Server
    print(data) # print reply from Server
  



sendReceive()
# for i in range(5):
#   Thread(target=sendReceive).start()
