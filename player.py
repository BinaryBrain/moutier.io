class Player:
    def __init__(self, conn, name, symbol):
        self.conn = conn
        self.name = name
        self.symbol = symbol
        self.posX = 0
        self.posY = 0

    def __str__(self):
        return f'{self.name} [{self.symbol}]'
