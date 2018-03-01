import pygame
from scripts import tools
from .classes.Buttons import Buttons
from ..Globals import Globals

spritesheet = pygame.image.load("assets\\buttons\\button-start.png")

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

black = (0,0,0)

class MainMenu(object):
    def __init__(self):
        tools.State.__init__(self)
        self.next = None
        self.buttons = Buttons()
        self.buttonHovered = False
        self.hover = False
        self.startPrime = False  # start button has been held down
        self.globals = Globals()

    def draw(self, screen):
        pygame.draw.rect(screen, black, (000,000,1280,720))  # background
        self.buttons.draw(screen)

    def get_evt(self,event):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if event.type == pygame.QUIT:
            self.done = True
        #animation for the button
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                print ("[MainMenu(STATE)] O button pressed")

        # mouse over
        if (self.buttons.posX + 236) >= mouse[0] >= self.buttons.posX and (self.buttons.posY + self.buttons.height) >= mouse[1] >= self.buttons.posY and not self.startPrime:
            self.buttons.image = startButtonHover
            self.buttons.startButton = self.buttons.image.convert_alpha()

        # mouse back on while held start button
        elif self.startPrime and (self.buttons.posX + 236) >= mouse[0] >= self.buttons.posX and (self.buttons.posY + self.buttons.height) >= mouse[1] >= self.buttons.posY:
            self.buttons.image = startButtonClicked
            self.buttons.startButton = self.buttons.image.convert_alpha()
            self.buttons.startButton.convert()

        # mouse off
        elif not (self.buttons.posX + 240) >= mouse[0] >= self.buttons.posX or not (self.buttons.posY + self.buttons.height) >= mouse[1] >= self.buttons.posY:
            self.buttons.image = startButtonNormal
            self.buttons.startButton = self.buttons.image.convert_alpha()

        #for changing states button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if click[0] == 1 and (self.buttons.posX + 240) >= mouse[0] >= self.buttons.posX and (self.buttons.posY + self.buttons.height) >= mouse[1] >= self.buttons.posY:
                self.buttons.image = startButtonClicked
                self.buttons.startButton = self.buttons.image.convert_alpha()
                self.startPrime = True
            elif click[2] == 1:
                print("[MainMenu(STATE)] Rightclick pressed, state revealed as: {0}".format(Globals.state))

        if event.type == pygame.MOUSEBUTTONUP:
            if click[0] == 0 and self.startPrime and (self.buttons.posX + 240) >= mouse[0] >= self.buttons.posX and (self.buttons.posY + self.buttons.height) >= mouse[1] >= self.buttons.posY:
                Globals.state = "AVARICE"
                self.next = Globals.state
                self.finished = True
            if self.startPrime:
                self.startPrime = False

    def update(self, screen, keys, currentTime, dt):
        self.draw(screen)

        pass

    def startup(self, currentTime, persistent):
        '''
        Add variables passed in persistent to the proper attributes and
        set the start time of the State to the current time.
        @ Overwritten portion
        '''
        self.persist = persistent
        self.startTime = currentTime

    def cleanup(self):
        self.done = False
        return self.persist


