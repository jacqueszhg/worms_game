import pygame


class GameConfig:
    #TAille de la fenetre de jeux
    WINDOW_H = 650
    WINDOW_W = 1000
    Y_PLATEFORM = 550
    LISTE_BLOCK = []
    WORMS_W = 32
    WORMS_H = 25
    BLOCK_W = 50
    BLOCK_H = 50
    DT = 0.5
    FORCE_LEFT = -20
    FORCE_RIGHT = -FORCE_LEFT
    GRAVITY = 9.81
    FORCE_JUMP = -100

    #Pour les méthodes de pygame qui on besoin que pygame soit initialisé avant
    #donc création d'une fonction init() appeller quand dans le main on fait pygame.init()
    def init():
        GameConfig.BACKGROUND_IMG = pygame.image.load('assets/fond/fond_nuage.jpg')
        GameConfig.BACKGROUND_IMG = pygame.transform.scale(GameConfig.BACKGROUND_IMG,(1000,650))
        GameConfig.BRICK_IMG = pygame.image.load('assets/block/brick_block_mario.png')
        GameConfig.BRICK_IMG = pygame.transform.scale(GameConfig.BRICK_IMG,(50,50))
        GameConfig.SURPRISE_IMG = pygame.image.load('assets/block/surprise_block_mario.png')
        GameConfig.SURPRISE_IMG = pygame.transform.scale(GameConfig.SURPRISE_IMG,(50,50))
        GameConfig.DIRT_UP_IMG = pygame.image.load('assets/block/dirt_block_Up.png')
        GameConfig.DIRT_UP_IMG = pygame.transform.scale(GameConfig.DIRT_UP_IMG,(50,50))
        GameConfig.DIRT_DOWN_IMG = pygame.image.load('assets/block/dirt_block_Down.png')
        GameConfig.DIRT_DOWN_IMG = pygame.transform.scale(GameConfig.DIRT_DOWN_IMG,(50,50))
        GameConfig.STATIC_LEFT_IMG = pygame.image.load('assets/worms/worms_statique.png')


