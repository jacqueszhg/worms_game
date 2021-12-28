import math

import pygame

from game_config import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self,vx,image,worms,mouse_pos):
        super().__init__()
        self.velocity = vx
        self.worms = worms
        self.image = image
        self.angle = 0
        self.image = pygame.transform.scale(self.image,(15,15))
        self.origine_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = worms.rect.x + 26
        self.rect.y = worms.rect.y +10
        self.mouse_position = mouse_pos

        self.v0 = 0.0
        self.alpha = 0.0

    def remove(self):
        self.worms.all_bullets.remove(self)

    def move(self,window):
        self.rect.x += self.velocity
        pygame.draw.line(window,(255,0,0),self.worms.rect.topright,(self.mouse_position))

        #vérifier si la bullet est hors écran
        if self.rect.x > 1000 or self.rect.x < 0 or self.rect.y<0 or self.rect.y > 650:
            #supprimer la bullet
            self.remove()