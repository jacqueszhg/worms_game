import numpy as np
import pygame

from block import *
from game_config import *


class Map:
    """
    0 = rien
    1 = dirt up
    2 = block mario
    3 = block mario surpise
    4 = dirt down
    """

    def __init__(self):
        self.matrice_map = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])

        #Ajoute dans un tableau tout les blocs crées
        for ligne in range(13):
            for colonne in range(20):
                block = self.matrice_map[ligne][colonne]

                if block == 1:
                    GameConfig.LISTE_BLOCK.append(Block(colonne*50,ligne*50))
                    for ligne2 in range(ligne+1,13):
                        self.matrice_map[ligne2][colonne] = 4

                elif block == 2:
                    GameConfig.LISTE_BLOCK.append(Block(colonne*50,ligne*50))

                elif block==3:
                    GameConfig.LISTE_BLOCK.append(Block(colonne*50,ligne*50))

                elif block == 4:
                    GameConfig.LISTE_BLOCK.append(Block(colonne*50,ligne*50))
        #print(GameConfig.LISTE_BLOCK)


    def draw(self,window):
        for ligne in range(13):
            for colonne in range(20):
                block = self.matrice_map[ligne][colonne]

                if block == 1:
                    window.blit(GameConfig.DIRT_UP_IMG, (colonne * 50, ligne * 50))
                    for ligne2 in range(ligne+1,13):
                        self.matrice_map[ligne2][colonne] = 4

                elif block == 2:
                    window.blit(GameConfig.BRICK_IMG, (colonne * 50, ligne * 50))

                elif block==3:
                    window.blit(GameConfig.SURPRISE_IMG, (colonne * 50, ligne * 50))

                elif block == 4:
                    window.blit(GameConfig.DIRT_DOWN_IMG, (colonne * 50, ligne * 50))
