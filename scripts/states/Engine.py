import pygame, math, time, random
from enum import Enum, auto
from .classes.BoardField import BoardField
from .classes.Card import Card
from .classes.Board import Board

from .. import tools

from ..Globals import Globals
'''
This class is the actual game between two players
'''
print("[Engine.py]Engine Loaded")

#THIS IS JUS A DUMMY OBJECT

'''
GAMEBOARD NOTES:
Needs:
Standard coordinates (and corresponding area for blitting) for rows, coin, portraits, playername, and etc. 
I'm sure we can come up with an algorithm so that we can have the cards that have been set to reposition when another 
card gets played

Biggest issue of them all (I think):
Phases of the game
Rough code estimate would be like:

(a loop, 2-3 times)
    round starts
    <draw cards for both players>
    player1 receives first 10 cards
    player2 receives first 10 cards
    <larger hand cards displayed on screen>
    player1 chooses to mulligan or not
    player2 chooses to mulligan or not
    <cards assume hand coordinates and scale>
    <coin toss animation> - first player to take turn decided
    (an inner round loop, repeats however many times possible)
        start turn
        <animations expected for this phase> - this part lol
        end of turn
    (end of inner round loop, repeat)

(end of phase, repeat)
<victory animation> - a player gets crowned victorious
'''
# class which holds the game flow
class Engine(object):
    # def __init__(self): we're gonna create
    def __init__(self):
        tools.State.__init__(self)  # inheriting from State class.

        self.next = "GAME_SUMMARY"  # the next state by default would be the victory/defeat summary screen

        self.bgm = None  # the bgm of the hero
        self.waitTick = pygame.time.get_ticks()  # will be used to for computing how long it has already waited  # up for deletion

        # Game trackers
        self.turn_no = 0
        self.player = None
        self.player2 = None
        self.first_player = None # does not change after coin toss
        self.opponent = None
        self.passed = None  # a player has passed their turn
        self.cards_played = 0  # counter to determine how many cards you've played that turn
        self.phase = Phase.COIN_TOSS

        # logic booleans
        self.first_player_set = False  # becomes true after coin toss, and hands/decks set
        self.holdingCard = False
        self.done_turn = False
        self.may_flip_board = False
        self.may_count_turn = False
        self.may_drag = False
        # self.opening = True

        # objects
        self.board = None  # this rarely changes, maybe the board graphic but idk
        self.deck = None
        self.hand = None
        self.opponent_deck = None
        self.opponent_hand = None

        self.boardFieldOpp2 = None  # opponent back row
        self.boardFieldOpp = None   # opponent front row
        self.boardField = None      # player front row
        self.boardField2 = None     # player back row
        # self.boardFieldList = [self.boardField, self.boardField2, self.boardFieldOpp, self.boardFieldOpp2]
        self.boardFieldList = [self.boardField, self.boardField2]
        # self.boardCardList = list()

        self.allCardsList = list()

        self.clickedCard = list()

        '''scenario: the 10 hand cards start at the top of the deck/deckImgHolder3, then use waitTick so that 1 card animates(similarly to the click-and-drag animation)
         to its hand position every 1 second
         formula for wait:
                  if currentTick - self.waitTick >= self.drawCardWait:
                        self.waitTick = currentTick
                        [do stuff]
        '''
        self.drawCardSound = pygame.mixer.Sound("assets\\cards\\draw_card.wav")     # may be confused with draw()


        self.opening = True
        # self.drawCardWait = 250
        self.drawCardWait = 50
        self.openingIndex = 0
        self.openingX = 220                # hand coordinate is from 220 to 1020 (PLAYER)
        self.openingY = 600
        self.openingXOpp = 220  # hand coordinate is from 220 to 1020 (OPP)
        self.openingYOpp = -20


        self.deckImgHolder1 = Card()     #add formula to determine how many deckImgHolders; ex. (no. of cards in deck) / 3 = (no. of deckImgHolders)
        self.deckImgHolder2 = Card()     # or have preset of (x number of deckHolders) then hide the top deckHolder for every 5 cards removed from deck
        self.deckImgHolder3 = Card()


        '''
        UI things (initial state)
        '''
        self.showEndTurnButton = False
        self.showPassTurnButton = False
        self.showHandButton = False
        self.endTurnImg = pygame.image.load("assets\\buttons\\end_turn.bmp").convert_alpha()
        self.passTurnImg = pygame.image.load("assets\\buttons\\pass_turn.bmp").convert_alpha()
        self.showHandImg = pygame.image.load("assets\\buttons\\show_hand.bmp").convert_alpha()
        self.mouseOnEndTurnButton = False
        self.mouseOnPassTurnButton = False
        self.mouseOnShowHandButton = False
        self.endTurnImgX = 50
        self.endTurnImgY = 335
        self.showHandImgX = Globals.RESOLUTION_X * 0.44
        self.showHandImgY = Globals.RESOLUTION_Y * 0.90
        self.endTurnImgDimensionX = 110
        self.endTurnImgDimensionY = 53

        self.graveYardX = Globals.RESOLUTION_X * 0.80
        self.graveYardY = Globals.RESOLUTION_Y * 0.80
        self.graveYardList = list()

        self.graveYardOppX = Globals.RESOLUTION_X * 0.80
        self.graveYardOppY = Globals.RESOLUTION_Y * 0.25
        self.graveYardListOpp = list()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  _____                       ______                _   _
