from bullet import *
from game_config import *
from worms import *

class Round:
    #Methode qui permet de dire quel worms joue et de passer au tour suivant
    def next_round():
        """
        if GameConfig.PLAY < len(GameConfig.LIST_WORMS) :
            GameConfig.PLAY = GameConfig.PLAY + 1
        else:
            GameConfig.PLAY = 0
        while GameConfig.LIST_WORMS[GameConfig.PLAY].is_dead():
            if GameConfig.PLAY < len(GameConfig.LIST_WORMS):
                GameConfig.PLAY = GameConfig.PLAY + 1
            else:
                GameConfig.PLAY = 0
        """
        if GameConfig.LIST_WORMS[GameConfig.PLAY].arme_corde_ninja == True:
            GameConfig.PLAY = GameConfig.PLAY
        elif GameConfig.PLAY + 1 < len(GameConfig.LIST_WORMS):
            GameConfig.PLAY = GameConfig.PLAY + 1
        else:
            GameConfig.PLAY = 0

Round.next_round = staticmethod(Round.next_round)