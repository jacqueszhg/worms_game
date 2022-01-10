import random

import numpy as np
import numpy.polynomial.polynomial as nppol
import pygame

from game_config import *

class Map:
    def __init__(self):
        #self.px = [0,200,300,640,650,999,1000, 1200, 1450, 1715, 1800, 1920]
        self.px = [0,200,250,400,450,600,650,750,900,950,1100,1300,1400,1500,1650,1750,1800,1920]
        self.py = [self.f(e) for e in self.px]
        self.polynome = self.get_poly_lagrange(self.px,self.py)
        '''self.matrice_map = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ])'''

        self.matrice_map = np.zeros((int(GameConfig.WINDOW_H/25)+1, int(GameConfig.WINDOW_W/25)+1))
        for i in range(len(self.matrice_map[0])):
            self.matrice_map[0][i] = 1
        nbligne, nbcolonne = self.matrice_map.shape
        for i in range(1, nbligne):
            self.matrice_map[i][0] = 1
            self.matrice_map[i][-1] = 1

        # Ajoute dans un tableau tout les blocs crées
        for ligne in range(nbligne):
            for colonne in range(nbcolonne):
                block = self.matrice_map[ligne][colonne]
                if block == 1:
                    GameConfig.MUR.append(pygame.Rect(colonne * GameConfig.MUR_W, ligne * GameConfig.MUR_H, GameConfig.MUR_W,GameConfig.MUR_H))

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

    def fonction_principale(self):
        # Interpolation de points
        '''
        px = [0,
              random.randint(0, 100), random.randint(100, 200),
              random.randint(550, 560),random.randint(555, 560),
              random.randint(600, 700),random.randint(700, 800),
              1000]
        '''
        #px = [0,200,300,640,650,900,1000]
        #py = [self.f(e) for e in px]

        #p = self.get_poly_lagrange(self.px, self.py)

        x = np.linspace(0, GameConfig.WINDOW_W, GameConfig.WINDOW_W)
        yp = nppol.polyval(x, self.polynome)
        return x,yp

    def createMap(self):
        x,y = self.fonction_principale()
        print(x, y)
        for ligne in range(len(x)):
            #GameConfig.BLOCKS.append(pygame.Rect(x[ligne],y[ligne],GameConfig.WINDOW_W/100,GameConfig.WINDOW_W/100))
            GameConfig.BLOCKS[ligne] = []
            GameConfig.BLOCKS[ligne].append(pygame.Rect(x[ligne],y[ligne],GameConfig.WINDOW_W/100,GameConfig.WINDOW_W/100))

        """
        for ligne in range(0,GameConfig.WINDOW_W,11):
            x = GameConfig.BLOCKS[ligne].x
            y = GameConfig.BLOCKS[ligne].y
            for colonne in range(y,GameConfig.WINDOW_H,11):
                GameConfig.BLOCKS.append(pygame.Rect(x, colonne,11,11))
        """

        for ligne in range(0,GameConfig.WINDOW_W,11):
            for i in range(len(GameConfig.BLOCKS[ligne])):
                x = GameConfig.BLOCKS[ligne][i].x
                y = GameConfig.BLOCKS[ligne][i].y
                for colonne in range(y,GameConfig.WINDOW_H,11):
                    GameConfig.BLOCKS[ligne].append(pygame.Rect(x, colonne,11,11))

    def draw(self,window):
        """
        for i in range(len(GameConfig.BLOCKS)):
            g = pygame.transform.scale(GameConfig.DIRT_BLOCK_IMG, (GameConfig.BLOCKS[i][2], GameConfig.BLOCKS[i][3]))
            window.blit(g,GameConfig.BLOCKS[i])
        """

        for i in range(len(GameConfig.BLOCKS)):
            for y in range (len(GameConfig.BLOCKS[i])):
                g = pygame.transform.scale(GameConfig.DIRT_BLOCK_IMG, (GameConfig.BLOCKS[i][y][2], GameConfig.BLOCKS[i][y][3]))
                window.blit(g,GameConfig.BLOCKS[i][y])

        for i in range (len(GameConfig.MUR)):
            g = pygame.transform.scale(GameConfig.DIRT_BLOCK_IMG, (GameConfig.MUR_W, GameConfig.MUR_H))
            window.blit(g,GameConfig.MUR[i])

    def f(sellf,x):
        return 5 * x * np.sin(x)/200+1000

    def f2(self,x):
        return 5 * x * np.sin(x)/200+100

    def getPolynome(self,x):
        return nppol.polyval(x,self.polynome)