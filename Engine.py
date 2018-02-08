import pygame, math, time, random
from HCI_3CS1_IMPACT.BoardField import BoardField
from HCI_3CS1_IMPACT.Card import Card
from HCI_3CS1_IMPACT.Board import Board

from scripts.Globals import Globals
'''
This class is responsible for holding the main loop, graphics rendering, and scene/event handling.
'''



#THIS IS JUS A DUMMY OBJECT

'''
GAMEBOARD NOTES:
Needs:
Standard coordinates (and corresponding area for blitting) for rows, coin, portraits, playername, and etc. 
I'm sure we can come up with an algorithm so that we can have the cards that have been set to reposition when another 
card gets played

Biggest issue of them all (I think):
Phases of the game
Rough code estimate would be like:

(a loop, 2-3 times)
    round starts
    <draw cards for both players>
    player1 receives first 10 cards
    player2 receives first 10 cards
    <larger hand cards displayed on screen>
    player1 chooses to mulligan or not
    player2 chooses to mulligan or not
    <cards assume hand coordinates and scale>
    <coin toss animation> - first player to take turn decided
    (an inner round loop, repeats however many times possible)
        start turn
        <animations expected for this phase> - this part lol
        end of turn
    (end of inner round loop, repeat)

(end of phase, repeat)
<victory animation> - a player gets crowned victorious
'''
#this too, THESE NEED TO GO TO THEIR OWN CLASSES AT SOME POINT LADS

