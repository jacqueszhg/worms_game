from move import Move
from worms import *
from game_config import *
from map import *
from game_config import *

class GameState:
    def __init__(self):
        self.map = Map()
        self.map.createMap()
        GameConfig.LIST_WORMS.append(Worms(20, self.map))
        GameConfig.LIST_WORMS.append(Worms(500, self.map))
        GameConfig.LIST_WORMS.append(Worms(750, self.map))



    def draw(self,window):
        window.blit(GameConfig.BACKGROUND_IMG,(0,0))
        self.map.draw(window)
        font = pygame.font.SysFont("BradBunRb", 25)
        for i in range(len(GameConfig.LIST_WORMS)):
            GameConfig.LIST_WORMS[i].draw(window)
            life_text = font.render(f"{GameConfig.LIST_WORMS[i].life}", 1, (0, 0, 0))
            if not GameConfig.LIST_WORMS[i].is_dead(i):
                window.blit(life_text, (GameConfig.LIST_WORMS[i].rect.x, GameConfig.LIST_WORMS[i].rect.y - 20))
        for i in range(len(GameConfig.LIST_WORMS)):
            if GameConfig.LIST_WORMS[i].is_dead(i):
                GameConfig.LIST_WORMS_DEAD.append(GameConfig.LIST_WORMS[i])
                GameConfig.LIST_WORMS[i].remove()
                GameConfig.LIST_WORMS[i].image = GameConfig.STANDING_IMG_MORT


    def advance_state(self, next_move,window):
        for j in GameConfig.LIST_WORMS_DEAD:
            j.charge_position()
        for i in range(len(GameConfig.LIST_WORMS)):
            if not GameConfig.LIST_WORMS[i].is_dead(i):
                if GameConfig.PLAY == i:
                    GameConfig.LIST_WORMS[i].advance_state(next_move, self.map, window)
                    # recuperer les projectiles du joueur
                    for bullet in GameConfig.LIST_WORMS[i].all_bullets:
                        bullet.move(window)
                    # affiche la bullet
                    GameConfig.LIST_WORMS[i].all_bullets.draw(window)
                else:
                    GameConfig.LIST_WORMS[i].charge_position()

