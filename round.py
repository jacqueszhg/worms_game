from bullet import *
from game_config import *
from worms import *

class Round:
    #Methode qui permet de dire quel worms joue et de passer au tour suivant
    def next_round():
        if GameConfig.LIST_WORMS[GameConfig.PLAY].arme_corde_ninja == True:
            GameConfig.PLAY = GameConfig.PLAY
        # Vérifie qu'on ne soit pas au dernier joueur si ce n'est pas le cas on ajoute 1 pour passer au joueur suivant
        elif GameConfig.PLAY + 1 < len(GameConfig.LIST_WORMS):
            GameConfig.PLAY = GameConfig.PLAY + 1
        # Si c'est le dernier joueur on repasse au premier joueur
        else:
            GameConfig.PLAY = 0

Round.next_round = staticmethod(Round.next_round)