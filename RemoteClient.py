
MAX_MESSAGE_LENGTH = 1024


class RemoteClient:

    """Wraps a remote client socket."""

    def __init__(self, conn):
        self.connection = conn

    def get_connection(self):
        return self.connection

    # def get_address(self):
    #     return self.address



