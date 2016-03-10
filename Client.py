from socket import *
from Protocol import Protocol
from Board import Board
from Client_UI import ClientUI
from GameUI import GameUI

from OthelloBoard import OthelloBoard
from OthelloGameUI import OthelloGameUI

from Connect4Board import Connect4Board
from Connect4GameUI import Connect4GameUI

class Client:

    def __init__(self, address=('localhost', 9999)):
        self.address = address
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.address)
        self.username = ""
        self.game_type = ""
        self.game_id = ""
        self.game_ui = GameUI()
        self.game_board = Board()
        self.player_key = ""
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
            self.game_type = "Connect4"
            # self.send_data(Protocol.new_game(self.username, "Connect4"))
        elif user_input.upper() == "O":
            self.game_type = "Othello"
            # self.send_data(Protocol.new_game(self.username, "Othello"))
        else:
            self.game_type = "Battleship"
            # self.send_data(Protocol.new_game(self.username, "Battleship"))

    def _set_game_in_server(self):

        self.send_data(Protocol.new_game(self.username, self.game_type))

        _expected_answer = self.receive_data()

        if _expected_answer == "GAME_SET":
            pass
        else:
            ClientUI.print_detail("Huge error. Server sent back >>> " + _expected_answer)

    def select_player(self):

        user_input = ClientUI.select_player()

        if user_input.upper() == "A":
            self._set_game_in_server()
            self.send_data(Protocol.auto_player(self.username))
        else:
            self._set_game_in_server()

            self.send_data(Protocol.send_list(self.username, self.game_type))

            data = self.receive_data().strip()

            player_list = data.split('@')

            del player_list[0]

            print("\nPlease insert the username that you would like to play with:")
            print("------------------------------------------------------------")
            for index in range(len(player_list)):
                ClientUI.print_detail(str(index + 1) + " -> " + player_list[index])

            print("----------------------------------------------------------")
            player_name = ClientUI.get_user_input("\nEnter the username: ")

            self.send_data(Protocol.play_with(self.username, player_name))

            _expected_answer = self.receive_data()

            # while True:
            #     if _expected_answer == "":
            #         _expected_answer = self.receive_data()
            #     else:
            #         break

            if _expected_answer == "PLAYER_MATCHED":
                print("PLAYER_MATCHED from client ", _expected_answer)
            elif _expected_answer == "PLAYER_NOT_EXIST_ANYMORE":
                print("Player either disconnected or playing with another user.")
                print("Please try it again !!!")
                self.select_player()
            else:
                ClientUI.print_detail("Huge error. Server sent back 1>>> " + _expected_answer)

    def setup_game(self):
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

            self.set_game_board()
            self.set_game_ui()

            if data[0] == self.username:
                self.player_key = self.game_board.get_player_turn()
                print("Game_ID: ", self.game_id)
                print("username: ", self.username, "  >>> 1st player >>> Your annotation is: ", self.player_key)
                self.game_ui.print_scores(self.game_board)
                self.game_ui.print_board(self.game_board)
                # self.game_ui.print_turn(self.game_board)
            else:
                self.player_key = self.game_board.get_next_player()
                print("Game_ID: ", self.game_id)
                print("username: ", self.username, "  >>> 2nd player >>> Your annotation is: ", self.player_key)
                self.game_ui.print_scores(self.game_board)
                self.game_ui.print_board(self.game_board)
                # self.game_ui.print_turn(self.game_board)

    def set_game_board(self):
        if self.game_type == "Othello":
            self.game_board = OthelloBoard()
        elif self.game_type == "Connect4":
            self.game_board = Connect4Board()
        # else:
        #     self.game_board = BattleshipBoard()

    def set_game_ui(self):
        if self.game_type == "Othello":
            self.game_ui = OthelloGameUI()
        elif self.game_type == "Connect4":
            self.game_ui = Connect4GameUI()
        # else:
        #     self.game_ui = BattleshipGameUI()

    def play_game(self):
        if self.player_key == self.game_board.get_player_turn():
            print("\nIt's your turn. Please make your move!!!\nYour game annotation is: ", self.player_key)
            move = self.game_ui.make_move(self.game_board)
            print(str(move[0])+' ------ '+str(move[1]))
            self.send_data(Protocol.play_game(self.game_id, str(move[0]) + "@" + str(move[1])))
        else:
            print("\nIt is not your turn. Please wait for the next player to make his/her move.")

        _expected_answer = self.receive_data()
        while _expected_answer == "":
            _expected_answer = self.receive_data()
        while _expected_answer != "GAME_OVER":

            if "UPDATE" in _expected_answer:
                # print("UPDATE from client")
                count = 0
                temp = _expected_answer.split('@')
                del temp[0]
                #print(temp)
                # print("Before update", self.game_board.get_game_state())
                for row in range(self.game_board.get_num_rows()):
                    for col in range(self.game_board.get_num_columns()):
                        self.game_board.get_game_state()[row][col] = temp[count]
                        count += 1
                # print("after update", self.game_board.get_game_state())
            
            elif "READY" in _expected_answer:
                # print("READY from client")
                self.game_ui.print_scores(self.game_board)
                self.game_ui.print_board(self.game_board)
                # print(self.game_board.get_player_turn())
                # self.game_ui.print_turn(self.game_board)
                print("\nIt's your turn. Please make your move!!!\nYour game annotation is: ", self.player_key)
                move = self.game_ui.make_move(self.game_board)
                self.send_data(Protocol.play_game(self.game_id, str(move[0]) + "@" + str(move[1])))
            
            elif _expected_answer == "SWITCH_PLAYER":
                #print("SWITCH_PLAYER from client")
                # print(self.game_board.get_player_turn())
                # print("Before SWITCH_PLAYER", self.game_board.get_player_turn())
                self.game_board.switch_Turn()
                # print("After SWITCH_PLAYER", self.game_board.get_player_turn())
            
            elif "WAIT" in _expected_answer:
                # print("WAIT from client")
                self.game_ui.print_scores(self.game_board)
                self.game_ui.print_board(self.game_board)
                # self.game_ui.print_turn(self.game_board)
                print("\nIt is not your turn. Please wait for the next player to make his/her move.")
            
            elif "NO_MOVE_FOR_YOU" in _expected_answer:
                print("\nThere is no move for you. Changing the turn.")
            
            elif _expected_answer == "INVALID_MOVE":
                print("\nInvalid move. Please try it again !!!")
                move = self.game_ui.make_move(self.game_board)
                self.send_data(Protocol.play_game(self.game_id, str(move[0]) + "@" + str(move[1])))
            else:
                pass
                # print("Else from client ", _expected_answer)

            _expected_answer = self.receive_data()

        self.game_ui.print_scores(self.game_board)
        self.game_ui.print_board(self.game_board)
        print(self.game_board.winning_player())

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
    client.setup_game()
    client.play_game()
    #client.chat()
