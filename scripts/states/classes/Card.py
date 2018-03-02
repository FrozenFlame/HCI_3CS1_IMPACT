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
        self.frontImg = pygame.image.load("assets\\cards\\democard.png")
        self.flipAnimating = False
        self.flipped = False
        self.flipX = 74
        self.front = False
        self.back = True  # the card is face down initially. is this wrong?
        self.img = None
        self.frontImg = pygame.image.load("assets\\cards\\democard.png").convert_alpha()
        self.backImg = pygame.image.load("assets\\cards\\democardBack.png").convert_alpha()  # Card backs for opposing cards and for cards in deck.
        self.img = self.backImg
        self.speed = 10
        self.blitted = False

        self.onBoard = False
        self.disabled = False
        self.onTop = False

        # animated positioning junk
        self.destination = None  # is a Tuple x,y
        self.distance = 0.0
        self.vector = None
        self.flipDisplace = 0

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
                else: #this is for returning the card to your hand with animation
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

    def flip(self):  # flip initiator
        self.flipAnimating = True
        # self.flipAnimation()

    def flipAnim(self, waitTick):  # flip animation to be called per tick.
        waitTime = 10
        if self.flipX > 0 and not self.flipped:  # shrinking animation
            # print("Engine.py - "); print(a.flipX)
            currentTick = pygame.time.get_ticks()
            if currentTick - waitTick >= waitTime:
                # print("flipAnimating")
                waitTick = currentTick
                self.img = pygame.transform.smoothscale(self.img, (self.flipX, 100))
                self.flipDisplace = (self.width - self.img.get_rect().size[0])
                # self.posX = self.defaultPos[0] + self.flipDisplace/2 # currently using defaultPos[0] would cause a jump in the animation to occur
                print("[Card.py] - width[{0}] - img_rect [{1}] = flipDisplace[{2}] ".format(self.width, self.img.get_rect().size[0], self.flipDisplace))
                print("[Card.py] - SHRINK posX: {0}: ".format(self.posX))
                print("[Card.py] - flipX: {0}".format(self.flipX))
                print("[Card.py] - img.get_rect().size {0}".format(self.img.get_rect().size[0] / 2))

                self.flipX -= 20
        ################################################################################
        elif self.flipX <= 0 and not self.flipped:  # time to flip trigger + changing of image
            self.flipX += 20
            if self.front:
                print("front to back")
                self.img = pygame.transform.smoothscale(self.backImg, (self.flipX, 100))
                self.flipped = True
                self.back = True
                self.front = False
            elif self.back:  # growing animation to face up
                print("back to front")
                self.img = pygame.transform.smoothscale(self.frontImg, (self.flipX, 100))
                self.flipped = True
                self.back = False
                self.front = True
        ################################################################################
        elif self.flipX <= 74 and self.flipped:  # growing animation
            print("[Card.py] - GROW posX: {0}: ".format(self.posX))
            print("[Card.py] - width[{0}] - img_rect [{1}] = flipDisplace[{2}] ".format(self.width,
                                                                                        self.img.get_rect().size[0],
                                                                                        self.flipDisplace))
            # print(a.flipX)
            currentTick = pygame.time.get_ticks()
            if currentTick - waitTick >= waitTime:
                # print("flipAnimating")
                waitTick = currentTick
                self.img = pygame.transform.smoothscale(self.img, (self.flipX, 100))
                self.flipDisplace = (self.width - self.img.get_rect().size[0])
                # self.posX = self.defaultPos[0] + self.flipDisplace/2 # currently using defaultPos[0] would cause a jump in the animation to occur
                self.flipX += 20
        ################################################################################
        elif self.flipX >= 75 and self.flipped:  # animation completed, new image face set
            if self.front:
                self.img = self.frontImg
            if self.back:
                self.img = self.backImg
            self.flipped = False
            self.flipAnimating = False
            # self.posX = self.defaultPos[0] # apparently negligible if your calculations are correct
            self.flipX = 74  # restoring flipX back to original value

    # waitTick = pygame.time.get_ticks()
    # currentTick = pygame.time.get_ticks()
    # waitTime = 10 #millisecond
    #
    # x = 75
    # while x > 0:
    #     currentTick = pygame.time.get_ticks()
    #     if currentTick - waitTick >= waitTime:
    #         waitTick = currentTick
    #         self.img = pygame.transform.scale(self.img, (x, 100))
    #         x -= 1
    #     else:
    #         continue
    #     #time.sleep(0.001)
    #
    # if self.img == self.frontImg:
    #     self.img = self.backImg
    # else:#if self.img == self.backImg:
    #     self.img = self.frontImg
    #
    # while x < 75:
    #     currentTick = pygame.time.get_ticks()
    #     if currentTick - waitTick >= waitTime:
    #         waitTick = currentTick
    #         self.img = pygame.transform.scale(self.img, (x, 100))
    #         x += 1
    #     else:
    #         continue
    #     #time.sleep(0.001)


