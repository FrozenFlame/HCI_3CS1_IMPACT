import pygame
from pygame import *

spritesheet = pygame.image.load("D:/Avarice/HCI_3CS1_IMPACT/assets/buttons/button-start-spritesheet.png")

character = pygame.Surface((247,70),pygame.SRCALPHA)
character.blit(spritesheet,(-1,0))
character = pygame.transform.scale(character, (247*3,70*3))
startButtonNormal = character

class Buttons(object):
    def __init__(self):
        self.image = startButtonNormal
        self.startButton = pygame.transform.scale(self.image, (300, 100))
        self.startButton.convert()
        self.posX = 500
        self.posY = 300
        self.width = 300
        self.height = 100
        self.rect = Rect(self.posX, self.posY, self.width, self.height)
        self.blitted = False


    def draw(self, screen):
        screen.blit(self.startButton, (self.posX, self.posY))
        self.blitted = True










