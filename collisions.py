from direction import Direction


def check_collisions(game, player):
    square = game.map.squares[player.pos_x][player.pos_y]
    check_conquest(game, player, square)
    check_kill(game, player, square)
    check_new_trail(game, player, square)


def check_kill(game, player, square):
    if square.has_trail:
        if player is not square.trail_owner or player.direction is not Direction.STOP:
            dead_player = square.trail_owner
            dead_player.kill()
            game.map.remove_player_trail(dead_player)


def check_conquest(game, player, square):
    if player.has_trail and square.is_owned and square.owner is player:
        player.trail_end = square
        game.map.convert_owned_zone(player)
        game.map.remove_player_trail(player)
        pass


def check_new_trail(game, player, square):
    if not square.is_owned or square.owner is not player:
        if not player.has_trail:
            player.has_trail = True
            player.trail_start = game.map.squares[player.prev_pos_x][player.prev_pos_y]
