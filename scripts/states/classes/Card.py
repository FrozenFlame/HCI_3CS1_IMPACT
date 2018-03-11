import pygame, math
class Card(object):
    def __init__(self):
        self.frontImg = pygame.image.load("assets\\cards\\democard.png").convert_alpha()
        self.backImg = pygame.image.load("assets\\cards\\democardBack.png").convert_alpha()  # Card backs for opposing cards and for cards in deck.
        self.img = pygame.transform.smoothscale(self.backImg, (round(self.frontImg.get_rect().size[0] *0.33), round(self.frontImg.get_rect().size[1] *0.33))) # self.img is the CURRENT image to be drawn on the screen
        self.width = self.img.get_rect().size[0]  # img's initial width
        self.height = self.img.get_rect().size[1]  # img's initial height

        self.posX = 1181  # offset by 1 from deckImgHolder3 because the card latches to the mouse cursor if its equal (deckImgHolder3 = 1180,563)
        self.posY = 563

        self.defaultPos = (65, 500)

        self.flipX = self.width

        self.speed = 10  # movespeed on the screen

        self.owner = ""  # the owner of the card

        #
        #  ____              _
        # |  _ \            | |
        # | |_) | ___   ___ | | ___  __ _ _ __  ___
        # |  _ < / _ \ / _ \| |/ _ \/ _` | '_ \/ __|
        # | |_) | (_) | (_) | |  __/ (_| | | | \__ \
        # |____/ \___/ \___/|_|\___|\__,_|_| |_|___/
        #

        self.onBoard = False
        self.disabled = False
        self.onTop = False
        self.mayBePreviewed = False  # makes it so only cards you are allowed to see get a preview.
        self.flipAnimating = False
        self.flipped = False
        self.front = False
        self.back = True  # the card is face down initially. is this wrong?
        self.blitted = False
        self.isHeld = False
        self.resting = True  # unused for now

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
                else:  #this is for returning the card to your hand with animation
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

    def collide_rect(self, x1, y1, x2, y2):
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
                self.img = pygame.transform.smoothscale(self.img, (self.flipX, self.height))
                self.flipDisplace = (self.width - self.img.get_rect().size[0])
                # self.posX = self.defaultPos[0] + self.flipDisplace/2 # currently using defaultPos[0] would cause a jump in the animation to occur
                # print("[Card.py] - width[{0}] - img_rect [{1}] = flipDisplace[{2}] ".format(self.width, self.img.get_rect().size[0], self.flipDisplace))
                # print("[Card.py] - SHRINK posX: {0}: ".format(self.posX))
                # print("[Card.py] - flipX: {0}".format(self.flipX))
                # print("[Card.py] - img.get_rect().size {0}".format(self.img.get_rect().size[0] / 2))

                self.flipX -= 20
        ################################################################################
        elif self.flipX <= 0 and not self.flipped:  # time to flip trigger + changing of image
            self.flipX += 20
            if self.front:
                # print("front to back")
                self.img = pygame.transform.smoothscale(pygame.transform.smoothscale(self.backImg, (round(self.frontImg.get_rect().size[0] *0.33), round(self.frontImg.get_rect().size[1] *0.33))), (self.flipX, self.height))
                self.flipped = True
                self.back = True
                self.front = False
            elif self.back:  # growing animation to face up
                # print("back to front")
                self.img = pygame.transform.smoothscale(pygame.transform.smoothscale(self.frontImg, (round(self.frontImg.get_rect().size[0] *0.33), round(self.frontImg.get_rect().size[1] *0.33))), (self.flipX, self.height))
                self.flipped = True
                self.back = False
                self.front = True
        ################################################################################
        elif self.flipX <= 74 and self.flipped:  # growing animation
            # print("[Card.py] - GROW posX: {0}: ".format(self.posX))
            # print("[Card.py] - width[{0}] - img_rect [{1}] = flipDisplace[{2}] ".format(self.width,
            #                                                                             self.img.get_rect().size[0],
            #                                                                             self.flipDisplace))
            # print(a.flipX)
            currentTick = pygame.time.get_ticks()
            if currentTick - waitTick >= waitTime:
                # print("flipAnimating")
                waitTick = currentTick
                self.img = pygame.transform.smoothscale(self.img, (self.flipX, self.height))
                self.flipDisplace = (self.width - self.img.get_rect().size[0])
                # self.posX = self.defaultPos[0] + self.flipDisplace/2 # currently using defaultPos[0] would cause a jump in the animation to occur
                self.flipX += 20
        ################################################################################
        elif self.flipX >= 75 and self.flipped:  # animation completed, new image face set
            if self.front:
                self.img = pygame.transform.smoothscale(self.frontImg, (round(self.frontImg.get_rect().size[0] *0.33), round(self.frontImg.get_rect().size[1] *0.33)))
            if self.back:
                self.img = pygame.transform.smoothscale(self.backImg, (round(self.frontImg.get_rect().size[0] *0.33), round(self.frontImg.get_rect().size[1] *0.33)))
            self.flipped = False
            self.flipAnimating = False
            # self.posX = self.defaultPos[0] # apparently negligible if your calculations are correct
            self.flipX = 74  # restoring flipX back to original value

    def set_owner(self, new_owner):  # new_owner is type Player
        self.owner = new_owner

    def rfrsh_heightwidth(self):  # refreshes width and height values
        self.width = self.img.get_rect().size[0]  # img's initial width
        self.height = self.img.get_rect().size[1]  # img's initial height


