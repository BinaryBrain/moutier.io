import time
import asyncio
import constants
import collisions
from map import Map
from screen import Screen
from square import Square
from trail_direction import TrailDirection
from heapq import heapify, heappush
from math import sqrt


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
                    self.map.squares[x][y] = Square(x, y, player)

    def remove_player_trail(self, player):
        # This could be optimized by storing trails as a list of squares in Player
        player.has_trail = False
        for x in range(self.map.width):
            for y in range(self.map.height):
                square = self.map.squares[x][y]
                if square.has_trail and square.trail_owner is player:
                    self.map.squares[x][y].has_trail = False
                    self.map.squares[x][y].trail_owner = None

    def convert_owned_zone(self, player):
        # TODO Convert to owned zone
        # Check if other players have at least one owned square or kill them
        shortest_owned_path = self.a_star(player.trail_start, player.trail_end, player)
        if shortest_owned_path:
            # self.basic_fill_zone(player, shortest_owned_path)
            # (x, y) = self.find_square_in_player_trail(player)
            # self.fill_zone(player, x, y)
            self.is_trail_close_path(player)
        else:
            self.is_trail_close_path(player)
            print("Zone is not closed")

    def is_trail_close_path(self, player):
        for x in range(self.map.width):
            for y in range(self.map.height):
                if (
                    self.map.squares[x][y].has_trail
                    and self.map.squares[x][y].trail_owner is player
                ):
                    self.map.squares[x][y].has_trail = False
                    self.map.squares[x][y].trail_owner = None
                    self.map.squares[x][y].is_owned = True
                    self.map.squares[x][y].owner = player

    # This method is not really optimized but should work
    def basic_fill_zone(self, player, shortest_owned_path):
        # Optimize by taking only bounding box?
        squares_to_be_filled = []
        for x in range(len(self.map.squares)):
            for y in range(len(self.map.squares[x])):
                if self.is_square_inside_player_trail(
                    player, shortest_owned_path, x, y
                ):
                    squares_to_be_filled.append(self.map.squares[x][y])
        for square in squares_to_be_filled:
            square.is_owned = True
            square.owner = player

    def is_square_inside_player_trail(self, player, shortest_owned_path, pos_x, pos_y):
        # Because of owned block, we may need to measure whether
        # the area A is smaller than B to make A the inside.
        # Otherwise, could we count the number of turns in each direction?
        # Third option: we could do an A* to find the path between
        # the entry point and the exit point to create a full loop.
        counter = self.count_intersection_from_square(
            player, shortest_owned_path, pos_x, pos_y
        )
        return counter % 2 == 1

    def count_intersection_from_square(self, player, shortest_owned_path, pos_x, pos_y):
        counter = 0
        y = pos_y
        for x in range(pos_x, self.map.width):
            square = self.map.squares[x][y]

            if square.has_trail and square.trail_owner is player:
                direction = square.trail_direction
                if (
                    direction is TrailDirection.VERTICAL
                    or direction is TrailDirection.LEFT_UP
                    or direction is TrailDirection.RIGHT_UP
                ):
                    counter += 1

            if square in shortest_owned_path:
                counter += 1
        return counter

    def a_star(self, start_square, end_square, player):
        discovered_squares = []
        heapify(discovered_squares)
        heappush(discovered_squares, (0, id(start_square), start_square))
        came_from = {}
        cost_from_start = {start_square: 0}
        cost_through_square = {start_square: self.h_func(start_square, end_square)}

        while len(discovered_squares) > 0:
            current = discovered_squares[0][2]
            if current is end_square:
                return self.reconstruct_path(came_from, end_square)

            discovered_squares.remove(discovered_squares[0])
            for neighbor in self.get_neighbors(current, player):
                tentative_cost_from_start = cost_from_start[current] + 1
                if (
                    neighbor not in cost_from_start
                    or tentative_cost_from_start < cost_from_start[neighbor]
                ):
                    came_from[neighbor] = current
                    cost_from_start[neighbor] = tentative_cost_from_start
                    cost_through_square[
                        neighbor
                    ] = tentative_cost_from_start + self.h_func(neighbor, end_square)
                    tup = (cost_from_start[neighbor], id(neighbor), neighbor)
                    if tup not in discovered_squares:
                        heappush(discovered_squares, tup)

        return None

    def h_func(self, square1, square2):
        return sqrt(
            abs(square1.pos_x - square2.pos_x) ** 2
            + abs(square1.pos_y - square2.pos_y) ** 2
        )

    def reconstruct_path(self, came_from, end_square):
        path = [end_square]
        should_continue = True
        while should_continue:
            if end_square in came_from:
                previous_square = came_from[end_square]
                path.insert(0, previous_square)
                end_square = previous_square
            else:
                should_continue = False
        return path

    def get_neighbors(self, square, player):
        # check if it's a walkable square
        neighbors = []
        x = square.pos_x
        y = square.pos_y
        if x >= 1:
            neighbors.append(self.map.squares[x - 1][y])
        if x < self.map.width - 1:
            neighbors.append(self.map.squares[x + 1][y])
        if y >= 1:
            neighbors.append(self.map.squares[x][y - 1])
        if y < self.map.height - 1:
            neighbors.append(self.map.squares[x][y + 1])

        def filter_func(s):
            return s.is_owned and s.owner is player

        neighbors = filter(filter_func, neighbors)

        return list(neighbors)

    # def find_square_in_player_trail(self, player):
    #    (x, y) = self.find_approximative_center_of_trail(player)
    #    if self.is_square_inside_player_trail(player, x, y):
    #        print("Square is in trail")
    #        return (x, y)
    #    else:
    #        print("Square is not in trail")
    #        # TODO find next intersection and cross it to be inside trail

    # def find_approximative_center_of_trail(self, player):
    #     counter = 0
    #     add_x = 0
    #     add_y = 0
    #     for y in range(self.map.height):
    #         for x in range(self.map.width):
    #             square = self.map.squares[x][y]
    #             if square.has_trail and square.trail_owner is player:
    #                 counter += 1
    #                 add_x += x
    #                 add_y += y
    #     return (round(add_x / counter), round(add_y / counter))
