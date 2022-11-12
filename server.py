import socket
import selectors
import asyncio
import constants

from player import Player
from game import Game
from direction import Direction
from color import Color, usable_colors

HOST = ""
PORT = 4848


class Server:
    def __init__(self):
        self.host = HOST
        self.port = PORT

        self.sel = selectors.DefaultSelector()

        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.players = set()
        self.game = Game(self)

    def accept_new_connection(self, soc, mask):
        conn, address = soc.accept()
        print(f"New connection ({len(self.players) + 1}) from: {address[0]}")
        conn.setblocking(False)
        player = Player(
            conn,
            "BinaryBrain",
            Color[usable_colors[len(self.players) % len(usable_colors)]],
        )
        self.players.add(player)
        self.set_mode(conn)
        self.set_client_echo(conn, True)
        self.clear_screen(conn)
        self.sel.register(conn, selectors.EVENT_READ, self.read_client_data)

        if len(self.players) >= 1:
            self.game.initialize_game()

    def read_client_data(self, conn, mask):
        data = conn.recv(1024)
        player = next(p for p in self.players if p.conn == conn)
        if data:
            if data == constants.KEY_UP and player.direction != Direction.DOWN:
                player.define_direction(Direction.UP)
            if data == constants.KEY_DOWN and player.direction != Direction.UP:
                player.define_direction(Direction.DOWN)
            if data == constants.KEY_LEFT and player.direction != Direction.RIGHT:
                player.define_direction(Direction.LEFT)
            if data == constants.KEY_RIGHT and player.direction != Direction.LEFT:
                player.define_direction(Direction.RIGHT)

            try:
                text = data.decode("utf-8").strip()
                # else:
                # broadcast(str + '\r\n')
            except UnicodeDecodeError:
                print("Control character received", data)
        else:
            print("Good bye!")
            self.sel.unregister(conn)
            self.players.remove(
                next(p for p in self.players if p.conn == conn)
            )  # remove player from list
            conn.close()

    def send(self, conn, msg):
        try:
            conn.send(msg.encode("utf-8"))
        except BrokenPipeError:
            pass

    def broadcast(self, msg):
        for player in self.players:
            self.send(player.conn, msg)

    def broadcast_clear_screen(self):
        for player in self.players:
            self.clear_screen(player.conn)

    def clear_screen(self, conn):
        self.send(conn, constants.CLEAR_CHARACTER)

    # Change the mode so that each character is sent without pressing ENTER
    def set_mode(self, conn):
        conn.send(b"\xff\xfd\x22")  # IAC DO LINEMODE
        conn.send(b"\xff\xfa\x22\x01\x00\xff\xf0")  # IAC SB LINEMODE MODE 0 IAC SE

    def set_client_echo(self, conn, bool):
        if bool:
            conn.send(b"\xff\xfb\x01")  # IAC WILL ECHO
        else:
            conn.send(b"\xff\xfc\x01")  # IAC WILL NOT ECHO

    async def start(self):
        self.soc.bind((self.host, self.port))
        self.soc.listen()
        self.soc.setblocking(False)

        print("Server listening...")
        self.sel.register(self.soc, selectors.EVENT_READ, self.accept_new_connection)

        while True:
            events = self.sel.select(0)  # set to 0 for non-blocking loop
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
            await asyncio.sleep(1 / 5)  # TODO sync on FPS or something


try:
    server = Server()
    # Run both loops in parallel
    loop = asyncio.get_event_loop()
    loop.create_task(server.game.loop())
    loop.create_task(server.start())
    loop.run_forever()
except KeyboardInterrupt:
    print("\rStopping server")
finally:
    server.soc.close()
