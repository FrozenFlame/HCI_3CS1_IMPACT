from .Card import Card
class Hero:
    def __init__(self, name, img):
        self.name = name
        self.img = img




    def get_deck(self):  # TEMPORARILY FILLED WITH STATIC DATA
        # common pool 28, unique pool ~20
        deck = [Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(),  # common 28
                Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(),  #

                Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(), # unique 20
                Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card(), Card()] #
        return deck
