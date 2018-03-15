import pygame, math
import pygame
from ...Globals import Globals

spritesheet = pygame.image.load("assets/buttons/button-start.png")

resizer = 1.2


#203, 73, rect of first button

class Buttons(object):
    def __init__(self, x ,y):

        character = pygame.Surface((203, 74), pygame.SRCALPHA)  # first line is dimension of the button
        character.blit(spritesheet, (0, 0))  # second line is the DISPLACEMENT on the sprite sheet
        character = pygame.transform.smoothscale(character, (round(203 * resizer), round(74 * resizer)))
        self.startButtonNormal = character

        character = pygame.Surface((203, 74), pygame.SRCALPHA)
        character.blit(spritesheet, (0, -74))
        character = pygame.transform.smoothscale(character, (round(203 * resizer), round(74 * resizer)))
        self.startButtonHover = character

        character = pygame.Surface((203, 74), pygame.SRCALPHA)
        character.blit(spritesheet, (0, -148))
        character = pygame.transform.smoothscale(character, (round(203 * resizer), round(74 * resizer)))
        self.startButtonClicked = character

        self.image = self.startButtonNormal
        self.startButton = pygame.transform.scale(self.image, (300, 100))
        self.startButton.convert()

        self.posX = x
        self.posY = y
        self.width = 200 *resizer
        self.height = 75 *resizer
        self.rect = pygame.Rect(self.posX, self.posY, self.width, self.height)
        self.rect.center = self.posX , self.posY
        self.blitted = False
        self.startPrime = False  # button has been held down
        self.has_message = False # wants to return something to where it has been instantiated
        self.message = {}
        # related to Movable (some things changed to fit button schema
        self.defPosX = self.posX - self.width *0.5
        self.defPosY = self.posY - self.height *0.5
        self.defaultPos = self.defPosX, self.defPosY
        self.exact_position = list(self.rect)
        self.speed = 500
        self.dspeed = 0
        self.distance = None
        self.destination = None
        self.vector = None
        self.move_type = "distance"
        # end

        self.finished = False  # context specific for changing state

    def draw(self, screen):
        screen.blit(self.startButton, self.rect)
        self.blitted = True


    def get_message(self):
        return self.message

    def get_evt(self, click, event, mouse):

        # mouse over
        if (self.posX + self.width) >= mouse[0] >= self.posX and (self.posY + self.height) >= mouse[1] >= self.posY and not self.startPrime:
            self.image = self.startButtonHover
            self.startButton = self.image.convert_alpha()

        # mouse back on while held start button
        elif self.startPrime and (self.posX + self.width) >= mouse[0] >= self.posX and (self.posY + self.height) >= mouse[1] >= self.posY:
            self.image = self.startButtonClicked
            self.startButton = self.image.convert_alpha()
            self.startButton.convert()

        # mouse off
        elif not (self.posX + self.width) >= mouse[0] >= self.posX or not (self.posY + self.height) >= mouse[1] >= self.posY:
            self.image = self.startButtonNormal
            self.startButton = self.image.convert_alpha()

        #for changing states button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if click[0] == 1 and (self.posX + self.width) >= mouse[0] >= self.posX and (self.posY + self.height) >= mouse[1] >= self.posY:
                self.image = self.startButtonClicked
                self.startButton = self.image.convert_alpha()
                self.startPrime = True
            elif click[2] == 1:
                print("[MainMenu(STATE)] Rightclick pressed, state revealed as: {0}".format(Globals.state))

        if event.type == pygame.MOUSEBUTTONUP:
            if click[0] == 0 and self.startPrime and (self.posX + self.width) >= mouse[0] >= self.posX and (self.posY + self.height) >= mouse[1] >= self.posY:
                self.image = self.startButtonNormal
                self.has_message = True
                # old code, direct hotwire to game
                # Globals.state = "AVARICE"

                # self.next = Globals.state
                # print("Start clicked state is now: ", Globals.state)
                # self.finished = True

                print("[Buttons.py (Start)] Start clicked, showing Hero select")
                self.message = {
                    "phase": "TO_HERO"
                }

            if self.startPrime:
                self.startPrime = False

    def refresh_appearance(self):
        self.startButton = pygame.transform.scale(self.image, (300, 100))

    def set_image(self, img):
        self.startButton = img

    # Movable related

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

                else:  #this is for returning the card to your hand with animation
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
                    self.rect = self.posX, self.posY
                    self.exact_position = self.rect


    def change_acceleration(self, newdistancespeed):
        self.distancespeed = newdistancespeed

    def update_rect_center(self, posx,posy):
        self.rect.center = posx, posy

    # setting of destination, or the relative vector to location
    def set_destination(self, x,y):
        if self.move_type == "constant":
            xDistance = x - self.exact_position[0]
            yDistance = y - self.exact_position[1]
            self.distance = math.hypot(xDistance, yDistance)  # distance from default position
            try:
                # self.vector = (self.speed + (self.distance * 10)) * xDistance / self.distance, (
                #         self.speed + (self.distance * 10)) * yDistance / self.distance
                self.vector = (self.speed * xDistance / self.distance), (self.speed * yDistance / self.distance)
                self.destination = list((x,y))
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


    def back_to_default(self):
        self.set_destination(*self.defaultPos)

