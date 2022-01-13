import time

import pygame

import map
from bullet import Bullet
from game_config import *
from map import *
from bullet import *

class Worms(pygame.sprite.Sprite):
    LEFT = -1
    RIGHT = 1
    NONE = 0
    PLAY = 0


    def __init__(self,x, map):
        pygame.sprite.Sprite.__init__(self)
        GameConfig.Y_PLATEFORM = int(map.getPolynome(x))
        self.rect = pygame.Rect(x,
                                GameConfig.Y_PLATEFORM - GameConfig.WORMS_H,
                                GameConfig.WORMS_W,
                                GameConfig.WORMS_H)
        self.image = GameConfig.STANDING_IMG_DROIT

        #initialisation de la vitesse
        self.vx = 0
        self.vy = 0

        #Initialisation d'un temp pour faire tourner les images
        self.temp = 0

        #Liste qui va contenir les projectiles tirer par le worms
        self.all_bullets = pygame.sprite.Group()
        self.tirer = False
        self.life = 100
        self.arme_corde_ninja = False
        self.corde = 0

        #Variable
        self.anxienXCorde = -10
        self.ancienYCorde = -10

        #Variable d'état du worms
        self.jouer = False
        self.mort = False

    """
    Fonction qui déssine notre worms à l'écran
    """
    def draw(self,window):
        window.blit(self.image, self.rect)
        font = pygame.font.SysFont("BradBunRb", 25)
        if self.mort == False:
            life_text = font.render(f"{self.life}", 1, (0, 0, 0))
            window.blit(life_text, (self.rect.x, self.rect.y - 20))

    """
    Fonction qui modélise la trajectoire d'une pendule, utilisable pour réaliser la corde ninja
    """
    def equationCorde(self,t,teta,teta2):
        return teta2, ((-0.4/GameConfig.MASSE_WORMS)*teta2) - ((GameConfig.GRAVITY/20)*np.sin(teta))

    """
    Modélsation du déplaccement du worms lorsqu'il utilise la corde ninja
    """
    def moveCordeNinja(self):
        #Permet au worms de rester sur la corde
        self.rect.x = self.anxienXCorde
        self.rect.y = self.ancienYCorde

        for b in self.all_bullets:
            #On ne peut se déplacer avec la corde que si elle s'est accroché à un mur
            if b.toucherMur == True:
                keys = pygame.key.get_pressed()

                #Utilsation du vecteur directeur de la droite formé par le womrs et le point d'attache de la corde
                pointA = [self.rect.x, self.rect.y]
                pointB = self.corde.rect
                vecteurAB = [(pointB[0] - pointA[0]), (pointB[1] - pointA[1])]

                #Calcule d'un pgcd pour avoir le vecteur directeur de la droite la plus petite possible
                pgcd = GameConfig.pgcd(vecteurAB[0], vecteurAB[1])

                #On monte sur la corde
                if keys[pygame.K_e]:
                    self.rect.x = self.rect.x + (vecteurAB[0]/pgcd)
                    self.rect.y = self.rect.y + (vecteurAB[1]/pgcd)
                    self.anxienXCorde = self.rect.x
                    self.ancienYCorde = self.rect.y
                #On descend sur la corde
                if keys[pygame.K_s]:
                    self.rect.x = self.rect.x - (vecteurAB[0]/pgcd)
                    self.rect.y = self.rect.y - (vecteurAB[1]/pgcd)
                    self.anxienXCorde = self.rect.x
                    self.ancienYCorde = self.rect.y

    """
    Fonction, mouvement basique du worms sur le sol, déplacement gauche, droite et saut
    """
    def moveClassique(self,fx,fy):
        # Vitesse du worms sur le déplacement horizontale
        self.vx = fx * GameConfig.DT

        # On détermine si le worms est sur le sol, si oui on peut sauter
        # Lorsqu'il saute il est summit à la gravité
        if self.on_ground():
            self.vy = fy * GameConfig.DT
        else:
            self.vy = self.vy + GameConfig.GRAVITY * GameConfig.DT

        # Position
        #Déplacement du womrs en X
        self.rect = self.rect.move(self.vx * GameConfig.DT, self.vy * GameConfig.DT)
        x = self.rect.left
        vx_min = (-x + (GameConfig.MUR_W-15))/ GameConfig.DT #peut pas sortit de l'écran à gauche
        vx_max = ( GameConfig.WINDOW_W- GameConfig.MUR_W-GameConfig.WORMS_W - x) / GameConfig.DT #peut pas sortir de l'écran à droite
        self.vx = min(self.vx, vx_max)

        y = self.rect.top

        #Position du worms en Y
        GameConfig.Y_PLATEFORM = GameConfig.BLOCKS[self.rect.x][0].top
        vy_max = (GameConfig.Y_PLATEFORM - GameConfig.WORMS_H - y) / GameConfig.DT
        self.vy = min(self.vy, vy_max)
        self.vx = max(self.vx, vx_min)
        self.rect = self.rect.move(self.vx * GameConfig.DT, self.vy * GameConfig.DT)

    """
    Fonction qui change l'état du worms
    """
    def advance_state(self, next_move,map,window):
        # Acceleration
        fx = 0
        fy = 0
        if next_move.left:
            clock = time.time()
            if(clock-self.temp < 0.2):
                fx = GameConfig.FORCE_LEFT
                self.image = GameConfig.STANDING_IMG_GAUCHE
            elif(clock-self.temp < 0.4):
                fx = GameConfig.FORCE_LEFT
                self.image = GameConfig.WALK_LEFT_IMG1
            elif(clock-self.temp < 0.6):
                fx = GameConfig.FORCE_LEFT
                self.image = GameConfig.WALK_LEFT_IMG2
            else:
                self.temp = time.time()
                self.image = GameConfig.STANDING_IMG_GAUCHE
                GameConfig.WORMS_DROIT = False
        elif next_move.right:
            clock = time.time()
            if(clock-self.temp < 0.2):
                fx = GameConfig.FORCE_RIGHT
                self.image = GameConfig.STANDING_IMG_DROIT
            elif(clock-self.temp < 0.4):
                fx = GameConfig.FORCE_RIGHT
                self.image = GameConfig.WALK_RIGHT_IMG1
            elif(clock-self.temp < 0.6):
                fx = GameConfig.FORCE_RIGHT
                self.image = GameConfig.WALK_RIGHT_IMG2
            else:
                self.temp = time.time()
                self.image = GameConfig.STANDING_IMG_DROIT
            GameConfig.WORMS_DROIT = True
        else:
            if(GameConfig.WORMS_DROIT):
                self.image = GameConfig.STANDING_IMG_DROIT
            else:
                self.image = GameConfig.STANDING_IMG_GAUCHE

        if next_move.jump:
                fy = GameConfig.FORCE_JUMP
                if(GameConfig.WORMS_DROIT):
                    self.image = GameConfig.WALK_JUMP_IMG_DROIT
                else:
                    self.image = GameConfig.WALK_JUMP_IMG_GAUCHE

        self.weaponChoice(next_move,window)
        if self.arme_corde_ninja != True:
            self.moveClassique(fx, fy)
        else:
            self.moveCordeNinja()

        self.is_dead()

    def on_ground(self):
        if(self.rect.bottom == GameConfig.Y_PLATEFORM):
            return True
        return False

    def weaponChoice(self,next_move,window):
        if(next_move.carabine):
            self.arme_corde_ninja = False
            self.shoot("carabine",window)
        elif(next_move.rocket):
            self.arme_corde_ninja = False
            self.shoot("rocket",window)
        elif(next_move.grenade):
            self.arme_corde_ninja = False
            self.shoot("grenade",window)
        elif next_move.corde_ninja:
            self.arme_corde_ninja = True
            self.shoot("corde_ninja",window)

    def shoot(self,weapon,window):
        mouse_pos = pygame.mouse.get_pos()
        if(mouse_pos < (self.rect.x,self.rect.y)):
            pygame.draw.line(window, (255, 0, 0), (self.rect.topleft[0], self.rect.topleft[1]), mouse_pos)
        else:
            pygame.draw.line(window, (255, 0, 0), self.rect.topright, mouse_pos)


        angle = [mouse_pos[0] - self.rect.x + 26, mouse_pos[1] - self.rect.y + 10]

        if self.tirer == False:
            GameConfig.VENT = random.randrange(-10,10,2)
            self.tirer = True

        if(weapon == "carabine"):
            if pygame.mouse.get_pressed()[0] == True and len(self.all_bullets) == 0:
                self.all_bullets.add(Bullet(10,GameConfig.BULLET_CARABINE_IMG,self,mouse_pos, weapon,angle,GameConfig.VENT))
                self.tirer = False
            else:
                Bullet(10, GameConfig.BULLET_CARABINE_IMG, self, mouse_pos, weapon,angle,GameConfig.VENT).draw(window)
            #self.bullet = Bullet(10,GameConfig.BULLET_CARABINE_IMG,self,mouse_pos)
        elif(weapon == "rocket"):
            if pygame.mouse.get_pressed()[0] == True and len(self.all_bullets) == 0:
                self.all_bullets.add(Bullet(10, GameConfig.BULLET_ROCKET_IMG, self, mouse_pos, weapon,angle,GameConfig.VENT))
                self.tirer = False
            else:
                Bullet(10, GameConfig.BULLET_ROCKET_IMG, self, mouse_pos, weapon,angle,GameConfig.VENT).draw(window)
        elif weapon == "grenade":
            if pygame.mouse.get_pressed()[0] == True and len(self.all_bullets) == 0:
                self.all_bullets.add(Bullet(10, GameConfig.BULLET_GRENADE_IMG, self, mouse_pos, weapon,angle,GameConfig.VENT))
                self.tirer = False
            else:
                Bullet(10, GameConfig.BULLET_GRENADE_IMG, self, mouse_pos, weapon,angle,GameConfig.VENT).draw(window)
        elif weapon == "corde_ninja":
            self.anxienXCorde = self.rect.x
            self.ancienYCorde = self.rect.y
            self.arme_corde_ninja = True
            if pygame.mouse.get_pressed()[0] == True and len(self.all_bullets) == 0:
                self.corde = Bullet(10, GameConfig.BULLET_CORDE_NINJA_IMG, self, mouse_pos, weapon, angle, GameConfig.VENT)
                #self.all_bullets.add(Bullet(10, GameConfig.BULLET_CORDE_NINJA_IMG, self, mouse_pos, weapon,angle,GameConfig.VENT))
                self.all_bullets.add(self.corde)
                self.tirer = False
            else:
                Bullet(10, GameConfig.BULLET_CORDE_NINJA_IMG, self, mouse_pos, weapon,angle,GameConfig.VENT).draw(window)


    # Methode qui retourne True si le worms est mort et retourne False si il est vivant
    def is_dead(self):
        if self.life <= 0 or self.rect.bottom >= GameConfig.WINDOW_H:
            self.image = GameConfig.STANDING_IMG_MORT
            self.rect.update(self.rect.left,self.rect.top,0,0)
            self.mort = True
    def charge_position(self):

        # Vitesse
        self.vx = 1 * GameConfig.DT
        if self.on_ground():
            self.vy = 1 * GameConfig.DT
        else:
            self.vy = self.vy + GameConfig.GRAVITY * GameConfig.DT

        # Position
        self.rect = self.rect.move(self.vx * GameConfig.DT, self.vy * GameConfig.DT)

        x = self.rect.left
        vx_min = (-x + (GameConfig.MUR_W-15))/ GameConfig.DT #peut pas sortit de l'écran à gauche
        vx_max = ( GameConfig.WINDOW_W- GameConfig.MUR_W-GameConfig.WORMS_W - x) / GameConfig.DT #peut pas sortir de l'écran à droite
        self.vx = min(self.vx, vx_max)

        y = self.rect.top
        a = GameConfig.BLOCKS[self.rect.x][0].top


        vy_max = (a - GameConfig.WORMS_H - y) / GameConfig.DT

        self.vy = min(self.vy, vy_max)
        self.vx = max(self.vx, vx_min)

        self.rect = self.rect.move(self.vx * GameConfig.DT, self.vy * GameConfig.DT)

