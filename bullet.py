import math
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
    def __init__(self,velocity,image,worms,mouse_pos,type):
        super().__init__()
        self.worms = worms
        self.image = image
        self.angle = (1.57)/math.pi
        self.image = pygame.transform.scale(self.image,(15,15))
        self.rect = self.image.get_rect()
        self.rect.x = worms.rect.x + 26
        self.rect.y = worms.rect.y + 10
        self.y_origine = self.rect.y
        self.mouse_pos = mouse_pos
        self.x0 = worms.rect.x + 26
        self.y0 = worms.rect.y + 10

        #vitesse initiale
        if(self.mouse_pos < (self.worms.rect.x,self.worms.rect.y)):
            self.velocity = -velocity
        else:
            self.velocity = velocity
        self.temp = time.time()
        self.type = type


        self.a = 0
        self.i = 0

        #méthode4
        """
        self.vx = self.velocity * math.cos(self.angle)
        self.vy = self.velocity * math.sin(self.angle)
        """
        self.vx0 = velocity



    def remove(self):
        self.worms.all_bullets.remove(self)

    def draw(self,window):
        window.blit(self.image,self.rect)

    def touch(self):
        if self.rect.colliderect(GameConfig.LIST_WORMS[0]) or self.rect.colliderect(GameConfig.LIST_WORMS[1]):
            return True
        return False

    def move(self,window):
        if(self.type == "carabine"):
            self.moveCarabine()
        if self.type =="rocket":
            self.moveRocket()

        #vérifier si la bullet est hors écran
        #ajouter une condition que la bullet disparait qu'on un certain temps est passé
        if self.rect.x > GameConfig.WINDOW_W or self.rect.x < 0 or self.rect.y<0 or self.rect.y > 650 :
            #supprimer la bullet
            self.remove()

        #vérifier si la bullet touche un autre joueur
        if self.touch():
            self.remove()
            if self.rect.colliderect(GameConfig.LIST_WORMS[0]):
                GameConfig.PLAY = 0
            if self.rect.colliderect(GameConfig.LIST_WORMS[1]):
                GameConfig.PLAY = 1



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
        # gere la vitesse
        dt = 1.5

        # self.rect.x += self.velocity
        self.rect.x += self.velocity * dt

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

    def moveRocket(self):
        """
        alpha = 90
        t = time.time() - self.temp

        self.rect.x += self.velocity * math.cos(alpha* t)
        #self.rect.y = (1/2)*GameConfig.GRAVITY * (t**2) + self.velocity* math.sin(alpha) * t + self.y0
        #self.rect.y = ((-GameConfig.GRAVITY / (2*(self.velocity**2)*(math.cos(alpha)**2)))*(t**2)+ math.tan(alpha)*t)+self.y0
        self.rect.y = -0.5*((GameConfig.GRAVITY*(t**2)/((math.cos(alpha)**2)*self.velocity**2))) +math.tan(alpha)*t+self.y0
        print(self.rect.x, self.rect.y)
        """

        """
        #Je défini les points nécessaire pour calculer la trajectoire
        # le point O, va corespondre au pint (0,0)
        pointO = [self.rect.x,self.rect.y]
        Les positions du projectile à différent instant t
        x(t) = v0 * cos(alpha) * t
        y(t) = -1/2g * t² + v0 * sin(alpha) * t
        
        On veut pas avoir de t dans nos formules on la subtitue avec x(t):
        t = x/(v0*cos(alpha)
        y(x) -1/2g * (x/(v0*cos(alpha)))² + v0 * sin(alpha) * (x/v0 * cos(alpha))
        y(x) = -(g/(2 *v0² cos²(alpha)))x² + tan(aplha) * x
        or cos²(x) = (1+cos(2x))/(2)
        """
        """
        alpha = math.radians(60)
        cosCarreAlpha = (1+math.cos(2*alpha))/2
        self.rect.x += self.velocity
        print(cosCarreAlpha)
        self.rect.y = -(GameConfig.GRAVITY/(2*(self.velocity**2)*cosCarreAlpha)) * (self.rect.x**2) + math.tan(alpha)*self.rect.x - self.y0
        print(self.rect.y)
        """

        """
        def zdot(z, t):
            Calcul de la dérivée de z=(x, y, vx, vy) à l'instant t.

            x, y, vx, vy = z
            alphav = alpha * N.hypot(vx, vy)

            return (vx, vy, -alphav * vx, -g - alphav * vy)  # dz/dt = (vx,vy,x..,y..)

        g = 9.81  # Pesanteur [m/s2]
        cx = 0.45  # Coefficient de frottement d'une sphère
        rhoAir = 1.2  # Masse volumique de l'air [kg/m3] au niveau de la mer, T=20°C
        rad = 0.1748 / 2  # Rayon du boulet [m]
        rho = 6.23e3  # Masse volumique du boulet [kg/m3]
        mass = 4. / 3. * N.pi * rad ** 3 * rho  # Masse du boulet [kg]
        alpha = 0.5 * cx * rhoAir * N.pi * rad ** 2 / mass  # Coefficient de frottement par unité de masse
        #print("Masse du boulet: {:.2f} kg".format(mass))
        #print("Coefficient de frottement par unité de masse: {} S.I.".format(alpha))
        v0 = 10.  # Vitesse initiale [m/s]
        alt = 45.  # Inclinaison du canon [deg]
        alt *= N.pi / 180.  # Inclinaison [rad]
        z0 = (0., 0., v0 * N.cos(alt), v0 * N.sin(alt))  # (x0, y0, vx0, vy0)
        tc = N.sqrt(mass / (g * alpha))
        #print("Temps caractéristique: {:.1f} s".format(tc))é
        t = N.linspace(0, tc, 1000)
        zs = SI.odeint(zdot, z0, t)
        ypos = zs[:, 1] >= 0  # y>0?
        #print("temps de coll. t(y~0) = {:.0f} s".format(t[ypos][-1]))  # Dernier instant pour lequel y>0
        #print("portée x(y~0) = {:.0f} m".format(zs[ypos, 0][-1]))  # Portée approximative du canon
        # print "y(y~0) = {:.0f} m".format(zs[ypos, 1][-1]) # ~0
        #print("vitesse(y~0): {:.0f} m/s".format(N.hypot(zs[ypos, 2][-1], zs[ypos, 3][-1])))

        
        if(self.a <3):
            self.rect.y = -zs[self.i][self.a] + self.y0
            print(self.rect.y)
            self.a += 1
        else:
            self.rect.y = -zs[self.i][self.a] + self.y0
            self.a = 0é
            self.i +=self.velocity
            self.rect.x = self.i
        print(zs[ypos,0],zs[ypos,1])
        print(ypos)
        """

        """
        def traj(syst, t):
            [x, y, vx, vy] = syst
            alpha = math.atan(vy / vx)
            dxdt = vx
            dydt = vy
            dvxdt = -(k / m) * (vx ** 2) * math.cos(alpha)
            dvydt = -(k / m) * (vy ** 2) * math.sin(alpha) - g
            return (dxdt, dydt, dvxdt, dvydt)

        r = 0.02  # 1cm en m
        cx = 0.3
        rho = 0  # 1.225kg/m3 pour l'air
        s = math.pi * (r ** 2)  # surface d'un disque de rayon r
        steel_density = 7800  # 7800kg/m^3 pour l'acier
        m = 4 / 3 * math.pi * math.pow(r, 3) * steel_density  # Vol * density
        k = cx * rho * s / 2  # juste pour simplifier l'equation
        g = 9.81

        t = np.linspace(0, 10, 1000)
        systCI = [0, 0, 12, 12]
        sols = odeint(traj, systCI, t)
        x = sols[:, 0]
        y = sols[:, 1]
        if(self.i < GameConfig.WINDOW_W):
            self.rect.x = x[self.i] + self.x0
            self.rect.y = y[self.i] + self.y0
            self.i +=100
        elif self.rect.y < GameConfig.WINDOW_H:
            self.rect.y += self.velocity
        """

        """
        def bougerProjectile(x, y, vx, vy, ax, ay, dt):
            vx += ax * dt
            vy += ay * dt
            x += vx * dt
            y += vy * dt
            return (x, y, vx, vy)

        if(self.rect.y < GameConfig.WORMS_H or self.rect.x < GameConfig.WINDOW_W):
            self.rect.x, self.rect.y, self.vx, self.vy = bougerProjectile(self.rect.x, self.rect.y, self.vx, self.vy, 0.0, -GameConfig.GRAVITY, 1)
        """
