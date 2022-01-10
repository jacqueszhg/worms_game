from bullet import *
from game_config import *
from worms import *

class Round:
    def next_round():
        if GameConfig.PLAY < len(GameConfig.LIST_WORMS) - 1:
            GameConfig.PLAY = GameConfig.PLAY + 1
        else:
            GameConfig.PLAY = 0
        while GameConfig.LIST_WORMS[GameConfig.PLAY].is_dead(GameConfig.PLAY):
            if GameConfig.PLAY < len(GameConfig.LIST_WORMS) - 1:
                GameConfig.PLAY = GameConfig.PLAY + 1
            else:
                GameConfig.PLAY = 0

Round.next_round = staticmethod(Round.next_round)