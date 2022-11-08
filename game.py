import time
import asyncio
from map import Map
from screen import Screen

FPS = 5


class Game:
    def __init__(self, server):
        self.fps = FPS
        self.map = Map(40, 40)
        self.server = server
        self.screen = Screen(40, 40)
        self.t = 0

    async def loop(self):
        while True:
            start_timer = time.time()
            for player in self.server.players:
                player.move(self.map)
                self.map.update(player)
                player.define_direction(player.direction)

            self.draw()
            end_timer = time.time()
            await asyncio.sleep(1 / FPS - (end_timer - start_timer))
            self.t = self.t + 1

    def draw(self):
        self.screen.draw(self.map.to_lines(), 0, 0)
        for player in self.server.players:
            self.screen.draw([[str(player)]], player.pos_x, player.pos_y)
        self.sendScreen()

    def sendScreen(self):
        self.server.broadcast(self.screen.getCurrentScreen())
