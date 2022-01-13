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
        self.vx = 0
        self.vy = 0
        self.temp = 0
        self.all_bullets = pygame.sprite.Group()
        self.tirer = False
        self.life = 100
        self.arme_corde_ninja = False
        self.corde = 0

        self.x0 = -10
        self.y0 = -10
        self.jouer = False

    def draw(self,window):
        window.blit(self.image, self.rect)
        GameConfig.displayMessage(window,"vent "+str(GameConfig.VENT),50,100,100)

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

        # Vitesse
        self.vx = fx * GameConfig.DT
        if self.on_ground():
            self.vy = fy * GameConfig.DT
        else:
            self.vy = self.vy + GameConfig.GRAVITY * GameConfig.DT

        # Position
        self.rect = self.rect.move(self.vx * GameConfig.DT, self.vy * GameConfig.DT)

        x = self.rect.left
        vx_min = (-x + (GameConfig.MUR_W-15))/ GameConfig.DT #peut pas sortit de l'écran à gauche
        vx_max = ( GameConfig.WINDOW_W- GameConfig.MUR_W-GameConfig.WORMS_W - x) / GameConfig.DT #peut pas sortir de l'écran à droite
        self.vx = min(self.vx, vx_max)

        y = self.rect.top
        #GameConfig.Y_PLATEFORM = GameConfig.BLOCKS[self.rect.left].top
        #GameConfig.Y_PLATEFORM = map.f(self.rect.left)
        #GameConfig.Y_PLATEFORM = int(map.getPolynome(self.rect.left))
        #GameConfig.Y_PLATEFORM = GameConfig.BLOCKS[self.rect.x].top
        GameConfig.Y_PLATEFORM = GameConfig.BLOCKS[self.rect.x][0].top
        """
        for i in range (0,GameConfig.WINDOW_H):
            if GameConfig.BLOCK2[self.rect.x][i] != None:
                if (GameConfig.BLOCK2[self.rect.x][i].y > GameConfig.Y_PLATEFORM):
                    GameConfig.Y_PLATEFORM = GameConfig.BLOCK2[self.rect.x][i].y
        """

        """
        collision = False
        indice = 0
        while collision == False:
            if GameConfig.BLOCKS[indice][0] == self.rect[0] and GameConfig.BLOCKS[indice].top == self.rect.bottom:
                print("colission : ", GameConfig.BLOCKS[indice],self.rect)
                GameConfig.Y_PLATEFORM = GameConfig.BLOCKS[indice][1]
                collision = True
            if(indice < len(GameConfig.BLOCKS) - 1):
                indice = indice + 1
            else:
                collision = True
        """

        vy_max = (GameConfig.Y_PLATEFORM - GameConfig.WORMS_H - y) / GameConfig.DT

        self.vy = min(self.vy, vy_max)
        self.vx = max(self.vx, vx_min)

        self.rect = self.rect.move(self.vx * GameConfig.DT, self.vy * GameConfig.DT)

        if self.arme_corde_ninja == True:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                pointA = [self.rect.x, self.rect.y]
                pointB = self.corde.rect
                vecteurAB = [(pointB[0] - pointA[0]), (pointB[1] - pointA[1])]
                self.rect.x = (self.rect.x + vecteurAB[0]/2)
                self.rect.y = (self.rect.y + vecteurAB[1]/2)
                """
                b = -vecteurAB[0]
                if (b == 0):
                    b = 1
                a = vecteurAB[1]
                c = -(a * pointB[0]) - (b * pointB[1])
                self.rect.y = (-(a * x) - c) / b
                """
            if keys[pygame.K_s]:
                print("descen")

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

        angle = (mouse_pos[0] - self.rect.x + 26, mouse_pos[1] - self.rect.y + 10)

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
            if pygame.mouse.get_pressed()[0] == True and len(self.all_bullets) == 0:
                self.corde = Bullet(10, GameConfig.BULLET_CORDE_NINJA_IMG, self, mouse_pos, weapon, angle, GameConfig.VENT)
                #self.all_bullets.add(Bullet(10, GameConfig.BULLET_CORDE_NINJA_IMG, self, mouse_pos, weapon,angle,GameConfig.VENT))
                self.all_bullets.add(self.corde)
                self.tirer = False
                self.x0 = self.rect.x
                self.y0 = self.rect.y
                self.arme_corde_ninja = True

            else:
                Bullet(10, GameConfig.BULLET_CORDE_NINJA_IMG, self, mouse_pos, weapon,angle,GameConfig.VENT).draw(window)

    def is_dead(self):
        if self.life <= 0 or self.rect.bottom >= GameConfig.WINDOW_H:
            return True
        return False

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
        """
        a = -10
        for i in range (0,GameConfig.WINDOW_H,GameConfig.BLOCK_H):
            if GameConfig.BLOCK2[self.rect.x][i] != None:
                if (GameConfig.BLOCK2[self.rect.x][i].y > a):
                    a = GameConfig.BLOCK2[self.rect.x][i].y
        """

        """
        collision = False
        indice = 0
        while collision == False:
            if GameConfig.BLOCKS[indice][0] == self.rect[0] and GameConfig.BLOCKS[indice].top == self.rect.bottom:
                print("colission : ", GameConfig.BLOCKS[indice],self.rect)
                GameConfig.Y_PLATEFORM = GameConfig.BLOCKS[indice][1]
                collision = True
            if(indice < len(GameConfig.BLOCKS) - 1):
                indice = indice + 1
            else:
                collision = True
        """

        vy_max = (a - GameConfig.WORMS_H - y) / GameConfig.DT

        self.vy = min(self.vy, vy_max)
        self.vx = max(self.vx, vx_min)

        self.rect = self.rect.move(self.vx * GameConfig.DT, self.vy * GameConfig.DT)

