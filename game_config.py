import numpy as np
import pygame
import random

class GameConfig:
    WINDOW_H = pygame.display.set_mode().get_size()[1] - 100
    WINDOW_W = pygame.display.set_mode().get_size()[0] - 200
    Y_PLATEFORM = 516
    BLOCKS = {}
    BLOCKS_DETRUIT = []
    BLOCK_W =  int(WINDOW_W/100)
    BLOCK_H =  int(WINDOW_W/100)
    """
    BLOCK2 = [None] * WINDOW_W

    for i in range(len(BLOCK2)):
        tmp = [None] * WINDOW_H
        BLOCK2[i] = tmp
        """

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
    MASSE_MUR = 20
    MASSE_GRENADE = 5
    MASSE_WORMS = 9
    VENT = random.randrange(-10, 10, 2)

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

    def euleur(t,vx,vy,x,y,vxn,vyn,xn,yn,dt):
        vx = dt * vx
        vy = dt * vy
        x = dt * x
        y = dt * y
        vxFin = vxn + vx
        vyFin = vyn + vy
        xFin = xn + x
        yFin = yn + y
        return vxFin,vyFin,xFin,yFin

    def mouvement_pendulaire(t,teta,teta2,l):
        b = 0.4
        return teta2, (b/GameConfig.MASSE_WORMS)*teta2 + (GameConfig.GRAVITY/l**2)*np.sin(teta)

    def displayMessage(window, text, fontSize, x, y):
        font = pygame.font.Font('assets/font/BradBunR.ttf', fontSize)
        img = font.render(text, True, (255, 255, 255))
        displayRect = img.get_rect()
        displayRect.center = (x, y)
        window.blit(img, displayRect)

GameConfig.euleur = staticmethod(GameConfig.euleur)
GameConfig.mouvement_pendulaire = staticmethod(GameConfig.mouvement_pendulaire)
GameConfig.displayMessage = staticmethod(GameConfig.displayMessage)

