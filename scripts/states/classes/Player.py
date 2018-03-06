class Player:
    def __init__(self, user, hero):
        self.user = user
        self.hero = hero
        '''
        cards that will be pulled based on name
        '''
        # note: the data found in the heroes are hardcoded for now
        self.deck = hero.get_deck()
        self.hand = []  # initially empty because this will be made in-game


    def shuffle_deck(self):  # self explanatory
        pass

