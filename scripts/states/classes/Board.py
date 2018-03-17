import pygame, random, math
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
        # game related, update Lol this is all located in the Engine class directly
        self.player1 = None # player class
        self.player2 = None # player class
        self.hand1 = None
        self.hand2 = None
        self.deck1 = None
        self.deck2 = None
        self.grave1 = None  # forgot about these though
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
            self.left = pygame.image.load("assets\\board\\coinleft.png").convert_alpha()
            self.right = pygame.image.load("assets\\board\\coinleft.png").convert_alpha()
            self.img = self.left  # image visible to the people
            self.rect = self.img.get_rect()
            self.side = 0  # 0 and 1 for point left and point right

            # animation things
            self.animating = False  # spinning in the air
            self.longanim = False
            self.defaultPos = 1280/2, 720/2
            self.posX = self.defaultPos[0]
            self.posY = self.defaultPos[1]
            self.exact_position = self.posX, self.posY
            self.rect.center = self.posX, self.posY
            self.is_visible = True

            self.exact_position = list(self.rect.center)
            self.speed = 1000
            self.dspeed = 7
            self.distance = None
            self.destination = None
            self.vector = None
            self.move_type = "constant"
            self.scalespeed = 10

        def flip(self):
            self.animating = True
            self.longanim = False
            self.side = 0 if self.side != 0 else 1

        def flipAnim(self):
            pass
        def toss(self): # random first toss in the game
            self.animating = True
            self.longanim = True
            self.side = random.randrange(0,2)
        def point_left(self):
            self.img = self.left
        def point_right(self):
            self.img = self.right


        def update(self, dTime):
            if self.destination:
                if self.move_type == "constant":
                    # self.set_destination(self.defaultPos[0], self.defaultPos[1])
                    travelled = math.hypot(self.vector[0] * dTime, self.vector[1] * dTime)
                    self.distance -= travelled
                    print("Distance, ", self.distance)
                    if self.distance <= 0:  # destination reached
                        # self.posX = self.defaultPos[0]  # * dTime
                        # self.posY = self.defaultPos[1]  # * dTime
                        self.rect.center = self.exact_position = self.destination
                        self.destination = None

                    else:  # this is for returning the card to your hand with animation
                        # self.posX += self.vector[0] * dTime
                        # self.posY += self.vector[1] * dTime
                        self.exact_position[0] += self.vector[0] * dTime
                        self.exact_position[1] += self.vector[1] * dTime
                        self.rect.center = self.exact_position

                elif self.move_type == "distance":
                    self.set_destination(self.destination[0], self.destination[1])
                    travelled = math.hypot(self.vector[0] * dTime, self.vector[1] * dTime)
                    self.distance -= travelled
                    if self.distance <= 0:  # destination reached
                        # self.posX = self.defaultPos[0]  # * dTime
                        # self.posY = self.defaultPos[1]  # * dTime
                        self.rect.center = self.posX, self.posY
                        self.exact_position = self.rect.center
                        self.destination = None
                    else:  # this is for returning the card to your hand with animation
                        self.posX += self.vector[0] * dTime
                        self.posY += self.vector[1] * dTime
                        self.rect.center = self.posX, self.posY
                        self.exact_position = self.rect.center

        def set_absolute(self, absolutexy):
            self.posX = absolutexy[0]
            self.posY = absolutexy[1]
            self.exact_position = list((absolutexy[0], absolutexy[1]))
            self.rect.center = absolutexy[0], absolutexy[1]

        # setting of destination, or the relative vector to location
        def set_destination(self, x, y):
            if self.move_type == "constant":
                xDistance = x - self.exact_position[0]
                yDistance = y - self.exact_position[1]
                self.distance = math.hypot(xDistance, yDistance)  # distance from default position
                try:
                    # self.vector = (self.speed + (self.distance * 10)) * xDistance / self.distance, (
                    #         self.speed + (self.distance * 10)) * yDistance / self.distance
                    self.vector = (self.speed * xDistance / self.distance), (self.speed * yDistance / self.distance)
                    self.destination = list((x, y))
                except ZeroDivisionError:
                    pass
            elif self.move_type == "distance":
                xDistance = x - self.posX
                yDistance = y - self.posY
                self.distance = math.hypot(xDistance, yDistance)  # distance from default position
                try:
                    self.vector = ((self.distance * self.dspeed)) * xDistance / self.distance, (
                        (self.distance * self.dspeed)) * yDistance / self.distance
                    self.destination = list((x, y))
                except ZeroDivisionError:
                    pass


        def draw(self, screen):
            screen.blit(self.img, self.rect)


