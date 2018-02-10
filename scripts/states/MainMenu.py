import pygame
from scripts import tools
from .classes.Buttons import Buttons
from ..Globals import Globals

spritesheet = pygame.image.load("assets\\buttons\\button-start-spritesheet.png")

character = pygame.Surface((247,70),pygame.SRCALPHA)
character.blit(spritesheet,(-1,0))
character = pygame.transform.scale(character, (247*3,70*3))
startButtonNormal = character

character = pygame.Surface((263,72),pygame.SRCALPHA)
character.blit(spritesheet,(1,-72))
character = pygame.transform.scale(character, (263*3,72*3))
startButtonHover = character

character = pygame.Surface((263,72),pygame.SRCALPHA)
character.blit(spritesheet,(1,-143))
character = pygame.transform.scale(character, (263*3,72*3))
startButtonClicked = character

black = (0,0,0)

class MainMenu(object):
    def __init__(self):
        tools.State.__init__(self)
        self.next = None
        self.buttons = Buttons()
        self.buttonHovered = False
        self.hover = False
        self.globals = Globals()

    def draw(self, screen):
        pygame.draw.rect(screen, black, (500,300,245,100))
        self.buttons.draw(screen)

    def get_evt(self,event):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if event.type == pygame.QUIT:
            self.done = True
            #animation for the button
        if (self.buttons.posX + 236) >= mouse[0] >= self.buttons.posX and (self.buttons.posY + self.buttons.height) >= mouse[1] >= self.buttons.posY:
            self.buttons.image = startButtonHover
            self.buttons.startButton = pygame.transform.scale(self.buttons.image, (self.buttons.width, self.buttons.height)).convert_alpha()


        elif not (self.buttons.posX + 240) >= mouse[0] >= self.buttons.posX and (self.buttons.posY + self.buttons.height) >= mouse[1] >= self.buttons.posY:
            self.buttons.image = startButtonNormal
            self.buttons.startButton = pygame.transform.scale(self.buttons.image,(self.buttons.width, self.buttons.height)).convert_alpha()

            #for changing states button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if click[0] == 1 and (self.buttons.posX + 240) >= mouse[0] >= self.buttons.posX and (self.buttons.posY + self.buttons.height) >= mouse[1] >= self.buttons.posY:
                self.buttons.image = startButtonClicked
                self.buttons.startButton = pygame.transform.scale(self.buttons.image,(self.buttons.width, self.buttons.height)).convert_alpha()
                self.buttons.startButton.convert()
                Globals.state = "AVARICE"
                self.next = Globals.state
                self.finished = True

            elif click[2] == 1:
                print(Globals.state)

        if event.type == pygame.MOUSEBUTTONUP:
            pass

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


