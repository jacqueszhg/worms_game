import pygame


class GameConfig:
    #TAille de la fenetre de jeux
    WINDOW_H = 640
    WINDOW_W = 960
    Y_PLATEFORM = 510
    WORMS_W = 64
    WORMS_H = 64
    DT = 0.5
    FORCE_LEFT = -20
    FORCE_RIGHT = -FORCE_LEFT
    GRAVITY = 9.81
    FORCE_JUMP = -100

    #Pour les méthodes de pygame qui on besoin que pygame soit initialisé avant
    #donc création d'une fonction init() appeller quand dans le main on fait pygame.init()
    def init():
        GameConfig.BACKGROUND_IMG = pygame.image.load('assets/fond_nuage.jpg')
        GameConfig.BACKGROUND_IMG = pygame.transform.scale(GameConfig.BACKGROUND_IMG,(960,640))
        GameConfig.BRICK_IMG = pygame.image.load('assets/brick_block_mario.png')
        GameConfig.BRICK_IMG = pygame.transform.scale(GameConfig.BRICK_IMG, (100,100))
        GameConfig.SURPRISE_IMG = pygame.image.load('assets/surprise_block_mario.png')
        GameConfig.SURPRISE_IMG = pygame.transform.scale(GameConfig.SURPRISE_IMG, (120,120))
        GameConfig.STANDING_IMG = pygame.image.load('assets/standing.png')

