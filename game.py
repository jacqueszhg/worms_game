# import des modules et des autres fichiers
import pygame
from game_config import *

## En dessous les fonctions utiles pour la gestion du jeu (affichage de message, rejouer, etc.)

# Boucle de jeu
from game_state import *
from move import *


def game_loop(window):
    quitting = False
    game_state = GameState()
    while not quitting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
        next_move = get_next_move()
        game_state.advance_state(next_move)
        pygame.time.delay(15)
        game_state.draw(window)
        pygame.display.update()


def get_next_move():
    next_move = Move()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        next_move.right = True
    if keys[pygame.K_LEFT]:
        next_move.left = True
    if keys[pygame.K_UP]:
        next_move.jump = True
    return next_move

# Fonction principale
def main():
    #Initialisation de l'outil pygame
    pygame.init()
    #Met en place le background
    GameConfig.init()

    #Initialisation de la fenetre de jeux, avec son nom
    window = pygame.display.set_mode((GameConfig.WINDOW_W,GameConfig.WINDOW_H))
    pygame.display.set_caption("Worms")
    #Lance le jeux
    game_loop(window)
    #Ferme pygame proprement
    pygame.quit()
    #Ferme python proprement
    quit()


# Lancement de la fonction principale
main()