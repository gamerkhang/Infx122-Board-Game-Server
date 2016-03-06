from socket import *
from Protocole import *


class Client:

    def __init__(self, address=('localhost', 9999)):
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

    def select_game(self):
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

        if user_input.upper() == "C":
            self._send_data(new_game_protocole(self.username, "Connect4"))
        elif user_input.upper() == "O":
            self._send_data(new_game_protocole(self.username, "Othello"))
        else:
            self._send_data(new_game_protocole(self.username, "Battleship"))

        _expected_answer = self.receive_data()
        if _expected_answer == "GAME_SET":
            pass
        else:
            print("Huge error. Server sent back >>> " , _expected_answer)

    def select_player(self):
        print("******** Select a Player ********")
        user_input = ""
        while True:
            print("a -> Auto-Selection ")
            print("l -> Select from the list of players")
            user_input = input()
            if user_input.upper() not in ["A", "L"]:
                print("Invalid input. Please try it again.")
            else:
                break

        if user_input.upper() == "A":
            self._send_data(select_auto_player_protocole(self.username))
        else:
            self._send_data("SEND_LIST@", self.username)
            player_list = self.receive_data().split('@')
            for index in range(len(player_list)):
                print(index, " ", player_list[index])
            player_name = input("Enter the name of player you would like to play with: ")
            self._send_data(select_list_player_protocole(self.username, player_name))

    def play(self):
        _expected_answer = self.receive_data()

        if _expected_answer == "WAIT":
            print("WAIT for another player...")
            while True:
                _expected_answer = self.receive_data()
                if _expected_answer == "READY":
                    break

        if _expected_answer == "READY":
            print("READY to player")
            self._send_data("READY to play from client ")
            _expected_answer = self.receive_data()
            print("_expected_answer ", _expected_answer)

    def _login(self):

        while True:
            self.username = input("Enter your Username: ").strip()

            self._send_data(login_protocole(self.username))

            _expected_answer = self.receive_data()

            if _expected_answer == "VALID_USERNAME":
                break
            elif _expected_answer == "":
                print("Huge error. Server sent back >>> " , _expected_answer)
            else:
                print("Invalid username. Please try it again.")

    def _new_account(self):

        while True:
            self.username = input("Enter your Username: ").strip()

            self._send_data(new_user_protocole(self.username))

            _expected_answer = self.receive_data()
            if _expected_answer == "VALID_USERNAME":
                break
            elif _expected_answer == "":
                print("Huge error. Server sent back >>> " , _expected_answer)
            else:
                print("Someone already has that username. Try another?")

    def receive_data(self):
        data = str(self.client_socket.recv(1024), "utf-8")
        # data = self.client_socket.recv(1024).decode("utf-8")
        print("client Received Message >>>", data)
        return data.strip()

    def _send_data(self, data):
        self.client_socket.sendall(bytes(data + "\n", "utf-8"))
        # print("client sending ", data)
        # self.client_socket = socket(AF_INET, SOCK_STREAM)
        # self.client_socket.connect(self.address)
        # self.client_socket.sendto(data.encode(), self.address)
        # print("client sent" , data)

    def send_data(self, data):
        pass
        #self.client_socket.sendall(bytes(data + "\n", "utf-8"))
            #print("client sending ", data)
            # self.client_socket = socket(AF_INET, SOCK_STREAM)
            # self.client_socket.connect(self.address)
            #self.client_socket.sendto(data.encode(), self.address)
            #print("client sent", data)

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

                    self.send_data(message)
                    #self.client_socket.sendto(message.encode(), self.address)
                    data = self.receive_data()
                    print(data)
                    #data = self.client_socket.recv(1024) # waits for a reply from Server
                    # print(data.decode("utf-8")) # print reply from Server
                    if data != "quit":
                        play = False
                    else:
                        play = True
                else:
                    data = self.receive_data()
                    print(data)
                    #data = self.client_socket.recv(1024) # waits for a reply from Server
                    #print(data.decode("utf-8"))  # print reply from Server
                    play = True
        else:

            play = False

            while True:

                if play:
                    message = input("Enter message: ") # takes input for what to send

                    if message == "quit": # check to see if user quits
                        self.client_socket.close()  # closes socket is user quicks
                        break  # breaks out of looop and exits program

                    self.send_data(message)
                    data = self.receive_data()
                    print(data)
                    #self.client_socket.sendto(message.encode(), self.address) # allows client to send data to Server
                    #data = self.client_socket.recv(1024) # waits for a reply from Server
                    #print(data.decode("utf-8") ) # print reply from Server
                    play = False
                else:
                    data = self.receive_data()
                    print(data)
                    #data = self.client_socket.recv(1024) # waits for a reply from Server
                    #print(data.decode("utf-8")) # print reply from Server
                    play = True


if __name__ == '__main__':

    client = Client()
    client.welcome()
    client.select_game()
    client.select_player()
    client.play()
    # client.chat()
