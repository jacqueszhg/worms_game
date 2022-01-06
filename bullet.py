import math
import random
import time

import pygame
import game_config
from game_config import *

"""
import numpy as N
import scipy.integrate as SI
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


class Bullet(pygame.sprite.Sprite):
    def __init__(self,velocity,image,worms,mouse_pos,type,angle,vent):
        super().__init__()
        self.worms = worms
        self.image = image
        self.image = pygame.transform.scale(self.image,(15,15))
        self.rect = self.image.get_rect()
        self.rect.x = worms.rect.topright[0]
        self.rect.y = worms.rect.topright[1]
        self.y_origine = self.rect.y
        self.mouse_pos = mouse_pos
        #vitesse initiale
        if(self.mouse_pos < (self.worms.rect.x,self.worms.rect.y)):
            self.velocity = -velocity
            self.rect.x = worms.rect.topleft[0] - 15
            self.rect.y = worms.rect.topleft[1]
        else:
            self.velocity = velocity

        self.x0 = self.rect.x
        self.y0 = self.rect.y
        #self.vx = velocity * np.cos(angle)
        #self.vy = velocity * np.sin(angle)
        self.vx = angle[0]
        self.vy = angle[1]

        self.temp = time.time()
        self.type = type
        self.vent = vent
        self.toucherMur = False

    def remove(self):
        self.worms.all_bullets.remove(self)

    def draw(self,window):
        window.blit(self.image,self.rect)

    def touch(self):
        for i in range(len(GameConfig.LIST_WORMS)):
            if self.rect.colliderect(GameConfig.LIST_WORMS[i]):
                return True
        return False

    def move(self,window):
        if(self.type == "carabine"):
            self.moveCarabine()
        if self.type =="rocket":
            self.moveRocket()
        if self.type == "grenade":
            self.moveGrenade()


        #vérifier si la bullet est hors écran
        #ajouter une condition que la bullet disparait qu'on un certain temps est passé
        if self.rect.x > GameConfig.WINDOW_W or self.rect.x < 0 or self.rect.y<0 or self.rect.y > 650 or time.time() - self.temp > 5 or self.toucherMur == True:
            #supprimer la bullet
            self.remove()
            blockDetruit = []
            if(self.type == "grenade" or self.type == "rocket"):
                circle = pygame.draw.circle(window,(255,255,255),self.rect.center,40)
                for i in range(len(GameConfig.BLOCKS)):
                    if pygame.Rect.colliderect(circle, GameConfig.BLOCKS[i]):
                        blockDetruit.append(GameConfig.BLOCKS[i])

            for i in blockDetruit:
                GameConfig.BLOCKS.remove(i)

        #vérifier si la bullet touche un autre joueur
        if self.touch():
            self.remove()
            for i in range(len(GameConfig.LIST_WORMS)):
                if self.rect.colliderect(GameConfig.LIST_WORMS[i]):
                    GameConfig.LIST_WORMS[i].life = GameConfig.LIST_WORMS[i].life - 100
                    if not GameConfig.LIST_WORMS[i].is_death(i):
                        GameConfig.PLAY = i





    def moveCarabine(self):
        # idée 1 tire que en ligne droite
        """
        self.rect.x += self.velocity
        self.rect.y = self.m * self.rect.x + self.y_origine
        self.rect.x += self.velocity
        """

        # idée 2 pas réussie à mettre en oeuvre
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

        # idée 3 equation cartésienne foncitonne mais quelque soucis
        """
        self.rect.x += self.velocity

        pointA = [self.x0,self.y0]
        pointB = self.mouse_pos
        vecteurAB = [(pointB[0] - pointA[0]),(pointB[1]-pointA[1])]
        b = -vecteurAB[0]
        if(b ==0):
            b=1
        a =vecteurAB[1]
        c = -(a*pointB[0]) - (b*pointB[1])
        self.rect.y = (-(a * self.rect.x)-c)/b
        """

        # mélange idée 3 et 2 fonction mais queleque soucis
        self.rect.x += self.velocity

        pointA = [self.x0, self.y0]
        pointB = self.mouse_pos
        vecteurAB = [(pointB[0] - pointA[0]), (pointB[1] - pointA[1])]
        b = -vecteurAB[0]
        if (b == 0):
            b = 1
        a = vecteurAB[1]
        c = -(a * pointB[0]) - (b * pointB[1])
        self.rect.y = (-(a * self.rect.x) - c) / b
        # self.rect.y -= 12 selon une puissance donnée on fait baisé la balle


    def moveGrenade(self):
        dt = 0.3
        t = self.rect.x + dt
        vxn = self.vx
        vyn = self.vy
        xn = self.rect.x
        yn = self.rect.y

        #vx,vy,x,y = self.F_Gravite(t,vxn,vyn,xn,yn)
        #vx,vy,x,y = self.F_Gravite_Friction(t,vxn,vyn,xn,yn)
        vx,vy,x,y = self.F_Gravite_Friction_Vent(t,vxn,vyn,xn,yn)
        vx = dt * vx
        vy = dt * vy
        x = dt * x
        y = dt * y

        self.vx = vxn + vx
        self.vy = vyn + vy
        self.rect.x = xn + x
        self.rect.y = yn + y
        collision = False
        for i in range(len(GameConfig.BLOCKS)):
            if self.rect.colliderect(GameConfig.BLOCKS[i]) and collision == False:
                self.chocElastique()
                collision = True
        for  i in range(len(GameConfig.MUR)):
            if self.rect.colliderect(GameConfig.MUR[i])and collision == False:
                self.chocElastique()
                collision = True

    #https://fr.wikipedia.org/wiki/Choc_élastique
    def chocElastique(self):
         newVx = ((GameConfig.MASSE_GRENADE - GameConfig.MASSE_MUR)/(GameConfig.MASSE_GRENADE + GameConfig.MASSE_MUR)) * self.vx
         newVy = ((GameConfig.MASSE_GRENADE - GameConfig.MASSE_MUR)/(GameConfig.MASSE_GRENADE + GameConfig.MASSE_MUR)) * self.vy
         self.vx = newVx
         self.vy = newVy

    def moveRocket(self):
        dt = 0.3
        t = self.rect.x + dt
        vxn = self.vx
        vyn = self.vy
        xn = self.rect.x
        yn = self.rect.y

        #vx,vy,x,y = self.F_Gravite(t,vxn,vyn,xn,yn)
        #vx,vy,x,y = self.F_Gravite_Friction(t,vxn,vyn,xn,yn)
        vx,vy,x,y = self.F_Gravite_Friction_Vent(t,vxn,vyn,xn,yn)
        vx = dt * vx
        vy = dt * vy
        x = dt * x
        y = dt * y

        self.vx = vxn + vx
        self.vy = vyn + vy
        self.rect.x = xn + x
        self.rect.y = yn + y


        for i in range(len(GameConfig.BLOCKS)):
            if self.rect.colliderect(GameConfig.BLOCKS[i]) and self.toucherMur == False:
                self.toucherMur = True
        for  i in range(len(GameConfig.MUR)):
            if self.rect.colliderect(GameConfig.MUR[i])and self.toucherMur == False:
                self.toucherMur = True


    def F_Gravite(self,t,vx,vy,x,y):
        return 0,GameConfig.GRAVITY,vx,vy

    def F_Gravite_Friction(self,t,vx,vy,x,y):
        k = 0.023
        vx2 = vx**2
        vy2 = vy**2
        return k * np.sqrt(vx2+vy2),\
               k * np.sqrt(vx2+vy2) + GameConfig.GRAVITY,\
               vx,vy

    def F_Gravite_Friction_Vent(self,t,vx,vy,x,y):
        k = 0.023
        vx2 = vx**2
        vy2 = vy**2
        return k * np.sqrt(vx2+vy2) + self.vent,\
               k * np.sqrt(vx2+vy2) + GameConfig.GRAVITY,\
               vx,vy