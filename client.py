from client_state import ClientState


class Client:
    def __init__(self, conn):
        self.conn = conn
        self.name = None
        self.state = ClientState.WELCOME
