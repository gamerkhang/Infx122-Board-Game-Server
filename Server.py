from socket import *
from threading import Thread
import RemoteClient


class Host:

    def __init__(self, address=('localhost', 8000)):
        self.host_socket = socket(AF_INET, SOCK_STREAM)
        self.host_socket.bind(address)
        self.host_socket.listen(5)
        self.remote_clients = []

        for i in range(5):
            Thread(target=self.client_handler).start()

        # *********************************
        print("Server is running......")

    @staticmethod
    def receive_data(conn):
        data = conn.recv(1024)
        print("Server - Received Message", repr(data))
        return data

    @staticmethod
    def broadcast_data(conn, data):
        conn.sendall(data)

    def client_handler(self):

        (conn, _address) =  self.host_socket.accept()
        self.remote_clients += [RemoteClient(conn, _address)]

        print(_address, "is Connected")
        print(conn, "conn is Connected")

        while 1:
            data = self.receive_data(conn)
            if not data:
                break
            print(self.remote_clients)
            for con in self.remote_clients:
                try:
                    if data == "quit":
                        if conn == con:
                            del con
                        else:
                            pass
                        self.broadcast_data(con, data)
                    else:
                        self.broadcast_data(con, data)
                except:
                    continue

if __name__ == '__main__':

    host = Host()
