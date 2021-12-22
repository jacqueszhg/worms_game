import random

import numpy as np
import numpy.polynomial.polynomial as nppol
import pygame

from game_config import *

class Map:

    """
        Fonction prenant en paramètre un ensemble de valeurs racines et un indice i
        et retournant un polynôme valant 0 pour toutes les valeurs
        de racines, sauf racines[i] et valant 1 en racines[i]
    """
    def Q(self,racines, i):

        x = list(racines)

        del x[i]

        bi = nppol.polyvalfromroots(racines[i], x)

        Ri = nppol.polyfromroots(x)

        Qi = (1 / bi) * Ri
        return Qi

    """
        Fonction prenant en paramètre un ensemble de valeurs px
        et retournant une base de polynômes de Lagrange (le i-ème polynôme vaut 0 pour toutes les valeurs
        de px, sauf px[i] et valant 1 en px[i])
    """

    def base_lagrange(self,px):

        tab = []

        for i in range(len(px)):
            tab.append(self.Q(px, i))

        return tab

    """
        Fonction prenant en paramètre un ensemble de points représenté par deux tableaux :
        - px représentant les abscisses,
        - py rerépsentant les ordonnées
        et retournant un polynôme donc la représentation passe par tous ces points.
    """

    def get_poly_lagrange(self,px, py):

        P = nppol.polyzero
        tab_q = self.base_lagrange(px)

        for i in range(len(py)):
            #     # principe : P = P + py[i]*tab_q[i]
            temp = py[i] * tab_q[i]
            P = nppol.polyadd(P, temp)

        return P

    def f(self,x):
        return 5 * x * np.sin(x)/200+600

    def f2(self,x):
        return 5 * x * np.sin(x)/200+100

    def fonction_principale(self):
        # Interpolation de points
        #px = [0, random.randint(1, 100), random.randint(100, 200), random.randint(200, 400),random.randint(400, 700),random.randint(700, 999),1000]
        px = [90, 120,150,170,500,600,900,1000]
        py = [self.f(e) for e in px]

        p = self.get_poly_lagrange(px, py)

        x = np.linspace(0, GameConfig.WINDOW_W, 100)
        yp = nppol.polyval(x, p)
        return x,yp


    def createMap(self):
        x,y = self.fonction_principale()
        for ligne in range(len(x)):
            GameConfig.BLOCKS.append(pygame.Rect(x[ligne],y[ligne],GameConfig.WINDOW_W/100,GameConfig.WINDOW_W/100))


    def draw(self,window):
        for i in range(len(GameConfig.BLOCKS)):
            window.blit(GameConfig.DIRT_BLOCK_IMG,GameConfig.BLOCKS[i])