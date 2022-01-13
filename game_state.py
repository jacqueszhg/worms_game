import pygame

from move import Move
from worms import *
from game_config import *
from map import *
from game_config import *
from round import *

class GameState:
    def __init__(self):
        self.map = Map()
        self.map.createMap()
        GameConfig.LIST_WORMS.append(Worms(85, self.map))
        GameConfig.LIST_WORMS.append(Worms(200, self.map))
        GameConfig.LIST_WORMS.append(Worms(300, self.map))

    # Methode qui créer la map et qui affiche les worms vivant / morts
    def draw(self,window):
        window.blit(GameConfig.BACKGROUND_IMG,(0,0))
        self.map.draw(window)
        font = pygame.font.SysFont("BradBunRb", 25)
        #Affichage des worms sur la map au démarage du jeu et affichage de la vie au dessus de leurs têtes
        for i in range(len(GameConfig.LIST_WORMS)):
            GameConfig.LIST_WORMS[i].draw(window)
            life_text = font.render(f"{GameConfig.LIST_WORMS[i].life}", 1, (0, 0, 0))
            if not GameConfig.LIST_WORMS[i].is_dead():
                window.blit(life_text, (GameConfig.LIST_WORMS[i].rect.x, GameConfig.LIST_WORMS[i].rect.y - 20))
        #Affichage de l'image du worms mort lorsque qu'un joueur est mort
        for worms in GameConfig.LIST_WORMS_DEAD:
            worms.draw(window)


    # Methode qui permet de faire jouer les worms et de modifier leurs position
    def advance_state(self, next_move,window):
        # Permet de modifier la position du joueur mort pour que l'image des worms morts suivent la position du terrain si celui-ci se détruit
        for j in GameConfig.LIST_WORMS_DEAD:
            j.charge_position()

        # Permet le déplacement du worms a qui est le tour et qu'il puisse tirer
        wormsCourant = GameConfig.LIST_WORMS[GameConfig.PLAY]
        wormsCourant.advance_state(next_move, self.map, window)
        for bullet in GameConfig.LIST_WORMS[GameConfig.PLAY].all_bullets:
            bullet.move(window)
        wormsCourant.all_bullets.draw(window)

        # Changement de position des worms vivant pour qu'ils suivent la destruction du terrain
        for worms in GameConfig.LIST_WORMS:
            if worms != wormsCourant:
                worms.charge_position()
            if worms.is_dead():
                GameConfig.LIST_WORMS_DEAD.append(worms)
                worms.image = GameConfig.STANDING_IMG_MORT
                GameConfig.LIST_WORMS.remove(worms)
                Round.next_round()

        # Une fois que le worms a fini sont tour passage au tour suivant
        if(wormsCourant.jouer):
            wormsCourant.jouer = False
            Round.next_round()

        # Lorsqu'il reste plus qu'un worms en vie affichage du menu de fin de partie pour quitter le jeu ou pour relancer la partie
        if(len(GameConfig.LIST_WORMS) == 1):
            GameConfig.displayMessage(window, "VOUS AVEZ GAGNEZ", 100, int(GameConfig.WINDOW_W / 2),
                                      int(GameConfig.WINDOW_H / 2)-100)
            GameConfig.displayMessage(window, "APPUYER SUR ENTRER POUR REJOUER", 80, int(GameConfig.WINDOW_W / 2),
                                  int(GameConfig.WINDOW_H / 2))
            GameConfig.displayMessage(window, "APPUYER SUR ECHAP POUR QUITTER", 80, int(GameConfig.WINDOW_W / 2),
                                  int(GameConfig.WINDOW_H / 2)+100)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                print("a")
                return 1
            if keys[pygame.K_ESCAPE]:
                return -1
        return 0
        """
        for numJoueur in range(len(GameConfig.LIST_WORMS)):
            if (numJoueur != GameConfig.PLAY):
                GameConfig.LIST_WORMS[numJoueur].charge_position()
                if GameConfig.LIST_WORMS[numJoueur].is_dead():
                    GameConfig.LIST_WORMS_DEAD.append(GameConfig.LIST_WORMS[numJoueur])
                    GameConfig.LIST_WORMS[numJoueur].image = GameConfig.STANDING_IMG_MORT
                    GameConfig.LIST_WORMS.remove(GameConfig.LIST_WORMS[numJoueur])
                    Round.next_round()
                    wormsCourantMort = True
        """

        """
        for numJoueur in range(len(GameConfig.LIST_WORMS)):
            if(numJoueur == GameConfig.PLAY):
                GameConfig.LIST_WORMS[numJoueur].advance_state(next_move, self.map, window)
                for bullet in GameConfig.LIST_WORMS[numJoueur].all_bullets:
                    bullet.move(window)
                GameConfig.LIST_WORMS[numJoueur].all_bullets.draw(window)
                
            else:
                GameConfig.LIST_WORMS[numJoueur].charge_position()
        """
        """
        for i in range(len(GameConfig.LIST_WORMS)):
            if GameConfig.LIST_WORMS[i].is_dead():
                GameConfig.LIST_WORMS_DEAD.append(GameConfig.LIST_WORMS[i].is_dead())
                GameConfig.LIST_WORMS[i].is_dead().image = GameConfig.STANDING_IMG_MORT
                GameConfig.LIST_WORMS.remove(GameConfig.LIST_WORMS[i].is_dead())
            elif GameConfig.PLAY == i:
                GameConfig.LIST_WORMS[i].advance_state(next_move, self.map, window)
                if GameConfig.LIST_WORMS[i].is_dead():
                    Round.next_round()
                # recuperer les projectiles du joueur
                for bullet in GameConfig.LIST_WORMS[i].all_bullets:
                    bullet.move(window)
                # affiche la bullet
                GameConfig.LIST_WORMS[i].all_bullets.draw(window)
            else:
                GameConfig.LIST_WORMS[i].charge_position()
        """




