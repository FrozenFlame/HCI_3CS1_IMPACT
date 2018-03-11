import pygame, random
from ...Globals import Globals

class Board(object):
    def __init__(self):
        # graphics related
        self.posX = 0.0
        self.posY = 0.0
        self.specialEffects = None # a class which is responsible for spawning certain graphics like smoke fire rain coins etc. which are temporary
        self.coin = self.Coin() # coin held by dummyboard
        self.animating = False
        self.img = pygame.image.load("assets\\board\\DemoGameboard.png").convert_alpha() #img converted
        self.endTurnImg = None # image of turn end button
        self.handButtonImg = None # image of "show hand" button. for multiplayer purposes.
        self.pauseImg = None # when a player decides to access the menu w/ Esc
        self.phaseImg = None # image that flies by when a player is about to take a turn (accompanied with some text)
        self.previewCard = None # big card to the right, duplicates appearance of card being moused over.
        self.hasPreviewCard = False
        # game related
        self.player1 = None # player class
        self.player2 = None # player class
        self.hand1 = None
        self.hand2 = None
        self.deck1 = None
        self.deck2 = None
        self.grave1 = None
        self.grave2 = None

        # Row Lists for fields (from the bottom)
        self.row1 = [] # bottom most - player's back row
        self.row2 = []
        self.row3 = []
        self.row4 = [] # top most - opponent's back row

    def draw(self, screen):
        screen.blit(self.img, (self.posX, self.posY))
        self.blitted = True # currently was an experiment only.
        if self.hasPreviewCard and not self.previewCard.flipAnimating:
            # tempC = self.previewCard.img.scale(self.previewCard.height*1.5, self.previewCard.width*1.5)
            # tempC = pygame.transform.scale(self.previewCard.img,(150, 200))
            screen.blit(self.previewCard.frontImg, (Globals.RESOLUTION_X * 0.81, Globals.RESOLUTION_Y * 0.265))

    def tossCoin(self):  # the first flip of the game.
        self.coin.toss()

    def flipCoin(self):  # the basic turnover
        self.coin.flip()

    class Coin(object):
        def __init__(self):
            # self.img have image here
            self.side = 0 # 0 and 1 for heads and tails
            self.animating = False # spinning in the air
        def flip(self):
            self.side = 0 if self.side != 0 else 1
        def toss(self): # random first toss in the game
            self.side = random.randrange(0,2)
