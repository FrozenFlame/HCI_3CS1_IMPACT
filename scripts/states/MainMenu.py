import pygame, math, time, random
from enum import Enum, auto

from scripts import tools
from .classes.Buttons import Buttons
from .classes.Player import Player
from .classes.Hero import Hero
from .classes.User import User
from .classes.DeckBuilder import DeckBuilder

from ..Globals import Globals

spritesheet = pygame.image.load("assets\\buttons\\button-start.png")

character = pygame.Surface((203, 74),pygame.SRCALPHA)   # first line is dimension of the button
character.blit(spritesheet,(0,0))                       # second line is the DISPLACEMENT on the sprite sheet
character = pygame.transform.scale(character, (203*3,73*3))
startButtonNormal = character

character = pygame.Surface((203,74),pygame.SRCALPHA)
character.blit(spritesheet,(0,-74))
character = pygame.transform.scale(character, (203*3,74*3))
startButtonHover = character

character = pygame.Surface((203,74),pygame.SRCALPHA)
character.blit(spritesheet,(0,-148))
character = pygame.transform.scale(character, (203*3,74*3))
startButtonClicked = character

khaki = (121, 150, 79)
brown = (122, 104, 58)
class MainMenu(object):
    def __init__(self):
        tools.State.__init__(self)
        self.next = None
        self.buttons = Buttons(Globals.RESOLUTION_X*0.50, Globals.RESOLUTION_Y *0.80)
        self.buttons.posX -= self.buttons.width *0.5
        self.buttons.posY -= self.buttons.height *0.5

        self.buttonHovered = False
        self.hover = False
        self.startPrime = False  # start button has been held down
        self.globals = Globals()

        # logo
        self.logo = pygame.image.load("assets/logo/Avarice-Logo-final.png").convert_alpha()
        self.logo_pos = 0,0

        #background
        self.backdrop = pygame.image.load("assets/logo/backdrop.jpg").convert_alpha()

        self.phase = Phase.MAIN

    def display_text(self, text, screen):
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        textSurf, textRect = self.text_objects(text, largeText)  # Text Surface and Text Rect
        textRect.center = (Globals.RESOLUTION_X * 0.2, Globals.RESOLUTION_Y * 0.2)
        screen.blit(textSurf, textRect)


    def text_objects(self, text, font):
        textSurface = font.render(text, True, (255,255,255))
        return textSurface, textSurface.get_rect()

    def draw(self, screen):
        pygame.draw.rect(screen, brown, (000,000,1280,720))  # background
        # screen.blit(self.backdrop, (0,0))
        self.display_text("good day",screen)
        self.buttons.draw(screen)
        screen.blit(self.logo, self.logo_pos)

    def get_evt(self,event):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if event.type == pygame.QUIT:
            self.done = True
        #animation for the button
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                print ("[MainMenu(STATE)] O button pressed")


        self.buttons.get_evt(click, event, mouse)
        if self.buttons.has_message:
            self.buttons.has_message = False
            self.finished = self.buttons.get_message()["finished"]
            self.next = self.buttons.get_message()["next"]


        #
        # # mouse over
        # if (self.buttons.posX + self.buttons.width) >= mouse[0] >= self.buttons.posX and (self.buttons.posY + self.buttons.height) >= mouse[1] >= self.buttons.posY and not self.startPrime:
        #     self.buttons.image = startButtonHover
        #     self.buttons.startButton = self.buttons.image.convert_alpha()
        #
        # # mouse back on while held start button
        # elif self.startPrime and (self.buttons.posX + self.buttons.width) >= mouse[0] >= self.buttons.posX and (self.buttons.posY + self.buttons.height) >= mouse[1] >= self.buttons.posY:
        #     self.buttons.image = startButtonClicked
        #     self.buttons.startButton = self.buttons.image.convert_alpha()
        #     self.buttons.startButton.convert()
        #
        # # mouse off
        # elif not (self.buttons.posX + self.buttons.width) >= mouse[0] >= self.buttons.posX or not (self.buttons.posY + self.buttons.height) >= mouse[1] >= self.buttons.posY:
        #     self.buttons.image = startButtonNormal
        #     self.buttons.startButton = self.buttons.image.convert_alpha()
        #
        # #for changing states button
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if click[0] == 1 and (self.buttons.posX + self.buttons.width) >= mouse[0] >= self.buttons.posX and (self.buttons.posY + self.buttons.height) >= mouse[1] >= self.buttons.posY:
        #         self.buttons.image = startButtonClicked
        #         self.buttons.startButton = self.buttons.image.convert_alpha()
        #         self.startPrime = True
        #     elif click[2] == 1:
        #         print("[MainMenu(STATE)] Rightclick pressed, state revealed as: {0}".format(Globals.state))
        #
        # if event.type == pygame.MOUSEBUTTONUP:
        #     if click[0] == 0 and self.startPrime and (self.buttons.posX + self.buttons.width) >= mouse[0] >= self.buttons.posX and (self.buttons.posY + self.buttons.height) >= mouse[1] >= self.buttons.posY:
        #         Globals.state = "AVARICE"
        #         self.next = Globals.state
        #         self.finished = True
        #     if self.startPrime:
        #         self.startPrime = False

    def update(self, screen, keys, currentTime, dt):
        self.draw(screen)


    def startup(self, currentTime, persistent):
        '''
        Add variables passed in persistent to the proper attributes and
        set the start time of the State to the current time.
        @ Overwritten portion
        '''
        self.persist = persistent
        self.startTime = currentTime

    def cleanup(self):  # state is finished
        self.done = False

        '''
            TEST ONLY STATIC PERSIST
        '''
        if not Globals.gameStart:  # game is the selected next state
            usera = User("Champion", 99, 0)
            userb = User("Challenger", 0, 0)
            heroa = Hero("Victoria", "this is supposed to be a surface, not a string")
            herob = Hero("King of Beggars", "this is supposed to be a surface, not a string")
            playera = Player(usera, heroa, DeckBuilder.build_deck(""))
            playerb = Player(userb, herob, DeckBuilder.build_deck(""))

            self.persist['playerA'] = playera
            self.persist['playerB'] = playerb
            self.persist['STARTED'] = False  # this is a flag that Engine will use to determine it to set down the pieces in place.
            Globals.gameStart = True

        return self.persist



class Phase(Enum):

    MAIN = auto()
    TO_MAIN = auto()
    TO_HERO = auto()
    HERO_SELECT = auto()

