import random

from worms import *


class GameState:
    def __init__(self):
        self.worms = Worms(20)

    def draw(self,window):
        window.blit(GameConfig.BACKGROUND_IMG,(0,0))
        window.blit(GameConfig.BRICK_IMG,(0,500))
        window.blit(GameConfig.BRICK_IMG,(100,500))
        window.blit(GameConfig.BRICK_IMG,(200,450))
        window.blit(GameConfig.BRICK_IMG,(250,350))
        window.blit(GameConfig.BRICK_IMG,(350,375))
        window.blit(GameConfig.BRICK_IMG,(375,475))
        window.blit(GameConfig.BRICK_IMG,(385,575))
        window.blit(GameConfig.BRICK_IMG,(575,450))

        window.blit(GameConfig.SURPRISE_IMG,(700,100))
        self.worms.draw(window)

    def advance_state(self,next_move):
        self.worms.advance_state(next_move)