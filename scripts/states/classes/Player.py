class Player:
    def __init__(self, user, hero, deck):
        self.user = user
        self.hero = hero
        '''
        cards that will be pulled based on name
        '''
        # note: the data found in the heroes are hardcoded for now
        self.deck = deck
        self.hand = []  # initially empty because this will be made in-game

        self.cash = 0  # in game total cash value
        self.cashNegatives = list()
        self.cashPositives = list()
        self.hitpoints = 2  # life

    def renew_balances(self):
        del self.cashNegatives
        del self.cashPositives
        self.cashNegatives = list()
        self.cashPositives = list()


    def shuffle_deck(self):  # self explanatory
        pass

