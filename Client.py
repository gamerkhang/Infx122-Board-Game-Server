from socket import *
from Protocol import Protocol
from Client_UI import ClientUI


class Client:

    def __init__(self, address=('localhost', 9999)):
        self.address = address
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.address)
        self.username = ""
        self.game = ""
        self.game_id = ""

        # *********************************
        print("Client connected...")

    def receive_data(self):
        data = str(self.client_socket.recv(1024), "utf-8")
        # print("client Received Message >>>", data)  # For debugging
        return data.strip()

    def send_data(self, data):
        self.client_socket.sendall(bytes(data + "\n", "utf-8"))

    def welcome(self):

        user_input = ClientUI.welcome()

        if user_input.upper() == "L":
            self.login()
        else:
            self.new_account()

    def login(self):

        while True:
            self.username = ClientUI.get_user_input("Enter your Username: ")

            self.send_data(Protocol.login(self.username))

            _expected_answer = self.receive_data()

            if _expected_answer == "VALID_USERNAME":
                break
            elif _expected_answer == "":
                ClientUI.print_detail("Huge error. Server sent back >>> " + _expected_answer)
            else:
                ClientUI.print_detail("Invalid username. Please try it again.")

    def new_account(self):

        while True:
            self.username = input("Enter your Username: ").strip()

            self.send_data(Protocol.new_user(self.username))

            _expected_answer = self.receive_data()

            if _expected_answer == "VALID_USERNAME":
                break
            elif _expected_answer == "":
                print("Huge error. Server sent back >>> ", _expected_answer)
            else:
                print("Someone already has that username. Try another?")

    def select_game(self):

        user_input = ClientUI.select_game()

        if user_input.upper() == "C":
            self.game = "Connect4"
            self.send_data(Protocol.new_game(self.username, "Connect4"))
        elif user_input.upper() == "O":
            self.game = "Othello"
            self.send_data(Protocol.new_game(self.username, "Othello"))
        else:
            self.game = "Battleship"
            self.send_data(Protocol.new_game(self.username, "Battleship"))

        _expected_answer = self.receive_data()

        if _expected_answer == "GAME_SET":
            pass
        else:
            ClientUI.print_detail("Huge error. Server sent back >>> " + _expected_answer)

    def select_player(self):

        user_input = ClientUI.select_player()

        if user_input.upper() == "A":
            self.send_data(Protocol.auto_player(self.username))
        else:
            self.send_data("SEND_LIST@", self.username)

            player_list = self.receive_data().split('@')

            for index in range(len(player_list)):
                ClientUI.print_detail(str(index) + " " + player_list[index])

            player_name = ClientUI.get_user_input("Enter the name of player you would like to play with: ")

            self.send_data(Protocol.list_of_players(self.username, player_name))

    def play(self):
        _expected_answer = self.receive_data()

        if _expected_answer == "WAIT":
            ClientUI.print_detail("WAIT for another player...")
            while True:
                _expected_answer = self.receive_data()
                if _expected_answer == "READY":
                    break

        if _expected_answer == "READY":
            ClientUI.print_detail("READY to player")

        _expected_answer = self.receive_data()

        if "GAME-ID" in _expected_answer:
            data = _expected_answer.split("@")
            self.game_id = data[1]
            data = data[1].split("_")

            if data[0] == self.username:
                print("username: ", self.username, "  >>> I am the 1st player")
                print("Game_ID: ", self.game_id)
            else:
                print("username: ", self.username, "  >>> I am the 2nd player")
                print("Game_ID: ", self.game_id)





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
    client.chat()
