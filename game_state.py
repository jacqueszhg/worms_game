from worms import *
from game_config import *
from map import *

class GameState:
    def __init__(self):
        self.map = Map()
        self.map.createMap()
        self.worms = Worms(20)


    def draw(self,window):
        window.blit(GameConfig.BACKGROUND_IMG,(0,0))
        self.map.draw(window)
        self.worms.draw(window)

    def advance_state(self, next_move,window):
        self.worms.advance_state(next_move,self.map,window)

        #recuperer les projectiles du joueur
        for bullet in self.worms.all_bullets:
            bullet.move(window)
        #affiche la bullet
        self.worms.all_bullets.draw(window)