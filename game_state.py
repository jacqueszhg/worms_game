from move import Move
from worms import *
from game_config import *
from map import *
from game_config import *

class GameState:
    def __init__(self):
        self.map = Map()
        self.map.createMap()
        self.worms = Worms(20, self.map)
        self.worms_ennemy = Worms(750, self.map)
        GameConfig.LIST_WORMS.append(self.worms)
        GameConfig.LIST_WORMS.append(self.worms_ennemy)
        print(GameConfig.LIST_WORMS)



    def draw(self,window):
        window.blit(GameConfig.BACKGROUND_IMG,(0,0))
        self.map.draw(window)
        self.worms.draw(window)
        self.worms_ennemy.draw(window)


    def advance_state(self, next_move,window):
        if GameConfig.PLAY == 0:
            self.worms.advance_state(next_move, self.map, window)
            # recuperer les projectiles du joueur
            for bullet in self.worms.all_bullets:
                vent = random.randrange(-100,100,10)
                bullet.move(window,vent)
            # affiche la bullet
            self.worms.all_bullets.draw(window)
        elif GameConfig.PLAY == 1:
            self.worms_ennemy.advance_state(next_move, self.map, window)
            # recuperer les projectiles du joueur ennemy
            for bullet in self.worms_ennemy.all_bullets:
                bullet.move(window)
            # affiche la bullet
            self.worms_ennemy.all_bullets.draw(window)

