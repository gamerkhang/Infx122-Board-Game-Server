
MAX_MESSAGE_LENGTH = 1024


class RemoteClient:

    """Wraps a remote client socket."""

    def __init__(self, conn, _address):
        self.connection = conn
        self.address = _address

    def get_connection(self):
        return self.connection

    def get_address(self):
        return self.address



