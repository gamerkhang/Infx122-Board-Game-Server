
MAX_MESSAGE_LENGTH = 1024


class RemoteClient:

    """Wraps a remote client socket."""

    def __init__(self, name, conn, _address):
        #self.name = name
        self.connection = conn
        self.address = _address


