import time
import socket
import selectors
import asyncio
import const

from client import Client
from client_state import ClientState
from game import Game

HOST = ""
PORT = 4848


class Server:
    def __init__(self):
        self.host = HOST
        self.port = PORT

        self.sel = selectors.DefaultSelector()

        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.clients = set()
        self.game = Game(self)

    def accept_new_connection(self, soc, mask):
        conn, address = soc.accept()
        print(f"New connection ({len(self.clients) + 1}) from: {address[0]}")
        conn.setblocking(False)
        client = Client(conn)
        self.clients.add(client)
        self.clear_screen(client)
        self.sel.register(conn, selectors.EVENT_READ, self.read_client_data)
        self.send(client, "Please enter your name: ")

    def set_name(self, client, name):
        client.name = name
        self.game.add_player(client)
        self.set_line_mode(client.conn)
        self.set_client_echo(client.conn, True)

    def read_client_data(self, conn, mask):
        data = conn.recv(1024)
        client = next(c for c in self.clients if c.conn == conn)
        if data:
            if client.state is ClientState.IN_GAME:
                self.game.handle_input(client, data)
            try:
                if client.state is ClientState.WELCOME:
                    name = data.decode("utf-8").strip()
                    self.set_name(client, name)
                    self.send(client, "Waiting for other players to join...\r\n")
            except UnicodeDecodeError:
                print("Control character received", data)
        else:
            print("Good bye!")
            self.sel.unregister(conn)
            self.clients.remove(
                next(c for c in self.clients if c.conn == conn)
            )  # remove client from list
            self.game.remove_player(client)
            conn.close()

    def send(self, client, msg):
        try:
            client.conn.send(msg.encode("utf-8"))
        except BrokenPipeError:
            pass

    def broadcast(self, clients, msg):
        for client in clients:
            self.send(client, msg)

    def clear_screen(self, client):
        self.send(client, const.CLEAR_CHARACTER)

    # Change the mode so that each character is sent without pressing ENTER
    def set_line_mode(self, conn):
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
            await asyncio.sleep(1 / 100)

    async def game_loop(self):
        while True:
            start_timer = time.time()
            self.game.loop()

            end_timer = time.time()
            await asyncio.sleep(1 / const.FPS - (end_timer - start_timer))

    def game_over(self):
        self.game = Game(self)
        for c in self.clients:
            self.game.add_player(c)


try:
    server = Server()
    # Run both loops in parallel
    loop = asyncio.get_event_loop()
    loop.create_task(server.game_loop())
    loop.create_task(server.start())
    loop.run_forever()
except KeyboardInterrupt:
    print("\rStopping server")
finally:
    server.soc.close()
