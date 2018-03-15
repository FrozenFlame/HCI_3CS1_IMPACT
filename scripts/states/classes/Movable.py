import math
'''
movable is a generic class that will allow us to take advantage of the animation code
'''

class Movable(object):

    def __init__(self, surface, speed, dspeed, move_type, defaultPos):
        self.surface = surface
        self.rect = surface.get_rect()
        self.posX = self.rect.center[0]
        self.posY = self.rect.center[1]

        self.is_visible = True

        self.defaultPos = defaultPos
        self.exact_position = list(self.rect.center)
        self.speed = speed
        self.dspeed = dspeed
        self.distance = None
        self.destination = None
        self.vector = None
        self.move_type = move_type

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
                self.vector = ((self.distance * self.dspeed)) * xDistance / self.distance, (
                       (self.distance * self.dspeed)) * yDistance / self.distance
                self.destination = list((x, y))
            except ZeroDivisionError:
                pass
        '''
        Distance: 100 (random angle)
        posX 100 defX 0 posY 200 defY 0
        '''
    def draw(self, screen):
        if self.is_visible:
            screen.blit(self.surface, self.rect)

    def back_to_default(self):
        self.set_destination(*self.defaultPos)
