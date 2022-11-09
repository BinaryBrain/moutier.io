from squareState import SquareState
from direction import Direction

def check_collisions(game, player):
    square = game.map.squares[player.pos_x][player.pos_y]
    check_conquest(game, player, square)
    check_kill(game, player, square)
    check_new_trail(game, player, square)

def check_kill(game, player, square):
    if square.state is SquareState.TRAIL:
        if player is not square.owner or player.direction is not Direction.STOP:
            dead_player = square.owner
            dead_player.kill()
            game.map.remove_player_trail(dead_player)

def check_conquest(game, player, square):
    if player.has_trail and square.state is SquareState.OWNED and square.owner is player:
        game.map.convert_owned_zone(player)
        player.has_trail = False
        game.map.remove_player_trail(player)
        pass

def check_new_trail(game, player, square):
    if square.state is not SquareState.OWNED or square.owner is not player:
        player.has_trail = True
