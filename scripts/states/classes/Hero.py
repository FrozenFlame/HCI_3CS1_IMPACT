from .Card import Card
class Hero:
    def __init__(self, name, img):
        self.name = name
        self.img = img




    def get_deck(self):  # TEMPORARILY FILLED WITH STATIC DATA
        # common pool 28, unique pool ~20
        deck = [Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name),  # common 28
                Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name),  #

                Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), # unique 20
                Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name), Card(self.name)] #
        return deck
