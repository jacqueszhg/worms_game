import pygame.sprite
from game_config import *
from block import *

class Worms:
        def __init__(self, x):
            pygame.sprite.Sprite.__init__(self)
            self.rect = pygame.Rect(x, GameConfig.Y_PLATEFORM - GameConfig.WORMS_H,
                                    GameConfig.WORMS_W,
                                    GameConfig.WORMS_H)
            self.image = GameConfig.STATIC_LEFT_IMG
            #self.rect = self.image.get_rect(x=x,y=y)
            self.vx = 0
            self.vy = 0

        def draw(self, window):
            window.blit(self.image, self.rect)

        def advance_state(self, next_move):
            # Acceleration
            fx = 0
            fy = 0
            if next_move.left:
                fx = GameConfig.FORCE_LEFT
            elif next_move.right:
                fx = GameConfig.FORCE_RIGHT
            if next_move.jump:
                fy = GameConfig.FORCE_JUMP
            # Vitesse
            self.vx = fx * GameConfig.DT

            indexBlock = 0
            for i in range(0,len(GameConfig.LISTE_BLOCK)):
                block = GameConfig.LISTE_BLOCK[i]
                if(self.rect.left > block.getRect().left and self.rect.right < block.getRect().right):
                    if(self.rect.bottom == block.getRect().top):
                        indexBlock = i

            print(indexBlock)
            if self.on_ground(indexBlock):
                self.vy = fy * GameConfig.DT
            else:
                self.vy = self.vy + GameConfig.GRAVITY * GameConfig.DT

            # Position
            x = self.rect.left
            vx_min = -x / GameConfig.DT
            vx_max = (GameConfig.WINDOW_W - GameConfig.WORMS_W - x) / GameConfig.DT
            self.vx = min(self.vx, vx_max)
            self.vx = max(self.vx, vx_min)

            y = self.rect.top
            #vy_max = (GameConfig.Y_PLATEFORM - GameConfig.WORMS_H - y) / GameConfig.DT
            vy_max = (GameConfig.LISTE_BLOCK[indexBlock].getRect().top - GameConfig.WORMS_H - y) / GameConfig.DT
            self.vy = min(self.vy, vy_max)

            self.rect = self.rect.move(self.vx * GameConfig.DT, self.vy * GameConfig.DT)


        def on_ground(self,indexBlock):
            #if (self.rect.bottom == GameConfig.Y_PLATEFORM):
            if(self.rect.bottom == GameConfig.LISTE_BLOCK[indexBlock].getRect().top):
                return True
            return False