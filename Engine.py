import pygame, math, time, random
from scripts.Globals import Globals
'''
This class is responsible for holding the main loop, graphics rendering, and scene/event handling.
'''

#THIS IS JUS A DUMMY OBJECT
class Dragbox(object):
    def __init__(self):
        self.height = 100
        self.width = 75
        self.posX = 1181     # offset by 1 from deckImgHolder3 because the card latches to the mouse cursor if its equal (deckImgHolder3 = 1180,563)
        self.posY = 563
        self.isHeld = False
        self.resting = True #unused for now
        self.defaultPos = (65,500)
        self.img = pygame.image.load("assets\\cards\\democard.png")
        self.img = self.img.convert_alpha()
        self.backimg = None # Card backs for opposing cards and for cards in deck.
        self.speed = 10
        self.blitted = False

        #animated positioning junk
        self.destination = None # is a Tuple x,y
        self.distance = 0.0
        self.vector = None
        
    #rename method soon
    def decider(self):
        if not self.resting:

            pass

    # change of position on screen (calculation)
    def update(self, dTime, mouseX, mouseY):

        if self.destination:
            if self.isHeld == True:
                self.posX = mouseX - self.width*0.75
                self.posY = mouseY - self.height*0.75

            # animating but not held card
            elif self.isHeld == False and self.resting == False:
                self.set_destination(self.defaultPos[0], self.defaultPos[1])
                travelled = math.hypot(self.vector[0]*dTime, self.vector[1]*dTime)
                self.distance -= travelled
                if self.distance <= 0:  # destination reached
                    self.posX = self.defaultPos[0] #* dTime
                    self.posY = self.defaultPos[1] #* dTime
                    self.resting = True
                    self.destination = None
                else:
                    self.posX += self.vector[0] *dTime
                    self.posY += self.vector[1] *dTime

        else:
            self.posX = mouseX
            self.posY = mouseY

    # setting of destination, or the relative vector to location
    def set_destination(self, x, y):
        xDistance = x - self.posX
        yDistance = y - self.posY
        self.distance = math.hypot(xDistance, yDistance)  # distance from default position
        try:
            self.vector = (self.speed + (self.distance*10))* xDistance / self.distance, (self.speed + (self.distance*10)) * yDistance / self.distance
            self.destination = list((x,y))
        except ZeroDivisionError:
            pass
        '''
        Distance: 100 (random angle)
        posX 100 defX 0 posY 200 defY 0
        '''

    def draw(self, screen):
        screen.blit(self.img, (self.posX, self.posY))
        self.blitted = True

    def collidepoint(self,x,y):
        collide = False
        if (self.posX + self.width) >= x >= self.posX  and (self.posY + self.height) >= y >= self.posY:
                collide = True
        return collide


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
class Dummyboard(object):
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
        self.cardPreview = None # big card to the right, duplicates appearance of card being moused over.

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

    def tossCoin(self):
        self.coin.toss()
    def flipCoin(self):
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



class Engine(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Avarice - A Greed-Based Card Game")
        self.screen = pygame.display.set_mode((1280,720))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = Globals.fps
        self.done = False

        self.board = Dummyboard()

        self.card = Dragbox()

        self.hand1 = Dragbox()
        self.hand2 = Dragbox()
        self.hand3 = Dragbox()
        self.hand4 = Dragbox()
        self.hand5 = Dragbox()
        self.hand6 = Dragbox()
        self.hand7 = Dragbox()
        self.hand8 = Dragbox()
        self.hand9 = Dragbox()
        self.hand10 = Dragbox()

        self.handList = [self.hand1, self.hand2, self.hand3, self.hand4, self.hand5, self.hand6, self.hand7, self.hand8, self.hand9, self.hand10]
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
        self.drawCardWait = 1000                                               #wait for 1 second, adjust this kasi parang ang bagal mag draw nung initial 10 cards
        self.opening = True
        self.openingIndex = 0
        self.x = 220
        self.y = 600

        self.deckImgHolder1 = Dragbox()     #add formula to determine how many deckImgHolders; ex. (no. of cards in deck) / 3 = (no. of deckImgHolders)
        self.deckImgHolder2 = Dragbox()     # or have preset of (x number of deckHolders) then hide the top deckHolder for every 5 cards removed from deck
        self.deckImgHolder3 = Dragbox()

    # handles events which happen in the program
    def eventLoop(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print("Pos: {0} , {1}".format(event.pos()[0], event.pos()[1]))
                click = pygame.mouse.get_pressed()
                # print("Clicked: {0}".format(click))

                if click[0] == 1 :

                    self.clickedCard = [s for s in self.handList if s.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])]     #pygame.Rect.collidepoint 	— 	test if a point is inside a rectangle
                                                                                                                                         #checking if mouse clicked on one of the hand cards
                    if len(self.clickedCard) == 1:                   # just mirroring self.card lol, more mirrored instances below @ update and draw function
                        print("handcard clicked")
                        self.clickedCard[0].isHeld = True
                        self.clickedCard[0].resting = False
                        self.clickedCard[0].set_destination(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

                    if (self.card.posX + self.card.width) >= pygame.mouse.get_pos()[0] >= self.card.posX and (self.card.posY + self.card.height) >= pygame.mouse.get_pos()[1] >= self.card.posY:
                        print("clicked")
                        self.card.isHeld = True
                        self.card.resting = False
                        self.card.set_destination(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            if event.type == pygame.MOUSEBUTTONUP:
                click = pygame.mouse.get_pressed()
                if click[0] == 0:
                    print("unheld")
                    self.card.isHeld = False
                    if not len(self.clickedCard) == 0:
                        self.clickedCard[0].isHeld = False
                        if self.clickedCard[0].destination == None:
                            self.clickedCard.pop()



    # orders individual elements to update themselves (your coordinates, sprite change, etc)
    def update(self, deltaTime):
        # demo 1 card only lang naman
        if not self.card.resting:
            self.card.update(deltaTime, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        if self.opening == True:
            currentTick = pygame.time.get_ticks()
            if currentTick - self.waitTick >= self.drawCardWait:
                if self.openingIndex < 10:
                    self.waitTick = currentTick
                    self.drawCardSound.play()
                    self.handList[self.openingIndex].resting = False
                    self.handList[self.openingIndex].set_destination(1180, 563)
                    self.handList[self.openingIndex].defaultPos = (self.x, self.y)
                    self.handList[self.openingIndex].update(deltaTime, self.x, self.y)
                    self.x += 80
                    self.openingIndex += 1
                if self.openingIndex == 10:
                    self.opening = False

            print("currentTick= {0} waitTick= {1} currentTick-waitTick= {2}".format(currentTick,self.waitTick,currentTick-self.waitTick))


        for h in self.handList:
            if not h.resting:
                h.update(deltaTime, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        self.deckImgHolder1.update(deltaTime, 1170, 565)
        self.deckImgHolder2.update(deltaTime, 1175, 564)
        self.deckImgHolder3.update(deltaTime, 1180, 563)

        pass

    # orders individual elements to draw themselves in the correct order (your blits)
    def draw(self):
        self.board.draw(self.screen)
        # self.screen.fill((100,100,100))
        if not self.card.blitted:               #another way of instantiating, compared to elif h.resting and not h.blitted in update method
            self.card.posX, self.card.posY = self.card.defaultPos
            self.card.blitted = True
        self.card.draw(self.screen)

        for h in self.handList:
            h.draw(self.screen)

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


