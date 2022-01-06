import time

import pygame

import map
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
        #GameConfig.Y_PLATEFORM = int(map.getPolynome(x))
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


    def draw(self,window):
        window.blit(self.image, self.rect)
        self.displayMessage(window,str(GameConfig.VENT),50,100,100)

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
        GameConfig.Y_PLATEFORM = GameConfig.BLOCKS[self.rect.x].top
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

    def on_ground(self):
        if(self.rect.bottom == GameConfig.Y_PLATEFORM):
            return True
        return False

    def weaponChoice(self,next_move,window):
        if(next_move.carabine):
            self.shoot("carabine",window)
        elif(next_move.rocket):
            self.shoot("rocket",window)
        elif(next_move.grenade):
            self.shoot("grenade",window)

    def shoot(self,weapon,window):
        mouse_pos = pygame.mouse.get_pos()
        if(mouse_pos < (self.rect.x,self.rect.y)):
            pygame.draw.line(window, (255, 0, 0), (self.rect.topleft[0], self.rect.topleft[1]), mouse_pos)
        else:
            pygame.draw.line(window, (255, 0, 0), self.rect.topright, mouse_pos)

        angle = (mouse_pos[0] - self.rect.x + 26, mouse_pos[1] - self.rect.y + 10)

        if self.tirer == False:
            GameConfig.VENT = random.randrange(-50,50,10)
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

    def displayMessage(self,window, text, fontSize, x, y):
        font = pygame.font.Font('assets/font/BradBunR.ttf', fontSize)
        img = font.render("vent" + text, True, (255,255,255))
        displayRect = img.get_rect()
        displayRect.center = (x, y)
        window.blit(img, displayRect)