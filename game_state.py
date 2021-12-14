import random

from map import *
from worms import *


class GameState:
    def __init__(self):
        self.worms = Worms(20)
        self.map = Map

    def draw(self,window):
        window.blit(GameConfig.BACKGROUND_IMG,(0,0))
        self.worms.draw(window)
        self.map.draw(window)

    def advance_state(self,next_move):
        self.worms.advance_state(next_move)