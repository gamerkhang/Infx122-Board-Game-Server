from RemoteClient import RemoteClient
from CurrentGames import CurrentGames
from Profile import Profile
import socketserver
from OthelloBoard import OthelloBoard
from OthelloLogic import OthelloLogic
from GameLogic import GameLogic


all_saved_profiles = []
wait_list = dict()
current_games = dict()


class TCPServer(socketserver.BaseRequestHandler):

    global all_saved_profiles
    global wait_list
    global current_games

    def handle(self):

        while True:
            str_data = self.receive_data()

            if str_data == '':
                break

            conn = self.request

            if "LOGIN" in str_data:
                self._login_handler(str_data, conn)
            elif "NEW_USER" in str_data:
                self._new_user_handler(str_data, conn)
            elif "NEW_GAME" in str_data:
                self._new_game(str_data, conn)
            elif "AUTO" in str_data:
                self._auto_player(str_data, conn)
            elif "SEND_LIST" in str_data:
                self._current_players(str_data, conn)
            elif "PLAY" in str_data():
                self.play_game(str_data, conn)

            # else:
            #     print("from here")
            #
            #     for key in self.current_games.keys():
            #         for con in self.current_games[key].get_connections():
            #             print(con)
            #             self.send_data(con, self.data)

    def receive_data(self):
        data = self.request.recv(1024).strip()
        str_data = data.decode("utf-8")
        print("Server - Received: ", str_data)
        return str_data

    def send_data(self, data):
        self.request.sendall(bytes(data + "\n", "utf-8"))
        print("Server - Sent: ", data)

    @staticmethod
    def send_data_to_connection(conn, data):
        conn.sendall(data.encode())
        print("Server - Send Message to a connection", data)

    def _login_handler(self, data, conn):

        data = data.split('@')
        username = data[1]
        username_exist = False
        global all_saved_profiles
        for profile in all_saved_profiles:
            if username == profile.get_username():
                username_exist = True
                break

        if username_exist:
            self.send_data_to_connection(conn, "INVALID_USERNAME")
        else:
            all_saved_profiles += [Profile(username)]
            self.send_data_to_connection(conn, "VALID_USERNAME")

    def _new_user_handler(self, data, conn):

        data = data.split('@')
        username = data[1]
        username_exist = False
        global all_saved_profiles
        for profile in all_saved_profiles:
            if username == profile.get_username():
                username_exist = True
                break

        if username_exist:
            self.send_data_to_connection(conn, "USERNAME_EXIST")
        else:
            all_saved_profiles += [Profile(username)]
            global wait_list
            wait_list[data[1]] = ("GAME_NOT_SET", RemoteClient(conn))
            self.send_data_to_connection(conn, "VALID_USERNAME")

    def _new_game(self, data, conn):
        data = data.split('@')
        global wait_list
        wait_list[data[1]] = (data[2], RemoteClient(conn))
        self.send_data_to_connection(conn, "GAME_SET")

    def _auto_player(self, data, conn):
        data = data.split('@')
        first_player = data[1]
        global wait_list
        game_to_play = wait_list[first_player][0]
        second_player = ''

        for player in wait_list.keys():
            if player != first_player and wait_list[player][0] == game_to_play:
                second_player = player
                break

        if second_player != "":
            global current_games
            current_games[first_player + "_" + second_player] = CurrentGames(game_to_play, first_player, second_player, RemoteClient(conn), wait_list[second_player][1], self._create_board(game_to_play))
            del wait_list[first_player]
            del wait_list[second_player]
            print("wait_list ", wait_list)  # For debugging
            print("current_games", current_games)   # For debugging

            for con in current_games[first_player + "_" + second_player].get_connections():
                self.send_data_to_connection(con, "READY")
                self.send_data_to_connection(con, "GAME-ID@" + first_player + "_" + second_player)

        else:
            wait_list[first_player] = (game_to_play, RemoteClient(conn))
            self.send_data_to_connection(conn, "WAIT")

    def _create_board(self, game: str):
        if game == "Connect4":
            pass
            #return Connect4Board()
        elif game == "Othello":
            return OthelloBoard()
        else:
            pass
            #return BattleshipBoard()

    def play_game(self, data, conn):
        data = data.split('@')
        current_game_id = data[1]
        current_move = data[2:]
        connection1 = conn
        global current_games
        for con in current_games[current_game_id].get_connections():
            if con != connection1:
                connection2 = con
        current_game_name = current_games[current_game_id].get_game()
        current_game_board = current_games[current_game_id].get_board()
        current_game_logic = GameLogic()
        if current_game_name == "Othello":
            current_game_logic = OthelloLogic()
        # elif current_game_name == "Connect4":
        #     current_game_logic = "Connect4Logic()"
        # elif current_game_name == "Battleship":
        #     current_game_logic = "BattleshipLogic()"
        try:
            current_game_logic.make_move(current_game_board, current_move)

            self.send_data_to_connection(connection1, "VALID_MOVE")

            move = ""
            for row in range(current_game_board.get_num_rows()):
                for col in range(current_game_board.get_num_columns()):
                    move += "@" + current_game_board[row][col]

            self.send_data_to_connection((connection1, "UPDATE" + move))
            self.send_data_to_connection((connection2, "UPDATE" + move))

            current_game_logic.switch_Turn(current_game_board)
            self.send_data_to_connection(connection1, "SWITCH_PLAYER")
            self.send_data_to_connection(connection2, "SWITCH_PLAYER")

            if current_game_logic.game_is_over(current_game_board):
                self.send_data_to_connection(connection1, "There is a Winner")
                self.send_data_to_connection(connection1, "There is a Winner")
            else:
                if len(current_game_logic.all_valid_moves()) != 0:
                    self.send_data_to_connection(connection1, "WAIT")
                    self.send_data_to_connection(connection2, "READY")
                else:
                    self.send_data_to_connection(connection2, "There is no move for you. Changing the turn.")

                    current_game_logic.switch_Turn(current_game_board)
                    self.send_data_to_connection(connection1, "SWITCH_PLAYER")
                    self.send_data_to_connection(connection2, "SWITCH_PLAYER")

                    self.send_data_to_connection(connection1, "READY")
                    self.send_data_to_connection(connection2, "WAIT")

        except:
            self.send_data_to_connection(conn, "INVALID_MOVE")


    def _current_players(self, str_data, conn):
        thelist = ""
        recv = str_data.split('@')
        cur = recv[1]
        for prof in all_saved_profiles:
            if cur != prof.get_username():
                thelist += prof.get_username()
                thelist += "@"
        self.send_data_to_connection(conn, thelist)

if __name__ == '__main__':

    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.ThreadingTCPServer((HOST, PORT), TCPServer)

    print("~SERVER HAS STARTED\n")

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
