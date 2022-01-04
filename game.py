import pygame
from game_config import *
from game_state import *
from move import *


def game_loop(window):
    quitting = False
    game_state = GameState()
    while not quitting :
        game_state.draw(window)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                quitting = True
        next_move = get_next_move()
        game_state.advance_state(next_move,window)
        pygame.time.delay(50)
        pygame.display.update()


def get_next_move():
    next_move = Move()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        next_move.right = True
    if keys[pygame.K_q]:
        next_move.left = True
    if keys[pygame.K_z] or keys[pygame.K_SPACE]:
        next_move.jump = True
    if keys[pygame.K_1]:
        next_move.carabine = True
    elif keys[pygame.K_2]:
        next_move.rocket = True

    return next_move


# Fonction principale
def main() :
    #initialise pygame
    pygame.init()
    GameConfig.init()

    #initialise la fenetre
    window = pygame.display.set_mode((GameConfig.WINDOW_W, GameConfig.WINDOW_H))
    pygame.display.set_caption("Worms")

    #lance le jeux avec les images
    game_loop(window)

    #quuitte le jeux
    pygame.quit()
    quit()


# Lancement de la fonction principale
main()
