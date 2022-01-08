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
        self.corde = []
        self.cordeIndice = 0

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
        if self.type == "corde_ninja":
            self.moveCordeNinja()
            pygame.draw.line(window, (88, 41, 0), (self.worms.rect.center[0], self.worms.rect.center[1]), self.rect.center,5)
            """
            for i in range(len(self.corde)):
                window.blit(GameConfig.DIRT_BLOCK_IMG, self.corde[i])
            """

        #vérifier si la bullet est hors écran
        #ajouter une condition que la bullet disparait qu'on un certain temps est passé
        if self.rect.x > GameConfig.WINDOW_W or self.rect.x < 0 or self.rect.y<0 or self.rect.y > 650 or time.time() - self.temp > 5 or self.toucherMur == True or self.touch():
            #supprimer la bullet
            if(self.type != "corde_ninja"):
                self.remove()

                if GameConfig.PLAY < len(GameConfig.LIST_WORMS) - 1:
                    GameConfig.PLAY = GameConfig.PLAY + 1
                else:
                    GameConfig.PLAY = 0
                while GameConfig.LIST_WORMS[GameConfig.PLAY].is_dead(GameConfig.PLAY):
                    if GameConfig.PLAY < len(GameConfig.LIST_WORMS) - 1:
                        GameConfig.PLAY = GameConfig.PLAY + 1
                    else:
                        GameConfig.PLAY = 0
            blockDetruit = []
            """
            if(self.type == "grenade" or self.type == "rocket"):
                circle = pygame.draw.circle(window,(255,255,255),self.rect.center,30)
                for i in range(len(GameConfig.BLOCKS)):
                    if pygame.Rect.colliderect(circle, GameConfig.BLOCKS[i]):
                        #blockDetruit.append(GameConfig.BLOCKS[i])
                        GameConfig.BLOCKS_DETRUIT.append(GameConfig.BLOCKS[i])

            for i in GameConfig.BLOCKS_DETRUIT:
                #GameConfig.BLOCKS.remove(i)
                i.y = 650

            """

            if(self.type == "grenade" or self.type == "rocket"):
                circle = pygame.draw.circle(window,(255,255,255),self.rect.center,40)
                for i in range(len(GameConfig.BLOCKS)):
                    for y in range(len(GameConfig.BLOCKS[i])):
                        if pygame.Rect.colliderect(circle, GameConfig.BLOCKS[i][y]):
                            blockDetruit.append(GameConfig.BLOCKS[i][y])
            elif self.type == "corde_ninja":
                if pygame.mouse.get_pressed()[0] == True:
                    pass
                    """
                    keys = pygame.key.get_pressed()
                    self.worms.rect.x = self.corde[self.cordeIndice].x
                    self.worms.rect.y = self.corde[self.cordeIndice].y
                    if self.cordeIndice < len(self.corde):
                        self.cordeIndice = self.cordeIndice + 1
                    if keys[pygame.K_s]:
                        if self.cordeIndice > 1:
                            self.cordeIndice = self.cordeIndice - 2
                        else :
                            self.cordeIndice = self.cordeIndice - 1
                    """
                else:
                    self.remove()



            for i in blockDetruit:
                for y in range(len(GameConfig.BLOCKS)):
                    if(i in GameConfig.BLOCKS[y]):
                        if(len(GameConfig.BLOCKS[y])>1):
                            GameConfig.BLOCKS[y].remove(i)
                        else:
                            i.y = i.bottom + 50

        if self.touch() and self.type != "corde_ninja":
            self.remove()
            for i in range(len(GameConfig.LIST_WORMS)):
                if self.rect.colliderect(GameConfig.LIST_WORMS[i]):
                    GameConfig.LIST_WORMS[i].life = GameConfig.LIST_WORMS[i].life - 50
                    if GameConfig.PLAY < len(GameConfig.LIST_WORMS) - 1:
                        GameConfig.PLAY = GameConfig.PLAY + 1
                    else:
                        GameConfig.PLAY = 0
                    while GameConfig.LIST_WORMS[GameConfig.PLAY].is_dead(GameConfig.PLAY):
                        if GameConfig.PLAY < len(GameConfig.LIST_WORMS) - 1:
                            GameConfig.PLAY = GameConfig.PLAY + 1
                        else:
                            GameConfig.PLAY = 0


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
        """
        for i in range(len(GameConfig.BLOCKS)):
            if self.rect.colliderect(GameConfig.BLOCKS[i]) and collision == False:
                self.chocElastique()
                collision = True
        for  i in range(len(GameConfig.MUR)):
            if self.rect.colliderect(GameConfig.MUR[i])and collision == False:
                self.chocElastique()
                collision = True
        """
        for i in range(len(GameConfig.BLOCKS)):
            for y in range(len(GameConfig.BLOCKS[i])):
                if self.rect.colliderect(GameConfig.BLOCKS[i][y]) and collision == False:
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

        """
        for i in range(len(GameConfig.BLOCKS)):
            if self.rect.colliderect(GameConfig.BLOCKS[i]) and self.toucherMur == False:
                self.toucherMur = True
        for i in range(len(GameConfig.MUR)):
            if self.rect.colliderect(GameConfig.MUR[i]) and self.toucherMur == False:
                self.toucherMur = True
        """

        for i in range(len(GameConfig.BLOCKS)):
            for y in range(len(GameConfig.BLOCKS[i])):
                if self.rect.colliderect(GameConfig.BLOCKS[i][y]) and self.toucherMur == False:
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

    def moveCordeNinja(self):
        #self.corde.append(pygame.Rect(self.rect.x, self.rect.y+10, 11, 11))
        if self.toucherMur == False:
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

            """
            for i in range(len(GameConfig.BLOCKS)):
                if self.rect.colliderect(GameConfig.BLOCKS[i]) and self.toucherMur == False:
                    self.toucherMur = True
            for i in range(len(GameConfig.MUR)):
                if self.rect.colliderect(GameConfig.MUR[i]) and self.toucherMur == False:
                    self.toucherMur = True
            """

            for i in range(len(GameConfig.BLOCKS)):
                for y in range(len(GameConfig.BLOCKS[i])):
                    if self.rect.colliderect(GameConfig.BLOCKS[i][y]) and self.toucherMur == False:
                        self.toucherMur = True
            for  i in range(len(GameConfig.MUR)):
                if self.rect.colliderect(GameConfig.MUR[i])and self.toucherMur == False:
                    self.toucherMur = True

    def mouvement_pendule(self):
        pass
