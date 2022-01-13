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

    '''
    Methode qui créait la map et qui affiche les worms vivant / morts
    '''
    def draw(self,window):
        # Affichage de la map et du vent
        window.blit(GameConfig.BACKGROUND_IMG,(0,0))
        self.map.draw(window)
        GameConfig.displayMessage(window, "vent " + str(GameConfig.VENT), 50, 100, 100)
        # Boucle qui parcours la liste de worms pour les afficher sur la map
        for i in range(len(GameConfig.LIST_WORMS)):
            GameConfig.LIST_WORMS[i].draw(window)
    '''
    Methode qui fait avancer le courant de la partie
    '''
    def advance_state(self, next_move,window):
        # Si le worms n'est pas mort alors on le fait jouer
        if GameConfig.LIST_WORMS[GameConfig.PLAY].mort == False:
            wormsCourant = GameConfig.LIST_WORMS[GameConfig.PLAY]
            wormsCourant.advance_state(next_move, self.map, window)
            # Appelle la méthode move dans la class bullet pour tirer
            for bullet in GameConfig.LIST_WORMS[GameConfig.PLAY].all_bullets:
                bullet.move(window)
            wormsCourant.all_bullets.draw(window)
            # Permet de d'appeller la class Round une fois que le joueur à jouer
            if (wormsCourant.jouer):
                wormsCourant.jouer = False
                Round.next_round()
                wormsCourant.is_dead()
        # Appelle la class Round si le worms est mort
        else:
             Round.next_round()

        # Permet de charger la position des worms en continue pour changer leurs positions si le sol se détruit sous eux
        for numWomrs in range(len(GameConfig.LIST_WORMS)):
            if numWomrs != GameConfig.PLAY:
                GameConfig.LIST_WORMS[numWomrs].charge_position()

        # On compte le nombre de morts pour voir combien de worms il reste en vie
        nbMort = 0
        for worms in GameConfig.LIST_WORMS:
            if worms.mort == True:
                nbMort = nbMort + 1

        # Si il ne reste plus que 1 worms en vie alors on affiche le menu de fin
        if(nbMort == len(GameConfig.LIST_WORMS)-1 or nbMort == len(GameConfig.LIST_WORMS)):
            if nbMort == nbMort == len(GameConfig.LIST_WORMS)-1:
                GameConfig.displayMessage(window, "VOUS AVEZ GAGNEZ", 100, int(GameConfig.WINDOW_W / 2),
                                          int(GameConfig.WINDOW_H / 2)-100)
            else:
                GameConfig.displayMessage(window, "EGALITE", 100, int(GameConfig.WINDOW_W / 2),
                                          int(GameConfig.WINDOW_H / 2)-100)
            GameConfig.displayMessage(window, "APPUYER SUR ENTRER POUR REJOUER", 80, int(GameConfig.WINDOW_W / 2),
                                  int(GameConfig.WINDOW_H / 2))
            GameConfig.displayMessage(window, "APPUYER SUR ECHAP POUR QUITTER", 80, int(GameConfig.WINDOW_W / 2),
                                  int(GameConfig.WINDOW_H / 2)+100)
            # Si le joueur appui sur Entrer on retourne 1 et si il appui sur Echap on retourne -1
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                return 1
            if keys[pygame.K_ESCAPE]:
                return -1
        return 0




