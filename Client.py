from socket import *


class Client:

    def __init__(self, address=('localhost', 8000)):
        self.address = address
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.address)
        self.name = ""

        # *********************************
        print("Client")

    def send_receive(self):

        message = eval(input("Enter 1 or 2: "))

        if message == 1:
            play = True

            while True:
                if play:
                    message = input("Enter message: ") # takes input for what to send

                    if message == "quit": # check to see if user quits
                        self.client_socket.close()  # closes socket is user quicks
                        break  # breaks out of looop and exits program

                    self.client_socket.sendto(message.encode(), self.address)
                    data = self.client_socket.recv(1024) # waits for a reply from Server
                    # print(data.decode("utf-8")) # print reply from Server
                    if data != "quit":
                        play = False
                    else:
                        play = True
                else:
                    data = self.client_socket.recv(1024) # waits for a reply from Server
                    print(data.decode("utf-8"))  # print reply from Server
                    play = True
        else:

            play = False

            while True:

                if play:
                    message = input("Enter message: ") # takes input for what to send

                    if message == "quit": # check to see if user quits
                        self.client_socket.close()  # closes socket is user quicks
                        break  # breaks out of looop and exits program

                    self.client_socket.sendto(message.encode(), self.address) # allows client to send data to Server
                    data = self.client_socket.recv(1024) # waits for a reply from Server
                    print(data.decode("utf-8") ) # print reply from Server
                    play = False
                else:
                    data = self.client_socket.recv(1024) # waits for a reply from Server
                    print(data.decode("utf-8")) # print reply from Server
                    play = True


if __name__ == '__main__':

    client = Client()
    client.send_receive()
