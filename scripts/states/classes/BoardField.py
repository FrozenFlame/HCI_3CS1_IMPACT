import pygame
class BoardField(object):
    def __init__(self,x1=0,y1=0,x2=0,y2=0, cards=list()):
        # x1,2 y1,2 are the dimensions of each point
        self.xStart = x1
        self.xEnd = x2
        self.yStart = y1
        self.yEnd = y2
        self.cardList = cards
        self.rect = pygame.Rect((self.xStart, self.yStart), (self.xEnd -self.xStart, self.yEnd -self.yStart))


        # BoardField(225,390,1010,470, 220, 380) sample
        # self.boardx = 220
        # self.boardy = 380
        self.boardx = self.xStart - 5
        self.boardy = self.yStart - 10

        self.unarranged = True

    def get_dimensions(self):
        # return (self.xStart, self.yStart, self.xEnd, self.yEnd)
        # return trim down bottom
        return (self.xStart, self.yStart, self.xEnd, self.yEnd-50)

    def get_rect(self):
        return self.rect

    def take_card(self, card):
        card.defaultPos = self.boardx, self.boardy
        self.cardList.append(card)
        # this is the TEMP WAY. We need to calculate based on num of cards in list.
        self.boardx += 80