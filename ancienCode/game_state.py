import random

from map import *
from worms import *


class GameState:
    def __init__(self):
        self.map = Map()
        self.worms = Worms(20)

    def draw(self,window):
        window.blit(GameConfig.BACKGROUND_IMG,(0,0))
        self.map.draw(window)
        self.worms.draw(window)


    def advance_state(self,next_move):
        self.worms.advance_state(next_move)