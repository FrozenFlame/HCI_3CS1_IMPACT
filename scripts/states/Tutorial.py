import pygame, math, time, random
from enum import Enum, auto
from .classes.BoardField import BoardField
from .classes.Card import Card, Type
from .classes.Board import Board
from .classes.Movable import Movable
from .classes.FontObj import FontObj
from .classes.Buff_Factory import Kind, Operation, BuffFactory

from .classes.Player import Player
from .classes.User import User
from .classes.Hero import Hero
from .classes.DeckBuilder import DeckBuilder

from .. import tools

from ..Globals import Globals

'''
This class is the actual game between two players
'''
print("[Engine.py]Engine Loaded")

# THIS IS JUS A DUMMY OBJECT

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
green = (255, 125, 0)


# class which holds the game flow
class Tutorial(object):
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
        self.winning_player = None
        self.cards_played = 0  # counter to determine how many cards you've played that turn
        self.phase = Phase.COIN_TOSS
        self.musicplayer = None
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
        self.hero_cutscene = False
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
        self.music_loaded = False
        self.is_showing_decide = False

        self.noSpells = True

        # self.opening = True

        # objects
        self.board = None  # this rarely changes, maybe the board graphic but idk
        self.deck = None
        self.hand = None
        self.opponent_deck = None
        self.opponent_hand = None

        self.boardFieldOpp2 = None  # opponent back row
        self.boardFieldOpp = None  # opponent front row
        self.boardFieldListOpp = [self.boardFieldOpp, self.boardFieldOpp2]
        self.boardField = None  # player front row
        self.boardField2 = None  # player back row
        # self.boardFieldList = [self.boardField, self.boardField2, self.boardFieldOpp, self.boardFieldOpp2]
        self.boardFieldList = [self.boardField, self.boardField2]
        # self.boardCardList = list()

        self.bplayer_img = None
        self.bplayer_font = None
        self.bplayer2_img = None
        self.bplayer2_font = None
        self.hero_turn_obj = None
        self.font_turn_obj = None
        self.font_decide_obj = None  # the object which shows who won the previous round

        self.allCardsList = list()

        self.clickedCard = list()

        '''scenario: the 10 hand cards start at the top of the deck/deckImgHolder3, then use waitTick so that 1 card animates(similarly to the click-and-drag animation)
         to its hand position every 1 second
         formula for wait:
                  if currentTick - self.waitTick >= self.drawCardWait:
                        self.waitTick = currentTick
                        [do stuff]
        '''
        self.drawCardSound = pygame.mixer.Sound("assets\\cards\\draw_card.wav")  # may be confused with draw()

        self.opening = True
        # self.drawCardWait = 250
        self.drawCardWait = 100
        self.openingIndex = 0
        self.openingX = 220  # hand coordinate is from 220 to 1020 (PLAYER)
        self.openingY = 610
        self.openingXOpp = 220  # hand coordinate is from 220 to 1020 (OPP)
        self.openingYOpp = -30

        self.deckImgHolder1 = Card()  # add formula to determine how many deckImgHolders; ex. (no. of cards in deck) / 3 = (no. of deckImgHolders)
        self.deckImgHolder2 = Card()  # or have preset of (x number of deckHolders) then hide the top deckHolder for every 5 cards removed from deck
        self.deckImgHolder3 = Card()

        self.deckImgHolderOpp1 = Card()
        self.deckImgHolderOpp2 = Card()
        self.deckImgHolderOpp3 = Card()

        '''
        UI things (initial state) we're gonna have to put some of these things in classes so that the game would be more scalable
        '''
        self.screen_center = Globals.RESOLUTION_X *0.5, Globals.RESOLUTION_Y *0.5
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
        self.top_slot = (Globals.RESOLUTION_X * 0.12-2, Globals.RESOLUTION_Y * 0.292)
        self.bottom_slot = (Globals.RESOLUTION_X * 0.12-2, Globals.RESOLUTION_Y * 0.855)
        self.coin_slot = (Globals.RESOLUTION_X * 0.082, Globals.RESOLUTION_Y * 0.5)

        # cash points
        self.botcash_coords = (75, 672)
        self.bot_cash_surf = FontObj.surface_factory("C0", "OLDENGL.ttf", 45, green)
        self.topcash_coords = (75, -5)
        self.top_cash_surf = FontObj.surface_factory("C0", "OLDENGL.ttf", 45, green)

        # fade things
        self.screen = pygame.display.set_mode((1280, 720))
        self.fadeScreen = pygame.Surface((1280, 720))
        self.fadeScreen.fill((0, 0, 0))  # black
        self.faded = False
        self.flewOut = False

        self.inGame = pygame.mixer.Sound("assets\\sounds\\mysterious sound.ogg")
        self.cracksmall = pygame.mixer.Sound("assets\\sounds\\glass breaking small.ogg")
        self.cracksmall.set_volume(0.30)
        self.crackbig = pygame.mixer.Sound("assets\\sounds\\glass breaking.ogg")
        self.crackbig.set_volume(0.20)
        self.flyOutEffect = pygame.mixer.Sound("assets\\sounds\\showHero.ogg")

        self.flyOutEffect.set_volume(0.20)

        self.spellPlayed = False
        self.playedSpell = None

        self.cashNegatives = list()
        # self.startup(pygame.time.get_ticks(),{})

        #  _____       _             _       _   _   _     _
        # /__   \_   _| |_ ___  _ __(_) __ _| | | |_| |__ (_)_ __   __ _ ___
        #   / /\/ | | | __/ _ \| '__| |/ _` | | | __| '_ \| | '_ \ / _` / __|
        #  / /  | |_| | || (_) | |  | | (_| | | | |_| | | | | | | | (_| \__ \
        #  \/    \__,_|\__\___/|_|  |_|\__,_|_|  \__|_| |_|_|_| |_|\__, |___/
        #                                                          |___/

        # tutorial-specific booleans TODO
        self.tut_wait = True
        self.tut_may_proceed = False
        self.tut_may_preview = False
        self.may_see_okay_button = False
        self.may_see_arrow = False
        self.may_see_arrowr = False
        self.tut_prep_jebait = True
        self.tut_may_now_end = False
        self.tut_favordiag_bool = True
        self.tut_welcome_bool = False  # TODO pseudocode for now
        self.tut_passend_bool = True  # this is the pass/end coin
        self.tut_passend2_bool = True  # Once you've played your cards, you must end your turn
        self.tut_passend3_bool = True  # However if you pass your turn, your opponent may play
        self.tut_passend4_bool = True  # We'll use that a little later.
        self.tut_cards_bool = True  # click show button
        self.tut_cards2_bool = True  # explain pt1
        self.tut_cards3_bool = True  # explain pt2
        self.tut_cards4_bool = True  # hover to see up close
        self.tut_place_bool = True  # go ahead, try to place a card
        self.tut_placeb_bool = True
        self.tut_place2_bool = True  # notice your score has gone up
        self.tut_place3_bool = True  # try to play another
        self.tut_second_card_played = False
        self.tut_place4_bool = True  # see that their values have added up...
        self.tut_place5_bool = True  # and may have even triggered their card effects for bonus cash!
        self.tut_place5b_bool = True  # your goal is to end the round with more cash than your opponent
        self.tut_place6_bool = True  # try playing another card!
        self.tut_place7_bool = True  # You couldn't place the card down.
        self.tut_place8_bool = True  # this is because you can only play 1 card per turn
        self.tut_place9_bool = True  # click the end turn coin at the left to end your turn
        # Don't black out the screen
        self.tut_black_bool = True  # Now, your opponent will start playing their cards
        self.tut_black2_bool = True  # Once a round has been decided after a series of turns
        self.tut_black3_bool = True  # A round winner may be decided, and the loser would lose hitpoints
        self.tut_black3b_bool = True  # Players draw a few cards before starting the next turn
        self.tut_black4_bool = True  # Each player has 2 lives each. The survivor shall be declared winner
        self.tut_black5_bool = True  # How far will you push the greed in order to win

        # tutorial screen coordinates
        self.tut_hand_coord = (Globals.RESOLUTION_X * 0.5, Globals.RESOLUTION_Y * 0.8)
        self.tut_okaybutton_coord = (Globals.RESOLUTION_X * 0.90, Globals.RESOLUTION_Y * 0.57)
        self.tut_board_arrow_coords = (Globals.RESOLUTION_X*0.85, Globals.RESOLUTION_Y * 0.7)
        self.tut_botscore_coord = Globals.RESOLUTION_X * 0.20, Globals.RESOLUTION_Y * 0.96
        # tutorial-specific objects
        self.tut_general_dialogue = FontObj.factory("Welcome to Avarice!", Globals.RESOLUTION_X * 0.5, Globals.RESOLUTION_Y * 0.5, "big_noodle_titling.ttf",
                                                    55, (255, 255, 255))
        self.tut_general_dialogue.set_absolute((1800, Globals.RESOLUTION_Y * 0.5))
        self.tut_okaybutton = Movable(pygame.image.load("assets\\buttons\\okay.png").convert_alpha(), 1200, 4, "distance", self.tut_okaybutton_coord)
        self.tut_arrow = Movable(pygame.image.load("assets\\arrow.png").convert_alpha(), 1200, 4, "distance", (self.coin_slot[0] + 130, self.coin_slot[1]))
        self.tut_arrowr = Movable(pygame.image.load("assets\\arrow2.png").convert_alpha(), 1200, 4, "distance", (self.screen_center[0]+25, self.coin_slot[1]))




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
        # random.shuffle(deck)
        first_ten = []
        for i in range(0, 10):  # self minus due to simultaneous pop will offset this
            first_ten.append(deck[i - i])
            deck.pop(i - i)
        return first_ten

    def draw_cards(self, amt, from_deck, to_hand):
        # print("Drawing {0} cards to {1}'s hand from {2}'s deck".format(amt, ))
        for i in range(0, amt):
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

            globs = self.bottom_slot
            globs2 = self.top_slot
            self.bplayer2_font.set_absolute((globs[0] - 85, globs[1] - 16))
            self.bplayer_font.set_absolute((globs2[0] - 85, globs2[1] - 22))

            self.player1heads = False

        else:
            self.bplayer2_img.set_absolute(self.top_slot)
            self.bplayer_img.set_absolute(self.bottom_slot)

            globs = self.bottom_slot
            globs2 = self.top_slot
            self.bplayer_font.set_absolute((globs[0] - 85, globs[1] - 16))
            self.bplayer2_font.set_absolute((globs2[0] - 85, globs2[1] - 22))

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

    def send_to_grave_fromboard(self, card, boardField):  # lite version? no cardstack difference though
        # print("Index to be tossed to grave: ",boardField.cardList.index(card))
        boardField.cardList.pop(boardField.cardList.index(card))
        if boardField.owner == self.player.user.username:
            # print("My boardfield")
            card.defaultPos = self.graveYardX, self.graveYardY
            self.graveYardList.append(card)
        else:
            card.defaultPos = self.graveYardOppX, self.graveYardOppY
            self.graveYardListOpp.append(card)

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

        for card in self.boardField.cardList:
            self.boardField.cardList.pop(self.boardField.cardList.index(card))
            self.graveYardList.append(card)
            card.defaultPos = self.graveYardX, self.graveYardY

        for card in self.boardField2.cardList:
            self.boardField2.cardList.pop(self.boardField2.cardList.index(card))
            self.graveYardList.append(card)
            card.defaultPos = self.graveYardX, self.graveYardY

        for card in self.boardFieldOpp.cardList:
            self.boardFieldOpp.cardList.pop(self.boardFieldOpp.cardList.index(card))
            self.graveYardListOpp.append(card)
            card.defaultPos = self.graveYardOppX, self.graveYardOppY

        for card in self.boardFieldOpp2.cardList:
            self.boardFieldOpp2.cardList.pop(self.boardFieldOpp2.cardList.index(card))
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
        self.recalculate_score(self.player, boardfieldlist)

        if self.cards_played == 2 and not self.passed:
            self.tut_second_card_played = True
            self.may_drag = False

    def end_turn(self):
        # self.done_turn = True
        self.showPassTurnButton = False
        self.showEndTurnButton = False
        self.cards_played = 0

    def recalculate_score(self, player, bFList):
        print("[Engine] recalculate score Previous cash: ", self.player.cash)
        player.cash = 0
        for bF in bFList:
            for c in bF.cardList:
                player.cash += c.current_val
        for utang in self.cashNegatives:
            player.cash -= utang
        print("[Engine] After recalculation cash: ", self.player.cash)
        # TODO lazy, no algorithm. Make a better algorithm in the future
        self.refresh_cash(player)

    def refresh_cash(self, player):
        self.bot_cash_surf = FontObj.surface_factory("C" + str(self.player.cash), "OLDENGL.ttf", 45, green)
        self.top_cash_surf = FontObj.surface_factory("C" + str(self.player2.cash), "OLDENGL.ttf", 45, green)

    def apply_effects(self, boardField):  # f this sh
        vehicleCounter = boardField.count_cardType(Type.VEHICLE)
        crimeCounter = boardField.count_cardType(Type.CRIME)
        personCounter = boardField.count_cardType(Type.PERSON)
        effectActivated = False

        for boardCard in boardField.cardList:
            if not boardCard.effectActivated:
                if boardCard.id is "butler":
                    print("Butler Effect")
                    if boardField.cardList.index(boardCard) != 0:
                        boardField.cardList[boardField.cardList.index(boardCard) - 1].current_val += 5
                        boardField.cardList[boardField.cardList.index(boardCard) - 1].recalculate()

                    boardCard.effectActivated = True
                    effectActivated = True
                    continue

                if boardCard.id is "saboteur":
                    print("Saboteur Effect")
                    sent = False
                    targetList = list()
                    for bF in self.boardFieldListOpp:
                        targetList.extend(bF.cardList)

                    if len(targetList) != 0:
                        for target in targetList:
                            r = random.randrange(0, 2)
                            if r == 1:
                                self.sendToGraveyard(target)
                                sent = True
                        if not sent:
                            self.sendToGraveyard(targetList[0])

                    boardCard.effectActivated = True
                    effectActivated = True
                    continue

                if boardCard.id is "resurrect":
                    print("Resurrect Effect")
                    personInGraveList = list()
                    for a in self.graveYardList:
                        if Type.PERSON in a.type:
                            personInGraveList.append(a)
                    if len(personInGraveList) > 0:
                        r = random.randrange(0, len(personInGraveList))
                        c = personInGraveList[r]
                        self.boardField.take_card(c)
                        # self.recalculate_score(self.boardFieldList)
                        self.graveYardList.pop(self.graveYardList.index(c))
                        c.flip()
                        c.disabled = False
                        c.resting = False
                        c.set_destination(*c.defaultPos)

                    boardCard.effectActivated = True
                    effectActivated = True
                    continue

                if boardCard.id is "reap":
                    print(boardCard.name, " effect activated")
                    for bf in self.boardFieldList:
                        for c in bf.cardList:
                            if c.id is 'farm':
                                self.player.cashPositives.append(c.current_val)
                                self.send_to_grave_fromboard(c, bf)

                    boardCard.effectActivated = True
                    effectActivated = True
                    continue

                if boardCard.id is "farmboy":
                    print(boardCard.name, " effect activated")
                    for c in boardField.cardList:
                        if c.id is 'farm':
                            c.current_val += 3
                        if Type.ANIMAL in c.type:
                            c.current_val += 1

                    boardCard.effectActivated = True
                    effectActivated = True
                    continue
        if effectActivated:
            for bf in self.boardFieldList:
                for a in bf.cardList:
                    a.img = pygame.transform.smoothscale(a.frontImg, (round(a.frontImg.get_rect().size[0] * 0.33), round(a.frontImg.get_rect().size[1] * 0.33)))
                    a.draw(self.screen)
                    print(a.name, "redrawn")
                bf.rearrange()
                print(bf, " cardlist size: ", len(bf.cardList))
                print(bf, "rearranged")

            for bf in self.boardFieldListOpp:
                for a in bf.cardList:
                    a.img = pygame.transform.smoothscale(a.frontImg, (round(a.frontImg.get_rect().size[0] * 0.33), round(a.frontImg.get_rect().size[1] * 0.33)))
                    a.draw(self.screen)
                    print(a.name, "redrawn")
                bf.rearrange()
                print(bf, " cardlist size: ", len(bf.cardList))
                print(bf, "rearranged")
            self.recalculate_score(self.player, self.boardFieldList)
            self.recalculate_score(self.player2, self.boardFieldListOpp)

        ############################################## end of effects #################################################
        if effectActivated:
            for bf in self.boardFieldList:
                for a in bf.cardList:
                    a.rebuildFront()
                    a.img = pygame.transform.smoothscale(a.frontImg, (round(a.frontImg.get_rect().size[0] * 0.33), round(a.frontImg.get_rect().size[1] * 0.33)))
                    # a.draw(self.screen)
                bf.rearrange()

            for bf in self.boardFieldListOpp:
                for a in bf.cardList:
                    a.rebuildFront()
                    a.img = pygame.transform.smoothscale(a.frontImg, (round(a.frontImg.get_rect().size[0] * 0.33), round(a.frontImg.get_rect().size[1] * 0.33)))
                    # a.draw(self.screen)
                bf.rearrange()
            print("====SELF GRAVEYARD====")
            for c in self.graveYardList:
                print(c.name)
            print("====OPPONENT GRAVEYARD====")
            for c in self.graveYardListOpp:
                print(c.name)
            self.recalculate_score(self.player, self.boardFieldList)
            self.recalculate_score(self.player2, self.boardFieldListOpp)

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
        # for bf in self.boardFieldList:
        #     for a in bf.cardList:
        #         if Type.SPELL in a.type:
        #             pygame.time.delay(1000)
        #             self.sendToGraveyard(a)
        #         else:
        #             a.draw(self.screen)
        #             print(a.name, "redrawn")
        #     bf.rearrange()
        #     print(bf, " cardlist size: ", len(bf.cardList))
        #     print(bf, "rearranged")
        #
        # for bf in self.boardFieldListOpp:
        #     for a in bf.cardList:
        #         if Type.SPELL in a.type:
        #             pygame.time.delay(1000)
        #             self.sendToGraveyard(a)
        #         else:
        #             a.draw(self.screen)
        #             print(a.name, "redrawn")
        #     bf.rearrange()
        #     print(bf, " cardlistopp size: ", len(bf.cardList))
        #     print(bf, "rearrangedopp")

        if event.type == pygame.QUIT:
            self.done = True
        # if self.board.hasPreviewCard:
        #   print("Previewing card.")
        # card is being moused

        # print("[Engine.py] - KEYDOWN: {0}".format(pygame.key.get_pressed()))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("[Engine(STATE)] Escape Pressed")
                # TEMPORARY METHOD:
                self.backToMain()
            if event.key == pygame.K_d:
                print("[Engine] self.allCardsList[0]: ", self.allCardsList[0])
                self.allCardsList[0].resting = False
                self.allCardsList[0].set_destination(100, 100)
            if event.key == pygame.K_a:
                print("defaultpos0 ", self.allCardsList[0].defaultPos[0], " defaultpos1 ", self.allCardsList[0].defaultPos[1])
        #     pass
        if self.cardMousedOver(pygame.mouse.get_pos()):
            # print("Mousingover")
            if self.clickedCard[0].front:
                if self.tut_may_preview:
                    self.board.hasPreviewCard = True
                    self.board.previewCard = self.clickedCard[0]  # this actually must be the card that's being moused over.
        elif not self.cardMousedOver(pygame.mouse.get_pos()):
            # print("notmousing")
            self.board.hasPreviewCard = False if not self.holdingCard else True

        ''' GET EVENT
         ____  _  _   __   ____  ____  ____ 
        (  _ \/ )( \ / _\ / ___)(  __)/ ___)
         ) __/) __ (/    \\___ \ ) _) \___ \
        (__)  \_)(_/\_/\_/(____/(____)(____/

        '''
        '''
                    > welcome to avarice!
                    > These are your cards below, click the show button to reveal them!
                    > Each card in Avarice may have value ...
                    > and may have an effect once you play it on your fields
                    > hover on a card to see it up close!
                    > try to place a card
                    > notice that your score may have changed.
                    > Play another card! 
        '''

        # tutorial button
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = pygame.mouse.get_pressed()
            if click[0] == 1:
                if self.tut_okaybutton.rect.collidepoint(pygame.mouse.get_pos()) and self.may_see_okay_button:
                    self.tut_may_proceed = True


        if self.phase == Phase.PLAY and not self.hero_cutscene:

            # TUTORIAL THINGS
            if self.tut_cards2_bool:  # explain pt1
                pass
            elif self.tut_cards3_bool:  # explain pt2
                pass
            elif self.tut_cards4_bool:  # hover to see up close
                pass
            elif self.tut_place_bool:  # go ahead, try to place a card
                pass
            elif self.tut_place2_bool:  # notice your score has gone up
                pass
            elif self.tut_place3_bool:  # try to play another
                pass
            elif self.tut_place4_bool:  # see that their values have added up...
                pass
            elif self.tut_place5_bool:  # and may have even triggered their card effects for bonus cash!
                pass
            elif self.tut_place5b_bool:  # your goal is to end the round with more cash than your opponent
                pass
            elif self.tut_place6_bool:  # try playing another card!
                pass
            elif self.tut_place7_bool:  # You couldn't place the card down.
                pass
            elif self.tut_place8_bool:  # this is because you can only play 1 card per turn
                pass
            elif self.tut_place9_bool:  # click the end turn coin at the left to end your turn
                pass
            # Don't black out the screen
            elif self.tut_black_bool:  # Now, your opponent will start playing their cards
                pass
            elif self.tut_black2_bool:  # Once a round has been decided after a series of turns
                pass
            elif self.tut_black3_bool:  # A round winner may be decided, and the loser would lose hitpoints
                pass
            elif self.tut_black3b_bool: # Players draw a few cards before starting the next turn
                pass
            elif self.tut_black4_bool:  # Each player has 2 lives each. The survivor shall be declared winner
                pass
            elif self.tut_black5_bool:  # How far will you push the greed in order to win
                pass

            if event.type == pygame.MOUSEBUTTONUP:
                click = pygame.mouse.get_pressed()

                if click[0] == 0:
                    if self.tut_prep_jebait:
                        self.tut_may_proceed = True


                    if self.mouseOnEndTurnButton and self.showEndTurnButton and self.tut_may_now_end:
                        self.tut_may_proceed = True
                    if self.mouseOnPassTurnButton and self.showPassTurnButton and self.tut_may_now_end:
                        pass

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

                        # let go into a boardField
                        # if self.clickedCard[0].colliderect(self.boardField.xStart,self.boardField.yStart,self.boardField.xEnd,self.boardField.yEnd) and not self.clickedCard[0].onBoard:
                        #     self.boardCardList.append(self.clickedCard[0])
                        #     self.clickedCard[0].onBoard = True
                        #


                        for bF in self.boardFieldList:
                            if self.clickedCard[0].collide_rect(*bF.get_dimensions()) and not self.clickedCard[0].onBoard:
                                bF.take_card(self.clickedCard[0])
                                self.clickedCard[0].onBoard = True
                                self.play_card(self.clickedCard[0], self.boardFieldList)
                                if Type.SPELL in self.clickedCard[0].type:
                                    self.spellPlayed = True
                                    self.playedSpell = self.clickedCard[0]

                        # TODO erase these boardfield card play below, they are obsolete.
                        # if self.player == self.first_player:
                        #     for bF in self.boardFieldList:
                        #         if self.clickedCard[0].collide_rect(*bF.get_dimensions()) and not self.clickedCard[0].onBoard:
                        #             bF.take_card(self.clickedCard[0])
                        #             self.clickedCard[0].onBoard = True
                        #             self.play_card(self.clickedCard[0], self.boardFieldList)
                        # elif self.player2 == self.first_player and not self.clickedCard[0].onBoard:
                        #     for bF in self.boardFieldListOpp:
                        #         if self.clickedCard[0].collide_rect(*bF.get_dimensions()):
                        #             bF.take_card(self.clickedCard[0])
                        #             self.clickedCard[0].onBoard = True
                        #             self.play_card(self.clickedCard[0], self.boardFieldListOpp)

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

                            if Type.SPELL in s.type and self.noSpells:
                                continue
                            else:
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



            if self.showHandButton and (self.showHandImgX + self.endTurnImgDimensionX) > pygame.mouse.get_pos()[0] > self.showHandImgX and (self.showHandImgY + self.endTurnImgDimensionY) > \
                    pygame.mouse.get_pos()[1] > self.showHandImgY and self.tut_may_proceed:
                self.mouseOnShowHandButton = True
                self.may_drag = True
            elif self.showHandButton:
                self.mouseOnShowHandButton = False
            if event.type == pygame.MOUSEBUTTONUP:
                click = pygame.mouse.get_pressed()
                if click[0] == 0:


                    if self.mouseOnShowHandButton and self.showHandButton:
                        self.musicplayer.prep_song_hero(self.player.hero.name)
                        self.musicplayer.play()
                        print("[Engine]Showing cards")
                        self.showHandButton = False
                        if self.faded:
                            self.board.coin.show_pass()
                            self.board.hasPreviewCard = False
                            self.refresh_cash(self.player)

                            self.fadeOut()

                        self.flip_hand(self.hand)
                        self.phase = Phase.PLAY
                        self.music_loaded = False
                        if not self.passed:
                            self.showPassTurnButton = True
                            self.board.coin.show_pass()
                        else:
                            self.showEndTurnButton = True
                            self.board.coin.show_end()

                        # cutscene prep:
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

                        # tutorial things
                        print("show button pressed")
                        self.tut_may_proceed = False
                        self.tut_cards_bool = False

                        self.tut_general_dialogue.set_destination(-400, self.screen_center[1] + 70)
                        self.may_see_okay_button = False
                        self.may_see_arrow = False

                        self.waitTick = pygame.time.get_ticks()
                        self.tut_wait = True


                        self.tut_may_proceed = False

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

        if self.is_showing_decide:
            self.font_decide_obj.update(deltaTime)

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
            if self.spellPlayed:
                if currentTime - self.waitTick >= 1000:  # this does not work; add something where the spell remains on board for 1second, then goes to graveyard, then rearrange board
                    self.waitTick = currentTime  # delete this comments when done
                    self.sendToGraveyard(self.playedSpell)
                    self.spellPlayed = False
            if self.hero_cutscene:  # TODO Cutscene #33333333
                if self.hero_cutscene_flyin:
                    self.hero_turn_obj.update(deltaTime)
                    self.font_turn_obj.update(deltaTime)
                    # these two set destination codes below are actually triggered in the get_evt block
                    self.hero_turn_obj.set_destination(*(Globals.RESOLUTION_X * 0.5, Globals.RESOLUTION_Y * 0.5))
                    self.font_turn_obj.set_destination(*(Globals.RESOLUTION_X * 0.5, Globals.RESOLUTION_Y * 0.5 + 200))
                    if currentTime - self.waitTick >= 2500:
                        self.hero_cutscene_flyin = False
                        self.waitTick = currentTime
                        self.hero_turn_obj.set_destination(*(-300, Globals.RESOLUTION_Y * 0.5))
                        self.font_turn_obj.set_destination(*(-300, Globals.RESOLUTION_Y * 0.5 + 200))
                        self.flyOutEffect.play()
                elif self.hero_cutscene_flyout:

                    self.hero_turn_obj.update(deltaTime)
                    self.font_turn_obj.update(deltaTime)

                    if currentTime - self.waitTick >= 800:  # timeout before players can start clicking around again

                        self.waitTick = currentTime

                        self.hero_cutscene_flyout = False
                        # self.control_enabled = True     actually non-factor I think
                        self.may_see_hero_cutscene = False
                        self.hero_cutscene = False

            # TUTORIAL THINGS

            if self.tut_cards2_bool:  # explain pt1
                if currentTime - self.waitTick >= 2480 and self.tut_wait:
                    print("Enter here please")
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("Each card in Avarice may have some value", self.screen_center[0]+450, self.screen_center[1]+220, "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0], self.screen_center[1]+220)
                    self.may_see_okay_button = True
                    self.tut_may_proceed = False
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_cards2_bool = False

                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1]+220)
                    self.may_see_okay_button = False

                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_cards3_bool:  # explain pt2
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("and may have an effect once placed on your two fields", self.screen_center[0]+450, self.screen_center[1]+220, "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0], self.screen_center[1]+220)
                    self.may_see_arrow = True
                    self.tut_arrow.set_absolute(self.tut_board_arrow_coords)
                    self.may_see_okay_button = True
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_cards3_bool = False

                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1]+220)
                    self.may_see_okay_button = False

                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_cards4_bool:  # hover to see up close
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("Point on a card to see their details to the right!", self.screen_center[0]+450, self.screen_center[1]+100, "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0], self.screen_center[1]+100)
                    self.may_see_arrow = False
                    self.tut_may_preview = True
                elif self.board.hasPreviewCard:
                    self.tut_may_proceed = False
                    self.tut_cards4_bool = False

                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1]+100)
                    self.may_see_okay_button = False

                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_place_bool:  # Here you can see your card
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("Here you see the card's type, value, effect, and name.", self.screen_center[0] + 450, self.screen_center[1] + 100, "big_noodle_titling.ttf",
                                                                55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0]-50, self.screen_center[1])
                    self.tut_arrowr.set_absolute((self.screen_center[0]+240,self.screen_center[1]+55))
                    self.may_see_arrowr = True


                elif currentTime - self.waitTick >= 4200:
                    self.tut_place_bool = False
                    self.tut_may_proceed = False

                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1]+100)
                    self.may_see_okay_button = False
                    self.tut_arrow.set_destination(Globals.RESOLUTION_X *0.94, Globals.RESOLUTION_Y *0.8)
                    self.may_see_arrowr = False

                    self.waitTick = currentTime
                    self.tut_wait = True

            elif self.tut_placeb_bool:  # Go ahead, drag a card onto one of your two fields
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("Go ahead, drag a card onto a field!", self.screen_center[0]+450, self.screen_center[1]-30, "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0], self.screen_center[1]-30)
                elif self.showEndTurnButton:
                    self.tut_may_proceed = False
                    self.tut_placeb_bool = False

                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1]-30)
                    self.may_see_okay_button = False

                    self.waitTick = currentTime
                    self.tut_wait = True

            elif self.tut_place2_bool:  # notice your score has gone up
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("Notice your score has gone up", self.screen_center[0]+450, self.screen_center[1]+50, "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0], self.screen_center[1]+50)
                    self.may_see_arrow = True
                    self.may_see_okay_button = True
                    self.tut_arrow.set_destination(*self.tut_botscore_coord)

                    self.noSpells = False
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_place2_bool = False

                    self.tut_general_dialogue.set_destination(-700, self.tut_botscore_coord[1])
                    self.may_see_okay_button = False

                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_place3_bool:  # try to play another
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("Try to play another card", self.screen_center[0]+450, self.screen_center[1]-30, "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0], self.screen_center[1]-30)
                    self.may_see_arrow = False
                elif self.tut_second_card_played:
                    self.tut_may_proceed = False
                    self.tut_place3_bool = False

                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1]-30)

                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_place4_bool:  # see that their values have added up...
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("See that the cards' values have added up", self.screen_center[0]+450, self.screen_center[1]+220, "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0], self.screen_center[1]+220)
                    self.tut_arrow.set_destination(self.screen_center[0]*0.23, self.screen_center[1] *0.96)
                elif currentTime - self.waitTick >= 5000:
                    self.tut_may_proceed = False
                    self.tut_place4_bool = False
                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1]+220)

                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_place5_bool:  # and may have even triggered their card effects for bonus cash!
                if currentTime - self.waitTick >= 300 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("and may have even triggered their card effects for bonus cash!", self.screen_center[0]+450, self.screen_center[1]+220, "big_noodle_titling.ttf", 40, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0], self.screen_center[1]+220)
                    self.may_see_okay_button = True
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_place5_bool = False
                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1]+220)

                    self.waitTick = currentTime
                    self.tut_wait = True

            elif self.tut_place5b_bool:  # your goal is to end the round with more cash than your opponent
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("your goal is to have more money than your opponent when the round ends", self.screen_center[0]+450, self.screen_center[1]-230, "big_noodle_titling.ttf", 36, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0]-30, self.screen_center[1]-230)
                    self.tut_arrow.set_destination(Globals.RESOLUTION_X*0.2, Globals.RESOLUTION_Y *0.03)
                    self.may_see_arrow = True
                    self.may_see_okay_button = True
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_place5b_bool = False

                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1]-230)
                    self.may_see_arrow = False
                    self.tut_prep_jebait = True

                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_place6_bool:  # try playing another card!
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("Try playing another card", self.screen_center[0]+700, self.screen_center[1], "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(*self.screen_center)
                    self.tut_arrow.set_destination(Globals.RESOLUTION_X*0.2, Globals.RESOLUTION_Y *0.08)
                    self.may_see_arrow = False
                    self.may_see_okay_button = False
                    self.tut_prep_jebait = True
                elif self.tut_may_proceed and self.tut_prep_jebait:
                    self.tut_may_proceed = False
                    self.tut_place6_bool = False
                    self.tut_prep_jebait = False
                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1])
                    self.may_see_arrow = False
                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_place7_bool:  # You couldn't place the card down.
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("Hold on, you've reached the limit of plays (2 max per turn)", self.screen_center[0]+700, self.screen_center[1]-10, "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0]+35, self.screen_center[1]-10)
                    self.may_see_okay_button = True
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_place7_bool = False

                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1]-10)
                    self.may_see_arrow = False
                    self.may_see_okay_button = False
                    self.waitTick = currentTime
                    self.tut_wait = True

            elif self.tut_place8_bool:  # this is because you can only play 2 card per turn
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("However, there may be a way to circumvent this", self.screen_center[0]+700, self.screen_center[1]-10, "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0], self.screen_center[1]-10)
                    self.may_see_okay_button = True
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_place8_bool = False

                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1] -10)
                    self.may_see_okay_button = False
                    self.tut_may_now_end = True
                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_place9_bool:  # click the end turn coin at the left to end your turn
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("Click the end turn coin at the left to end your turn", self.screen_center[0]+700, self.screen_center[1]-10, "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(*(self.screen_center[0]+110, self.screen_center[1]))
                    self.may_see_arrow = True
                    self.tut_arrow.set_destination(self.coin_slot[0] + 130, self.coin_slot[1])
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_place9_bool = False

                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1] -10)
                    self.may_see_okay_button = False
                    self.may_see_arrow = False
                    self.waitTick = currentTime
                    self.tut_wait = True
            # Don't black out the screen
            elif self.tut_black_bool:  # Now, your opponent will start playing their cards
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("Now, it's your opponent's turn.", self.screen_center[0]+700, self.screen_center[1], "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0], self.screen_center[1])
                    self.may_see_okay_button = True
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_black_bool = False

                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1])
                    self.may_see_okay_button = False

                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_black2_bool:  # Once a round has been decided after a series of turns
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("Once a player passes, and the next ends, the round is judged", self.screen_center[0] + 700, self.screen_center[1], "big_noodle_titling.ttf", 45, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0]+30, self.screen_center[1])
                    self.may_see_okay_button = True
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_black2_bool = False

                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1])
                    self.may_see_okay_button = False

                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_black3_bool:  # A round winner may be decided, and the loser would lose hitpoints
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("The loser would lose hitpoints (indicated by cracks)", self.screen_center[0] + 700, self.screen_center[1], "big_noodle_titling.ttf", 43, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0], self.screen_center[1])
                    self.may_see_okay_button = True
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_black3_bool = False

                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1])
                    self.may_see_okay_button = False

                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_black3b_bool:  # Players draw a few cards before starting the next turn
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("Players draw a few cards before starting the next turn", self.screen_center[0] + 700, self.screen_center[1], "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0], self.screen_center[1])
                    self.may_see_okay_button = True
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_black3b_bool = False

                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1])
                    self.may_see_okay_button = False

                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_black4_bool:  # Each player has 2 lives each. The survivor shall be declared winner
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("Each player has 2 hitpoints. The survivor shall be declared victorious", self.screen_center[0] + 700, self.screen_center[1], "big_noodle_titling.ttf", 50, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0], self.screen_center[1])
                    self.may_see_okay_button = True
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_black4_bool = False

                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1])
                    self.may_see_okay_button = False

                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_black5_bool:  # How far will you push the greed in order to win
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("How much luck and greed would it take to win?", self.screen_center[0] + 700, self.screen_center[1], "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0], self.screen_center[1])
                elif currentTime - self.waitTick >= 2600:
                    self.tut_may_proceed = False
                    self.tut_black5_bool = False
                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1])
                    self.may_see_okay_button = False

                    self.waitTick = currentTime
                    self.tut_wait = True


            else:
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.fadeIn()
                    self.backToMain()

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
                self.showEndTurnButton = False  # this is not working
        elif self.phase == Phase.PREP:

            # TUTORIAL THINGS
            if self.tut_favordiag_bool:
                if self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_general_dialogue.set_destination(-650, Globals.RESOLUTION_Y * 0.5)
                    self.tut_favordiag_bool = False
                    self.may_see_okay_button = False
                    self.tut_welcome_bool = True
                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_welcome_bool:  # TODO pseudocode for now
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("You had the favor of the coin toss, so you are going first.",self.screen_center[0]+450, self.screen_center[1],"big_noodle_titling.ttf",55,(255,255,255))
                    self.tut_general_dialogue.set_destination(*self.screen_center)
                    self.may_see_okay_button = True
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_welcome_bool = False

                    self.tut_general_dialogue.set_destination(-650, Globals.RESOLUTION_Y * 0.5)
                    self.may_see_okay_button = False

                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_passend_bool:  # this is the pass/end coin
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("This is the pass/end coin", self.screen_center[0]+450, self.screen_center[1], "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(*(self.screen_center[0]-100, self.screen_center[1]))
                    self.may_see_arrow = True
                    self.may_see_okay_button = True
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_passend_bool = False

                    self.tut_general_dialogue.set_destination(-400, self.screen_center[1])
                    self.may_see_okay_button = False

                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_passend2_bool:  # Once you've played your cards, you must end your turn
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("Once you've played your cards, you must end your turn", self.screen_center[0]+450, self.screen_center[1]+70, "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0]-50, self.screen_center[1]+70)
                    self.may_see_okay_button = True
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_passend2_bool = False

                    self.tut_general_dialogue.set_destination(-700, self.screen_center[1]+70)
                    self.may_see_okay_button = False

                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_passend3_bool:  # You made decide to not play your cards and pass the turn
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("You may decide to not play your cards and pass", self.screen_center[0]+450, self.screen_center[1]+70, "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0]-50, self.screen_center[1]+70)
                    self.may_see_okay_button = True
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_passend3_bool = False

                    self.tut_general_dialogue.set_destination(-600, self.screen_center[1]+70)
                    self.may_see_okay_button = False

                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_passend4_bool:  # We'll use that a little later.
                if currentTime - self.waitTick >= 500 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("We'll use this a little later", self.screen_center[0]+450, self.screen_center[1]+70, "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(self.screen_center[0]-50, self.screen_center[1]+70)
                    self.may_see_okay_button = True
                elif self.tut_may_proceed:
                    self.tut_may_proceed = False
                    self.tut_passend4_bool = False

                    self.tut_general_dialogue.set_destination(-400, self.screen_center[1]+70)
                    self.may_see_okay_button = False
                    self.may_see_arrow = False
                    self.waitTick = currentTime
                    self.tut_wait = True
            elif self.tut_cards_bool:  # click show button
                if currentTime - self.waitTick >= 600 and self.tut_wait:
                    self.tut_wait = False
                    self.tut_general_dialogue = FontObj.factory("Click the show button below!", self.screen_center[0] + 450, self.screen_center[1], "big_noodle_titling.ttf", 55, (255, 255, 255))
                    self.tut_general_dialogue.set_destination(*self.screen_center)
                    self.showHandButton = True
                    self.tut_may_proceed = True



            # more on animations updates
            if not len(self.hand) == 0:
                if self.hand[0].front:
                    self.flip_hand(self.hand)

            # self.showHandButton = False





        elif self.phase == Phase.END_ROUND:
            pass

        elif self.phase == Phase.OPENING:
            currentTick = currentTime
            # for now player 1 ALWAYS chooses heads
            if not self.first_player_set:

                print("LANDED HEADS")
                self.deck = self.player.deck
                self.opponent_deck = self.player2.deck
                self.hand = self.get_first_cards(self.deck, self.player.user.username)
                self.opponent_hand = self.get_first_cards(self.opponent_deck, self.player2.user.username)

                self.first_player = self.player

                self.musicplayer = MusicPlayer(self.player.hero.name, self.player2.hero.name)

                self.boardField.owner = self.player.user.username
                self.boardField2.owner = self.player.user.username

                self.boardFieldOpp.owner = self.player2.user.username
                self.boardFieldOpp2.owner = self.player2.user.username
                self.player1heads = True

                globs = self.bottom_slot
                globs2 = self.top_slot
                self.first_player_set = True

                # TODO I have a feeling this would cause some issues if the players used the same image, but we'll see. #python names not variables
                self.hero_turn_obj = Movable(self.player.hero.img, 1000, 4, "distance", (Globals.RESOLUTION_X * 0.5, Globals.RESOLUTION_Y * 0.5))
                self.font_turn_obj = FontObj.factory(self.player.user.username + "'s turn", -200, 0, "big_noodle_titling_oblique.ttf", 80, (255, 255, 255))
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
                self.inGame.play()
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
                    # animate coin?
                    if currentTime - self.waitTick <= 3000:  # how long we want the coin to be spinning before stopping it
                        self.waitTick = currentTime
                        self.board.coin.animating = False
                        self.first_toss_animating = False
                        if 0 == 0:
                            print("Coin pointing left")
                            self.board.coin.point_left()
                            self.board.coin.set_destination(Globals.RESOLUTION_X * 0.5, Globals.RESOLUTION_Y * 0.5)

                            # set bplayerimg to bottom left slot
                            self.bplayer_img.set_destination(*self.bottom_slot)
                            self.bplayer_img.scale_to((self.bplayer_img.original_surface.get_rect().size[0] * 0.70, self.bplayer_img.original_surface.get_rect().size[1] * 0.70))
                            # set bplayer2img to top left slot
                            self.bplayer2_img.set_destination(*self.top_slot)
                            self.bplayer2_img.scale_to((self.bplayer2_img.original_surface.get_rect().size[0] * 0.70, self.bplayer2_img.original_surface.get_rect().size[1] * 0.70))

                        else:
                            print("Coin pointing right")
                            self.board.coin.point_right()
                            self.board.coin.set_destination(Globals.RESOLUTION_X * 0.5, Globals.RESOLUTION_Y * 0.5)

                            # set bplayer2img to bottom left slot
                            self.bplayer_img.scale_to((self.bplayer_img.original_surface.get_rect().size[0] * 0.505, self.bplayer_img.original_surface.get_rect().size[1] * 0.505))
                            self.bplayer_img.set_destination(*self.top_slot)

                            self.bplayer2_img.scale_to((self.bplayer2_img.original_surface.get_rect().size[0] * 0.505, self.bplayer2_img.original_surface.get_rect().size[1] * 0.505))
                            self.bplayer2_img.set_destination(*self.bottom_slot)
                            # set bplayerimg to top left slot


                elif self.notif_pause:  # time paused to notify who goes first
                    if currentTime - self.waitTick >= 3000:
                        self.board.coin.show_pass()
                        self.notif_pause = False
                        self.may_see_first = True
                        # self.first_fontobj absolute position below first player card
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
                    self.may_see_okay_button = True
                    self.tut_general_dialogue.set_destination(Globals.RESOLUTION_X *0.5, Globals.RESOLUTION_Y *0.5)
                    self.phase = Phase.OPENING
            # self.phase = Phase.OPENING
            # block down below
            # if self.opening:
            #     self.phase = Phase.OPENING
            # else:
            #     self.phase = Phase.SWAP

        # tutorial elements
        self.tut_general_dialogue.update(deltaTime)
        self.tut_arrow.update(deltaTime)


        self.draw(screen)  # last function of update. execute draw

    # orders individual elements to draw themselves in the correct order (your blits)
    def draw(self, screen):
        screen.fill((255, 255, 255))

        self.board.draw(screen)

        self.board.coin.draw(screen)
        if self.big_portraits_visible:
            self.bplayer_img.draw(screen)
            self.bplayer2_img.draw(screen)
        onTopCard = None
        # cash draw
        if self.bot_cash_surf and self.top_cash_surf and not self.phase == Phase.COIN_TOSS:
            screen.blit(self.top_cash_surf, self.topcash_coords)
            screen.blit(self.bot_cash_surf, self.botcash_coords)

        for a in self.allCardsList:
            if not a.onTop:
                a.draw(screen)
            else:
                onTopCard = a
        if onTopCard != None:
            onTopCard.draw(screen)
            onTopCard.onTop = False
        if self.hand != None:
            for c in self.hand:
                c.draw(screen)

        if self.is_showing_decide:
            self.font_decide_obj.draw(screen)

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

        # tutorial elements
        self.tut_general_dialogue.draw(screen)
        if self.may_see_okay_button:
            self.tut_okaybutton.draw(screen)
        if self.may_see_arrow:
            self.tut_arrow.draw(screen)
        if self.may_see_arrowr:
            self.tut_arrowr.draw(screen)

    def startup(self, currentTime, persistent):

        self.persist = persistent
        self.startTime = currentTime

        '''
        testing persistent objects
        '''
        print("[Engine] ########################### ")
        print("[Engine] Entering the tutorial...")
        '''
        setting of board objects and setting of first perspective
        '''
        self.board = Board()
        # BoardField(x1=225, y1=390, x2=1010, y2=470, boardx=220, boardy=380)
        self.boardFieldOpp2 = BoardField(225, 105, 1010, 185)  # opponent back row
        self.boardFieldOpp = BoardField(225, 240, 1010, 320)  # opponent front row
        self.boardField = BoardField(225, 390, 1010, 470)  # player front row
        self.boardField2 = BoardField(225, 525, 1010, 605)  # player back row
        self.boardFieldList = [self.boardField, self.boardField2]
        self.boardFieldListOpp = [self.boardFieldOpp, self.boardFieldOpp2]

        self.first_player_set = False

        self.opening = True
        self.done_turn = False
        self.may_end_round = False
        self.passed = False
        self.done_drawing = False

        self.usera = User("Player 1", 99, 0)
        self.heroa = Hero("Billy", pygame.image.load("assets\\heroes\\hero_billy.png").convert_alpha())
        self.playera = Player(self.usera, self.heroa, DeckBuilder.build_deck("Tutorial"))  # NOTE set hero name deck here

        self.userb = User("Player 2", 99, 0)
        self.herob = Hero("King", pygame.image.load("assets\\heroes\\hero_king.png").convert_alpha())
        self.playerb = Player(self.userb, self.herob, DeckBuilder.build_deck("King"))  # NOTE set hero name deck here


        self.bplayer_img = Movable(self.heroa.img,1000, 4,"distance", (Globals.RESOLUTION_X *0.5 -250, Globals.RESOLUTION_Y * 0.45))

        self.bplayer2_img = Movable(self.herob.img,1000, 4,"distance", (Globals.RESOLUTION_X *0.5 +250, Globals.RESOLUTION_Y * 0.45))

        # Game trackers
        self.turn_no = 0
        self.player = self.playera
        self.player2 = self.playerb
        self.first_player = None  # does not change after coin toss
        self.opponent = None
        self.winning_player = None
        self.phase = Phase.COIN_TOSS
        self.cards_played = 0

        self.big_portraits_visible = True

    def cleanup(self):
        Globals.tutorial = False
        Globals.mainmenu = True
        pygame.mixer.music.fadeout(1000)
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

class MusicPlayer(object):
    def __init__(self, hero, hero2):
        self.hero = hero
        self.hero2 = hero2
        self.music_list = []
        self.victory = None
        self.music_list2 = []
        self.victory2 = None
        self.is_mirror = False
        self.last_played_index = random.randrange(0, 4)
        self.last_played_index2 = random.randrange(0, 4)
        self.to_play_hero2 = False
        self.last_hero = None
        self.has_victor = False
        self.bottom_win = False
        self.mc = pygame.mixer.music
        # self.mc2 = pygame.mixer.music
        if self.hero == self.hero2:
            self.is_mirror = True

        if not self.is_mirror:
            if self.hero == "Billy":
                self.music_list = [
                    "\\billy\\billy_theme01.ogg",
                    "\\billy\\billy_theme02.ogg",
                    "\\billy\\billy_theme03.ogg",
                    "\\billy\\billy_theme04.ogg",
                ]
                self.victory = "\\billy\\billy_victory.ogg"
            elif self.hero == "King":
                self.music_list = [
                    "\\king\\king_theme01.ogg",
                    "\\king\\king_theme02.ogg",
                    "\\king\\king_theme03.ogg",
                    "\\king\\king_theme04.ogg",
                ]
                self.victory = "\\king\\king_victory.ogg"
            else:
                self.music_list = [
                    "\\victoria\\victoria_theme01.ogg",
                    "\\victoria\\victoria_theme02.ogg",
                    "\\victoria\\victoria_theme03.ogg",
                    "\\victoria\\victoria_theme04.ogg",
                ]
                self.victory = "\\victoria\\victoria_victory.ogg"

            # FOR HERO 2 #
            if self.hero2 == "Billy":
                self.music_list2 = [
                    "\\billy\\billy_theme01.ogg",
                    "\\billy\\billy_theme02.ogg",
                    "\\billy\\billy_theme03.ogg",
                    "\\billy\\billy_theme04.ogg",
                ]
                self.victory2 = "\\billy\\billy_victory.ogg"
            elif self.hero2 == "King":
                self.music_list2 = [
                    "\\king\\king_theme01.ogg",
                    "\\king\\king_theme02.ogg",
                    "\\king\\king_theme03.ogg",
                    "\\king\\king_theme04.ogg",
                ]
                self.victory2 = "\\king\\king_victory.ogg"
            else:
                self.music_list2 = [
                    "\\victoria\\victoria_theme01.ogg",
                    "\\victoria\\victoria_theme02.ogg",
                    "\\victoria\\victoria_theme03.ogg",
                    "\\victoria\\victoria_theme04.ogg",
                ]
                self.victory2 = "\\victoria\\victoria_victory.ogg"
        else:
            if self.hero == "Billy":
                self.music_list = [
                    "\\billy\\billy_theme01.ogg",
                    "\\billy\\billy_theme02.ogg",
                    "\\billy\\billy_theme03.ogg",
                    "\\billy\\billy_theme04.ogg",
                ]
                self.victory = "\\billy\\billy_victory.ogg"
            elif self.hero == "King":
                self.music_list = [
                    "\\king\\king_theme01.ogg",
                    "\\king\\king_theme02.ogg",
                    "\\king\\king_theme03.ogg",
                    "\\king\\king_theme04.ogg",
                ]
                self.victory = "\\king\\king_victory.ogg"
            else:
                self.music_list = [
                    "\\victoria\\victoria_theme01.ogg",
                    "\\victoria\\victoria_theme02.ogg",
                    "\\victoria\\victoria_theme03.ogg",
                    "\\victoria\\victoria_theme04.ogg",
                ]
                self.victory = "\\victoria\\victoria_victory.ogg"

    def swap(self):  # change track after track has ended already
        pass

    def stop(self):
        pygame.mixer.music.stop()
        pass

    def prep_song(self):
        if not self.is_mirror:
            if not self.to_play_hero2:
                index = random.randrange(0, 4)
                while index == self.last_played_index:
                    index = random.randrange(0, 4)

                pygame.mixer.music.load("assets\\music\\heroes\\" + self.music_list[index])
                pygame.mixer.music.set_volume(Globals.music_volume)
                # pygame.mixer.music.play()
                self.to_play_hero2 = True

            elif self.to_play_hero2:
                index = random.randrange(0, 4)
                while index == self.last_played_index2:
                    index = random.randrange(0, 4)
                pygame.mixer.music.load("assets\\music\\heroes\\" + self.music_list2[index])
                pygame.mixer.music.set_volume(Globals.music_volume)
                # pygame.mixer.music.play()
                self.to_play_hero2 = False

    def prep_song_hero(self, hero):
        print("stop music")

        # if not self.last_hero == hero:
        #     if hero == self.hero:
        #         index = random.randrange(0, 4)
        #         while index == self.last_played_index:
        #             index = random.randrange(0, 4)
        #         self.mc2.load("assets\\music\\heroes\\" + self.music_list[index])
        #         self.mc2.set_volume(Globals.music_volume)
        #         self.last_hero = hero
        #
        #         self.to_play_hero2 = False
        #     elif hero == self.hero2:
        #         index = random.randrange(0, 4)
        #         while index == self.last_played_index2:
        #             index = random.randrange(0, 4)
        #         self.mc.load("assets\\music\\heroes\\" + self.music_list2[index])
        #         self.mc.set_volume(Globals.music_volume)
        #         self.last_hero = hero
        #
        #         self.to_play_hero2 = True
        # else:
        #     index = random.randrange(0, 4)
        #     while index == self.last_played_index:
        #         index = random.randrange(0, 4)
        #     self.mc2.load("assets\\music\\heroes\\" + self.music_list[index])
        #     self.mc2.set_volume(Globals.music_volume)
        #     self.last_hero = hero

        if hero == self.hero:
            index = random.randrange(0, 4)
            while index == self.last_played_index:
                index = random.randrange(0, 4)
            self.mc.load("assets\\music\\heroes\\" + self.music_list[index])
            self.last_played_index = index
            self.mc.set_volume(Globals.music_volume)
            self.last_hero = hero

        elif hero == self.hero2:
            index = random.randrange(0, 4)
            while index == self.last_played_index2:
                index = random.randrange(0, 4)
            self.mc.load("assets\\music\\heroes\\" + self.music_list2[index])
            self.last_played_index2 = index
            self.mc.set_volume(Globals.music_volume)
            self.last_hero = hero

    def play(self):
        self.mc.play()

    def prep_victory(self, hero):
        if hero == "Billy":
            self.victory = "\\billy\\billy_victory.ogg"
        elif hero == "King":

            self.victory = "\\king\\king_victory.ogg"
        else:
            self.victory = "\\victoria\\victoria_victory.ogg"
        self.mc.load("assets\\music\\heroes" + self.victory)


class Phase(Enum):
    # auto() is an enum function that makes it decide what type to use for that enum
    COIN_TOSS = auto()  # flipping of coin, decides player1 and 2
    OPENING = auto()  # 10 cards drawn

    SWAP = auto()  # Screen fades out, board flips
    PREP = auto()  # Player about to start turn
    PLAY = auto()  # Player controls are enabled, can click around etc.

    # currently not yet used
    END_ROUND = auto()  # both players have now selected PASS

    # NOTE: we might need intermediary phases here. To give space for proper animation maybe?

    # tracks how round ended #
    ROUND_DRAW = auto()  # Three cards drawn
    ROUND_TWO = auto()  # Two cards drawn
    FINAL_ROUND = auto()  # One card drawn
    MATCH_COMPLETE = auto()

