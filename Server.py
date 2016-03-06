from socket import *
from threading import Thread
from RemoteClient import RemoteClient
from CurrentGames import CurrentGames
from Profile import Profile

conns = []

class Host:

    def __init__(self, address=('127.0.0.1', 8000)):
        self.host_socket = socket(AF_INET, SOCK_STREAM)
        self.host_socket.bind(address)
        self.host_socket.listen(100)
        self.all_saved_profiles = []
        self.wait_list = dict()
        self.current_games = dict()
        self.remote_clients = []

        # *********************************
        print("Server is running......")

    def receive_data(self, conn):
        data = conn.recv(1024)
        print("Server - Received Message", data.decode("utf-8"))
        return data.decode("utf-8")

    def send_data(self, conn, data):
        print("Server - Send Message", data)
        conn.sendall(data.encode())

    @staticmethod
    def broadcast_data(conn, data):
        conn.sendall(data.encode())

    def client_handler(self):
        conn, _address = self.host_socket.accept()
        data = self.receive_data(conn)

        if "LOGIN" in data:
            self._login_handler(conn, data)
        elif "NEW_USER" in data:
            self._new_user_handler(conn, _address, data)
        elif "NEW_GAME" in data:
            self._new_game(conn, _address, data)
        elif "AUTO" in data:
            self._auto_player(conn, _address, data)
        else:
            print("from here")

            for key in self.current_games.keys():
                for con in self.current_games[key].get_connections():
                    print(con)
                    self.send_data(con, data)


                # for index in range(len(self.remote_clients)):
                #     try:
                #         if data == "quit":
                #             if conn == self.remote_clients[index].get_connection():
                #                 del self.remote_clients[index]
                #                 continue
                #             else:
                #                 self.send_data(self.remote_clients[index].get_connection(), data)
                #         else:
                #             self.send_data(self.remote_clients[index].get_connection(), data)
                #     except:
                #         del self.remote_clients[index]
                #         continue

    def _login_handler(self, conn, data):

        _data = data.split('@')
        username = _data[1]
        username_exist = False
        for _username in self.all_saved_profiles:
            if username == _username.get_username():
                username_exist = True
                break

        if username_exist:
            self.send_data(conn, "INVALID_USERNAME")
        else:
            self.all_saved_profiles += [Profile(username)]
            self.send_data(conn, "VALID_USERNAME")

    def _new_user_handler(self, conn, address, data):

        _data = data.split('@')
        username = _data[1]
        username_exist = False
        for _username in self.all_saved_profiles:
            if username == _username.get_username():
                username_exist = True
                break

        if username_exist:
            self.send_data(conn, "USERNAME_EXIST")
        else:
            self.all_saved_profiles += [Profile(username)]
            self.wait_list[_data[1]] = ("GAME_NOT_SET", RemoteClient(conn, address))
            self.send_data(conn, "VALID_USERNAME")

    def _new_game(self, conn, address, data):
        _data = data.split('@')
        self.wait_list[_data[1]] = (_data[2], RemoteClient(conn, address))
        print(self.wait_list)
        self.send_data(conn, "GAME_SET")

    def _auto_player(self, conn, address, data):
        _data = data.split('@')
        first_player = _data[1]
        game_to_play = self.wait_list[first_player][0]
        print("name of the game to play in auto mode", game_to_play)
        second_player = ''

        for player in self.wait_list.keys():
            if player != first_player and self.wait_list[player][0] == game_to_play:
                second_player = player
                break

        if second_player != "":
            self.current_games[first_player + "_" + second_player] = CurrentGames(first_player, second_player, RemoteClient(conn, address), self.wait_list[second_player][1])
            del self.wait_list[first_player]
            del self.wait_list[second_player]
            print(self.wait_list)
            print(self.current_games)

            for con in self.current_games[first_player + "_" + second_player].get_connections():
                print(con)
                self.send_data(con, "READY")

        else:
            self.wait_list[first_player] = (game_to_play, RemoteClient(conn, address))
            self.send_data(conn, "WAIT")


if __name__ == '__main__':

    host = Host()
    for i in range(100):
        Thread(target=host.client_handler).start()
