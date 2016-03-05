from socket import *
from Protocole import *
from signal import signal, SIGPIPE, SIG_DFL


class Client:

    def __init__(self, address=('localhost', 8000)):
        self.address = address
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.address)
        self.username = ""

        # *********************************
        print("Client")

    def welcome(self):
        print("************* Welcome Board Game *************")

        user_input = ""

        while True:
            print("l -> Login: ")
            print("c -> Create an account:")
            user_input = input()
            if user_input.upper() not in ["C", "L"]:
                print("Invalid input. Please try it again.")
            else:
                break

        if user_input.upper() == "L":

            self._login()
        else:
            self._new_account()

    def game(self):
        print("******** Select a Game ********")
        user_input = ""
        while True:
            print("c -> Connect4 ")
            print("o -> Othello")
            print("b -> Battleship")
            user_input = input()
            if user_input.upper() not in ["C", "O", "B"]:
                print("Invalid input. Please try it again.")
            else:
                break

        if user_input.upper() == "L":

            self._login()
        else:
            self._new_account()

    def _login(self):

            while True:
                self.username = input("Enter your Username: ").strip()

                self.send_data(login_protocole(self.username))

                data = self.receive_data()

                if data == "VALID_USERNAME":
                    break
                else:
                    print("Invalid username. Please try it again.")

    def _new_account(self):

        while True:
            self.username = input("Enter your Username: ").strip()

            self.send_data(new_user_protocole(self.username))

            data = self.receive_data()

            if data == "VALID_USERNAME":
                break
            elif data == "":
                print("Server did not responde")
            else:
                print("Someone already has that username. Try another?")

    def receive_data(self):

        return self.client_socket.recv(1024).decode("utf-8")

    def send_data(self, data):
        # try:
            self.client_socket.sendto(data.encode(), self.address)
        # except:
        #     print("except")
        #     self.client_socket = socket(AF_INET, SOCK_STREAM)
        #     self.client_socket.connect(self.address)
        #     self.send_data(data)

    def chat(self):

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
    client.welcome()
    client.chat()
