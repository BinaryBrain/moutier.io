FPS = 5
MIN_PLAYERS_TO_START = 1

CLEAR_CHARACTER = "\033[2J\r"
CURSOR_PREVIOUS_LINE = "\033[F"
KEY_UP = b"\x1b[A"
KEY_DOWN = b"\x1b[B"
KEY_RIGHT = b"\x1b[C"
KEY_LEFT = b"\x1b[D"

FULL_BLOCK = "\u2588"

PLAYER_UP = "\u25B2"  # ▲
PLAYER_DOWN = "\u25BC"  # ▼
PLAYER_LEFT = "\u25C0"  # ◀
PLAYER_RIGHT = "\u25B6"  # ▶
PLAYER_STOP = "\u25C6"  # ◆

TRAIL_HORIZONTAL = "\u2501"  # ━
TRAIL_VERTICAL = "\u2503"  # ┃
TRAIL_LEFT_DOWN = "\u2513"  # ┓
TRAIL_LEFT_UP = "\u251B"  # ┛
TRAIL_RIGHT_DOWN = "\u250F"  # ┏
TRAIL_RIGHT_UP = "\u2517"  # ┗

FRAME_PART = {}
# Up, Down, Left, Right
FRAME_PART[0b0011] = "\u2550"  # ═
FRAME_PART[0b1100] = "\u2551"  # ║
FRAME_PART[0b0101] = "\u2554"  # ╔
FRAME_PART[0b0110] = "\u2557"  # ╗
FRAME_PART[0b1001] = "\u255A"  # ╚
FRAME_PART[0b1010] = "\u255D"  # ╝
FRAME_PART[0b1110] = "\u2563"  # ╣
FRAME_PART[0b1101] = "\u2560"  # ╠
FRAME_PART[0b0111] = "\u2566"  # ╦
FRAME_PART[0b1011] = "\u2569"  # ╩
FRAME_PART[0b1101] = "\u2560"  # ╠
FRAME_PART[0b1110] = "\u2563"  # ╣
FRAME_PART[0b1111] = "\u256C"  # ╬

EMPTY_SQUARE = " "

SPAWN_MARGINS = 2