# |  __ \                      |  ___|              | | (_)
# | |  \/ __ _ _ __ ___   ___  | |_ _   _ _ __   ___| |_ _  ___  _ __  ___
# | | __ / _` | '_ ` _ \ / _ \ |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | |_\ \ (_| | | | | | |  __/ | | | |_| | | | | (__| |_| | (_) | | | \__ \
#  \____/\__,_|_| |_| |_|\___| \_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def flip_hand(self, hand):
        for h in hand:
            h.flip()

    def get_first_cards(self, deck, username):
        print("Giving first cards of: ", username )
        random.shuffle(deck)
        first_ten = []
        for i in range(0, 10):  # self minus due to simultaneous pop will offset this
            print("GETFIRST ", i)
            first_ten.append(deck[i-i])
            deck.pop(i-i)
        return first_ten

    def flip_coin(self):
        self.board.flipCoin()
    def toss_coin(self):
        self.board.tossCoin()
    def coin_side(self):
        return self.board.coin.side

    def shuffle_deck(self, deck):
        random.shuffle(deck)

    def swap_player(self, player):
        temp = player
        self.player = self.player2
        self.player2 = temp

    def sendToGraveyard(self, card):
        self.graveYardX += 5*(int(len((self.graveYardList)/5)))
        self.graveYardOppX += 5*(int(len((self.graveYardListOpp)/5)))


        for boardCard in self.boardField.cardList:
            if card == boardCard:
                self.boardField.cardList.pop(self.boardField.cardList.index(boardCard))
                self.graveYardList.append(card)
                card.defaultPos = self.graveYardX, self.graveYardY

        for boardCard in self.boardField2.cardList:
            if card == boardCard:
                self.boardField2.cardList.pop(self.boardField2.cardList.index(boardCard))
                self.graveYardList.append(card)
                card.defaultPos = self.graveYardX, self.graveYardY


        for boardCard in self.boardFieldOpp.cardList:
            if card == boardCard:
                self.boardFieldOpp.cardList.pop(self.boardFieldOpp.cardList.index(boardCard))
                self.graveYardListOpp.append(card)
                card.defaultPos = self.graveYardOppX, self.graveYardY

        for boardCard in self.boardFieldOpp2.cardList:
            if card == boardCard:
                self.boardFieldOpp2.cardList.pop(self.boardFieldOpp2.cardList.index(boardCard))
                self.graveYardListOpp.append(card)
                card.defaultPos = self.graveYardOppX, self.graveYardY


        card.resting = False
        card.set_destination(card.defaultPos)



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  _____                        _                 _
# |  __ \                      | |               (_)
# | |  \/ __ _ _ __ ___   ___  | |     ___   __ _ _  ___
# | | __ / _` | '_ ` _ \ / _ \ | |    / _ \ / _` | |/ __|
# | |_\ \ (_| | | | | | |  __/ | |___| (_) | (_| | | (__
#  \____/\__,_|_| |_| |_|\___| \_____/\___/ \__, |_|\___|
#                                            __/ |
#                                           |___/
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



    def cardMousedOver(self, xy) -> bool:
        self.clickedCard = [s for s in self.allCardsList if s.collidepoint(xy[0], xy[1])]  # not actually clicked, but moused over
        return True if len(self.clickedCard) == 1 else False

    # def cardMousedOver2(self, xy):
    #     self.clickedCard = [s for s in self.allCardsList if s.collidepoint(xy[0], xy[1])]
    #     return self.clickedCard


    def backToMain(self):
        Globals.state = "MAIN_MENU"
        self.next = Globals.state
        self.finished = True

    def play_card(self):  # initial concept, listener type thing.
        print("PLAYED BY: ", self.player.user.username)
        self.showPassTurnButton = False
        self.showEndTurnButton = True
        self.cards_played += 1
        print(self.cards_played)
        if self.cards_played == 3 and not self.passed:
            self.may_drag = False

    def end_turn(self):
        # self.done_turn = True
        self.showPassTurnButton = False
        self.showEndTurnButton = False
        self.cards_played = 0

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  _____ _        _        ______                _   _
# /  ___| |      | |       |  ___|              | | (_)
# \ `--.| |_ __ _| |_ ___  | |_ _   _ _ __   ___| |_ _  ___  _ __  ___
#  `--. \ __/ _` | __/ _ \ |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# /\__/ / || (_| | ||  __/ | | | |_| | | | | (__| |_| | (_) | | | \__ \
# \____/ \__\__,_|\__\___| \_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_evt(self, event):
        if event.type == pygame.QUIT:
            self.done = True
        #if self.board.hasPreviewCard:
         #   print("Previewing card.")
        #card is being moused

        # print("[Engine.py] - KEYDOWN: {0}".format(pygame.key.get_pressed()))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("[Engine(STATE)] Escape Pressed")
                # TEMPORARY METHOD:
                self.backToMain()
            if event.key == pygame.K_d:
                print("[Engine] self.allCardsList[0]: ", self.allCardsList[0])
                self.allCardsList[0].resting = False
                self.allCardsList[0].set_destination(100,100)
            if event.key == pygame.K_a:
                print("defaultpos0 ",self.allCardsList[0].defaultPos[0]," defaultpos1 ", self.allCardsList[0].defaultPos[1])
        #     pass
        if self.cardMousedOver(pygame.mouse.get_pos()):
            # print("Mousingover")
            if self.clickedCard[0].front:
                self.board.hasPreviewCard = True
                self.board.previewCard = self.clickedCard[0] # this actually must be the card that's being moused over.
        elif not self.cardMousedOver(pygame.mouse.get_pos()):
            # print("notmousing")
            self.board.hasPreviewCard = False if not self.holdingCard else True

        ''' GET EVENT
         ____  _  _   __   ____  ____  ____ 
        (  _ \/ )( \ / _\ / ___)(  __)/ ___)
         ) __/) __ (/    \\___ \ ) _) \___ \
        (__)  \_)(_/\_/\_/(____/(____)(____/
        
        '''
        if self.phase == Phase.PLAY:
            if event.type == pygame.MOUSEBUTTONUP:
                click = pygame.mouse.get_pressed()
                if click[0] == 0:

                    if self.mouseOnEndTurnButton and self.showEndTurnButton:
                        self.done_turn = True
                        self.showEndTurnButton = False
                    if self.mouseOnPassTurnButton and self.showPassTurnButton:
                        print("TURN PASSED")
                        self.done_turn = True
                        self.showEndTurnButton = False
                        self.showPassTurnButton = False
                        self.passed = True

                    print("unheld")
                    self.holdingCard = False
                    if self.cardMousedOver(pygame.mouse.get_pos()):
                        self.board.hasPreviewCard = False
                    if not len(self.clickedCard) == 0:
                        self.clickedCard[0].isHeld = False
                        # self.clickedCard[0].flip()

                        #let go into a boardField
                        # if self.clickedCard[0].colliderect(self.boardField.xStart,self.boardField.yStart,self.boardField.xEnd,self.boardField.yEnd) and not self.clickedCard[0].onBoard:
                        #     self.boardCardList.append(self.clickedCard[0])
                        #     self.clickedCard[0].onBoard = True

                        if self.player == self.first_player:  #
                            for bF in self.boardFieldList:
                                if self.clickedCard[0].collide_rect(*bF.get_dimensions()):
                                    bF.take_card(self.clickedCard[0])

                                    # bF.cardList.append(self.clickedCard[0])
                                    self.clickedCard[0].onBoard = True
                                    print("Card({0}) placed into BoardField({1})".format(self.clickedCard[0].name, bF.owner))
                                    print("This is BoardFieldCoordinates: {0}".format(bF.boardy))
                                    self.play_card()
                                    # self.end_turn()
                        elif self.player2 == self.first_player:
                            for bF in self.boardFieldListOpp:
                                if self.clickedCard[0].collide_rect(*bF.get_dimensions()):
                                    bF.take_card(self.clickedCard[0])

                                    # bF.cardList.append(self.clickedCard[0])
                                    self.clickedCard[0].onBoard = True
                                    print("Card({0}) placed into BoardField({1})".format(self.clickedCard[0].name, bF.owner))
                                    print("This is BoardFieldCoordinates: {0}".format(bF.boardy))
                                    self.play_card()
                                    # self.end_turn()



                        # # OPPONENT Board placement/collision logic
                        # for bF in self.boardFieldListOpp: # REMOVE THIS THIS IS JUST TO FIND THE RIGHT NUMBERS FOR BOARDFIELD
                        #     if self.clickedCard[0].collide_rect(*bF.get_dimensions()) and not self.clickedCard[0].onBoard:
                        #         bF.take_card(self.clickedCard[0])
                        #
                        #         # bF.cardList.append(self.clickedCard[0])
                        #         self.clickedCard[0].onBoard = True
                        #         print("Card({0}) placed into BoardField({1})".format(self.clickedCard[0], bF))
                        #         self.play_card()
                        #         self.end_turn()
                        #
                        # if self.clickedCard[0].destination == None:
                        #     self.clickedCard.pop()


            if event.type == pygame.MOUSEBUTTONDOWN and not self.opening:
                # print("AllCardsList: {0}HandsList: {1}BoardCardList:{2}".format(len(self.allCardsList), len(self.hand), len(self.boardCardList)))

                # print("Pos: {0} , {1}".format(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
                click = pygame.mouse.get_pressed()
                # print("Clicked: {0}".format(click))

                if click[0] == 1:

                    for s in self.allCardsList:
                        if s.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                            self.clickedCard.append(s)
                            s.onTop = True
                            self.allCardsList.pop(self.allCardsList.index(s))
                            self.allCardsList.append(s)

                    if len(self.clickedCard) > 0:
                        if self.clickedCard[0].disabled == False and self.clickedCard[0].onBoard == False and self.may_drag:
                            print("handcard clicked")
                            self.clickedCard[0].isHeld = True
                            self.holdingCard = True
                            self.clickedCard[0].resting = False
                            self.clickedCard[0].set_destination(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                            self.drawCardSound.play()

        elif self.phase == Phase.SWAP:
            # have some fade animation play here, give flag to swap elements, and prep someone to play >mostly flags in get_evt
            # pseudo flag fade out
            # pseudo flag delay, allow update to spin the board
            self.may_flip_board = True
            # pseudo flag fade in
            # pseudo flag cue prep phase
            pass
        elif self.phase == Phase.PREP:
            # accept click stroke onto "Show" Button
            # print("Player {0}, it's your turn.".format(self.player.user.username))
            if self.showHandButton and (self.showHandImgX + self.endTurnImgDimensionX) > pygame.mouse.get_pos()[0] > self.showHandImgX and (self.showHandImgY + self.endTurnImgDimensionY) > pygame.mouse.get_pos()[1] > self.showHandImgY:
                self.mouseOnShowHandButton = True
                self.may_drag = True
                pass
            elif self.showHandButton:
                self.mouseOnShowHandButton = False
                pass
            if event.type == pygame.MOUSEBUTTONUP:
                click = pygame.mouse.get_pressed()
                if click[0] == 0:
                    if self.mouseOnShowHandButton and self.showHandButton:
                        print("Showing cards")
                        self.flip_hand(self.hand)
                        self.phase = Phase.PLAY
                        self.showHandButton = False
                        self.showPassTurnButton = True
            # clicking this will set phase to Play

            # self.phase = Phase.PLAY  # TODO temporarily going to make it auto accept

        if self.done_turn:
            self.end_turn()
            self.phase = Phase.SWAP

    # orders individual elements to update themselves (your coordinates, sprite change, state, etc)
    def update(self, screen, keys, currentTime, deltaTime):
        # print("BOARD FIELDOpp2 LEN: ", len(self.boardFieldOpp2.cardList))
        # print("BOARD FIELDOpp LEN: ", len(self.boardFieldOpp.cardList))
        # print("BOARD FIELD LEN: ", len(self.boardField.cardList))
        # print("BOARD FIELD2 LEN: ", len(self.boardField2.cardList))

        ''' UPDATE
         ____  _  _   __   ____  ____  ____
        (  _ \/ )( \ / _\ / ___)(  __)/ ___)
         ) __/) __ (/    \\___ \ ) _) \___ \
        (__)  \_)(_/\_/\_/(____/(____)(____/
        
        '''
        if not self.opening:
            # print(self.player.user.username)
            # print(self.turn_no)
            # print(self.boardField.yStart)
            # print(self.hand[0].name)
            pass

        for a in self.allCardsList:  # updates all existing cards
            if not a.resting:
                if a.isHeld:
                    a.update(deltaTime, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                else:
                    a.update(deltaTime, a.defaultPos[0], a.defaultPos[1])
            if a.flipAnimating:  # card has been flipped, update through flipAnim function w/ waitTicks
                a.flipAnim(self.waitTick)
        if self.first_player_set:
            for h in self.hand:
                initialHandlength = len(self.hand)
                if h.onBoard:
                    self.hand.pop(self.hand.index(h))
                if len(self.hand) < initialHandlength:
                    initialHandlength = len(self.hand)
                    newX = 620 - (40 * len(self.hand))
                    for h2 in self.hand:
                        h2.resting = False
                        h2.set_destination(h.posX, h.posY)

                        # xRange of hand Cards is 220 to 1020 . 800 distance . middle point is 620 . starting handLength is 10 . formula? 620 - (40*handLength)
                        h2.defaultPos = (newX, self.openingY)  # 600 = self.openingY
                        h2.update(deltaTime, newX, self.openingY)
                        newX += 80
            for h in self.opponent_hand:
                initialHandlength = len(self.opponent_hand)
                if h.onBoard:
                    self.opponent_hand.pop(self.opponent_hand.index(h))
                if len(self.opponent_hand) < initialHandlength:
                    initialHandlength = len(self.opponent_hand)
                    newX = 620 - (40 * len(self.opponent_hand))
                    for h2 in self.opponent_hand:
                        h2.resting = False
                        h2.set_destination(h.posX, h.posY)

                        # xRange of hand Cards is 220 to 1020 . 800 distance . middle point is 620 . starting handLength is 10 . formula? 620 - (40*handLength)
                        h2.defaultPos = (newX, self.openingYOpp)  # 600 = self.openingY
                        h2.update(deltaTime, newX, self.openingYOpp)
                        newX += 80

        if self.phase == Phase.PLAY:
            if not self.done_turn:
                if self.showEndTurnButton and (self.endTurnImgX + self.endTurnImgDimensionX) > pygame.mouse.get_pos()[0] > self.endTurnImgX and (self.endTurnImgY + self.endTurnImgDimensionY) > \
                        pygame.mouse.get_pos()[1] > self.endTurnImgY:
                    self.mouseOnEndTurnButton = True
                    # print("Mouse on end turn button")
                elif self.showEndTurnButton:
                    self.mouseOnEndTurnButton = False
                    # print("Mouse NOT on end turn button")
                elif self.showPassTurnButton and (self.endTurnImgX + self.endTurnImgDimensionX) > pygame.mouse.get_pos()[0] > self.endTurnImgX and (self.endTurnImgY + self.endTurnImgDimensionY) > \
                        pygame.mouse.get_pos()[1] > self.endTurnImgY:
                    self.mouseOnPassTurnButton = True
                    # print("Mouse on pass turn button")
                elif self.showPassTurnButton:
                    self.mouseOnPassTurnButton = False
                    # print("Mouse NOT on pass turn button")
                pass
            else:
                self.phase = Phase.SWAP
                self.done_turn = False
                self.showEndTurnButton = False  #this is not working
        elif self.phase == Phase.SWAP:
            for hC in self.hand:
                hC.swap()
            for hC in self.opponent_hand:
                hC.swap()
            for bF in self.boardFieldList:
                bF.swap()
                bF.rearrange()
            for bF in self.boardFieldListOpp:
                bF.swap()
                bF.rearrange()
            # fade value changes fading in
            # FLIPPING BOARD #
            # print()
            self.flip_hand(self.hand)  # TODO somehow this line makes the cards swapping less consistently

            tempHand = self.hand
            tempDeck = self.deck
            tempBackRow = self.boardField2
            tempFrontRow = self.boardField
            tempBoardFieldList = self.boardFieldList

            self.hand = self.opponent_hand
            self.deck = self.opponent_deck
            self.boardField = self.boardFieldOpp
            self.boardField2 = self.boardFieldOpp2
            self.boardFieldList = [self.boardField, self.boardField2]
            # setting opponent
            self.opponent_hand = tempHand
            self.opponent_deck = tempDeck
            self.boardFieldOpp = tempFrontRow
            self.boardFieldOpp2 = tempBackRow
            self.boardFieldList = tempBoardFieldList

            '''
            a = b
            b = c
            c += 1
            print a
            '''

            # END OF FLIPPING BOARD #
            # fade value changes fading out

            if self.may_count_turn:
                self.turn_no += 1
                self.may_count_turn = False
            if self.first_player == self.player:
                self.may_count_turn = True

            self.swap_player(self.player)
            self.phase = Phase.PREP
            self.done_turn = False

        elif self.phase == Phase.PREP:
            # more on animations updates
            self.showHandButton = True

            pass
        elif self.phase == Phase.OPENING:
            currentTick = currentTime

            # for now player 1 ALWAYS chooses heads
            if not self.first_player_set:
                if self.coin_side() == 0:
                    print("LANDED HEADS")
                    self.deck = self.persist['playerA'].deck
                    self.opponent_deck = self.persist['playerB'].deck
                    self.hand = self.get_first_cards(self.deck,self.persist['playerA'].user.username)
                    self.opponent_hand = self.get_first_cards(self.opponent_deck,self.persist['playerB'].user.username)

                    self.player = self.persist['playerA']
                    self.first_player = self.persist['playerA']
                    self.player2 = self.persist['playerB']

                    self.boardField.owner = self.persist['playerA'].user.username
                    self.boardField2.owner = self.persist['playerA'].user.username

                    self.boardFieldOpp.owner = self.persist['playerB'].user.username
                    self.boardFieldOpp2.owner = self.persist['playerB'].user.username

                    self.first_player_set = True
                else:
                    print("LANDED TAILS")
                    self.deck = self.persist['playerB'].deck
                    self.opponent_deck = self.persist['playerA'].deck
                    self.hand = self.get_first_cards(self.deck, self.persist['playerB'].user.username)
                    self.opponent_hand = self.get_first_cards(self.opponent_deck, self.persist['playerA'].user.username)

                    self.player = self.persist['playerB']
                    self.first_player = self.persist['playerB']
                    self.player2 = self.persist['playerA']

                    self.boardField.owner = self.persist['playerB'].user.username
                    self.boardField2.owner = self.persist['playerB'].user.username

                    self.boardFieldOpp.owner = self.persist['playerA'].user.username
                    self.boardFieldOpp2.owner = self.persist['playerA'].user.username

                    self.first_player_set = True

            # graphical representation of card giving (hands are already pre determined by get_first_cards)
            if currentTick - self.waitTick >= self.drawCardWait:
                if self.openingIndex < 10:
                    self.waitTick = currentTick
                    self.drawCardSound.stop()
                    self.drawCardSound.play()
                    self.hand[self.openingIndex].resting = False
                    self.hand[self.openingIndex].set_destination(1180, 563)
                    self.hand[self.openingIndex].defaultPos = (self.openingX, self.openingY)
                    self.hand[self.openingIndex].update(deltaTime, self.openingX, self.openingY)

                    self.opponent_hand[self.openingIndex].resting = False
                    self.opponent_hand[self.openingIndex].set_destination(1180, 100)
                    self.opponent_hand[self.openingIndex].posY = 100
                    self.opponent_hand[self.openingIndex].defaultPos = (self.openingXOpp, self.openingYOpp)
                    self.opponent_hand[self.openingIndex].update(deltaTime, self.openingXOpp, self.openingYOpp)

                    self.allCardsList.append(self.hand[self.openingIndex])
                    self.allCardsList.append(self.opponent_hand[self.openingIndex])
                    self.openingX += 80
                    self.openingXOpp += 80
                    self.openingIndex += 1
                if self.openingIndex == 10:

                    self.opening = False
                    self.phase = Phase.PREP
        elif self.phase == Phase.COIN_TOSS:
            # additional animation updates
            self.toss_coin()
            self.phase = Phase.OPENING


        #
        self.deckImgHolder1.update(deltaTime, 1170, 565)
        self.deckImgHolder2.update(deltaTime, 1175, 564)
        self.deckImgHolder3.update(deltaTime, 1180, 563)

        self.draw(screen) # last function of update. execute draw







    # orders individual elements to draw themselves in the correct order (your blits)
    def draw(self, screen):
        self.board.draw(screen)
        # self.screen.fill((100,100,100))
        # if not self.card.blitted:               #another way of instantiating, compared to elif h.resting and not h.blitted in update method
        #     self.card.posX, self.card.posY = self.boardField.xStart, self.boardField.yStart
        #     self.card.blitted = True
        # self.card.draw(screen)

        onTopCard = None
        for a in self.allCardsList:
            if not a.onTop:
                a.draw(screen)
            else:
                onTopCard = a
        if onTopCard != None:
            onTopCard.draw(screen)
            onTopCard.onTop = False

        self.deckImgHolder1.draw(screen)
        self.deckImgHolder2.draw(screen)
        self.deckImgHolder3.draw(screen)

        if self.showEndTurnButton:
            screen.blit(self.endTurnImg, (self.endTurnImgX, self.endTurnImgY))
        elif self.showPassTurnButton:
            screen.blit(self.passTurnImg, (self.endTurnImgX, self.endTurnImgY))
        if self.showHandButton:
            screen.blit(self.showHandImg, (self.showHandImgX, self.showHandImgY))



    def startup(self, currentTime, persistent):

        self.persist = persistent
        self.startTime = currentTime

        '''
        testing persistent objects
        '''
        print("[Engine] ########################### ")
        print("[Engine] {0}({1}) vs {2}({3})".format(self.persist['playerA'].user.username, self.persist['playerA'].hero.name, self.persist['playerB'].user.username, self.persist['playerB'].hero.name))
        print("[Engine] THE BATTLE BEGINS")
        '''
        setting of board objects and setting of first perspective
        '''
        self.board = Board()
        # BoardField(x1=225, y1=390, x2=1010, y2=470, boardx=220, boardy=380)
        self.boardFieldOpp2 = BoardField(225,105,1010,185)  # opponent back row
        self.boardFieldOpp = BoardField(225,240,1010,320)  # opponent front row
        self.boardField = BoardField(225,390,1010,470)  # player front row
        self.boardField2 = BoardField(225,525,1010,605)  # player back row
        self.boardFieldList = [self.boardField, self.boardField2]
        self.boardFieldListOpp = [self.boardFieldOpp, self.boardFieldOpp2]

        # Game trackers
        self.turn_no = 0
        self.player = None
        self.player2 = None
        self.first_player = None  # does not change after coin toss
        self.opponent = None
        self.phase = Phase.COIN_TOSS
        self.cards_played = 0


        # #temp
        # self.deck = self.persist['playerB'].deck
        # self.opponent_deck = self.persist['playerA'].deck
        # self.hand = self.get_first_cards(self.deck)
        # self.opponent_hand = self.get_first_cards(self.opponent_deck)
        # self.player = self.persist['playerB']
        # self.first_player = self.persist['playerB']
        # self.player2 = self.persist['playerA']
        # #endtemp

        self.opening = True
        self.done_turn = False


    def cleanup(self):
        self.board = None
        self.boardField = None
        self.deck = None
        self.opponent_deck = None
        self.hand = None
        self.opponent_hand = None
        self.opening = False
        self.done = False
        Globals.gameStart = False
        return self.persist

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  _____                        _____ _
# |_   _|                      /  __ \ |
#   | | _ __  _ __   ___ _ __  | /  \/ | __ _ ___ ___  ___  ___
#   | || '_ \| '_ \ / _ \ '__| | |   | |/ _` / __/ __|/ _ \/ __|
#  _| || | | | | | |  __/ |    | \__/\ | (_| \__ \__ \  __/\__ \
#  \___/_| |_|_| |_|\___|_|     \____/_|\__,_|___/___/\___||___/
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Phase(Enum):
    # auto() is an enum function that makes it decide what type to use for that enum
    COIN_TOSS = auto()      # flipping of coin, decides player1 and 2
    OPENING = auto()        # 10 cards drawn

    SWAP = auto()           # Screen fades out, board flips
    PREP = auto()           # Player about to start turn
    PLAY = auto()           # Player controls are enabled, can click around etc.

    # currently not yet used
    END_ROUND = auto()      # both players have now selected PASS
    ROUND_DRAW = auto()     # Two cards drawn
    ROUND_TWO = auto()      # Two cards drawn
    FINAL_ROUND = auto()    # One card drawn
