import pygame

from game_config import *


class Block:
    def __init__(self,x,top):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,top,
                                GameConfig.BLOCK_W,
                                GameConfig.BLOCK_H)
    def getRect(self):
        return self.rect