from socket import *
from threading import Thread
from RemoteClient import RemoteClient


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
        if data:
            print("Server - Received Message", data.decode("utf-8"))
        return data.decode("utf-8")

    @staticmethod
    def broadcast_data(conn, data):
        conn.sendall(data.encode())

    def client_handler(self):
        conn, _address = self.host_socket.accept()
        self.remote_clients += [RemoteClient(conn, _address)]

        print(_address, "is Connected")
        print(conn, "conn is Connected")

        while 1:
            data = self.receive_data(conn)
            if not data:
                break
            for index in range(len(self.remote_clients)):
                try:
                    if data == "quit":
                        if conn == self.remote_clients[index].get_connection():
                            del self.remote_clients[index]
                            continue
                        else:
                            self.broadcast_data(self.remote_clients[index].get_connection(), data)
                    else:
                        self.broadcast_data(self.remote_clients[index].get_connection(), data)
                except:
                    del self.remote_clients[index]
                    continue
                    

if __name__ == '__main__':

    host = Host()
