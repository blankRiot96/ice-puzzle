from enum import Enum, auto


class State(Enum):
    GAME = auto()
    MAIN_MENU = auto()
    LEVEL_PICKER = auto()
    VICTORY = auto()
