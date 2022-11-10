import time
import asyncio
import constants
import collisions
from map import Map
from screen import Screen
from square import Square


class Game:
    def __init__(self, server):
        self.fps = constants.FPS
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
                collisions.check_collisions(self, player)

            self.draw()
            end_timer = time.time()
            await asyncio.sleep(1 / constants.FPS - (end_timer - start_timer))
            self.t = self.t + 1

    def draw(self):
        self.screen.draw(self.map.to_lines(), 0, 0)
        for player in self.server.players:
            self.screen.draw([[str(player)]], player.pos_x, player.pos_y)
        self.sendScreen()

    def sendScreen(self):
        self.server.broadcast(self.screen.getCurrentScreen())

    def initialize_game(self):
        for i, player in enumerate(self.server.players):
            player.pos_x = 1
            player.pos_y = 1
            for x in range(3):
                for y in range(3):
                    self.map.squares[x][y] = Square(player)
