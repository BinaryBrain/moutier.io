import constants
from squareState import SquareState
from direction import Direction
from trail_direction import TrailDirection


class Square:
    def __init__(self, state, owner=None):
        self.state = state
        self.owner = owner
        if self.state is SquareState.TRAIL:
            self.trail_direction = self.get_trail_direction(self.owner)
        else:
            self.trail_direction = None

    def __str__(self):
        if self.state is SquareState.NEUTRAL:
            return constants.EMPTY_SQUARE
        elif self.state is SquareState.TRAIL:
            if self.trail_direction is TrailDirection.HORIZONTAL:
                return self.owner.color + constants.TRAIL_HORIZONTAL
            elif self.trail_direction is TrailDirection.VERTICAL:
                return self.owner.color + constants.TRAIL_VERTICAL
            elif self.trail_direction is TrailDirection.LEFT_DOWN:
                return self.owner.color + constants.TRAIL_LEFT_DOWN
            elif self.trail_direction is TrailDirection.LEFT_UP:
                return self.owner.color + constants.TRAIL_LEFT_UP
            elif self.trail_direction is TrailDirection.RIGHT_DOWN:
                return self.owner.color + constants.TRAIL_RIGHT_DOWN
            elif self.trail_direction is TrailDirection.RIGHT_UP:
                return self.owner.color + constants.TRAIL_RIGHT_UP
        elif self.state is SquareState.OWNED:
            return self.owner.color + constants.FULL_BLOCK

    def get_trail_direction(self, player):
        pl = player.prev_direction is Direction.LEFT
        pr = player.prev_direction is Direction.RIGHT
        pu = player.prev_direction is Direction.UP
        pd = player.prev_direction is Direction.DOWN
        ps = player.prev_direction is Direction.STOP
        cl = player.direction is Direction.LEFT
        cr = player.direction is Direction.RIGHT
        cu = player.direction is Direction.UP
        cd = player.direction is Direction.DOWN

        if (pr and cu) or (pd and cl):
            return TrailDirection.LEFT_UP
        elif (pr and cd) or (pu and cl):
            return TrailDirection.LEFT_DOWN
        elif (pl and cu) or (pd and cr):
            return TrailDirection.RIGHT_UP
        elif (pl and cd) or (pu and cr):
            return TrailDirection.RIGHT_DOWN
        elif (pr and cl) or (pl and cr) or (pr and cr) or (pl and cl):
            return TrailDirection.HORIZONTAL
        elif (pu and cd) or (pd and cu) or (pu and cu) or (pd and cd):
            return TrailDirection.VERTICAL
        elif ps and (cl or cr):
            return TrailDirection.HORIZONTAL
        elif ps and (cu or cd):
            return TrailDirection.VERTICAL
        else:
            return TrailDirection.VERTICAL
