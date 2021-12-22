import time

import pygame
from game_config import *

class Worms(pygame.sprite.Sprite):
    LEFT = -1
    RIGHT = 1
    NONE = 0


    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,
                                GameConfig.Y_PLATEFORM - GameConfig.WORMS_H,
                                GameConfig.WORMS_W,
                                GameConfig.WORMS_H)
        self.image = GameConfig.STANDING_IMG_DROIT
        self.vx = 0
        self.vy = 0
        self.temp = 0

    def draw(self,window):
        window.blit(self.image, self.rect)

    def advance_state(self, next_move,window):
        # Acceleration
        fx = 0
        fy = 0
        if next_move.left:
            clock = time.time()
            if(clock-self.temp < 0.2):
                fx = GameConfig.FORCE_LEFT
                self.image = GameConfig.STANDING_IMG_GAUCHE
            elif(clock-self.temp < 0.4):
                fx = GameConfig.FORCE_LEFT
                self.image = GameConfig.WALK_LEFT_IMG1
            elif(clock-self.temp < 0.6):
                fx = GameConfig.FORCE_LEFT
                self.image = GameConfig.WALK_LEFT_IMG2
            else:
                self.temp = time.time()
                self.image = GameConfig.STANDING_IMG_GAUCHE
                GameConfig.WORMS_DROIT = False
        elif next_move.right:
            clock = time.time()
            if(clock-self.temp < 0.2):
                fx = GameConfig.FORCE_RIGHT
                self.image = GameConfig.STANDING_IMG_DROIT
            elif(clock-self.temp < 0.4):
                fx = GameConfig.FORCE_RIGHT
                self.image = GameConfig.WALK_RIGHT_IMG1
            elif(clock-self.temp < 0.6):
                fx = GameConfig.FORCE_RIGHT
                self.image = GameConfig.WALK_RIGHT_IMG2
            else:
                self.temp = time.time()
                self.image = GameConfig.STANDING_IMG_DROIT
            GameConfig.WORMS_DROIT = True

        else:
            if(GameConfig.WORMS_DROIT):
                self.image = GameConfig.STANDING_IMG_DROIT
            else:
                self.image = GameConfig.STANDING_IMG_GAUCHE

        if next_move.jump:
                fy = GameConfig.FORCE_JUMP
                if(GameConfig.WORMS_DROIT):
                    self.image = GameConfig.WALK_JUMP_IMG_DROIT
                else:
                    self.image = GameConfig.WALK_JUMP_IMG_GAUCHE


        # Vitesse
        self.vx = fx * GameConfig.DT
        if self.on_ground():
            self.vy = fy * GameConfig.DT
        else:
            self.vy = self.vy + GameConfig.GRAVITY * GameConfig.DT

        # Position
        self.rect = self.rect.move(self.vx * GameConfig.DT, self.vy * GameConfig.DT)

        x = self.rect.left
        vx_min = -x / GameConfig.DT
        vx_max = (GameConfig.WINDOW_W - GameConfig.WORMS_W - x) / GameConfig.DT
        self.vx = min(self.vx, vx_max)

        y = self.rect.top
        vy_max = (GameConfig.Y_PLATEFORM - GameConfig.WORMS_H - y) / GameConfig.DT
        self.vy = min(self.vy, vy_max)
        self.vx = max(self.vx, vx_min)

        self.rect = self.rect.move(self.vx * GameConfig.DT, self.vy * GameConfig.DT)

    def on_ground(self):
        if(self.rect.bottom == GameConfig.Y_PLATEFORM):
            return True
        return False