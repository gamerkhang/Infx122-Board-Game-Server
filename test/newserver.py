import socketserver
import threading

both_conn = 0
to_send = ""

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        global both_conn
        global to_send
        # self.request is the TCP socket connected to the client
        while True:
            self.data = self.request.recv(1024)
            if self.data == '':
                break

            self.data = self.data.strip()
            # print("{} wrote:".format(self.client_address[0]))
            str_data = (self.data).decode("utf-8")
            print("~recv: ", str_data)

            if str_data == "1" or str_data == "2":
                both_conn += 1
                print("~player", str_data, "is connected")
                self.request.sendall(bytes("CONN" + "\n", "utf-8"))

            elif str_data == "READY":
                if both_conn == 2:
                    self.request.sendall(self.data)
                else:
                    self.request.sendall(bytes("NO" + "\n", "utf-8"))
            elif str_data == "RECV":
                self.request.sendall(bytes(to_send + "\n", "utf-8"))
            else:
                to_send = str_data
                self.request.sendall(bytes("ACCEPT" + "\n", "utf-8"))

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)

    print("~SERVER HAS STARTED\n")

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
