from socket import *
from threading import Thread
# from RemoteClient import RemoteClient
from Profile import Profile


class Host:

    def __init__(self, address=('localhost', 8000)):
        self.host_socket = socket(AF_INET, SOCK_STREAM)
        self.host_socket.bind(address)
        self.host_socket.listen(5)
        self.all_saved_profiles = []
        self.remote_clients = []

        # *********************************
        print("Server is running......")

    def receive_data(self,conn):
        data = conn.recv(1024)
        if data:
            print("Server - Received Message", data.decode("utf-8"))
        return data.decode("utf-8")

    def send_data(self, conn, data):
        conn.sendall(data.encode())

    @staticmethod
    def broadcast_data(conn, data):
        conn.sendall(data.encode())

    def client_handler(self):
        conn, _address = self.host_socket.accept()

        data = self.receive_data(conn)
        print(data, "hereeee ")
        if "LOGIN" in data:
            self._login_handler(conn, data)
        elif "NEW_USER" in data:
            self._new_user_handler(conn, data)

        #
        # print(_address, "is Connected")
        # print(conn, "conn is Connected")
        #
        # while 1:
        #     data = self.receive_data(conn)
        #     if not data:
        #         break
        #
        #     for index in range(len(self.remote_clients)):
        #         try:
        #             if data == "quit":
        #                 if conn == self.remote_clients[index].get_connection():
        #                     del self.remote_clients[index]
        #                     continue
        #                 else:
        #                     self.send_data(self.remote_clients[index].get_connection(), data)
        #             else:
        #                 self.send_data(self.remote_clients[index].get_connection(), data)
        #         except:
        #             del self.remote_clients[index]
        #             continue

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

    def _new_user_handler(self, conn, data):

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
            self.send_data(conn, "VALID_USERNAME")

if __name__ == '__main__':

    host = Host()
    for i in range(5):
        Thread(target=host.client_handler).start()
