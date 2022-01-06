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



    def draw(self,window):
        window.blit(GameConfig.BACKGROUND_IMG,(0,0))
        self.map.draw(window)
        self.worms.draw(window)
        self.worms_ennemy.draw(window)
        font = pygame.font.SysFont("BradBunRb", 25)
        life_text1 = font.render(f"{GameConfig.LIFE1}", 1, (0,0,0))
        life_text2 = font.render(f"{GameConfig.LIFE2}", 1, (0,0,0))
        window.blit(life_text1, (self.worms.rect.x,self.worms.rect.y - 20))
        window.blit(life_text2, (self.worms_ennemy.rect.x,self.worms_ennemy.rect.y - 20))



    def advance_state(self, next_move,window):
        if GameConfig.PLAY == 0:
            self.worms.advance_state(next_move, self.map, window)
            # recuperer les projectiles du joueur
            for bullet in self.worms.all_bullets:
                bullet.move(window)
            # affiche la bullet
            self.worms.all_bullets.draw(window)
        elif GameConfig.PLAY == 1:
            self.worms_ennemy.advance_state(next_move, self.map, window)
            # recuperer les projectiles du joueur ennemy
            for bullet in self.worms_ennemy.all_bullets:
                bullet.move(window)
            # affiche la bullet
            self.worms_ennemy.all_bullets.draw(window)

