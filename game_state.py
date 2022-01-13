import pygame
from worms import *
from map import *
from round import *

class GameState:
    def __init__(self):
        self.map = Map()
        self.map.createMap()

        GameConfig.LIST_WORMS.append(Worms(100, self.map))
        GameConfig.LIST_WORMS.append(Worms(int(GameConfig.WINDOW_W/2), self.map))
        GameConfig.LIST_WORMS.append(Worms(GameConfig.WINDOW_W-100, self.map))

    # Methode qui créer la map et qui affiche les worms vivant / morts
    def draw(self,window):
        window.blit(GameConfig.BACKGROUND_IMG,(0,0))
        self.map.draw(window)
        GameConfig.displayMessage(window, "vent " + str(GameConfig.VENT), 50, 100, 100)
        for i in range(len(GameConfig.LIST_WORMS)):
            GameConfig.LIST_WORMS[i].draw(window)

    def advance_state(self, next_move,window):

        if GameConfig.LIST_WORMS[GameConfig.PLAY].mort == False:
            wormsCourant = GameConfig.LIST_WORMS[GameConfig.PLAY]
            wormsCourant.advance_state(next_move, self.map, window)
            for bullet in GameConfig.LIST_WORMS[GameConfig.PLAY].all_bullets:
                bullet.move(window)
            wormsCourant.all_bullets.draw(window)

            if (wormsCourant.jouer):
                wormsCourant.jouer = False
                Round.next_round()
                wormsCourant.is_dead()

        else:
             Round.next_round()

        for numWomrs in range(len(GameConfig.LIST_WORMS)):
            if numWomrs != GameConfig.PLAY:
                GameConfig.LIST_WORMS[numWomrs].charge_position()

        nbMort = 0
        for worms in GameConfig.LIST_WORMS:
            if worms.mort == True:
                nbMort = nbMort + 1

        if(nbMort == len(GameConfig.LIST_WORMS)-1):
            GameConfig.displayMessage(window, "VOUS AVEZ GAGNEZ", 100, int(GameConfig.WINDOW_W / 2),
                                      int(GameConfig.WINDOW_H / 2)-100)
            GameConfig.displayMessage(window, "APPUYER SUR ENTRER POUR REJOUER", 80, int(GameConfig.WINDOW_W / 2),
                                  int(GameConfig.WINDOW_H / 2))
            GameConfig.displayMessage(window, "APPUYER SUR ECHAP POUR QUITTER", 80, int(GameConfig.WINDOW_W / 2),
                                  int(GameConfig.WINDOW_H / 2)+100)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                return 1
            if keys[pygame.K_ESCAPE]:
                return -1
        return 0




