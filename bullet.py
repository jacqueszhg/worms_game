import math
import time

import pygame

from game_config import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self,vx,image,worms,mouse_pos):
        super().__init__()
        self.worms = worms
        self.image = image
        self.angle = 0
        self.image = pygame.transform.scale(self.image,(15,15))
        self.rect = self.image.get_rect()
        self.rect.x = worms.rect.x + 26
        self.rect.y = worms.rect.y + 10
        self.y_origine = self.rect.y
        self.mouse_pos = mouse_pos
        self.x = worms.rect.x
        self.y = worms.rect.y
        if(self.mouse_pos < (self.worms.rect.x,self.worms.rect.y)):
            self.velocity = -vx
        else:
            self.velocity = vx
        self.temp = time.time()


    def remove(self):
        self.worms.all_bullets.remove(self)

    def move(self,window):
        #idée 1 tire que en ligne droite
        """
        self.rect.x += self.velocity
        self.rect.y = self.m * self.rect.x + self.y_origine
        self.rect.x += self.velocity
        """

        #idée 2 pas réussie à mettre en oeuvre
        """
        vx = 0
        vy = 0
        ax = 0
        ay = -GameConfig.GRAVITY
        dt = 1

        vx += ax * dt
        vy += ay * dt
        self.rect.x += vx * dt
        self.rect.y += vy * dt
        print(self.rect.x,self.rect.y)
        """

        #idée 3 equation cartésienne foncitonne mais quelque soucis
        """
        self.rect.x += self.velocity

        pointA = [self.x,self.y]
        pointB = self.mouse_pos
        vecteurAB = [(pointB[0] - pointA[0]),(pointB[1]-pointA[1])]
        b = -vecteurAB[0]
        if(b ==0):
            b=1
        a =vecteurAB[1]
        c = -(a*pointB[0]) - (b*pointB[1])
        self.rect.y = (-(a * self.rect.x)-c)/b
        """

        #mélange idée 3 et 2 fonction mais queleque soucis
        #gere la vitesse
        dt = 1.5

        #self.rect.x += self.velocity
        self.rect.x += self.velocity * dt

        pointA = [self.x,self.y]
        pointB = self.mouse_pos
        vecteurAB = [(pointB[0] - pointA[0]),(pointB[1]-pointA[1])]
        b = -vecteurAB[0]
        if(b ==0):
            b=1
        a =vecteurAB[1]
        c = -(a*pointB[0]) - (b*pointB[1])
        self.rect.y = (-(a * self.rect.x)-c)/b
        #self.rect.y -= 12 selon une puissance donnée on fait baisé la balle

        pygame.draw.line(window,(255,0,0),(self.worms.rect.x+26,self.worms.rect.y +10),self.mouse_pos)

        #vérifier si la bullet est hors écran
        #ajouter une condition que la bullet disparait qu'on un certain temps est passé
        if self.rect.x > 1000 or self.rect.x < 0 or self.rect.y<0 or self.rect.y > 650 or (time.time()-self.temp>2) :
            #supprimer la bullet
            self.remove()