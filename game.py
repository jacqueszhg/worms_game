import pygame
from game_config import *
from game_state import *
from move import *


def game_loop(window):
    quitting = False
    game_state = GameState()
    fin = 0
    while not quitting and fin == 0:
        game_state.draw(window)
        souris(window)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                quitting = True
        next_move = get_next_move()
        fin = game_state.advance_state(next_move,window)
        pygame.time.delay(50)
        pygame.display.update()
    return fin


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
    elif keys[pygame.K_3]:
        next_move.grenade = True
    elif keys[pygame.K_4]:
        next_move.corde_ninja = True


    return next_move

def souris(window):
    pygame.mouse.set_visible(False)
    cursor = GameConfig.CURSOR_IMG.get_rect()
    # in your main loop update the position every frame and blit the image
    cursor.center = pygame.mouse.get_pos()  # update position
    window.blit(GameConfig.CURSOR_IMG, cursor)  # draw the cursor

def resetGame():
    GameConfig.LIST_WORMS = []
    GameConfig.LIST_WORMS_DEAD = []
    GameConfig.BLOCKS = {}
    GameConfig.BLOCKS_DETRUIT = {}
    GameConfig.PLAY = 0

# Fonction principale
def main() :
    #initialise pygame
    pygame.init()
    GameConfig.init()


    # initialise la fenetre
    window = pygame.display.set_mode((GameConfig.WINDOW_W, GameConfig.WINDOW_H))
    pygame.display.set_caption("Worms")

    rejouer = 1
    #lance le jeux avec les images
    while rejouer == 1:
        rejouer = game_loop(window)
        resetGame()


    #quuitte le jeux
    pygame.quit()
    quit()


# Lancement de la fonction principale
main()
