import math
import random
import time

import pygame
import game_config
from game_config import *
from round import *

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

        #Calcule distance pour la vitesse
        absolute_x = self.rect.x - mouse_pos[0]
        absolute_y = self.rect.y - mouse_pos[1]
        distance = (pow(pow(absolute_x, 2) + pow(absolute_y, 2), 0.5))/10
        if(distance > 50):
            distance = 50
        #vitesse initiale
        if(self.mouse_pos < (self.worms.rect.x,self.worms.rect.y)):
            self.velocity = -distance
            self.rect.x = worms.rect.topleft[0] - 15
            self.rect.y = worms.rect.topleft[1]
        else:
            self.velocity = distance

        self.x0 = self.rect.x
        self.y0 = self.rect.y
        print(angle)
        if angle[0] < -100:
            angle[0] = -100
            if angle[1] < 100:
                angle[1] = 100
            elif angle[1] > -100:
                angle[1] = -100
        if angle[0] > 100:
            angle[0] = 100
            if angle[1] < -100:
                angle[1] = -100
            elif angle[1] > 100:
                angle[1] = 100
        #vitesse de dire pour la grenade et le rocket
        self.vx = angle[0]
        self.vy = angle[1]

        self.temp = time.time()
        self.type = type
        self.vent = vent
        self.toucherMur = False

    def remove(self):
        self.worms.jouer = True
        self.worms.all_bullets.remove(self)

    def draw(self,window):
        window.blit(self.image,self.rect)

    def touch(self):
        for i in range(len(GameConfig.LIST_WORMS)):
            if self.rect.colliderect(GameConfig.LIST_WORMS[i]):
                return True
        return False

    def move(self,window):
        global degat
        if(self.type == "carabine"):
            self.moveCarabine()
        if self.type =="rocket":
            self.moveRocket()
        if self.type == "grenade":
            self.moveGrenade()
        if self.type == "corde_ninja":
            self.moveCordeNinja()
            pygame.draw.line(window, (88, 41, 0), (self.worms.rect.center[0], self.worms.rect.center[1]), self.rect.center,5)


        #vérifier si la bullet est hors écran
        #ajouter une condition que la bullet disparait qu'on un certain temps est passé
        if self.rect.x > GameConfig.WINDOW_W or self.rect.x < 0 or self.rect.y<0 or self.rect.y > GameConfig.WINDOW_H or time.time() - self.temp > 5 or self.toucherMur == True or self.touch():
            #supprimer la bullet
            if(self.type != "corde_ninja"):
                self.remove()
            if(self.type == "carabine"):
                for i in range(len(GameConfig.LIST_WORMS)):
                    if self.rect.colliderect(GameConfig.LIST_WORMS[i]):
                        GameConfig.LIST_WORMS[i].life = GameConfig.LIST_WORMS[i].life - 40

            blockDetruit = []
            if(self.type == "grenade" or self.type == "rocket"):
                circle = pygame.draw.circle(window,(255,255,255),self.rect.center,40)
                for i in range(len(GameConfig.BLOCKS)):
                    for y in range(len(GameConfig.BLOCKS[i])):
                        if pygame.Rect.colliderect(circle, GameConfig.BLOCKS[i][y]):
                            blockDetruit.append(GameConfig.BLOCKS[i][y])
                # Calcul de la distance entre le centre de l'explosion et joueur pour effectuer des dégâts adaptatif.
                # Utilisation de la formule de la distance entre 2 points qui est expliqué dans le rapport
                for i in range(len(GameConfig.LIST_WORMS)):
                    if pygame.Rect.colliderect(circle, GameConfig.LIST_WORMS[i]):
                        absolute_x = GameConfig.LIST_WORMS[i].rect.x-circle.centerx
                        absolute_y = GameConfig.LIST_WORMS[i].rect.y-circle.centery
                        distance = pow(pow(absolute_x, 2)+pow(absolute_y, 2), 0.5)
                        degat_nade = int((80 - distance)/2)
                        print(degat_nade)
                        GameConfig.LIST_WORMS[i].life = GameConfig.LIST_WORMS[i].life - degat_nade



            elif self.type == "corde_ninja":
                if pygame.mouse.get_pressed()[0] == True:
                    pass
                else:
                    self.remove()
                    self.toucherMur = False



            for i in blockDetruit:
                for y in range(len(GameConfig.BLOCKS)):
                    if(i in GameConfig.BLOCKS[y]):
                        if(len(GameConfig.BLOCKS[y])>1):
                            GameConfig.BLOCKS[y].remove(i)
                        else:
                            i.y = i.bottom + 50


    def moveCarabine(self):
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
        self.vx,self.vy,self.rect.x,self.rect.y = GameConfig.euleur(t,vx,vy,x,y,vxn,vyn,xn,yn,dt)

        collision = False

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
         newVx = ((GameConfig.MASSE_GRENADE - GameConfig.MASSE_MUR)/(GameConfig.MASSE_GRENADE + GameConfig.MASSE_MUR)) * (self.vx)
         newVy = ((GameConfig.MASSE_GRENADE - GameConfig.MASSE_MUR)/(GameConfig.MASSE_GRENADE + GameConfig.MASSE_MUR)) * (self.vy)
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
        self.vx,self.vy,self.rect.x,self.rect.y = GameConfig.euleur(t,vx,vy,x,y,vxn,vyn,xn,yn,dt)

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

            for i in range(len(GameConfig.BLOCKS)):
                for y in range(len(GameConfig.BLOCKS[i])):
                    if self.rect.colliderect(GameConfig.BLOCKS[i][y]) and self.toucherMur == False:
                        self.toucherMur = True
            for  i in range(len(GameConfig.MUR)):
                if self.rect.colliderect(GameConfig.MUR[i])and self.toucherMur == False:
                    self.toucherMur = True
