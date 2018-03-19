import pygame
class BoardField(object):
    def __init__(self,x1=0,y1=0,x2=0,y2=0, owner = "Nobody"):
        # x1,2 y1,2 are the dimensions of each point
        self.owner = owner
        self.xStart = x1
        self.xEnd = x2
        self.yStart = y1
        self.yEnd = y2
        self.cardList = []
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
        return (self.xStart, self.yStart, self.xEnd, self.yEnd-35)

    def get_rect(self):
        return self.rect

    def take_card(self, card):

        card.defaultPos = self.boardx, self.boardy
        self.cardList.append(card)
        card.onBoard = True
        # this is the TEMP WAY. We need to calculate based on num of cards in list.
        self.boardx += 80
        # print("[BoardField] I, {0} Owned by: {2} TOOK IN A CARD: {1}".format(self.boardy, card.name, self.owner))
        # print("I now have: {0} cards in my cardList who are:".format(len(self.cardList)))

        # for c in self.cardList:
        #     print("[BoardField] card.name, ",c.name)

    # quick n dirty
    def swap(self):
        # def __init__(self, x1=0, y1=0, x2=0, y2=0, owner="Nobody"):
        # self.boardFieldOpp2 = BoardField(225, 105, 1010, 185)  # opponent back row
        # self.boardFieldOpp = BoardField(225, 240, 1010, 320)  # opponent front row
        # self.boardField = BoardField(225, 390, 1010, 470)  # player front row
        # self.boardField2 = BoardField(225, 525, 1010, 605)  # player back row
        if self.yStart == 390:
            self.yStart = 240
            self.yEnd = 320
            self.boardy = self.yStart - 10
        elif self.yStart == 240:
            self.yStart = 390
            self.yEnd = 470
            self.boardy = self.yStart - 10

        elif self.yStart == 525:
            self.yStart = 105
            self.yEnd = 185
            self.boardy = self.yStart - 10
        elif self.yStart == 105:
            self.yStart = 525
            self.yEnd = 605
            self.boardy = self.yStart - 10
    def rearrange(self):
        self.boardx = self.xStart - 5
        for c in self.cardList:
            c.resting = False
            c.defaultPos = self.boardx, self.boardy
            c.set_destination(*c.defaultPos)
            self.boardx += 80

    def count_cardType(self, type):
        counter = 0
        for card in self.cardList:
            if type in card.type:
                counter += 1
        return counter

    def find_card(self, cardname):
        foundList = list()
        for card in self.cardList:
            if cardname is card.name:
                foundList.append(card)
        return foundList

    # make this class draw its cards within this class in order to have them render below non-board cards.