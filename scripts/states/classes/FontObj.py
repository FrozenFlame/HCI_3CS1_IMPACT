import pygame, math

class FontObj(object):
    def __init__(self, text, posx, posy, font,  fontsize, surface, rect, color):
        self.text = text
        self.surface = surface
        self.rect = rect
        self.font = font
        self.fontsize = fontsize
        self.posX = posx
        self.posY = posy
        self.color = color
        # booleans:
        self.is_visible = True

        # animation related
        self.defaultPos = (0,0)
        self.exact_position = list(self.rect.center)
        self.speed = 1000
        self.distancespeed = 10
        self.distance = None
        self.destination = None
        self.vector = None
        self.acceleration_factor = 0
        self.move_type = "distance"  # "accelerate", "decelerate", "constant", "distance"


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
                    self.rect.center = self.posX, self.posY
                    self.exact_position = self.rect.center

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
                self.vector = ((self.distance * self.distancespeed)) * xDistance / self.distance, (
                       (self.distance * self.distancespeed)) * yDistance / self.distance
                self.destination = list((x, y))
            except ZeroDivisionError:
                pass
        '''
        Distance: 100 (random angle)
        posX 100 defX 0 posY 200 defY 0
        '''
    # code from card
    # def update(self, dTime, mouseX, mouseY):
    #     if self.destination:
    #         if self.isHeld == True:
    #             self.posX = mouseX - self.width * 0.75
    #             self.posY = mouseY - self.height * 0.75
    #         # animating but not held card
    #         elif self.isHeld == False and self.resting == False:
    #             self.set_destination(self.defaultPos[0], self.defaultPos[1])
    #             travelled = math.hypot(self.vector[0] * dTime, self.vector[1] * dTime)
    #             self.distance -= travelled
    #             if self.distance <= 0:  # destination reached
    #                 self.posX = self.defaultPos[0]  # * dTime
    #                 self.posY = self.defaultPos[1]  # * dTime
    #                 self.resting = True
    #                 self.destination = None
    #             else:  # this is for returning the card to your hand with animation
    #                 self.posX += self.vector[0] * dTime
    #                 self.posY += self.vector[1] * dTime
    #     else:
    #         self.posX = mouseX
    #         self.posY = mouseY
    #
    #     # setting of destination, or the relative vector to location
    #
    # def set_destination(self, x, y):
    #     xDistance = x - self.posX
    #     yDistance = y - self.posY
    #     self.distance = math.hypot(xDistance, yDistance)  # distance from default position
    #     try:
    #         self.vector = (self.speed + (self.distance * 10)) * xDistance / self.distance, (
    #                 self.speed + (self.distance * 10)) * yDistance / self.distance
    #         self.destination = list((x, y))
    #     except ZeroDivisionError:
    #         pass
    #     '''
    #     Distance: 100 (random angle)
    #     posX 100 defX 0 posY 200 defY 0
    #     '''

    def go(self):   # 'orders' object to proceed to next destination
        pass
    def draw(self, screen):
        if self.is_visible:
            screen.blit(self.surface, self.rect)

    def factory(text, posx, posy, font, fontsize, color):
        largeText = pygame.font.Font('assets/fonts/' +font, fontsize)
        textSurf = largeText.render(text, True, color)
        textRect = textSurf.get_rect()
        textRect.center = (posx, posy)
        return FontObj(text, posx, posy, font, fontsize, textSurf, textRect,color)
    factory = staticmethod(factory)

    #
    # def display_text(self, text, screen):
    #     largeText = pygame.font.Font('freesansbold.ttf', 115)
    #     textSurf, textRect = self.text_objects(text, largeText)  # Text Surface and Text Rect
    #     textRect.center = (Globals.RESOLUTION_X * 0.2, Globals.RESOLUTION_Y * 0.2)
    #     screen.blit(textSurf, textRect)
    #
    # def text_objects(self, text, font):
    #     textSurface = font.render(text, True, (255, 255, 255))
    #     return textSurface, textSurface.get_rect()
    #

