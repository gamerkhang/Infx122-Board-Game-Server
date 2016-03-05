
class CurrentGames:

    def __init__(self, player1, player2, remote_client1, remote_client2):
        self.player1 = player1
        self.player2 = player2
        self.remote_client1 = remote_client1
        self.remote_client2 = remote_client2

    def get_player1(self):
        return self.player1

    def get_player2(self):
        return self.player2

    def get_remote_client1(self):
        return self.remote_client1

    def get_remote_client2(self):
        return self.remote_client2

    def get_connections(self):
        return [self.remote_client1.get_connection(), self.remote_client2.get_connection()]

