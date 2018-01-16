import pygame, math, time
'''
This class is responsible for holding the main loop, graphics rendering, and scene/event handling.
'''

#THIS IS JUS A DUMMY OBJECT
class Dragbox(object):
    def __init__(self):
        self.height = 100
        self.width = 75
        self.posX = 640
        self.posY = 250
        self.isHeld = False
        self.resting = True #unused for now
        self.defaultPos = (640,250)
        self.img = pygame.image.load("assets\\cards\\democard.png")
        self.img = self.img.convert_alpha()
        self.speed = 10

        #animated positing junk
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
        # print("set desti: {0}, {1}".format(x,y))
        # print("Mouse pos {0}".format(pygame.mouse.get_pos()))
        # print("Distance {0}".format(self.distance))
        # print("Vector: {0}".format(self.vector))
        # print()
        xDistance = x - self.posX
        yDistance = y - self.posY
        self.distance = math.hypot(xDistance, yDistance)  # distance from default position
        try:
            self.vector = (self.speed + (self.distance*10))* xDistance / self.distance, (self.speed + (self.distance*10)) * yDistance / self.distance
            self.destination = list((x,y))
        except ZeroDivisionError:
            pass
        # print(self.distance, xDistance, yDistance)
        # if distance > 0: # not at destination, perform operations below
        '''
        Distance: 100 (random angle)
        posX 100 defX 0 posY 200 defY 0
        
        '''
        '''old code
        self.posX = self.defaultPos[0]
        self.posY = self.defaultPos[1]
        '''

    def draw(self, screen):
        screen.blit(self.img, (self.posX, self.posY))

    def collidepoint(self,x,y):
        collide = False
        if (self.posX + self.width) >= x >= self.posX  and (self.posY + self.height) >= y >= self.posY:
                collide = True
        return collide

#this too, THESE NEED TO GO TO THEIR OWN CLASSES AT SOME POINT LADS
class dummyboard(object):
    def __init__(self):
        self.posX = 0.0
        self.posY = 0.0
        self.img = pygame.image.load("assets\\board\\DemoGameboard.png").convert_alpha()
    def draw(self, screen):
            screen.blit(self.img, (self.posX, self.posY))
            self.blitted = True
class Engine(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Avarice - A Greed-Based Card Game")
        self.screen = pygame.display.set_mode((1280,720))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.done = False
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

        self.deckImgHolder1 = Dragbox()     #add formula to determine how many deckImgHolders; ex. (no. of cards in deck) / 3 = (no. of deckImgHolders)
        self.deckImgHolder2 = Dragbox()     # or have preset of (x number of deckHolders) then hide the top deckHolder for every 5 cards removed from deck
        self.deckImgHolder3 = Dragbox()
        self.board = dummyboard()


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
                    if len(self.clickedCard) == 1:
                        self.clickedCard[0].isHeld = False



    # orders individual elements to update themselves (your coordinates, sprite change, etc)
    def update(self, deltaTime):
        # demo 1 card only lang naman
        if not self.card.resting:
            self.card.update(deltaTime, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        # if len(self.clickedCard) == 0:
        x = 80
        y = 570
        for h in self.handList:                     # some kind of issue around here i guess, when clicking cards toofast (one card is still moving but then you click another card and move it)
            if not h.resting and h == self.clickedCard[0]:
                h.update(deltaTime, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                if h.destination == None:
                    self.clickedCard.pop()
            elif h.resting and len(self.clickedCard) == 0:              # i think this refreshes all 10 cards after the moved card gets back to the hand, i meant for this part to just
                                                                        # initialize the first 10 cards ( run only once at the beginning of the program/ round in a game
                h.update(deltaTime,x,y)
                h.defaultPos = (x,y)
                x += 100

        self.deckImgHolder1.update(deltaTime, 1120, 500)
        self.deckImgHolder2.update(deltaTime, 1130, 500)
        self.deckImgHolder3.update(deltaTime, 1140, 500)

        pass

    # orders individual elements to draw themselves in the correct order (your blits)
    def draw(self):
        self.board.draw(self.screen)
        # self.screen.fill((100,100,100))
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


