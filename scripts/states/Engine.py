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
        # Game phase trackers
        self.dictionary = {} # names made available to the phasemanager

        self.phasemgr = PhaseManager(self.dictionary, self.waitTick)

        self.turn_no = 0
        self.phasemgr.set_phase(Phase.OPENING)


        # logic booleans
        self.holdingCard = False
        # self.opening = True

        # objects
        self.board = None  # this rarely changes, maybe the board graphic but idk
        self.deck = None
        self.hand = None
        self.opponent_deck = None
        self.opponent_hand = None
        self.boardFieldOpp2 = None  # bottom row, opponent
        self.boardFieldOpp = None  # top row, opponent
        self.boardField = None   # top row, player
        self.boardField2 = None  # bottom row, player

        self.boardCardList = list()

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

        # self.opening = True  # moved val to dictionary
        ## up for deletion ##
        # self.drawCardWait = 250  # wait for 1 second, adjust this kasi parang ang bagal mag draw nung initial 10 cards
        # self.openingIndex = 0
        # self.openingX = 220                # hand coordinate is from 220 to 1020
        # self.openingY = 600
        ## up for deletion ##

        self.deckImgHolder1 = Card()     #add formula to determine how many deckImgHolders; ex. (no. of cards in deck) / 3 = (no. of deckImgHolders)
        self.deckImgHolder2 = Card()     # or have preset of (x number of deckHolders) then hide the top deckHolder for every 5 cards removed from deck
        self.deckImgHolder3 = Card()


#
#  _____                       ______                _   _
# |  __ \                      |  ___|              | | (_)
# | |  \/ __ _ _ __ ___   ___  | |_ _   _ _ __   ___| |_ _  ___  _ __  ___
# | | __ / _` | '_ ` _ \ / _ \ |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | |_\ \ (_| | | | | | |  __/ | | | |_| | | | | (__| |_| | (_) | | | \__ \
#  \____/\__,_|_| |_| |_|\___| \_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#







    def get_first_cards(self, deck):
        random.shuffle(deck)
        first_ten = []
        for i in range(0, 10):  # self minus due to simultaneous pop will offset this
            first_ten.append(deck[i-i])
            deck.pop(i-i)

        return first_ten

    def flip_coin(self):
        pass

    def shuffle_deck(self, deck):
        random.shuffle(deck)
#
#  _____                        _                 _
# |  __ \                      | |               (_)
# | |  \/ __ _ _ __ ___   ___  | |     ___   __ _ _  ___
# | | __ / _` | '_ ` _ \ / _ \ | |    / _ \ / _` | |/ __|
# | |_\ \ (_| | | | | | |  __/ | |___| (_) | (_| | | (__
#  \____/\__,_|_| |_| |_|\___| \_____/\___/ \__, |_|\___|
#                                            __/ |
#                                           |___/
#



    def cardMousedOver(self, xy) -> bool:
        self.clickedCard = [s for s in self.allCardsList if s.collidepoint(xy[0], xy[1])]
        return True if len(self.clickedCard) == 1 else False

    # def cardMousedOver2(self, xy):
    #     self.clickedCard = [s for s in self.allCardsList if s.collidepoint(xy[0], xy[1])]
    #     return self.clickedCard


    def backToMain(self):
        Globals.state = "MAIN_MENU"
        self.next = Globals.state
        self.finished = True

