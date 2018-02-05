import pygame, math
class Card(object):
    def __init__(self):
        self.height = 100
        self.width = 75
        self.posX = 1181  # offset by 1 from deckImgHolder3 because the card latches to the mouse cursor if its equal (deckImgHolder3 = 1180,563)
        self.posY = 563
        self.isHeld = False
        self.resting = True  # unused for now
        self.defaultPos = (65, 500)
        self.img = pygame.image.load("assets\\cards\\democard.png")
        self.img = self.img.convert_alpha()
        self.backimg = pygame.image.load("assets\\cards\\democardBack.png")  # Card backs for opposing cards and for cards in deck.
        self.backimg = self.backimg.convert_alpha()
        self.speed = 10
        self.faceUp = False  # if card is facing up on the screen
        self.blitted = False

        self.onBoard = False
        self.disabled = False
        self.onTop = False

        # animated positioning junk
        self.destination = None  # is a Tuple x,y
        self.distance = 0.0
        self.vector = None

    # rename method soon
    # def decider(self):
    #     if not self.resting:
    #         pass

    # change of position on screen (calculation)
    def update(self, dTime, mouseX, mouseY):
        if self.destination:
            if self.isHeld == True:
                self.posX = mouseX - self.width * 0.75
                self.posY = mouseY - self.height * 0.75
            # animating but not held card
            elif self.isHeld == False and self.resting == False:
                self.set_destination(self.defaultPos[0], self.defaultPos[1])
                travelled = math.hypot(self.vector[0] * dTime, self.vector[1] * dTime)
                self.distance -= travelled
                if self.distance <= 0:  # destination reached
                    self.posX = self.defaultPos[0]  # * dTime
                    self.posY = self.defaultPos[1]  # * dTime
                    self.resting = True
                    self.destination = None
                else:
                    self.posX += self.vector[0] * dTime
                    self.posY += self.vector[1] * dTime
        else:
            self.posX = mouseX
            self.posY = mouseY

    # setting of destination, or the relative vector to location
    def set_destination(self, x, y):
        xDistance = x - self.posX
        yDistance = y - self.posY
        self.distance = math.hypot(xDistance, yDistance)  # distance from default position
        try:
            self.vector = (self.speed + (self.distance * 10)) * xDistance / self.distance, (
                    self.speed + (self.distance * 10)) * yDistance / self.distance
            self.destination = list((x, y))
        except ZeroDivisionError:
            pass
        '''
        Distance: 100 (random angle)
        posX 100 defX 0 posY 200 defY 0
        '''

    def draw(self, screen):
        screen.blit(self.img, (self.posX, self.posY))
        self.blitted = True

    # return boolean if card instance is moused over once function is called
    def collidepoint(self, x, y):
        collide = False
        if (self.posX + self.width) >= x >= self.posX and (self.posY + self.height) >= y >= self.posY:
            collide = True
        return collide

    def colliderect(self, x1, y1, x2, y2):
        boardCollide = False
        # x1rect = x1 + ((x2 - x1) * 0.40)
        # y1rect = y1 + ((y2 - y1) * 0.40)
        # x2rect = x1rect + 15
        # y2rect = y1rect + 15
        boardRect = pygame.Rect(x1, y1, (x2 - x1), (y2 - y1))
        tempRect = pygame.Rect(self.posX, self.posY, self.width, self.height)

        boardCollide = pygame.Rect.colliderect(tempRect, boardRect)

        return boardCollide

    #flip card
    def flip(self):
        pass