# class which holds the entire program.
class Engine(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Avarice - A Greed-Based Card Game")
        self.screen = pygame.display.set_mode((1280,720))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = Globals.fps
        self.done = False

        # logic booleans
        self.holdingCard = False

        # objects
        self.board = Board()
        # card and hand might be handled differently from this. These items might be found on the board instead.
        self.card = Card()
        self.hand1 = Card()
        self.hand2 = Card()
        self.hand3 = Card()
        self.hand4 = Card()
        self.hand5 = Card()
        self.hand6 = Card()
        self.hand7 = Card()
        self.hand8 = Card()
        self.hand9 = Card()
        self.hand10 = Card()
        self.handList = [self.hand1, self.hand2, self.hand3, self.hand4, self.hand5, self.hand6, self.hand7, self.hand8, self.hand9, self.hand10]

        self.boardField = BoardField(225,390,1010,470)
        self.boardCardList = list()

        self.allCardsList = list()

        self.clickedCard = list()

        '''scenario: the 10 hand cards start at the top of the deck/deckImgHolder3, then use waitTick so that 1 card animates(similarly to the click-and-drag animation)
         to its hand position every 1 second
         formula for wait:
                  if currentTick - self.waitTick >= self.drawCardWait:
                        self.waitTick = currentTick
                        [do stuff]
        '''
        self.drawCardSound = pygame.mixer.Sound("assets\\cards\\draw_card.wav")     # may be confused with draw()
        self.waitTick = pygame.time.get_ticks()                                #will be used to for computing how long it has already waited
        self.drawCardWait = 400                                               #wait for 1 second, adjust this kasi parang ang bagal mag draw nung initial 10 cards
        self.opening = True
        self.openingIndex = 0
        self.openingX = 220                # hand coordinate is from 220 to 1020
        self.openingY = 600

        self.deckImgHolder1 = Card()     #add formula to determine how many deckImgHolders; ex. (no. of cards in deck) / 3 = (no. of deckImgHolders)
        self.deckImgHolder2 = Card()     # or have preset of (x number of deckHolders) then hide the top deckHolder for every 5 cards removed from deck
        self.deckImgHolder3 = Card()

    # handles events which happen in the program
    def cardMousedOver(self, xy) -> bool:
        self.clickedCard = [s for s in self.allCardsList if s.collidepoint(xy[0], xy[1])]
        return True if len(self.clickedCard) == 1 else False
    def cardMousedOver2(self, xy):
        self.clickedCard = [s for s in self.allCardsList if s.collidepoint(xy[0], xy[1])]
        return self.clickedCard

    def eventLoop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            #if self.board.hasPreviewCard:
             #   print("Previewing card.")
            #card is being moused over
            if self.cardMousedOver(pygame.mouse.get_pos()):
                # print("Mousingover")
                self.board.hasPreviewCard = True
                self.board.previewCard = self.clickedCard[0]
            elif not self.cardMousedOver(pygame.mouse.get_pos()):
                # print("notmousing")
                self.board.hasPreviewCard = False if not self.holdingCard else True

            if event.type == pygame.MOUSEBUTTONDOWN and not self.opening:
                print(len(self.clickedCard))
                print("AllCardsList: {0}HandsList: {1}BoardCardList:{2}".format(len(self.allCardsList),len(self.handList),len(self.boardCardList)))

                print("Pos: {0} , {1}".format(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
                click = pygame.mouse.get_pressed()
                # print("Clicked: {0}".format(click))

                if click[0] == 1:

                    # self.clickedCard = [s for s in self.handList if s.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and not s.disabled and not s.onBoard]
                    #
                    # if len(self.clickedCard) == 1:
                    #     print("handcard clicked")
                    #     self.clickedCard[0].isHeld = True
                    #     self.holdingCard = True
                    #     self.clickedCard[0].resting = False
                    #     self.clickedCard[0].set_destination(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    #     self.drawCardSound.play()

                    for s in self.allCardsList:
                        if s.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                            self.clickedCard.append(s)
                            s.onTop = True
                            self.allCardsList.pop(self.allCardsList.index(s))
                            self.allCardsList.append(s)

                    if len(self.clickedCard) > 0:
                        if self.clickedCard[0].disabled == False and self.clickedCard[0].onBoard == False:
                            print("handcard clicked")
                            self.clickedCard[0].isHeld = True
                            self.holdingCard = True
                            self.clickedCard[0].resting = False
                            self.clickedCard[0].set_destination(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                            self.drawCardSound.play()

                    if (self.card.posX + self.card.width) >= pygame.mouse.get_pos()[0] >= self.card.posX and (self.card.posY + self.card.height) >= pygame.mouse.get_pos()[1] >= self.card.posY:
                        print("clicked")
                        self.card.isHeld = True
                        self.holdingCard = True
                        self.card.resting = False
                        self.card.set_destination(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            if event.type == pygame.MOUSEBUTTONUP:
                click = pygame.mouse.get_pressed()
                if click[0] == 0:
                    print("unheld")
                    self.card.isHeld = False
                    self.holdingCard = False
                    self.board.hasPreviewCard = False
                    if not len(self.clickedCard) == 0:
                        self.clickedCard[0].isHeld = False
                        self.clickedCard[0].flip()

                        if self.clickedCard[0].colliderect(self.boardField.xStart,self.boardField.yStart,self.boardField.xEnd,self.boardField.yEnd) and not self.clickedCard[0].onBoard:
                            self.boardCardList.append(self.clickedCard[0])
                            self.clickedCard[0].onBoard = True

                        if self.clickedCard[0].destination == None:
                            self.clickedCard.pop()



    # orders individual elements to update themselves (your coordinates, sprite change, etc)
    def update(self, deltaTime):
        # demo 1 card only lang naman
        if not self.card.resting:
            self.card.update(deltaTime, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        if self.opening:
            currentTick = pygame.time.get_ticks()
            if currentTick - self.waitTick >= self.drawCardWait:
                if self.openingIndex < 10:
                    self.waitTick = currentTick
                    self.drawCardSound.play()
                    self.handList[self.openingIndex].resting = False
                    self.handList[self.openingIndex].set_destination(1180, 563)
                    self.handList[self.openingIndex].defaultPos = (self.openingX, self.openingY)
                    self.handList[self.openingIndex].update(deltaTime, self.openingX, self.openingY)
                    self.allCardsList.append(self.handList[self.openingIndex])
                    self.openingX += 80
                    self.openingIndex += 1
                if self.openingIndex == 10:
                    self.opening = False

        boardx = 220
        boardy = 380
        for boardCard in self.boardCardList:
            boardCard.defaultPos = boardx,boardy
            boardx += 80

        for a in self.allCardsList:
            # if not h.resting and h.colliderect(self.bField1.xStart, self.bField1.yStart, self.bField1.xEnd, self.bField1.yEnd):
            #     print("Hurrah")
            #     h.defaultPos = (self.bField1.xStart, self.bField1.yStart)
            #     h.update(deltaTime, self.bField1.xStart, self.bField1.yStart)
            if not a.resting:
                a.update(deltaTime, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            if a.flipAnimating:
                waitTime = 10  # millisecond
                if a.flipX > 0 and not a.flipped:
                    print(a.flipX)
                    currentTick = pygame.time.get_ticks()
                    if currentTick - self.waitTick >= waitTime:
                        print("flipAnimating")
                        self.waitTick = currentTick
                        a.img = pygame.transform.smoothscale(a.img, (a.flipX, 100))
                        a.flipX -= 20
        ################################################################################
                elif a.flipX <= 0 and not a.flipped:
                    a.flipX += 20
                    if a.front:
                        print("front to back")
                        a.img = pygame.transform.smoothscale(a.backImg, (a.flipX, 100))
                        a.flipped = True
                        a.back = True
                        a.front = False
                    elif a.back:  # if self.img == self.backImg:
                        print("back to front")
                        a.img = pygame.transform.smoothscale(a.frontImg, (a.flipX, 100))
                        a.flipped = True
                        a.back = False
                        a.front = True
        ################################################################################
                elif a.flipX <= 74 and a.flipped:
                    print(a.flipX)
                    currentTick = pygame.time.get_ticks()
                    if currentTick - self.waitTick >= waitTime:
                        print("flipAnimating")
                        self.waitTick = currentTick
                        a.img = pygame.transform.smoothscale(a.img, (a.flipX, 100))
                        a.flipX += 20
        ################################################################################
                elif a.flipX >= 75 and a.flipped:
                    if a.front:
                        a.img = a.frontImg
                    if a.back:
                        a.img = a.backImg
                    a.flipped = False
                    a.flipAnimating = False
                    a.flipX = 74



        for h in self.handList:
            initialHandlength = len(self.handList)
            if h.onBoard:
                self.handList.pop(self.handList.index(h))
            if len(self.handList) < initialHandlength:
                initialHandlength = len(self.handList)
                newX = 620 - (40*len(self.handList))
                for h2 in self.handList:
                    h2.resting = False
                    h2.set_destination(h.posX, h.posY)

                    # xRange of handList Cards is 220 to 1020 . 800 distance . middle point is 620 . starting handLength is 10 . formula? 620 - (40*handLength)
                    h2.defaultPos = (newX, 600)    # 600 = self.openingY
                    h2.update(deltaTime, newX, 600)
                    newX += 80


        self.deckImgHolder1.update(deltaTime, 1170, 565)
        self.deckImgHolder2.update(deltaTime, 1175, 564)
        self.deckImgHolder3.update(deltaTime, 1180, 563)

    # orders individual elements to draw themselves in the correct order (your blits)
    def draw(self):
        self.board.draw(self.screen)
        # self.screen.fill((100,100,100))
        if not self.card.blitted:               #another way of instantiating, compared to elif h.resting and not h.blitted in update method
            self.card.posX, self.card.posY = self.boardField.xStart, self.boardField.yStart
            self.card.blitted = True
        self.card.draw(self.screen)

        onTopCard = None
        for a in self.allCardsList:
            if not a.onTop:
                a.draw(self.screen)
            else:
                onTopCard = a
        if onTopCard != None:
            onTopCard.draw(self.screen)
            onTopCard.onTop = False

        self.deckImgHolder1.draw(self.screen)
        self.deckImgHolder2.draw(self.screen)
        self.deckImgHolder3.draw(self.screen)

        # FPS
        pygame.display.set_caption("Avarice - A Greed-Based Card Game - FPS: {0:.2f}".format(self.clock.get_fps()))

    def main_loop(self):
        while not self.done:
            # dt is multiplied to the vector values here in order to simulate the movements over time.
            # without it, it would cause the graphic to teleport to the location instantaneously
            deltaTime = self.clock.tick(self.fps)/1000 # delta time (for framerate independence)

            #have input listener stage
            self.eventLoop()
            self.update(deltaTime)
            self.draw()
            pygame.display.update()