#  _____ _        _        ______                _   _
# /  ___| |      | |       |  ___|              | | (_)
# \ `--.| |_ __ _| |_ ___  | |_ _   _ _ __   ___| |_ _  ___  _ __  ___
#  `--. \ __/ _` | __/ _ \ |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# /\__/ / || (_| | ||  __/ | | | |_| | | | | (__| |_| | (_) | | | \__ \
# \____/ \__\__,_|\__\___| \_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#

    def get_evt(self, event):
        if event.type == pygame.QUIT:
            self.done = True
        #if self.board.hasPreviewCard:
         #   print("Previewing card.")
        #card is being moused
        self.phasemgr.get_event(event)


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
            self.board.hasPreviewCard = True
            self.board.previewCard = self.clickedCard[0] # this actually must be the card that's being moused over.
        elif not self.cardMousedOver(pygame.mouse.get_pos()):
            # print("notmousing")
            self.board.hasPreviewCard = False if not self.holdingCard else True

        if event.type == pygame.MOUSEBUTTONDOWN and not self.dictionary['opening']:
            print(len(self.clickedCard))
            print("AllCardsList: {0}HandsList: {1}BoardCardList:{2}".format(len(self.allCardsList), len(self.hand), len(self.boardCardList)))

            print("Pos: {0} , {1}".format(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
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
                    if self.clickedCard[0].disabled == False and self.clickedCard[0].onBoard == False:
                        print("handcard clicked")
                        self.clickedCard[0].isHeld = True
                        self.holdingCard = True
                        self.clickedCard[0].resting = False
                        self.clickedCard[0].set_destination(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                        self.drawCardSound.play()
        #
        # if event.type == pygame.MOUSEBUTTONUP:
        #     click = pygame.mouse.get_pressed()
        #     if click[0] == 0:
        #         print("unheld")
        #         self.holdingCard = False
        #         self.board.hasPreviewCard = False
        #         if not len(self.clickedCard) == 0:
        #             self.clickedCard[0].isHeld = False
        #             # self.clickedCard[0].flip()
        #             if self.clickedCard[0].colliderect(self.boardField.xStart,self.boardField.yStart,self.boardField.xEnd,self.boardField.yEnd) and not self.clickedCard[0].onBoard:
        #                 self.boardCardList.append(self.clickedCard[0])
        #                 self.clickedCard[0].onBoard = True
        #
        #             if self.clickedCard[0].destination == None:
        #                 self.clickedCard.pop()



    # orders individual elements to update themselves (your coordinates, sprite change, state, etc)
    def update(self, screen, keys, currentTime, deltaTime):
        self.phasemgr.update(currentTime, deltaTime)
        # if self.opening == True:
        #     currentTick = currentTime
        #     if currentTick - self.waitTick >= self.drawCardWait:
        #         if self.openingIndex < 10:
        #             self.waitTick = currentTick
        #             # self.drawCardSound.stop()
        #             self.drawCardSound.play()
        #             self.hand[self.openingIndex].resting = False
        #             self.hand[self.openingIndex].set_destination(1180, 563)
        #             self.hand[self.openingIndex].defaultPos = (self.openingX, self.openingY)
        #             self.hand[self.openingIndex].update(deltaTime, self.openingX, self.openingY)
        #             self.allCardsList.append(self.hand[self.openingIndex])
        #             self.openingX += 80
        #             self.openingIndex += 1
        #         if self.openingIndex == 10:
        #             self.opening = False

        boardx = 220
        boardy = 380
        for boardCard in self.boardCardList: #THIS IS FOR THE POSITION OF CARD WHILE DEPLOYING onto the board
            boardCard.defaultPos = boardx,boardy
            boardx += 80

        for a in self.allCardsList:  # updates all existing cards
            # if not h.resting and h.colliderect(self.bField1.xStart, self.bField1.yStart, self.bField1.xEnd, self.bField1.yEnd):
            #     print("Hurrah")
            #     h.defaultPos = (self.bField1.xStart, self.bField1.yStart)
            #     h.update(deltaTime, self.bField1.xStart, self.bField1.yStart)
            if not a.resting:
                if a.isHeld:
                    a.update(deltaTime, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                else:
                    a.update(deltaTime, a.defaultPos[0], a.defaultPos[1])

            if a.flipAnimating:  # card has been flipped, update through flipAnim function w/ waitTicks
                a.flipAnim(self.waitTick)

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
                    h2.defaultPos = (newX, 600)    # 600 = self.openingY
                    h2.update(deltaTime, newX, 600)
                    newX += 80
        #
        self.deckImgHolder1.update(deltaTime, 1170, 565)
        self.deckImgHolder2.update(deltaTime, 1175, 564)
        self.deckImgHolder3.update(deltaTime, 1180, 563)
        self.draw(screen)

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



    def startup(self, currentTime, persistent):
        '''
        Add variables passed in persistent to the proper attributes and
        set the start time of the State to the current time.
        @ Overwritten portion
        '''
        self.persist = persistent
        self.startTime = currentTime

        '''
        testing persistent objects
        '''
        print("[Engine] ########################### ")
        print("[Engine] {0}({1}) vs {2}({3})".format(self.persist['playerA'].user.username, self.persist['playerA'].hero.name, self.persist['playerB'].user.username, self.persist['playerB'].hero.name))
        print("[Engine] THE BATTLE BEGINS")
        print("[Engine] gameStart: ", Globals.gameStart)
        '''
        setting of board objects and setting of first perspective
        '''
        self.board = Board()
        # self.boardField = BoardField(225,390,1010,470)
        self.boardFieldOpp2 = None  # bottom row, opponent
        self.boardFieldOpp = None  # top row, opponent
        self.boardField = BoardField(225,390,1010,470)  # top row, player
        self.boardField2 = BoardField(225,390,1010,470)  # bottom row, player
        self.deck = self.persist['playerB'].deck
        self.opponent_deck = self.persist['playerA'].deck
        self.hand = self.get_first_cards(self.deck)
        self.opponent_hand = self.get_first_cards(self.opponent_deck)

        # self.opening = True

        # setting of initial dictionary key value pairs, made available to our PhaseManager

        self.dictionary.update({"opening_index": 0,
                                "hand": self.hand,
                                "opp_hand": self.opponent_hand,
                                "all_cards_list": self.allCardsList,
                                "openingX": 220,
                                "openingY": 600,
                                "opening": True,
                                "draw_wait_tick": 250,
                                "draw_sound": self.drawCardSound})

    def cleanup(self):
        self.board = None
        self.boardFieldOpp2 = None  # bottom row, opponent
        self.boardFieldOpp = None  # top row, opponent
        self.boardField = None  # top row, player
        self.boardField2 = None  # bottom row, player
        self.deck = None
        self.opponent_deck = None
        self.hand = None
        self.opponent_hand = None
        self.opening = False
        self.done = False
        Globals.gameStart = False
        return self.persist

#  _____                        _____ _
# |_   _|                      /  __ \ |
#   | | _ __  _ __   ___ _ __  | /  \/ | __ _ ___ ___  ___  ___
#   | || '_ \| '_ \ / _ \ '__| | |   | |/ _` / __/ __|/ _ \/ __|
#  _| || | | | | | |  __/ |    | \__/\ | (_| \__ \__ \  __/\__ \
#  \___/_| |_|_| |_|\___|_|     \____/_|\__,_|___/___/\___||___/
#

# Handles phase logic
class PhaseManager():
    def __init__(self, dictionary={}, wait=pygame.time.get_ticks()):
        self.phase = None
        self.waitTick = wait
        self.d = dictionary    # things which this class has been passed on in a dictionary. Might go unused? Since update will be provided a dictionary
        self.d['flip_hand_event'] = False
        self.has_event = False

    def set_phase(self, phase):
        self.phase = phase
        pass
    # the update thing here makes it so that each phase would update. Depends on the phase
    def update(self, currentTime, deltaTime):
        if self.phase == Phase.PLAY:
            pass

        elif self.phase == Phase.OPENING:
            currentTick = currentTime
            if currentTick - self.waitTick >= self.d['draw_wait_tick']:
                if self.d['opening_index'] < 10:
                    self.waitTick = currentTick
                    # self.drawCardSound.stop()
                    self.d['draw_sound'].play()
                    self.d['hand'][self.d['opening_index']].resting = False
                    self.d['hand'][self.d['opening_index']].set_destination(1180, 563)
                    self.d['hand'][self.d['opening_index']].defaultPos = (self.d['openingX'], self.d['openingY'])
                    self.d['hand'][self.d['opening_index']].update(deltaTime, self.d['openingX'], self.d['openingY'])
                    self.d['all_cards_list'].append(self.d['hand'][self.d['opening_index']])
                    self.d['openingX'] += 80
                    self.d['opening_index'] += 1
                if self.d['opening_index'] == 10:
                    self.d['opening'] = False
                    self.d['flip_hand_event'] = True
                    self.has_event = True
                    self.flip_hand(self.d['hand'])
                    self.set_phase(Phase.PLAY) # temporary, it should be more like button appears to click to reveal cards

                    # flip cards

    def set_dictionary(self, dictionary):
        self.d = dictionary
    def addto_dictionary(self, key, val):
        self.d[key] = val
    def delfrom_dictionary(self, key):
        del self.d[key]
    def empty_dictionary(self):
        self.d = {}

    def get_event(self, event):

        if self.phase == Phase.PLAY:
            if event.type == pygame.MOUSEBUTTONUP:
                click = pygame.mouse.get_pressed()
                if click[0] == 0:
                    print("unheld")
                    self.holdingCard = False
                    self.board.hasPreviewCard = False
                    if not len(self.clickedCard) == 0:
                        self.clickedCard[0].isHeld = False
                        # self.clickedCard[0].flip()
                        if self.clickedCard[0].colliderect(self.boardField.xStart,self.boardField.yStart,self.boardField.xEnd,self.boardField.yEnd) and not self.clickedCard[0].onBoard:
                            self.boardCardList.append(self.clickedCard[0])
                            self.clickedCard[0].onBoard = True

                        if self.clickedCard[0].destination == None:
                            self.clickedCard.pop()

    def flip_hand(self, hand):
        for h in hand:
            h.flip()


# gives the cues to our Phase Manager
class Phase(Enum):
    # auto() is an enum function that makes it decide what type to use for that enum
    OPENING = auto()        # 10 cards drawn, coin flips
    ROUND_TWO = auto()      # Two cards drawn
    FINAL_ROUND = auto()    # One card drawn
    SWAP = auto()           # Screen fades out, board flips
    PLAY = auto()           # Player controls are enabled, can click around etc.



