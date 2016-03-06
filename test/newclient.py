import socket
import sys

HOST, PORT = "localhost", 9999

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    print("::CONNECTION SUCCESS\n")

    # get player information--change this to login sequence later
    player = ""
    while player != "1" and player != "2":
        player = input("~PLAYER 1 OR PLAYER 2?: ")

    # send player information to server so it can set up
    sock.sendall(bytes(player + "\n", "utf-8"))
    resp = str(sock.recv(1024), "utf-8")
    assert resp == "CONN\n"

    if player == "2":
        sock.sendall(bytes("READY" + "\n", "utf-8"))
        wait = str(sock.recv(1024), "utf-8")
        assert wait == "READY"
        print("::SUCCESSFULLY CONNECTED TO PLAYER 1\n")
    elif player == "1":
        print("::PLEASE CONNECT PLAYER 2\n")

    # get available games from the server
    # prompt user for game selection

    # for testing purposes, we will take a string and send it to the server
    input_str = ""
    while input_str != "quit":
        input_str = input("~ENTER A MESSAGE: ")

        sock.sendall(bytes(input_str + "\n", "utf-8"))
        received = str(sock.recv(1024), "utf-8")
        if input_str == "RECV":
            print("~RESPONSE: ", received)
        else:
            assert received == "ACCEPT\n"
            #means the server accepted the transmission

finally:
    sock.close()
