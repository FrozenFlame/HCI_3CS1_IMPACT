class BoardField(object):
    def __init__(self,x1=0,y1=0,x2=0,y2=0, cards=[]):
        self.xStart = x1
        self.xEnd = x2
        self.yStart = y1
        self.yEnd = y2
        self.cards = cards