import pygame


class Carabine:
    def __init__(self,window):
        self.window = window

    def shoot(self,x_start,x_end,force):
        pygame.draw.line(self.window,(255,0,0),x_start,x_end)
        keys = pygame.mouse.get_pressed()
        if keys[0] == True:#Clique gauche
            print("je tire")