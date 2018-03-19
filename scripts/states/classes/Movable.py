import math, pygame
'''
movable is a generic class that will allow us to take advantage of the animation code
'''

class Movable(object):

    def __init__(self, surface, speed, dspeed, move_type, defaultPos):
        self.surface = surface
        self.original_surface = surface  # in case we need to clean it up again
        self.new_surface = None
        self.rect = surface.get_rect()
        self.defaultPos = defaultPos
        # self.posX = self.rect.center[0]
        # self.posY = self.rect.center[1]
        self.posX = self.defaultPos[0]
        self.posY = self.defaultPos[1]
        self.exact_position = self.posX, self.posY
        self.rect.center = self.posX, self.posY
        self.is_visible = True

        self.exact_position = list(self.rect.center)
        self.speed = speed
        self.dspeed = dspeed
        self.distance = None
        self.destination = None
        self.vector = None
        self.move_type = move_type

        # scale factors
        self.is_scaling = False
        self.new_width = 0
        self.new_height = 0
        self.scalespeed = 10  # more of a tick delay
        self.scalexfactor = 4
        self.scalexstack = 0  # a separate tracker
        self.scaleyfactor = 5
        self.scaleystack = 0

    def update(self, dTime):
        if self.destination:
            if self.move_type == "constant":
                # self.set_destination(self.defaultPos[0], self.defaultPos[1])
                travelled = math.hypot(self.vector[0] * dTime, self.vector[1] * dTime)
                self.distance -= travelled
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

    def draw(self, screen):
        if self.is_visible:
            screen.blit(self.surface, self.rect)

    def change_acceleration(self, newdistancespeed):
        self.distancespeed = newdistancespeed

    def update_rect_center(self, center):
        self.rect.center = center

    def current_pos_as_default(self):  # UNSTABLE for now
        self.defaultPos = self.exact_position = self.rect.center
    def set_absolute(self, absolutexy):
        self.posX = absolutexy[0]
        self.posY = absolutexy[1]
        self.exact_position = list((absolutexy[0], absolutexy[1]))
        self.rect.center = absolutexy[0], absolutexy[1]

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

    def back_to_default(self):
        self.set_destination(*self.defaultPos)

    def is_pointed(self, x, y):
        collide = False
        # if (self.posX + self.rect.width) >= x >= self.posX and (self.posY + self.rect.height) >= y >= self.posY:
        #     collide = True
        collide = self.rect.collidepoint(x,y)
        return collide

    def scale_to(self, newxy):
        self.is_scaling = True
        self.new_width = newxy[0]
        self.new_height = newxy[1]

    def scaleanim(self, waitTick):
        currentTick = pygame.time.get_ticks()
        if currentTick - waitTick >= self.scalespeed:
            waitTick = currentTick
            if self.is_scaling:
                # print("Scaling like a dog")
                # self.surface = pygame.transform.smoothscale(self.surface, (round(50), round(50))).convert_alpha()
                if self.surface.get_rect().size[0] > self.new_width or self.surface.get_rect().size[1] > self.new_height:  # shrinking block
                    self.scalexstack = (self.scalexstack + self.scalexfactor) if self.surface.get_rect().size[0] > self.new_width else 0
                    self.scaleystack = (self.scaleystack + self.scaleyfactor) if self.surface.get_rect().size[1] > self.new_height else 0
                    self.surface = pygame.transform.smoothscale(self.original_surface, (self.original_surface.get_rect().size[0] - self.scalexstack, self.original_surface.get_rect().size[1] - self.scaleystack)).convert_alpha()
                else:
                    self.is_scaling = False



    def instascale(self, width, height):
        self.surface = pygame.transform.smoothscale(self.original_surface, (round(width),round(height)))
        self.new_width = round(width)
        self.new_height = round(height)
        self.rect.center = self.exact_position
        # self.posX = absolutexy[0]
        # self.posY = absolutexy[1]
        # self.exact_position = list((absolutexy[0], absolutexy[1]))
        # self.rect.center = absolutexy[0], absolutexy[1]

    def original_scale(self):
        self.surface = self.original_surface


    def instascalenew(self,width,height,new_img=None):  # None means you have a new image queued up, else, yuo can get from the outside
        if new_img:
            self.surface = pygame.transform.smoothscale(self.surface, (round(width), round(height)))
            self.new_width = round(width)
            self.new_height = round(height)
        else:
            self.surface = pygame.transform.smoothscale(self.new_surface, (round(width), round(height)))
            self.new_width = round(width)
            self.new_height = round(height)