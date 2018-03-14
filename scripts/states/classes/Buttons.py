import pygame
from pygame import *
from ...Globals import Globals

spritesheet = pygame.image.load("assets/buttons/button-start.png")

character = pygame.Surface((203, 74),pygame.SRCALPHA)   # first line is dimension of the button
character.blit(spritesheet,(0,0))                       # second line is the DISPLACEMENT on the sprite sheet
# character = pygame.transform.scale(character, (203*3,73*3))
startButtonNormal = character

character = pygame.Surface((203,74),pygame.SRCALPHA)
character.blit(spritesheet,(0,-74))
# character = pygame.transform.scale(character, (203*3,147*3))
startButtonHover = character

character = pygame.Surface((203,74),pygame.SRCALPHA)
character.blit(spritesheet,(0,-148))
# character = pygame.transform.scale(character, (203*3,222*3))
startButtonClicked = character

#203, 73, rect of first button

class Buttons(object):
    def __init__(self, x ,y):
        self.image = startButtonNormal
        self.startButton = pygame.transform.scale(self.image, (300, 100))
        self.startButton.convert()

        self.posX = x
        self.posY = y
        self.width = 200
        self.height = 75
        self.rect = Rect(self.posX, self.posY, self.width, self.height)
        self.rect.center = self.posX, self.posY
        self.blitted = False
        self.startPrime = False  # button has been held down
        self.has_message = False # wants to return something to where it has been instantiated

        self.finished = False  # context specific for changing state

    def draw(self, screen):
        screen.blit(self.startButton, (self.posX, self.posY))
        self.blitted = True


    def get_message(self):
        return {
            "finished":self.finished,
            "next":Globals.state
        }

    def get_evt(self, click, event, mouse):

        # mouse over
        if (self.posX + self.width) >= mouse[0] >= self.posX and (self.posY + self.height) >= mouse[1] >= self.posY and not self.startPrime:
            self.image = startButtonHover
            self.startButton = self.image.convert_alpha()

        # mouse back on while held start button
        elif self.startPrime and (self.posX + self.width) >= mouse[0] >= self.posX and (self.posY + self.height) >= mouse[1] >= self.posY:
            self.image = startButtonClicked
            self.startButton = self.image.convert_alpha()
            self.startButton.convert()

        # mouse off
        elif not (self.posX + self.width) >= mouse[0] >= self.posX or not (self.posY + self.height) >= mouse[1] >= self.posY:
            self.image = startButtonNormal
            self.startButton = self.image.convert_alpha()

        #for changing states button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if click[0] == 1 and (self.posX + self.width) >= mouse[0] >= self.posX and (self.posY + self.height) >= mouse[1] >= self.posY:
                self.image = startButtonClicked
                self.startButton = self.image.convert_alpha()
                self.startPrime = True
            elif click[2] == 1:
                print("[MainMenu(STATE)] Rightclick pressed, state revealed as: {0}".format(Globals.state))

        if event.type == pygame.MOUSEBUTTONUP:
            if click[0] == 0 and self.startPrime and (self.posX + self.width) >= mouse[0] >= self.posX and (self.posY + self.height) >= mouse[1] >= self.posY:
                self.has_message = True
                Globals.state = "AVARICE"

                self.next = Globals.state
                print("Start clicked state is now: ", Globals.state)
                self.finished = True
            if self.startPrime:
                self.startPrime = False

        # mouse over
        # if (self.posX + self.width) >= mouse[0] >= self.posX and (self.posY + self.height) >= mouse[1] >= self.posY and not self.startPrime:
        #     self.image = startButtonHover
        #     self.startButton = self.image.convert_alpha()
        #
        # # mouse back on while held start button
        # elif self.startPrime and (self.posX + self.width) >= mouse[0] >= self.posX and (self.posY + self.height) >= mouse[1] >= self.posY:
        #     self.image = startButtonClicked
        #     self.startButton = self.image.convert_alpha()
        #     self.startButton.convert()
        #
        # # mouse off
        # elif not (self.posX + self.width) >= mouse[0] >= self.posX or not (self.posY + self.height) >= mouse[1] >= self.posY:
        #     self.image = startButtonNormal
        #     self.startButton = self.image.convert_alpha()
        #
        # #for changing states button
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if click[0] == 1 and (self.posX + self.width) >= mouse[0] >= self.posX and (self.posY + self.height) >= mouse[1] >= self.posY:
        #         self.image = startButtonClicked
        #         self.startButton = self.image.convert_alpha()
        #         self.startPrime = True
        #     elif click[2] == 1:
        #         print("[MainMenu(STATE)] Rightclick pressed, state revealed as: {0}".format(Globals.state))
        #
        # if event.type == pygame.MOUSEBUTTONUP:
        #     if click[0] == 0 and self.startPrime and (self.posX + self.width) >= mouse[0] >= self.posX and (self.posY + self.height) >= mouse[1] >= self.posY:
        #         self.has_message = True
        #         Globals.state = "AVARICE"
        #
        #         self.next = Globals.state
        #         print("Start clicked state is now: ", Globals.state)
        #         self.finished = True
        #     if self.startPrime:
        #         self.startPrime = False





