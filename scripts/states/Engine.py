import pygame, math, time, random
from enum import Enum, auto
from .classes.BoardField import BoardField
from .classes.Card import Card
from .classes.Card import Type
from .classes.Board import Board
from .classes.Movable import Movable
from .classes.FontObj import FontObj
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
        self.first_player = None  # does not change after coin toss
        self.opponent = None
        self.winning_player = None
        self.cards_played = 0  # counter to determine how many cards you've played that turn
        self.phase = Phase.COIN_TOSS

        '''
        CUTSCENE BOOLEANS
        '''
        # initial coin toss
        self.has_faded_tossed_coin = False
        self.has_tossed_coin = False
        self.first_toss_animating = True
        self.notif_pause = True
        self.may_see_first = False
        self.getting_in_place = True
        self.hero_cutscene = True
        self.hero_cutscene_flyin = True
        self.hero_cutscene_flyout = True
        self.may_see_hero_cutscene = False
        # logic booleans
        self.first_player_set = False  # becomes true after coin toss, and hands/decks set
        self.holdingCard = False
        self.done_turn = False
        self.done_drawing = False
        self.may_flip_board = False
        self.may_count_turn = False
        self.may_drag = False
        self.passed = False  # a player has passed their turn
        self.may_end_round = False  # prompting 2nd player to end his turn after opponent has passed.
        self.big_portraits_visible = False
        self.player1heads = False
        self.declared_winner = False
        # self.opening = True

        # objects
        self.board = None  # this rarely changes, maybe the board graphic but idk
        self.deck = None
        self.hand = None
        self.opponent_deck = None
        self.opponent_hand = None

        self.boardFieldOpp2 = None  # opponent back row
        self.boardFieldOpp = None   # opponent front row
        self.boardFieldListOpp = [self.boardFieldOpp, self.boardFieldOpp2]
        self.boardField = None      # player front row
        self.boardField2 = None     # player back row
        # self.boardFieldList = [self.boardField, self.boardField2, self.boardFieldOpp, self.boardFieldOpp2]
        self.boardFieldList = [self.boardField, self.boardField2]
        # self.boardCardList = list()

        self.bplayer_img = None
        self.bplayer2_img = None
        self.hero_turn_obj = None
        self.font_turn_obj = None


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
        self.drawCardWait = 100
        self.openingIndex = 0
        self.openingX = 220                # hand coordinate is from 220 to 1020 (PLAYER)
        self.openingY = 610
        self.openingXOpp = 220  # hand coordinate is from 220 to 1020 (OPP)
        self.openingYOpp = -30

        self.deckImgHolder1 = Card()     # add formula to determine how many deckImgHolders; ex. (no. of cards in deck) / 3 = (no. of deckImgHolders)
        self.deckImgHolder2 = Card()     # or have preset of (x number of deckHolders) then hide the top deckHolder for every 5 cards removed from deck
        self.deckImgHolder3 = Card()

        self.deckImgHolderOpp1 = Card()
        self.deckImgHolderOpp2 = Card()
        self.deckImgHolderOpp3 = Card()

        '''
        UI things (initial state) we're gonna have to put some of these things in classes so that the game would be more scalable
        '''
        self.showEndTurnButton = False
        self.showPassTurnButton = False
        self.showHandButton = False
        self.endTurnImg = pygame.image.load("assets\\buttons\\end_turn.bmp").convert_alpha()
        self.passTurnImg = pygame.image.load("assets\\buttons\\pass_turn.bmp").convert_alpha()
        self.showHandImg = pygame.image.load("assets\\buttons\\show_hand.png").convert_alpha()
        self.mouseOnEndTurnButton = False
        self.mouseOnPassTurnButton = False
        self.mouseOnShowHandButton = False
        self.endTurnImgX = 50
        self.endTurnImgY = 335
        self.showHandImgX = Globals.RESOLUTION_X * 0.44
        self.showHandImgY = Globals.RESOLUTION_Y * 0.90
        self.endTurnImgDimensionX = 110
        self.endTurnImgDimensionY = 53

        self.graveYardX = Globals.RESOLUTION_X * 0.828
        self.graveYardY = Globals.RESOLUTION_Y * 0.785
        self.graveYardList = list()

        self.graveYardOppX = Globals.RESOLUTION_X * 0.828
        self.graveYardOppY = Globals.RESOLUTION_Y * 0.065
        self.graveYardListOpp = list()

        # aim for the center of the slot # not center actually idk what's pygame doing with this part.
        self.top_slot = (Globals.RESOLUTION_X *0.155, Globals.RESOLUTION_Y *0.36)
        self.bottom_slot = (Globals.RESOLUTION_X *0.155, Globals.RESOLUTION_Y * 0.95)
        self.coin_slot = (Globals.RESOLUTION_X *0.082, Globals.RESOLUTION_Y *0.5)

        # fade things
        self.screen = pygame.display.set_mode((1280, 720))
        self.fadeScreen = pygame.Surface((1280, 720))
        self.fadeScreen.fill((0,0,0)) #black
        self.faded = False
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  _____                       ______                _   _
# |  __ \                      |  ___|              | | (_)
# | |  \/ __ _ _ __ ___   ___  | |_ _   _ _ __   ___| |_ _  ___  _ __  ___
# | | __ / _` | '_ ` _ \ / _ \ |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | |_\ \ (_| | | | | | |  __/ | | | |_| | | | | (__| |_| | (_) | | | \__ \
#  \____/\__,_|_| |_| |_|\___| \_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def fadeIn(self):
        alpha = 0
        while alpha <= 255:
            self.fadeScreen.set_alpha(alpha)
            self.draw(self.screen)
            self.screen.blit(self.fadeScreen, (0, 0))
            pygame.display.update()
            pygame.time.delay(1)
            alpha += 5
        self.faded = True

    def fadeOut(self):
        alpha = 250
        while alpha >= 0:
            self.fadeScreen.set_alpha(alpha)
            self.draw(self.screen)
            self.screen.blit(self.fadeScreen, (0, 0))
            pygame.display.update()
            pygame.time.delay(1)
            alpha -= 5
        self.faded = False

    def flip_hand(self, hand):
        for h in hand:
            h.flip()
    def flip_hand_down(self, hand):
        for h in hand:
            if h.front:
                h.flip()

    def get_first_cards(self, deck, username):
        print("Giving first cards of: ", username)
        random.shuffle(deck)
        first_ten = []
        for i in range(0, 10):  # self minus due to simultaneous pop will offset this
            first_ten.append(deck[i-i])
            deck.pop(i-i)
        return first_ten

    def draw_cards(self, amt, from_deck, to_hand):
        # print("Drawing {0} cards to {1}'s hand from {2}'s deck".format(amt, ))
        for i in range (0, amt):
            to_hand.append(from_deck[0])
            from_deck.pop(0)

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

    def swap_portrait(self):
        if self.player1heads:
            self.bplayer_img.set_absolute(self.top_slot)
            self.bplayer2_img.set_absolute(self.bottom_slot)
            self.player1heads = False
        else:
            self.bplayer2_img.set_absolute(self.top_slot)
            self.bplayer_img.set_absolute(self.bottom_slot)
            self.player1heads = True



    def empty_field_to_grave(self, boardField, graveYardList):
        # boardField.cardList.pop(boardField.cardList.index(card))
        graveYardList.extend(boardField.cardList)

        if boardField.owner == self.player.user.username:
            # print("My boardfield")
            for c in boardField.cardList:
                c.defaultPos = self.graveYardX, self.graveYardY
                c.flip()
                c.onBoard = False
                c.disabled = True
                c.resting = False
                c.set_destination(*c.defaultPos)
        else:
            for c in boardField.cardList:
                c.defaultPos = self.graveYardOppX, self.graveYardOppY
                c.flip()
                c.onBoard = False
                c.disabled = True
                c.resting = False
                c.set_destination(*c.defaultPos)

        boardField.cardList = []
        boardField.rearrange()


    def send_to_grave_fromboard(self, card, boardField, graveYardList):  # lite version? no cardstack difference though
        # print("Index to be tossed to grave: ",boardField.cardList.index(card))
        boardField.cardList.pop(boardField.cardList.index(card))
        graveYardList.append(card)
        if boardField.owner == self.player.user.username:
            # print("My boardfield")
            card.defaultPos = self.graveYardX, self.graveYardY
        else:
            card.defaultPos = self.graveYardOppX, self.graveYardOppY

        card.flip()
        card.onBoard = False
        card.disabled = True
        card.resting = False
        card.set_destination(*card.defaultPos)

        # card.flip()
        # card.onBoard = False
        # card.disabled = True
        # card.resting = False
        # card.set_destination(*card.defaultPos)  # NOTE: added a star to unpack the tuple, so taht set_destination gets the x and y it wanted

    def sendToGraveyard(self, card):
        # NOTE: changed placement of /5. Due to it raising an error that a list cannot be divided by an int
        # from: 5*(int(len((self.graveYardList)/5)))
        # to:   5*(int(len((self.graveYardList))/5))
        '''
        self.graveYardX += 5*(int(len((self.graveYardList))/5))
        self.graveYardY -= 1*(int(len((self.graveYardList))/5))

        self.graveYardOppX += 5*(int(len((self.graveYardListOpp))/5))
        self.graveYardOppY -= 1*(int(len((self.graveYardList))/5))
        '''
        if len(self.graveYardList) == 5:
            self.graveYardX += 5
            self.graveYardY -= 1

        if len(self.graveYardList) == 10:
            self.graveYardX += 5
            self.graveYardY -= 1

        if len(self.graveYardList) == 15:
            self.graveYardX += 5
            self.graveYardY -= 1

        if len(self.graveYardListOpp) == 5:
            self.graveYardOppX += 5
            self.graveYardOppY -= 1

        if len(self.graveYardListOpp) == 10:
            self.graveYardOppX += 5
            self.graveYardOppY -= 1

        if len(self.graveYardListOpp) == 15:
            self.graveYardOppX += 5
            self.graveYardOppY -= 1

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
                card.defaultPos = self.graveYardOppX, self.graveYardOppY

        for boardCard in self.boardFieldOpp2.cardList:
            if card == boardCard:
                self.boardFieldOpp2.cardList.pop(self.boardFieldOpp2.cardList.index(boardCard))
                self.graveYardListOpp.append(card)
                card.defaultPos = self.graveYardOppX, self.graveYardOppY


        card.flip()
        card.onBoard = False
        card.disabled = True
        card.resting = False
        card.set_destination(*card.defaultPos)  # NOTE: added a star to unpack the tuple, so taht set_destination gets the x and y it wanted



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

    def play_card(self, card, boardfieldlist):  # initial concept, listener type thing.
        print("PLAYED BY: ", self.player.user.username)
        self.board.coin.show_end()
        self.showPassTurnButton = False
        self.showEndTurnButton = True
        self.cards_played += 1
        # print(self.cards_played)
        self.recalculate_score(boardfieldlist)

        if self.cards_played == 2 and not self.passed:
            self.may_drag = False

    def end_turn(self):
        # self.done_turn = True
        self.showPassTurnButton = False
        self.showEndTurnButton = False
        self.cards_played = 0

    def recalculate_score(self, bFList):
        print("[Engine] recalculate score Previous cash: ", self.player.cash)
        self.player.cash = 0
        for bF in bFList:
            for c in bF.cardList:
                self.player.cash += c.current_val
        print("[Engine] After recalculation cash: ", self.player.cash)

    def apply_effects(self, boardField): #f this sh
        vehicleCounter = boardField.count_cardType(Type.VEHICLE)
        blackCounter = boardField.count_cardType(Type.BLACK)
        personCounter = boardField.count_cardType(Type.PERSON)
        effectActivated = False

        for boardCard in boardField.cardList:
            if not boardCard.effectActivated:
                if boardCard.name is "Parking Lot":
                    boardCard.current_val += (2*vehicleCounter)
                    boardCard.effectActivated = True
                    effectActivated = True
                    continue

                if boardCard.name is "Loan Slip":   #cmon bruddah just draw the freakin cards
                    self.draw_cards(2, self.deck, self.hand)
                    self.player.cash -= 15
                    boardCard.effectActivated = True
                    effectActivated = True
                    continue

                if boardCard.name is "Lemonade Stand":
                    boardCard.current_val += (3*personCounter)
                    print (boardCard.current_val)
                    boardCard.effectActivated = True
                    effectActivated = True
                    continue

                if boardCard.name is "Credit Card":
                    for card in boardField.cardList:
                        if Type.PERSON in card.type:
                            card.current_val += 2
                        elif Type.OBJECT in card.type:
                            card.current_val -= 1
                    boardCard.effectActivated = True
                    effectActivated = True
                    continue

                if boardCard.name is "Butler":
                    if boardField.cardList.index(boardCard) != 0:
                        boardField.cardList[boardField.cardList.index(boardCard) - 1].current_val += 5
                    boardCard.effectActivated = True
                    effectActivated = True
                    continue

                if boardCard.name is "Arsonist":    #WORKING POGCHAMP
                    arsonIndex = boardField.cardList.index(boardCard)
                    if arsonIndex < len(self.boardFieldOpp.cardList) and Type.STRUCTURE in self.boardFieldOpp.cardList[arsonIndex].type:
                        self.sendToGraveyard(self.boardFieldOpp.cardList[arsonIndex])
                    if arsonIndex < len(self.boardFieldOpp2.cardList) and Type.STRUCTURE in self.boardFieldOpp2.cardList[arsonIndex].type:
                        self.sendToGraveyard(self.boardFieldOpp2.cardList[arsonIndex])
                    boardCard.effectActivated = True
                    effectActivated = True
                    continue

                if boardCard.name is "Saboteur":
                    boardRandom = random.randrange(2)
                    cardRandom = random.randrange(len(self.boardFieldListOpp[boardRandom]))
                    self.sendToGraveyard(self.boardFieldListOpp[boardRandom].cardList[cardRandom])

                    boardCard.effectActivated = True
                    effectActivated = True
                    continue

                if boardCard.name is "Maid":
                    for a in self.boardField.cardList:
                        if a is "Mansion":
                            a.current_val += 3
                    for a in self.boardField2.cardList:
                        if a is "Mansion":
                            a.current_val += 3

                    boardCard.effectActivated = True
                    effectActivated = True
                    continue

                if boardCard.name is "Police Officer":
                    for a in self.boardFieldOpp.cardList:
                        if Type.BLACK and Type.PERSON in a.type:
                            self.sendToGraveyard(a)
                    for a in self.boardFieldOpp2.cardList:
                        if Type.BLACK and Type.PERSON in a.type:
                            self.sendToGraveyard(a)

                    boardCard.effectActivated = True
                    effectActivated = True
                    continue

                if boardCard.name is "Impound Lot":
                    for a in self.boardFieldOpp.cardList:
                        if Type.VEHICLE in a.type:
                            a.current_val -= 2
                    for a in self.boardFieldOpp2.cardList:
                        if Type.VEHICLE in a.type:
                            a.current_val -= 2

                    boardCard.effectActivated = True
                    effectActivated = True
                    continue

                if boardCard.name is "Junkyard":
                    count = 0
                    for a in self.graveYardList:
                        if Type.VEHICLE in a.type:
                            count += 1
                    for a in self.graveYardListOpp:
                        if Type.VEHICLE in a.type:
                            count += 1
                    boardCard.current_val += (2*count)

                    boardCard.effectActivated = True
                    effectActivated = True
                    continue

                if boardCard.name is "Resurrect":
                    personInGraveList = list()
                    for a in self.graveYardList:
                        if Type.PERSON in a.type:
                            personInGraveList.append(a)
                    if len(personInGraveList) > 0:
                        r = random.randrange(len(personInGraveList))
                        c = personInGraveList[r]
                        self.boardField.take_card(c)
                        self.play_card(c, self.boardFieldList)
                        self.graveYardList.pop(self.graveYardList.index(c))
                        c.flip()
                        c.disabled = False
                        c.resting = False
                        c.set_destination(*c.defaultPos)

                    boardCard.effectActivated = True
                    effectActivated = True
                    continue

                if boardCard.name is "Rebuild":
                    graveList = list()
                    for a in self.graveYardList:
                        if Type.VEHICLE or Type.STRUCTURE in a.type:
                            graveList.append(a)
                    if len(graveList) > 0:
                        r = random.randrange(len(graveList))
                        c = graveList[r]
                        self.boardField.take_card(c)
                        self.play_card(c, self.boardFieldList)
                        self.graveYardList.pop(self.graveYardList.index(c))
                        c.flip()
                        c.disabled = False
                        c.resting = False
                        c.set_destination(*c.defaultPos)

                    boardCard.effectActivated = True
                    effectActivated = True
                    continue

        if effectActivated:
            self.recalculate_score(self.boardFieldList)
            for a in self.boardField.cardList:
                a.draw(self.screen)
            for a in self.boardField2.cardList:
                a.draw(self.screen)

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
        if self.phase == Phase.PLAY and not self.hero_cutscene:
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

                        if self.player.cash < self.player2.cash:
                            self.may_end_round = True

                    print("unheld")
                    self.holdingCard = False
                    if self.cardMousedOver(pygame.mouse.get_pos()):
                        self.board.hasPreviewCard = False
                    if not len(self.clickedCard) == 0:
                        if len(self.clickedCard) > 1:  # cheap man gaming
                            for c in self.clickedCard:
                                c.isHeld = False
                        else:
                            self.clickedCard[0].isHeld = False
                        # self.clickedCard[0].flip()

                        #let go into a boardField
                        # if self.clickedCard[0].colliderect(self.boardField.xStart,self.boardField.yStart,self.boardField.xEnd,self.boardField.yEnd) and not self.clickedCard[0].onBoard:
                        #     self.boardCardList.append(self.clickedCard[0])
                        #     self.clickedCard[0].onBoard = True

                        if self.player == self.first_player:
                            for bF in self.boardFieldList:
                                if self.clickedCard[0].collide_rect(*bF.get_dimensions()) and not self.clickedCard[0].onBoard:
                                    bF.take_card(self.clickedCard[0])
                                    self.clickedCard[0].onBoard = True
                                    self.play_card(self.clickedCard[0], self.boardFieldList)
                        elif self.player2 == self.first_player and not self.clickedCard[0].onBoard:
                            for bF in self.boardFieldListOpp:
                                if self.clickedCard[0].collide_rect(*bF.get_dimensions()):
                                    bF.take_card(self.clickedCard[0])
                                    self.clickedCard[0].onBoard = True
                                    self.play_card(self.clickedCard[0], self.boardFieldListOpp)


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


            if event.type == pygame.MOUSEBUTTONDOWN and not self.opening and not self.hero_cutscene:
                click = pygame.mouse.get_pressed()
                if click[0] == 1:

                    for s in self.allCardsList:
                        if s.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                            self.clickedCard.append(s)
                            s.onTop = True
                            self.allCardsList.pop(self.allCardsList.index(s))
                            self.allCardsList.append(s)

                    if len(self.clickedCard) > 0:
                        if self.clickedCard[0].disabled == False and self.clickedCard[0].onBoard == False and self.clickedCard[0].front and self.may_drag:
                            print("handcard clicked")
                            self.clickedCard[0].isHeld = True
                            self.holdingCard = True
                            self.clickedCard[0].resting = False
                            self.clickedCard[0].set_destination(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                            self.drawCardSound.play()

            if self.done_turn:
                self.end_turn()
                if self.may_end_round:
                    # giving a point to a player/ draw
                    self.passed = False
                    self.may_end_round = False
                    self.phase = Phase.END_ROUND
                    self.done_turn = False
                elif not self.passed:
                    self.phase = Phase.SWAP
                else:
                    self.may_end_round = True
                    self.phase = Phase.SWAP
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
                        print("[Engine]Showing cards")
                        self.showHandButton = False
                        if self.faded:
                            self.board.coin.show_pass()
                            self.fadeOut()
                        self.flip_hand(self.hand)
                        self.phase = Phase.PLAY
                        if not self.passed:
                            self.showPassTurnButton = True
                            self.board.coin.show_pass()
                        else:
                            self.showEndTurnButton = True
                            self.board.coin.show_end()

                        #cutscene prep:
                        self.waitTick = pygame.time.get_ticks()  # this is so that fly in doesn't end instantly
                        self.hero_cutscene = True
                        self.hero_cutscene_flyin = True
                        self.hero_cutscene_flyout = True
                        self.may_see_hero_cutscene = True
                        # swapping it to the next player's assets
                        self.hero_turn_obj.surface = self.player.hero.img
                        self.font_turn_obj = FontObj.factory(self.player.user.username + "'s turn", -100, 0, "big_noodle_titling_oblique.ttf", 80, (255, 255, 255))
                        self.font_turn_obj.distancespeed = 3.5
                        self.hero_turn_obj.set_absolute((Globals.RESOLUTION_X * 0.5 + 1200, Globals.RESOLUTION_Y * 0.5))
                        self.font_turn_obj.set_absolute((Globals.RESOLUTION_X * 0.5 + 1200, Globals.RESOLUTION_Y * 0.5 + 200))

            # clicking this will set phase to Play

    # orders individual elements to update themselves (your coordinates, sprite change, state, etc)
    def update(self, screen, keys, currentTime, deltaTime):
        self.deckImgHolder1.update(deltaTime, 1170, 565)
        self.deckImgHolder2.update(deltaTime, 1175, 564)
        self.deckImgHolder3.update(deltaTime, 1180, 563)

        self.deckImgHolderOpp1.update(deltaTime, 1170, 50)
        self.deckImgHolderOpp2.update(deltaTime, 1175, 49)
        self.deckImgHolderOpp3.update(deltaTime, 1180, 48)
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


        if self.board.coin.animating:
            self.board.coin.flipAnim()

        ''' UPDATE
         ____  _  _   __   ____  ____  ____
        (  _ \/ )( \ / _\ / ___)(  __)/ ___)
         ) __/) __ (/    \\___ \ ) _) \___ \
        (__)  \_)(_/\_/\_/(____/(____)(____/
        
        '''

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
            if len(self.boardField.cardList) != 0:
                self.apply_effects(self.boardField)
            if len(self.boardField2.cardList) != 0:
                self.apply_effects(self.boardField2)
            if self.hero_cutscene:  # TODO Cutscene
                if self.hero_cutscene_flyin:
                    self.hero_turn_obj.update(deltaTime)
                    self.font_turn_obj.update(deltaTime)
                    # these two set destination codes below are actually triggered in the get_evt block
                    self.hero_turn_obj.set_destination(*(Globals.RESOLUTION_X*0.5, Globals.RESOLUTION_Y*0.5))
                    self.font_turn_obj.set_destination(*(Globals.RESOLUTION_X*0.5, Globals.RESOLUTION_Y*0.5 +200))
                    if currentTime - self.waitTick >= 2500:
                        self.hero_cutscene_flyin = False
                        self.waitTick = currentTime
                        self.hero_turn_obj.set_destination(*(-400, Globals.RESOLUTION_Y*0.5))
                        self.font_turn_obj.set_destination(*(-400, Globals.RESOLUTION_Y*0.5 +200))
                elif self.hero_cutscene_flyout:
                    self.hero_turn_obj.update(deltaTime)
                    self.font_turn_obj.update(deltaTime)
                    if currentTime - self.waitTick >= 800:  # timeout before players can start clicking around again
                        self.waitTick = currentTime
                        self.hero_cutscene_flyout = False
                        # self.control_enabled = True     actually non-factor I think
                        self.may_see_hero_cutscene = False
                        self.hero_cutscene = False



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

            else:  # this part is not triggering because the phase has been changed @ the get_evt block
                self.phase = Phase.SWAP
                self.done_turn = False
                self.showEndTurnButton = False  #this is not working
        elif self.phase == Phase.PREP:
            # more on animations updates
            if not len(self.hand) == 0:
                if self.hand[0].front:
                    self.flip_hand(self.hand)



            self.showHandButton = True


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
            self.flip_hand(self.hand)

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
            self.fadeIn()
            self.swap_portrait()

        elif self.phase == Phase.END_ROUND:
            # here we compare scores, decide which hero to damage, and give score.
            self.empty_field_to_grave(self.boardField, self.graveYardList)
            self.empty_field_to_grave(self.boardField2, self.graveYardList)
            self.empty_field_to_grave(self.boardFieldOpp, self.graveYardListOpp)
            self.empty_field_to_grave(self.boardFieldOpp2, self.graveYardListOpp)
            # for boardCard in self.boardField.cardList:
            #     # self.sendToGraveyard(boardCard)
            #     print("Trashing some dogs1")
            #     self.empty_field_to_grave(self.boardField, self.graveYardList)
            # for boardCard in self.boardField2.cardList:
            #     # self.sendToGraveyard(boardCard)
            #     print("Trashing some dogs2")
            #     self.send_to_grave_fromboard(boardCard, self.boardField2, self.graveYardList)
            #     self.empty_field_to_grave(self.boardField2, self.graveYardList)
            # for boardCard in self.boardFieldOpp.cardList:
            #     print("Trashing some dogs3")
            #     # self.sendToGraveyard(boardCard)
            #     self.send_to_grave_fromboard(boardCard, self.boardFieldOpp, self.graveYardListOpp)
            # for boardCard in self.boardFieldOpp2.cardList:
            #     print("Trashing some dogs4")
            #     # self.sendToGraveyard(boardCard)
            #     self.send_to_grave_fromboard(boardCard, self.boardFieldOpp2, self.graveYardListOpp)

            if self.player.cash > self.player2.cash:
                print("Player {0} has more cash".format(self.player.user.username))
                self.player2.hitpoints -= 1
                if self.player.hitpoints == 1 and self.player2.hitpoints == 1:
                    self.phase = Phase.FINAL_ROUND
                else:
                    self.phase = Phase.MATCH_COMPLETE if self.player2.hitpoints == 0 else Phase.ROUND_TWO
                    if self.phase == Phase.MATCH_COMPLETE:
                        self.hero_turn_obj.surface = self.player.hero.img
                        self.font_turn_obj = FontObj.factory(self.player.user.username + " WINS", -100, 0, "big_noodle_titling_oblique.ttf", 80, (255, 255, 255))
                        self.font_turn_obj.distancespeed = 3.5
                        self.hero_turn_obj.set_absolute((Globals.RESOLUTION_X * 0.5 + 1200, Globals.RESOLUTION_Y * 0.5))
                        self.font_turn_obj.set_absolute((Globals.RESOLUTION_X * 0.5 + 1200, Globals.RESOLUTION_Y * 0.5 + 200))

                        self.hero_turn_obj.set_destination(*(-400, Globals.RESOLUTION_Y * 0.5))
                        self.font_turn_obj.set_destination(*(-400, Globals.RESOLUTION_Y * 0.5 + 200))
            elif self.player.cash == self.player2.cash:
                print("Both players have equal amount of cash!")
                self.phase = Phase.ROUND_DRAW
            else:
                print("Opponent {0} has more cash".format(self.player2.user.username))
                self.player.hitpoints -= 1
                if self.player.hitpoints == 1 and self.player2.hitpoints == 1:
                    self.phase = Phase.FINAL_ROUND
                else:
                    self.phase = Phase.MATCH_COMPLETE if self.player.hitpoints == 0 else Phase.ROUND_TWO
                    if self.phase == Phase.MATCH_COMPLETE:
                        self.hero_turn_obj.surface = self.player2.hero.img
                        self.font_turn_obj = FontObj.factory(self.player2.user.username + " WINS", -100, 0, "big_noodle_titling_oblique.ttf", 80, (255, 255, 255))
                        self.font_turn_obj.distancespeed = 3.5
                        self.hero_turn_obj.set_absolute((Globals.RESOLUTION_X * 0.5 + 1200, Globals.RESOLUTION_Y * 0.5))
                        self.font_turn_obj.set_absolute((Globals.RESOLUTION_X * 0.5 + 1200, Globals.RESOLUTION_Y * 0.5 + 200))
                        self.hero_turn_obj.set_destination(*(Globals.RESOLUTION_X * 0.5 , Globals.RESOLUTION_Y * 0.5))
                        self.font_turn_obj.set_destination(*(Globals.RESOLUTION_X * 0.5 , Globals.RESOLUTION_Y * 0.5 + 200))

            # play appropriate animations
            # check if it was the winning blow
                #2 play animations if a player is found victorious

            # else enter next round, draw appropriate num of cards
        elif self.phase == Phase.ROUND_TWO:
            print("[Engine] Entering Round Two!")
            num_of_cards = 2
            if not self.done_drawing:
                # please burn cards in future patch (w/ animations muhaha)
                self.draw_cards(num_of_cards, self.deck, self.hand)
                self.draw_cards(num_of_cards, self.opponent_deck, self.opponent_hand)
                print("Player Hand Size: ", len(self.hand))
                if len(self.hand) > 10:
                    print("Player {0} hand overload!".format(self.player.user.username))
                print("Player opponent hand Size: ", len(self.opponent_hand))
                if len(self.opponent_hand) > 10:
                    print("Player {0} hand overload!".format(self.player2.user.username))
                self.flip_hand_down(self.hand)
                self.flip_hand_down(self.opponent_hand)
                self.done_drawing = True
            currentTick = currentTime
            if currentTick - self.waitTick >= self.drawCardWait:

                if self.openingIndex < num_of_cards:
                    self.waitTick = currentTick
                    self.drawCardSound.play()
                    newX = 620 - (40 * (len(self.hand)-(num_of_cards-(self.openingIndex+1))))
                    for h2 in self.hand:
                        h2.resting = False
                        h2.set_destination(h.posX, h.posY)
                        h2.defaultPos = (newX, self.openingY)  # 600 = self.openingY
                        h2.update(deltaTime, newX, self.openingY)
                        newX += 80
                    newXOpp = 620 - (40 * (len(self.opponent_hand)-(num_of_cards-(self.openingIndex+1))))
                    for h2 in self.opponent_hand:
                        h2.resting = False
                        h2.set_destination(h.posX, h.posY)
                        h2.defaultPos = (newXOpp, self.openingYOpp)  # 600 = self.openingY
                        h2.update(deltaTime, newXOpp, self.openingYOpp)
                        newXOpp += 80

                    handex = (len(self.hand) - num_of_cards) + self.openingIndex
                    handexopp = (len(self.opponent_hand) - num_of_cards) + self.openingIndex
                    self.hand[handex].resting = False
                    self.hand[handex].set_destination(1180, 563)

                    self.opponent_hand[handexopp].resting = False
                    self.opponent_hand[handexopp].set_destination(1180, 100)
                    self.opponent_hand[handexopp].posY = 100

                    self.allCardsList.append(self.hand[handex])
                    self.allCardsList.append(self.opponent_hand[handexopp])

                    self.openingIndex += 1
                else:
                    self.opening = False
                    self.done_drawing = False
                    self.openingIndex = 0
                    self.phase = Phase.PREP

        elif self.phase == Phase.MATCH_COMPLETE:
            if not self.declared_winner:
                self.declared_winner = True
                print("[Engine] Match Complete!")
                self.winning_player = self.player if self.player.hitpoints > 0 else self.player2
                print("{0} wins!".format(self.winning_player.user.username))
                self.may_see_hero_cutscene = True
            else:
                self.hero_turn_obj.update(deltaTime)
                self.font_turn_obj.update(deltaTime)

        elif self.phase == Phase.FINAL_ROUND:
            print("[Engine] Entering Final Round!")

            num_of_cards = 1
            if not self.done_drawing:
                # please burn cards in future patch (w/ animations muhaha)
                self.draw_cards(num_of_cards, self.deck, self.hand)
                self.draw_cards(num_of_cards, self.opponent_deck, self.opponent_hand)
                print("Player Hand Size: ", len(self.hand))
                if len(self.hand) > 10:
                    print("Player {0} hand overload!".format(self.player.user.username))
                print("Player opponent hand Size: ", len(self.opponent_hand))
                if len(self.opponent_hand) > 10:
                    print("Player {0} hand overload!".format(self.player2.user.username))
                self.flip_hand_down(self.hand)
                self.flip_hand_down(self.opponent_hand)
                self.done_drawing = True
            currentTick = currentTime
            if currentTick - self.waitTick >= self.drawCardWait:

                if self.openingIndex < num_of_cards:
                    self.waitTick = currentTick
                    self.drawCardSound.play()
                    newX = 620 - (40 * (len(self.hand) - (num_of_cards - (self.openingIndex + 1))))
                    for h2 in self.hand:
                        h2.resting = False
                        h2.set_destination(h.posX, h.posY)
                        h2.defaultPos = (newX, self.openingY)  # 600 = self.openingY
                        h2.update(deltaTime, newX, self.openingY)
                        newX += 80
                    newXOpp = 620 - (40 * (len(self.opponent_hand) - (num_of_cards - (self.openingIndex + 1))))
                    for h2 in self.opponent_hand:
                        h2.resting = False
                        h2.set_destination(h.posX, h.posY)
                        h2.defaultPos = (newXOpp, self.openingYOpp)  # 600 = self.openingY
                        h2.update(deltaTime, newXOpp, self.openingYOpp)
                        newXOpp += 80

                    handex = (len(self.hand) - num_of_cards) + self.openingIndex
                    handexopp = (len(self.opponent_hand) - num_of_cards) + self.openingIndex
                    self.hand[handex].resting = False
                    self.hand[handex].set_destination(1180, 563)

                    self.opponent_hand[handexopp].resting = False
                    self.opponent_hand[handexopp].set_destination(1180, 100)
                    self.opponent_hand[handexopp].posY = 100

                    self.allCardsList.append(self.hand[handex])
                    self.allCardsList.append(self.opponent_hand[handexopp])

                    self.openingIndex += 1
                else:
                    self.opening = False
                    self.done_drawing = False
                    self.openingIndex = 0
                    self.phase = Phase.PREP

        elif self.phase == Phase.ROUND_DRAW:
            print("[Engine] Round Draw!")
            num_of_cards = 3
            if not self.done_drawing:
                # please burn cards in future patch (w/ animations muhaha)
                self.draw_cards(num_of_cards, self.deck, self.hand)
                self.draw_cards(num_of_cards, self.opponent_deck, self.opponent_hand)
                print("Player Hand Size: ", len(self.hand))
                if len(self.hand) > 10:
                    print("Player {0} hand overload!".format(self.player.user.username))
                print("Player opponent hand Size: ", len(self.opponent_hand))
                if len(self.opponent_hand) > 10:
                    print("Player {0} hand overload!".format(self.player2.user.username))
                self.flip_hand_down(self.hand)
                self.flip_hand_down(self.opponent_hand)
                self.done_drawing = True
            currentTick = currentTime
            if currentTick - self.waitTick >= self.drawCardWait:

                if self.openingIndex < num_of_cards:
                    self.waitTick = currentTick
                    self.drawCardSound.play()
                    newX = 620 - (40 * (len(self.hand) - (num_of_cards - (self.openingIndex + 1))))
                    for h2 in self.hand:
                        h2.resting = False
                        h2.set_destination(h.posX, h.posY)
                        h2.defaultPos = (newX, self.openingY)  # 600 = self.openingY
                        h2.update(deltaTime, newX, self.openingY)
                        newX += 80
                    newXOpp = 620 - (40 * (len(self.opponent_hand) - (num_of_cards - (self.openingIndex + 1))))
                    for h2 in self.opponent_hand:
                        h2.resting = False
                        h2.set_destination(h.posX, h.posY)
                        h2.defaultPos = (newXOpp, self.openingYOpp)  # 600 = self.openingY
                        h2.update(deltaTime, newXOpp, self.openingYOpp)
                        newXOpp += 80

                    handex = (len(self.hand) - num_of_cards) + self.openingIndex
                    handexopp = (len(self.opponent_hand) - num_of_cards) + self.openingIndex
                    self.hand[handex].resting = False
                    self.hand[handex].set_destination(1180, 563)

                    self.opponent_hand[handexopp].resting = False
                    self.opponent_hand[handexopp].set_destination(1180, 100)
                    self.opponent_hand[handexopp].posY = 100

                    self.allCardsList.append(self.hand[handex])
                    self.allCardsList.append(self.opponent_hand[handexopp])

                    self.openingIndex += 1
                else:
                    self.opening = False
                    self.done_drawing = False
                    self.openingIndex = 0
                    self.phase = Phase.PREP

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
                    self.opponent = self.persist['playerB']

                    self.boardField.owner = self.persist['playerA'].user.username
                    self.boardField2.owner = self.persist['playerA'].user.username

                    self.boardFieldOpp.owner = self.persist['playerB'].user.username
                    self.boardFieldOpp2.owner = self.persist['playerB'].user.username
                    self.player1heads = True
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
                    self.player1heads = False

                self.first_player_set = True

                # TODO I have a feeling this would cause some issues if the players used the same image, but we'll see. #python names not variables
                self.hero_turn_obj = Movable(self.player.hero.img,1000,4,"distance",(Globals.RESOLUTION_X *0.5, Globals.RESOLUTION_Y * 0.5))
                self.font_turn_obj = FontObj.factory(self.player.user.username+"'s turn",-200,0,"big_noodle_titling_oblique.ttf",80,(255,255,255))
                self.font_turn_obj.distancespeed = 3.5
                self.hero_turn_obj.set_absolute((Globals.RESOLUTION_X * 0.5 + 1200, Globals.RESOLUTION_Y * 0.5))
                self.font_turn_obj.set_absolute((Globals.RESOLUTION_X * 0.5 + 1200, Globals.RESOLUTION_Y * 0.5 + 200))

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
                    self.openingIndex = 0
                    self.opening = False
                    self.drawCardWait = 1000
                    self.phase = Phase.PREP

        elif self.phase == Phase.COIN_TOSS:
            # note : timings below have been adjusted to allow faster debugging
            # additional animation updates
            self.board.coin.update(deltaTime)

            if not self.has_faded_tossed_coin:
                self.board.coin.is_visible = False
                self.board.coin.set_absolute((Globals.RESOLUTION_X * 0.5, -300))
                self.fadeOut()
                self.has_faded_tossed_coin = True

            elif not self.has_tossed_coin and currentTime - self.waitTick >= 1000:  # wait 2 seconds
                print("COIN TOSSED")
                self.board.coin.set_destination(Globals.RESOLUTION_X * 0.5, Globals.RESOLUTION_Y * 0.5)
                self.board.coin.is_visible = True
                self.toss_coin()
                self.waitTick = currentTime
                self.has_tossed_coin = True
            if self.has_tossed_coin:
                if self.first_toss_animating:
                    #animate coin?
                    if currentTime - self.waitTick <= 3000:  # how long we want the coin to be spinning before stopping it
                        self.waitTick = currentTime
                        self.board.coin.animating = False
                        self.first_toss_animating = False
                        if self.coin_side() == 0:
                            print("Coin pointing left")
                            self.board.coin.point_left()
                            self.board.coin.set_destination(Globals.RESOLUTION_X*0.5, Globals.RESOLUTION_Y*0.5)

                            # set bplayerimg to bottom left slot
                            self.bplayer_img.set_destination(*self.bottom_slot)
                            self.bplayer_img.scale_to((self.bplayer_img.original_surface.get_rect().size[0]*0.505, self.bplayer_img.original_surface.get_rect().size[1]*0.505))
                            # set bplayer2img to top left slot
                            self.bplayer2_img.set_destination(*self.top_slot)
                            self.bplayer2_img.scale_to((self.bplayer2_img.original_surface.get_rect().size[0]*0.505, self.bplayer2_img.original_surface.get_rect().size[1]*0.505))

                        else:
                            print("Coin pointing right")
                            self.board.coin.point_right()
                            # set bplayer2img to bottom left slot

                            self.bplayer_img.scale_to((self.bplayer_img.original_surface.get_rect().size[0] * 0.505, self.bplayer_img.original_surface.get_rect().size[1] * 0.505))
                            self.bplayer2_img.scale_to((self.bplayer2_img.original_surface.get_rect().size[0] * 0.505, self.bplayer2_img.original_surface.get_rect().size[1] * 0.505))
                            self.bplayer2_img.set_destination(*self.bottom_slot)
                            self.board.coin.set_destination(Globals.RESOLUTION_X * 0.5, Globals.RESOLUTION_Y * 0.5)
                            # set bplayerimg to top left slot
                            self.bplayer_img.set_destination(*self.top_slot)


                elif self.notif_pause:  # time paused to notify who goes first
                    if currentTime - self.waitTick >= 3000:
                        self.board.coin.show_pass()
                        self.notif_pause = False
                        self.may_see_first = True
                        #self.first_fontobj absolute position below first player card
                        self.waitTick = currentTime
                elif self.getting_in_place:
                    self.board.coin.set_destination(*self.coin_slot)
                    self.bplayer_img.update(deltaTime)  # these two will take their place
                    self.bplayer2_img.update(deltaTime)
                    self.bplayer_img.scaleanim(self.waitTick)
                    self.bplayer2_img.scaleanim(self.waitTick)
                    if currentTime - self.waitTick >= 2000:
                        self.getting_in_place = False
                else:
                    print("Everything in place, take first turn")
                    # refresh graphic (smoothscale resolution problems)
                    self.bplayer_img.surface = pygame.transform.smoothscale(self.bplayer_img.original_surface, (round(self.bplayer_img.original_surface.get_rect().size[0] *0.505), round(self.bplayer_img.original_surface.get_rect().size[1] * 0.505)))
                    self.bplayer2_img.surface = pygame.transform.smoothscale(self.bplayer2_img.original_surface, (round(self.bplayer2_img.original_surface.get_rect().size[0] * 0.505), round(self.bplayer2_img.original_surface.get_rect().size[1] * 0.505)))

                    # self.bplayer_img.set_absolute(self.top_slot)
                    # self.bplayer2_img.set_absolute(self.bottom_slot)
                    self.phase = Phase.OPENING
            # self.phase = Phase.OPENING
            # block down below
            # if self.opening:
            #     self.phase = Phase.OPENING
            # else:
            #     self.phase = Phase.SWAP




        # for a in self.allCardsList:
        #     if a.front and (a in self.hand or a in self.boardField.cardList or a in self.boardField2.cardList):
        #         # a.addTexts(self.player.hero.name)
        #     elif a.front:
        #         # a.addTexts(self.player2.hero.name)
        self.draw(screen)  # last function of update. execute draw

    # orders individual elements to draw themselves in the correct order (your blits)
    def draw(self, screen):
        screen.fill((255, 255, 255))

        self.board.draw(screen)
        # if not self.card.blitted:               # another way of instantiating, compared to elif h.resting and not h.blitted in update method
        #     self.card.posX, self.card.posY = self.boardField.xStart, self.boardField.yStart
        #     self.card.blitted = True
        # self.card.draw(screen)

        self.board.coin.draw(screen)
        if self.big_portraits_visible:
            self.bplayer_img.draw(screen)
            self.bplayer2_img.draw(screen)
        onTopCard = None
        for a in self.allCardsList:
            if not a.onTop:
                a.draw(screen)
                # if a.front:
                #     a.textBaseVal.draw(screen)
                #     a.textCurrVal.draw(screen)
                #     a.textName.draw(screen)
            else:
                onTopCard = a
        if onTopCard != None:
            onTopCard.draw(screen)
            # if onTopCard.front:
            #     onTopCard.textBaseVal.draw(screen)
            #     onTopCard.textCurrVal.draw(screen)
            #     onTopCard.textName.draw(screen)
            onTopCard.onTop = False

        self.deckImgHolder1.draw(screen)
        self.deckImgHolder2.draw(screen)
        self.deckImgHolder3.draw(screen)

        self.deckImgHolderOpp1.draw(screen)
        self.deckImgHolderOpp2.draw(screen)
        self.deckImgHolderOpp3.draw(screen)

        # if self.showEndTurnButton:
        #     screen.blit(self.endTurnImg, (self.endTurnImgX, self.endTurnImgY))
        # elif self.showPassTurnButton:
        #     screen.blit(self.passTurnImg, (self.endTurnImgX, self.endTurnImgY))


        if self.faded:
            self.screen.blit(self.fadeScreen, (0, 0))

        if self.showHandButton:
            screen.blit(self.showHandImg, (self.showHandImgX, self.showHandImgY))

        if self.may_see_hero_cutscene:
            self.hero_turn_obj.draw(screen)
            self.font_turn_obj.draw(screen)

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
        self.winning_player = None
        self.phase = Phase.COIN_TOSS
        self.cards_played = 0

        self.opening = True
        self.done_turn = False
        self.may_end_round = False
        self.passed = False
        self.done_drawing = False

        self.bplayer_img = persistent['portraitA']
        self.bplayer_img.set_absolute((Globals.RESOLUTION_X *0.5 -250, Globals.RESOLUTION_Y * 0.45))
        self.bplayer2_img = persistent['portraitB']
        self.bplayer2_img.set_absolute((Globals.RESOLUTION_X *0.5 +250, Globals.RESOLUTION_Y * 0.45))
        self.big_portraits_visible = True

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


    # NOTE: we might need intermediary phases here. To give space for proper animation maybe?

    # tracks how round ended #
    ROUND_DRAW = auto()     # Three cards drawn
    ROUND_TWO = auto()      # Two cards drawn
    FINAL_ROUND = auto()    # One card drawn
    MATCH_COMPLETE = auto()

