import pygame
import random

class GameConfig:
    WINDOW_H = 1080
    WINDOW_W = 1920
    Y_PLATEFORM = 516
    #BLOCKS = []
    BLOCKS = {}
    BLOCKS_DETRUIT = []
    MUR = []
    MUR_H = 25
    MUR_W = 25
    WORMS_H = 35
    WORMS_W = 32
    DT = 0.5
    FORCE_LEFT = -20
    FORCE_RIGHT = -FORCE_LEFT
    GRAVITY = 9.81
    FORCE_JUMP = -70
    WORMS_DROIT = True
    LIST_WORMS = []
    LIST_WORMS_DEAD = []
    PLAY = 0
    LIFE1 = 100
    LIFE2 = 100
    MASSE_MUR = 20
    MASSE_GRENADE = 5
    VENT = random.randrange(-20, 20, 2)



    def init():

        GameConfig.BACKGROUND_IMG = pygame.image.load('assets/fond/fond_nuage.jpg')
        GameConfig.BACKGROUND_IMG = pygame.transform.scale(GameConfig.BACKGROUND_IMG,(GameConfig.WINDOW_W,GameConfig.WINDOW_H))

        GameConfig.CURSOR_IMG = pygame.image.load('assets/cursor.png')
        GameConfig.CURSOR_IMG = pygame.transform.scale(GameConfig.CURSOR_IMG,(15,15))

        GameConfig.STANDING_IMG_GAUCHE = pygame.image.load('assets/worms/worms_statique.png')
        GameConfig.STANDING_IMG_DROIT = pygame.transform.flip(GameConfig.STANDING_IMG_GAUCHE,True,False)

        GameConfig.WALK_LEFT_IMG1 = pygame.image.load('assets/worms/worms_move1.png')
        GameConfig.WALK_LEFT_IMG2 = pygame.image.load('assets/worms/worms_move2.png')

        GameConfig.WALK_RIGHT_IMG1 = pygame.transform.flip(GameConfig.WALK_LEFT_IMG1,True,False)
        GameConfig.WALK_RIGHT_IMG2 = pygame.transform.flip(GameConfig.WALK_LEFT_IMG2,True,False)

        GameConfig.WALK_JUMP_IMG_GAUCHE = pygame.image.load('assets/worms/worms_jump1.png')
        GameConfig.WALK_JUMP_IMG_DROIT = pygame.transform.flip(GameConfig.WALK_JUMP_IMG_GAUCHE,True,False)

        GameConfig.DIRT_BLOCK_IMG = pygame.image.load('assets/block/dirt_block_Down.png')
        GameConfig.DIRT_BLOCK_IMG = pygame.transform.scale(GameConfig.DIRT_BLOCK_IMG,(20,10))

        GameConfig.BULLET_CARABINE_IMG = pygame.image.load('assets/bullet/bullet_carabine.png')
        GameConfig.BULLET_CARABINE_IMG = pygame.transform.scale(GameConfig.BULLET_CARABINE_IMG,(15,15))

        GameConfig.BULLET_ROCKET_IMG = pygame.image.load('assets/bullet/bullet_rocket.png')
        GameConfig.BULLET_ROCKET_IMG = pygame.transform.scale(GameConfig.BULLET_ROCKET_IMG,(15,15))

        GameConfig.BULLET_GRENADE_IMG = pygame.image.load('assets/bullet/bullet_grenade.png')
        GameConfig.BULLET_GRENADE_IMG = pygame.transform.scale(GameConfig.BULLET_GRENADE_IMG,(15,15))

        GameConfig.BULLET_CORDE_NINJA_IMG = pygame.image.load('assets/bullet/bullet_corde_ninja.png')
        GameConfig.BULLET_CORDE_NINJA_IMG = pygame.transform.scale(GameConfig.BULLET_CORDE_NINJA_IMG,(30,25))

        GameConfig.STANDING_IMG_MORT = pygame.image.load('assets/worms/worms_mort.png')

