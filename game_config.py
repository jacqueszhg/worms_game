import numpy as np
import pygame
import random

class GameConfig:
    #Récupération de la dimension d'écran de l'utilisateur
    WINDOW_H = pygame.display.set_mode().get_size()[1] - 100
    WINDOW_W = pygame.display.set_mode().get_size()[0] - 200

    #La plateforme sur lequel peut marcher notre worms
    Y_PLATEFORM = 516

    #Tableau qui contient les block de notre jeux
    BLOCKS = {}
    BLOCKS_DETRUIT = []

    #Dimension de nos blocks
    BLOCK_W =  int(WINDOW_W/100)
    BLOCK_H =  int(WINDOW_W/100)

    #Dimensio des blocks mur
    MUR = []
    MUR_H = 25
    MUR_W = 25

    #Dimension du worms
    WORMS_H = 35
    WORMS_W = 32

    #L'intervalle de temps pour mettre en oeuvre la force de la gravité
    DT = 0.5
    GRAVITY = 9.81

    #Variable pour le worms
    FORCE_LEFT = -20 #distance : déplacement à gauche
    FORCE_RIGHT = -FORCE_LEFT #distance : déplacement à gauche
    FORCE_JUMP = -70 #hauteur de saut
    WORMS_DROIT = True #connaitre la direction du worms

    #Contient nos womrs qui jouent
    LIST_WORMS = []
    PLAY = 0
    MASSE_MUR = 20
    MASSE_GRENADE = 5
    MASSE_WORMS = 9
    VENT = random.randrange(-10, 10, 2)

    """
    Chargement des images utilile pour le jeux
    """
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

    """
    Fonction de euleur pour résoudre des équations diférentielle
    """
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

    """
    Fonction pour afficher du texte sur l'écran
    """
    def displayMessage(window, text, fontSize, x, y):
        font = pygame.font.Font('assets/font/BradBunR.ttf', fontSize)
        img = font.render(text, True, (255, 255, 255))
        displayRect = img.get_rect()
        displayRect.center = (x, y)
        window.blit(img, displayRect)

    """
    Calcule du pgcd
    """
    def pgcd(a,b):
        d = 1
        while a != b:
            d = abs(b - a)
            b = a
            a = d
        return d

GameConfig.euleur = staticmethod(GameConfig.euleur)
GameConfig.displayMessage = staticmethod(GameConfig.displayMessage)
GameConfig.pgcd = staticmethod(GameConfig.pgcd)
