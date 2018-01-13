import pygame, math
'''
This class is responsible for holding the main loop, graphics rendering, and scene/event handling.
'''

#THIS IS JUS A DUMMY OBJECT
class Dragbox(object):
    def __init__(self):
        self.height = 100
        self.width = 75
        self.posX = 640
        self.posY = 550
        self.isHeld = False
        self.resting = True #unused for now
        self.defaultPos = (640,550)
        self.img = pygame.image.load("assets\\cards\\democard.png")
        self.speed = 500

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
        # if self.isHeld == True:
        #     self.distance = math.hypot((self.defaultPos[0] - self.posX), (self.defaultPos[1] - self.posY))
        #     # print(distance)
        #     self.posX = mouseX - (self.width *0.75)
        #     self.posY = mouseY - (self.height *0.75)
        #     self.resting = False
        # elif self.isHeld == False and self.resting == False: # condition dropped to illegal zone
        #     self.set_target(self.defaultPos[0], self.defaultPos[1])
        #     travelled =  math.hypot(self.vector[0]*dTime, self.vector[1]*dTime)
        #     self.distance -= travelled
        #     if self.distance <= 0:  # destination reached
        #         self.posX = self.defaultPos[0] * dTime
        #         self.posY = self.defaultPos[1] * dTime
        #         self.resting = True
        #     else:
        #         self.posX += self.vector[0]
        #         self.posY += self.vector[1]
        if self.destination:
            if self.isHeld == True:
                self.set_destination(mouseX, mouseY)
                # print ("TRUE")
                travelled = math.hypot(self.vector[0] * dTime, self.vector[1] * dTime)
                self.distance -= travelled
                if self.distance <= 0:  # destination reached
                    self.posX = self.defaultPos[0] #* dTime
                    self.posY = self.defaultPos[1] #* dTime
                    self.resting = True
                    self.destination = None
                    # print("lol")
                else:
                    self.posX += self.vector[0] *dTime
                    self.posY += self.vector[1] *dTime
                    # print("lol2")
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
    # setting of destination, or the relative vector to location
    def set_destination(self, x, y):
        print("set desti: {0}, {1}".format(x,y))
        print("Mouse pos {0}".format(pygame.mouse.get_pos()))
        print("Distance {0}".format(self.distance))
        print("Vector: {0}".format(self.vector))
        print()
        xDistance = x - self.posX
        yDistance = y - self.posY
        self.distance = math.hypot(xDistance, yDistance)  # distance from default position
        try:
            self.vector = self.speed * xDistance / self.distance, self.speed * yDistance / self.distance
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

    # handles events which happen in the program
    def eventLoop(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print("Pos: {0} , {1}".format(event.pos()[0], event.pos()[1]))
                click = pygame.mouse.get_pressed()
                # print("Clicked: {0}".format(click))

                if click[0] == 1:
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


    # orders individual elements to update themselves (your coordinates, sprite change, etc)
    def update(self, deltaTime):
        # demo 1 card only lang naman
        if not self.card.resting:
            self.card.update(deltaTime, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        pass

    # orders individual elements to draw themselves in the correct order (your blits)
    def draw(self):
        self.screen.fill((100,100,100))
        self.card.draw(self.screen)
        pass

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


