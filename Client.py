from socket import *
from Protocol import Protocol
from Board import Board
from Client_UI import ClientUI
from GameUI import GameUI

from OthelloBoard import OthelloBoard
from OthelloGameUI import OthelloGameUI

from Connect4Board import Connect4Board
from Connect4GameUI import Connect4GameUI

from BattleshipBoard import BattleshipBoard
from BattleshipGameUI import BattleshipGameUI

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
        self.battleship_setup = True
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

        self.username = ClientUI.get_user_input("Enter your Username: ")

        self.send_data(Protocol.login(self.username))

        _expected_answer = self.receive_data()

        if _expected_answer == "VALID_USERNAME":
            pass
        elif _expected_answer == "":
            ClientUI.print_detail("Huge error. Server sent back >>> " + _expected_answer)
        else:
            ClientUI.print_detail("\nInvalid username. Please try it again.\n")
            self.welcome()

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
        elif user_input.upper() == "O":
            self.game_type = "Othello"
        else:
            self.game_type = "Battleship"

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

            while True:

                self.send_data(Protocol.send_list(self.username, self.game_type))

                data = self.receive_data().strip()

                while "MATCH_LIST" not in data:
                    data = self.receive_data().strip()

                player_list = data.split('@')

                del player_list[0]
                if len(player_list) != 0:
                    print("\nPlease insert the username that you would like to play with:")
                    print("------------------------------------------------------------")
                    for index in range(len(player_list)):
                        ClientUI.print_detail(str(index + 1) + " -> " + player_list[index])

                    print("----------------------------------------------------------")
                    player_name = ClientUI.get_user_input("\nEnter the username: ")

                    self.send_data(Protocol.play_with(self.username, player_name))
                    break
                else:
                    print("\nThere is no player. Please try it again!!!\n")
                    self.select_player()
                    break

    def setup_game(self):
        _expected_answer = self.receive_data()

        if _expected_answer == "WAIT":
            ClientUI.print_detail("WAIT for another player...")
            #while True:
                #_expected_answer = self.receive_data()
                #if _expected_answer == "READY":
                    #break
            _expected_answer = self.receive_data()
            print(_expected_answer)

        if _expected_answer == "READY":
            ClientUI.print_detail("READY to player")
            _expected_answer = self.receive_data()
        elif "READY" in _expected_answer:
            _expected_answer = _expected_answer[5:]
            print("recv concat~")
            print(_expected_answer)

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
            else:
                self.player_key = self.game_board.get_next_player()
                print("Game_ID: ", self.game_id)
                print("username: ", self.username, "  >>> 2nd player >>> Your annotation is: ", self.player_key)
                self.game_ui.print_scores(self.game_board)
                self.game_ui.print_board(self.game_board)

    def set_game_board(self):
        if self.game_type == "Othello":
            self.game_board = OthelloBoard()
        elif self.game_type == "Connect4":
            self.game_board = Connect4Board()
        else:
            self.game_board = BattleshipBoard()

    def set_game_ui(self):
        if self.game_type == "Othello":
            self.game_ui = OthelloGameUI()
        elif self.game_type == "Connect4":
            self.game_ui = Connect4GameUI()
        else:
            self.game_ui = BattleshipGameUI()

    def play_game(self):
        if self.game_type == "Battleship":
            if self.battleship_setup:
                self.game_ui.setUp(self.game_board)
                states = ""
                for row in range(self.game_board.get_num_rows()):
                    for col in range(self.game_board.get_num_columns()):
                        states += "@" + self.game_board.get_game_state()[row][col]
                states += "@"

                self.send_data(Protocol.set_ship(self.game_id, str(states)))

                self.battleship_setup = False

        if self.player_key == self.game_board.get_player_turn():
            print("\nIt's your turn. Please make your move!!!\nYour game annotation is: ", self.player_key)
            move = self.game_ui.make_move(self.game_board)

            self.send_data(Protocol.play_game(self.game_id, str(move[0]) + "@" + str(move[1])))
        else:
            print("\nIt is not your turn. Please wait for the next player to make his/her move.")

        _expected_answer = self.receive_data()
        while _expected_answer == "":
            _expected_answer = self.receive_data()

        while _expected_answer != "GAME_OVER":

            if "BS_PRIMARY" in _expected_answer: # for Battleship Primary Grid
                count = 0
                temp = _expected_answer.split('@')
                del temp[0]
                for row in range(self.game_board.get_num_rows()):
                    for col in range(self.game_board.get_num_columns()):
                        self.game_board.primaryGrid1[row][col] = temp[count]
                        count += 1

            if "BS_TRACKING" in _expected_answer: # for Battleship Tracking Grid
                count = 0
                temp = _expected_answer.split('@')
                del temp[0]
                for row in range(self.game_board.get_num_rows()):
                    for col in range(self.game_board.get_num_columns()):
                        self.game_board.trackingGrid1[col][row] = temp[count]
                        count += 1

            if "UPDATE" in _expected_answer:
                count = 0
                temp = _expected_answer.split('@')
                del temp[0]
                for row in range(self.game_board.get_num_rows()):
                    for col in range(self.game_board.get_num_columns()):
                        self.game_board.get_game_state()[row][col] = temp[count]
                        count += 1

            elif "READY" in _expected_answer:
                self.game_ui.print_scores(self.game_board)
                self.game_ui.print_board(self.game_board)
                print("\nIt's your turn. Please make your move!!!\nYour game annotation is: ", self.player_key)
                move = self.game_ui.make_move(self.game_board)
                self.send_data(Protocol.play_game(self.game_id, str(move[0]) + "@" + str(move[1])))

            elif _expected_answer == "SWITCH_PLAYER":
                self.game_board.switch_Turn()

            elif "WAIT" in _expected_answer:
                print("WAIT from client")
                self.game_ui.print_scores(self.game_board)
                self.game_ui.print_board(self.game_board)
                print("\nIt is not your turn. Please wait for the next player to make his/her move.")

            elif "NO_MOVE_FOR_YOU" in _expected_answer:
                print("\nThere is no move for you. Changing the turn.")

            elif _expected_answer == "INVALID_MOVE":
                print("\nInvalid move. Please try it again !!!")
                move = self.game_ui.make_move(self.game_board)
                self.send_data(Protocol.play_game(self.game_id, str(move[0]) + "@" + str(move[1])))
            else:
                pass

            _expected_answer = self.receive_data()

        self.game_ui.print_scores(self.game_board)
        self.game_ui.print_board(self.game_board)
        print(self.game_board.winning_player())


if __name__ == '__main__':

    client = Client()
    client.welcome()
    user_input = ""
    while user_input != "Q":
        client.select_game()
        client.select_player()
        client.setup_game()
        client.play_game()
        while True:
            user_input = ClientUI.get_user_input("\n****** Make a Selection ******\np -> Play Again:\nq -> Quit:\n").upper()
            if user_input not in ["Q", "P"]:
                ClientUI.print_detail("\nInvalid input. Please try it again !!!")
            else:
                break

    ClientUI.print_detail("\nGood Bye!!!")
