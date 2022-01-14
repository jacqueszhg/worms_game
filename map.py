import random

import numpy as np
import numpy.polynomial.polynomial as nppol
import pygame

from game_config import *

class Map:
    def __init__(self):
        # Initialisation des points d'abscisse aléatoire
        self.px = [0,
                   random.randrange(100, 200),
                   random.randrange(100, 200),
                   random.randrange(GameConfig.WINDOW_W - 300, GameConfig.WINDOW_W - 200),
                   random.randrange(GameConfig.WINDOW_W - 300, GameConfig.WINDOW_W - 200),
                   GameConfig.WINDOW_W]

        # Associe une image pour chaque x, pour avoir des points d'interpolations
        self.py = [self.f(e) for e in self.px]

        # Obtient le polynome passant pour tout les points d'interpolation
        self.polynome = self.getPolyLagrange(self.px,self.py)

        # Calcule pour déterminer la taille de la matrice qui contiendra les murs du jeu
        if((GameConfig.WINDOW_H/GameConfig.MUR_H) %2 == 0): #Si le résultat est pair pas de soucis, mais si impair on grande un taille au-dessus
            H = int(GameConfig.WINDOW_H / GameConfig.MUR_H)
        else:
            H = int(GameConfig.WINDOW_H/ GameConfig.MUR_H) + 1

        if (GameConfig.WINDOW_W/GameConfig.MUR_W) % 2 == 0:
            W = int(GameConfig.WINDOW_W/GameConfig.MUR_W)
        else:
            W = int(GameConfig.WINDOW_W/GameConfig.MUR_W) + 1

        # Création de la matrice pour la map avec les blocks sur le tour de la map
        # D'abord une matrice que à zéro
        self.matrice_map = np.zeros((int(H), int(W)))

        #On met à 1 les casses qui font le contours de la matrice
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
        Fonction prenant en paramètre les abscisse de nos point d'interpolation et le point i à mettre à 1
         -racines sont les autre points d'interpolation à mettre à 0 
        Retourne le polynôme élémentaire, Li avec toutes les racines à 0, mais 1 pour racines[i]
    """
    def L(self,racines, i):
        x = list(racines)
        del x[i]

        # On calcule le numérateur de L
        numerateur = nppol.polyfromroots(x)

        # On calcule le dénominateur de L
        denominateur = nppol.polyvalfromroots(racines[i], x)

        # On calcule L
        Li = numerateur/denominateur
        return Li


    """
        Fonction qui prend en paramètre les abscisse de nos point d'interpolations
        et retourne tout les Li, polynome elementaire de lagrange
    """
    def polynomeElementaireLagrange(self,px):
        tab = []
        #Création de tout nos polynome élémentaire de lagrange
        for i in range(len(px)):
            tab.append(self.L(px, i))
        return tab

    """
        Fonction qui prend en paramètre un tableau nos point d'interpolation et leur valeur en abscisse
        Retourne un polynôme de degré i <= 5, qui passe par tous les points d'interpolations
    """
    def getPolyLagrange(self,px, py):
        P = nppol.polyzero

        #On possède tout nos polynomes élémentaires
        tab_q = self.polynomeElementaireLagrange(px)

        #Appliquons la formule de notre polynome P
        for i in range(len(py)):
            #Réalisation de la somme
            temp = py[i] * tab_q[i]
            P = nppol.polyadd(P, temp) #fait la somme de deux polynome
        return P

    """
    Fonction qui nous retourne selon un nombre de d'absccisse demandé, tout les images associé
    """
    def fonctionLagrange(self):
        x = np.linspace(0, GameConfig.WINDOW_W, GameConfig.WINDOW_W)

        #Pour les différent x donnée on récupère leur valeur en ordonnée, avec le polynome créer
        yp = nppol.polyval(x, self.polynome)
        return x,yp

    """
    Fonction qui créer la map, en ajoutant dans une liste tout les blocks qui suivent la fontion de lagrange, créer avec notre initialisation
    """
    def createMap(self):
        x,y = self.fonctionLagrange()
        for ligne in range(len(x)):
            GameConfig.BLOCKS[ligne] = []
            GameConfig.BLOCKS[ligne].append(pygame.Rect(x[ligne],y[ligne],GameConfig.WINDOW_W/100,GameConfig.WINDOW_W/100))

        for ligne in range(0,GameConfig.WINDOW_W,11):
            for i in range(len(GameConfig.BLOCKS[ligne])):
                x = GameConfig.BLOCKS[ligne][i].x
                y = GameConfig.BLOCKS[ligne][i].y
                for colonne in range(y,GameConfig.WINDOW_H,11):
                    GameConfig.BLOCKS[ligne].append(pygame.Rect(x, colonne,11,11))

    """
    Fonction qui dessina la map
    """
    def draw(self,window):
        for i in range(len(GameConfig.BLOCKS)):
            for y in range (len(GameConfig.BLOCKS[i])):
                g = pygame.transform.scale(GameConfig.DIRT_BLOCK_IMG, (GameConfig.BLOCKS[i][y][2], GameConfig.BLOCKS[i][y][3]))
                window.blit(g,GameConfig.BLOCKS[i][y])

        for i in range (len(GameConfig.MUR)):
            g = pygame.transform.scale(GameConfig.DIRT_BLOCK_IMG, (GameConfig.MUR_W, GameConfig.MUR_H))
            window.blit(g,GameConfig.MUR[i])

    def f(self,x):
        return 5 * x * np.sin(x)/200+GameConfig.WINDOW_H-100

    """
    Fonction qui retourne le polynome de lagrange
    """
    def getPolynome(self,x):
        return nppol.polyval(x,self.polynome)