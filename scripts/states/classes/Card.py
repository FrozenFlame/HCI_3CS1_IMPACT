import pygame, math
from enum import Enum, auto
from .FontObj import FontObj

class Card(object):
    def __init__(self, name="Generic", base_val = 0, effect=None, type=None, heroOwner="Generic"):

        if type is None:
            self.type = []
        else:
            self.type = type

        # Game related
        self.name = name
        self.base_val = base_val
        self.current_val = base_val  # this is what is processed
        self.effect = None           # this is the buff/debuff/constant this particular card applies
        self.buffs = []
        self.debuffs = []
        self.constants = []
        self.effect = effect
        self.effectActivated = False

        self.owner = heroOwner      #owner of the card

        self.fontDictionary = {"King": 'POORICH.TTF',
                          "Billy": 'POORICH.TTF',
                          "Victoria": 'big_noodle_titling_oblique.ttf',
                          "Generic": 'OLDENGL.TTF'}
        fontChoice = self.fontDictionary[self.owner]

        self.name_surf = FontObj.surface_factory(str(self.name), fontChoice, 34, (0, 0, 0))
        self.currval_surf = FontObj.surface_factory(str(self.current_val), fontChoice, 50, (0, 0, 0))
        self.baseval_surf = FontObj.surface_factory(str(self.base_val), fontChoice, 25, (0, 0, 0))
        # self.name_surf = FontObj.surface_factory(name, "assets\\fonts\\GARABD.TTF", 14, (0, 0, 0))

        self.frontImg = pygame.image.load("assets\\cards\\democard.png").convert_alpha()
        self.frontImg.blit(self.name_surf, (self.frontImg.get_rect().size[0] *0.05, self.frontImg.get_rect().size[1] *0.82))
        self.frontImg.blit(self.currval_surf, (self.frontImg.get_rect().size[0] *0.76,self.frontImg.get_rect().size[1] *0.52))
        self.frontImg.blit(self.baseval_surf, (self.frontImg.get_rect().size[0] *0.86,self.frontImg.get_rect().size[1] *0.74))

        self.backImg = pygame.image.load("assets\\cards\\democardBack.png").convert_alpha()  # Card backs for opposing cards and for cards in deck.
        self.img = pygame.transform.smoothscale(self.backImg, (round(self.frontImg.get_rect().size[0] *0.33), round(self.frontImg.get_rect().size[1] *0.33))) # self.img is the CURRENT image to be drawn on the screen
        self.width = self.img.get_rect().size[0]  # img's initial width
        self.height = self.img.get_rect().size[1]  # img's initial height

        self.posX = 1181  # offset by 1 from deckImgHolder3 because the card latches to the mouse cursor if its equal (deckImgHolder3 = 1180,563)
        self.posY = 563

        self.defaultPos = (65, 500)

        self.flipX = self.width

        self.speed = 10  # movespeed on the screen




        # pygame.font.init()
        # fontDictionary = {"King Of Beggars": 'POORICH.TTF',
        #           "Uncle Billy": 'POORICH.TTF',
        #           "Victoria": 'big_noodle_titling.ttf'}
        # fontChoice = fontDictionary[self.owner]
        # font = pygame.font.Font('assets/fonts/' + fontChoice, 8)
        #
        # self.textBaseVal = font.render(self.base_val, False, (0,0,0))
        # self.textCurrVal = font.render(self.current_val, False, (0,0,0))
        # self.textName = font.render(self.name, False, (0,0,0))

        #
        #  ____              _
        # |  _ \            | |
        # | |_) | ___   ___ | | ___  __ _ _ __  ___
        # |  _ < / _ \ / _ \| |/ _ \/ _` | '_ \/ __|
        # | |_) | (_) | (_) | |  __/ (_| | | | \__ \
        # |____/ \___/ \___/|_|\___|\__,_|_| |_|___/
        #

        self.onBoard = False
        self.disabled = False
        self.onTop = False
        self.mayBePreviewed = False  # makes it so only cards you are allowed to see get a preview.
        self.flipAnimating = False
        self.flipped = False
        self.front = False
        self.back = True  # the card is face down initially. is this wrong?
        self.blitted = False
        self.isHeld = False
        self.resting = True  # unused for now

        # animated positioning junk
        self.destination = None  # is a Tuple x,y
        self.distance = 0.0
        self.vector = None
        self.flipDisplace = 0



    # rename method soon
    # def decider(self):
    #     if not self.resting:
    #         pass




    # change of position on screen (calculation)
    def update(self, dTime, mouseX, mouseY):
        if self.destination:
            if self.isHeld == True:
                self.posX = mouseX - self.width * 0.75
                self.posY = mouseY - self.height * 0.75
            # animating but not held card
            elif self.isHeld == False and self.resting == False:
                self.set_destination(self.defaultPos[0], self.defaultPos[1])
                travelled = math.hypot(self.vector[0] * dTime, self.vector[1] * dTime)
                self.distance -= travelled
                if self.distance <= 0:  # destination reached
                    self.posX = self.defaultPos[0]  # * dTime
                    self.posY = self.defaultPos[1]  # * dTime
                    self.resting = True
                    self.destination = None
                else:  #this is for returning the card to your hand with animation
                    self.posX += self.vector[0] * dTime
                    self.posY += self.vector[1] * dTime
        else:
            self.posX = mouseX
            self.posY = mouseY

    # setting of destination, or the relative vector to location
    def set_destination(self, x, y):
        xDistance = x - self.posX
        yDistance = y - self.posY
        self.distance = math.hypot(xDistance, yDistance)  # distance from default position
        try:
            self.vector = (self.speed + (self.distance * 10)) * xDistance / self.distance, (
                    self.speed + (self.distance * 10)) * yDistance / self.distance
            self.destination = list((x, y))
        except ZeroDivisionError:
            pass
        '''
        Distance: 100 (random angle)
        posX 100 defX 0 posY 200 defY 0
        '''

    def draw(self, screen):
        screen.blit(self.img, (self.posX, self.posY))
        self.blitted = True

    # return boolean if card instance is moused over once function is called
    def collidepoint(self, x, y):
        collide = False
        if (self.posX + self.width) >= x >= self.posX and (self.posY + self.height) >= y >= self.posY:
            collide = True
        return collide

    def collide_rect(self, x1, y1, x2, y2):
        boardCollide = False
        # x1rect = x1 + ((x2 - x1) * 0.40)
        # y1rect = y1 + ((y2 - y1) * 0.40)
        # x2rect = x1rect + 15
        # y2rect = y1rect + 15
        boardRect = pygame.Rect(x1, y1, (x2 - x1), (y2 - y1))
        tempRect = pygame.Rect(self.posX, self.posY, self.width, self.height)

        boardCollide = pygame.Rect.colliderect(tempRect, boardRect)

        return boardCollide

    def flip(self):  # flip initiator
        self.flipAnimating = True
        # self.flipAnimation()

    def flipAnim(self, waitTick):  # flip animation to be called per tick.
        waitTime = 10
        if self.flipX > 0 and not self.flipped:  # shrinking animation
            # print("Engine.py - "); print(a.flipX)
            currentTick = pygame.time.get_ticks()
            if currentTick - waitTick >= waitTime:
                # print("flipAnimating")
                waitTick = currentTick
                self.img = pygame.transform.smoothscale(self.img, (self.flipX, self.height))
                self.flipDisplace = (self.width - self.img.get_rect().size[0])
                # self.posX = self.defaultPos[0] + self.flipDisplace/2 # currently using defaultPos[0] would cause a jump in the animation to occur
                # print("[Card.py] - width[{0}] - img_rect [{1}] = flipDisplace[{2}] ".format(self.width, self.img.get_rect().size[0], self.flipDisplace))
                # print("[Card.py] - SHRINK posX: {0}: ".format(self.posX))
                # print("[Card.py] - flipX: {0}".format(self.flipX))
                # print("[Card.py] - img.get_rect().size {0}".format(self.img.get_rect().size[0] / 2))

                self.flipX -= 20
        ################################################################################
        elif self.flipX <= 0 and not self.flipped:  # time to flip trigger + changing of image
            self.flipX += 20
            if self.front:
                # print("front to back")
                self.img = pygame.transform.smoothscale(pygame.transform.smoothscale(self.backImg, (round(self.frontImg.get_rect().size[0] *0.33), round(self.frontImg.get_rect().size[1] *0.33))), (self.flipX, self.height))
                self.flipped = True
                self.back = True
                self.front = False
            elif self.back:  # growing animation to face up
                # print("back to front")
                self.img = pygame.transform.smoothscale(pygame.transform.smoothscale(self.frontImg, (round(self.frontImg.get_rect().size[0] *0.33), round(self.frontImg.get_rect().size[1] *0.33))), (self.flipX, self.height))
                self.flipped = True
                self.back = False
                self.front = True
        ################################################################################
        elif self.flipX <= 74 and self.flipped:  # growing animation
            # print("[Card.py] - GROW posX: {0}: ".format(self.posX))
            # print("[Card.py] - width[{0}] - img_rect [{1}] = flipDisplace[{2}] ".format(self.width,
            #                                                                             self.img.get_rect().size[0],
            #                                                                             self.flipDisplace))
            # print(a.flipX)
            currentTick = pygame.time.get_ticks()
            if currentTick - waitTick >= waitTime:
                # print("flipAnimating")
                waitTick = currentTick
                self.img = pygame.transform.smoothscale(self.img, (self.flipX, self.height))
                self.flipDisplace = (self.width - self.img.get_rect().size[0])
                # self.posX = self.defaultPos[0] + self.flipDisplace/2 # currently using defaultPos[0] would cause a jump in the animation to occur
                self.flipX += 20
        ################################################################################
        elif self.flipX >= 75 and self.flipped:  # animation completed, new image face set
            if self.front:
                self.img = pygame.transform.smoothscale(self.frontImg, (round(self.frontImg.get_rect().size[0] *0.33), round(self.frontImg.get_rect().size[1] *0.33)))
            if self.back:
                self.img = pygame.transform.smoothscale(self.backImg, (round(self.frontImg.get_rect().size[0] *0.33), round(self.frontImg.get_rect().size[1] *0.33)))
            self.flipped = False
            self.flipAnimating = False
            # self.posX = self.defaultPos[0] # apparently negligible if your calculations are correct
            self.flipX = 74  # restoring flipX back to original value

    def set_owner(self, new_owner):  # new_owner is type Player
        self.owner = new_owner

    def rfrsh_heightwidth(self):  # refreshes width and height values
        self.width = self.img.get_rect().size[0]  # img's initial width
        self.height = self.img.get_rect().size[1]  # img's initial height

    def swap(self):
        # def __init__(self, x1=0, y1=0, x2=0, y2=0, owner="Nobody"):
        # self.boardFieldOpp2 = BoardField(225, 105, 1010, 185)  # opponent back row
        # self.boardFieldOpp = BoardField(225, 240, 1010, 320)  # opponent front row
        # self.boardField = BoardField(225, 390, 1010, 470)  # player front row
        # self.boardField2 = BoardField(225, 525, 1010, 605)  # player back row
        if self.defaultPos[1] == -30:
            self.defaultPos = self.defaultPos[0], 610
        elif self.defaultPos[1] == 610:
            self.defaultPos = self.defaultPos[0], -30

        self.resting = False
        self.set_destination(self.defaultPos[0],self.defaultPos[1])

    # def addTexts(self, hero):
    #     fontChoice = self.fontDictionary[hero]
    #     self.textCurrVal = FontObj.factory(str(self.current_val), self.defaultPos[0]+(self.width*0.82), self.defaultPos[1]+(self.height*0.4), fontChoice, 14, (0, 0, 0))
    #     self.textBaseVal = FontObj.factory(str(self.base_val), self.defaultPos[0]+(self.width*0.82), self.defaultPos[1]+(self.height*0.72), fontChoice, 11, (0, 0, 0))
    #     self.textName = FontObj.factory(self.name, self.defaultPos[0]+(self.width*0.5), self.defaultPos[1]+(self.height*0.88), fontChoice, 12, (0, 0, 0))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  _____               _  ______                _   _
# /  __ \             | | |  ___|              | | (_)
# | /  \/ __ _ _ __ __| | | |_ _   _ _ __   ___| |_ _  ___  _ __  ___
# | |    / _` | '__/ _` | |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | \__/\ (_| | | | (_| | | | | |_| | | | | (__| |_| | (_) | | | \__ \
#  \____/\__,_|_|  \__,_| \_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # note: rearrange order at some point
    # unused functions for now
    def receive_buff(self, buff):
        self.buffs.append(buff)
    def remove_all_buffs(self):
        self.buffs = []
    def receive_debuff(self, debuff):
        self.debuffs.append(debuff)

    def recalculate(self):
        # consider computation order
        # affect and renew current_val
        pass

    def apply_buff(self, target):
        target.receive_buff(self.effect)
'''
    def createKingOfBeggarsCollection(self, deckCardList, allCardList):
        buffFactory = BuffFactory()
        #blackMarketEffect = buffFactory.factory(buffFactory.Kind.CONSTANT,buffFactory.Operation.ADD, "COUNT OBJECTS PLAYED IN YOUR FIELD")

        blackMarket = Card("Black Market", 15, None, [Type.STRUCTURE, Type.BLACK])
        #blackMarket.receive_buff(blackMarketEffect)

        pickPocket = Card("Pick Pocket", 2, None, [Type.PERSON, Type.BLACK])
        strangeGravedigger = Card("Strange Gravedigger", 5, None, [Type.PERSON, Type.BLACK])
        robinHood = Card("Robin Hood", 10, None, [Type.PERSON, Type.BLACK])
        slums = Card("Slums", 0, None, [Type.STRUCTURE])
        kingpin = Card("Kingpin", 10, None, [Type.PERSON, Type.BLACK])
        bodyDouble = Card("Body Double", 15, None, [Type.PERSON])
        junker = Card("Junker", 7, None, [Type.VEHICLE])
        beg = Card("Beg", 0, None, [Type.SPELL])
        scam = Card("Scam", 0, None, [Type.SPELL, Type.BLACK])

        blackMarket2 = Card("Black Market", 15, None, [Type.STRUCTURE, Type.BLACK])
        pickPocket2 = Card("Pick Pocket", 2, None, [Type.PERSON, Type.BLACK])
        strangeGravedigger2 = Card("Strange Gravedigger", 5, None, [Type.PERSON, Type.BLACK])
        robinHood2 = Card("Robin Hood", 10, None, [Type.PERSON, Type.BLACK])
        slums2 = Card("Slums", 0, None, [Type.STRUCTURE])
        kingpin2 = Card("Kingpin", 10, None, [Type.PERSON, Type.BLACK])
        bodyDouble2 = Card("Body Double", 15, None, [Type.PERSON])
        junker2 = Card("Junker", 7, None, [Type.VEHICLE])
        beg2 = Card("Beg", 0, None, [Type.SPELL])
        scam2 = Card("Scam", 0, None, [Type.SPELL, Type.BLACK])

        deckCardList.extend([blackMarket, pickPocket, strangeGravedigger, robinHood, slums, kingpin, bodyDouble, junker, beg, scam])
        deckCardList.extend([blackMarket2, pickPocket2, strangeGravedigger2, robinHood2, slums2, kingpin2, bodyDouble2, junker2, beg2, scam2])
        allCardList.extend([blackMarket, pickPocket, strangeGravedigger, robinHood, slums, kingpin, bodyDouble, junker, beg, scam])
        allCardList.extend([blackMarket2, pickPocket2, strangeGravedigger2, robinHood2, slums2, kingpin2, bodyDouble2, junker2, beg2, scam2])


    def createUncleBillyCollection(self, deckCardList, allCardList):
        buffFactory = BuffFactory()

        slaughterHouse = Card("Slaughter House", 0, None, [Type.STRUCTURE])
        cropDuster = Card("Crop Duster", 10, None, [Type.VEHICLE])
        farm = Card("Farm", 15, None, [Type.STRUCTURE])
        farmBoy = Card("Farm Boy", 5, None, [Type.PERSON])
        barn = Card("Barn", 0, None, [Type.STRUCTURE])
        cow = Card("Cow", 7, None, [Type.ANIMAL])
        chicken = Card("Chicken", 5, None, [Type.ANIMAL])
        farmDog = Card("Farm Dog", 3, None, [Type.ANIMAL])
        reap = Card("Reap", 0, None, [Type.SPELL])
        drought = Card("Drought", 0, None, [Type.SPELL])
        waterPurifier = Card("Water Purifier", 5, None, [Type.OBJECT])

        slaughterHouse2 = Card("Slaughter House", 0, None, [Type.STRUCTURE])
        cropDuster2 = Card("Crop Duster", 10, None, [Type.VEHICLE])
        farm2 = Card("Farm", 15, None, [Type.STRUCTURE])
        farmBoy2 = Card("Farm Boy", 5, None, [Type.PERSON])
        barn2 = Card("Barn", 0, None, [Type.STRUCTURE])
        cow2 = Card("Cow", 7, None, [Type.ANIMAL])
        chicken2 = Card("Chicken", 5, None, [Type.ANIMAL])
        farmDog2 = Card("Farm Dog", 3, None, [Type.ANIMAL])
        reap2 = Card("Reap", 0, None, [Type.SPELL])
        drought2 = Card("Drought", 0, None, [Type.SPELL])
        waterPurifier2 = Card("Water Purifier", 5, None, [Type.OBJECT])

        deckCardList.extend([slaughterHouse, cropDuster, farm, farmBoy, barn, cow, chicken, farmDog, reap, drought, waterPurifier])
        deckCardList.extend([slaughterHouse2, cropDuster2, farm2, farmBoy2, barn2, cow2, chicken2, farmDog2, reap2, drought2, waterPurifier2])
        allCardList.extend([slaughterHouse, cropDuster, farm, farmBoy, barn, cow, chicken, farmDog, reap, drought, waterPurifier])
        allCardList.extend([slaughterHouse2, cropDuster2, farm2, farmBoy2, barn2, cow2, chicken2, farmDog2, reap2, drought2, waterPurifier2])


    def createVictoriaCollection(self, deckCardList, allCardList):
        buffFactory = BuffFactory()

        insurance = Card("Insurance", 0, None, [Type.OBJECT])
        shareHolder = Card("Share Holder", 10, None, [Type.PERSON])
        superstar = Card("Superstar", 15, None, [Type.PERSON])
        hacker = Card("Hacker", 15, None, [Type.PERSON, Type.BLACK])
        university = Card("University", 15, None, [Type.STRUCTURE])
        skyscraper = Card("Skyscraper", 3, None, [Type.STRUCTURE])
        supplyTruck = Card("Supply Truck", 8, None, [Type.VEHICLE])
        riotResponseVehicle = Card("Riot Response Vehicle", 10, None, [Type.VEHICLE])
        innovate = Card("Innovate", 0, None, [Type.SPELL])
        solidWorkforce = Card("Solid Workforce", 0, None, [Type.SPELL])

        insurance2 = Card("Insurance", 0, None, [Type.OBJECT])
        shareHolder2 = Card("Share Holder", 10, None, [Type.PERSON])
        superstar2 = Card("Superstar", 15, None, [Type.PERSON])
        hacker2 = Card("Hacker", 15, None, [Type.PERSON, Type.BLACK])
        university2 = Card("University", 15, None, [Type.STRUCTURE])
        skyscraper2 = Card("Skyscraper", 3, None, [Type.STRUCTURE])
        supplyTruck2 = Card("Supply Truck", 8, None, [Type.VEHICLE])
        riotResponseVehicle2 = Card("Riot Response Vehicle", 10, None, [Type.VEHICLE])
        innovate2 = Card("Innovate", 0, None, [Type.SPELL])
        solidWorkforce2 = Card("Solid Workforce", 0, None, [Type.SPELL])

        deckCardList.extend([insurance, shareHolder, superstar, hacker, university, skyscraper, supplyTruck, riotResponseVehicle, innovate, solidWorkforce])
        deckCardList.extend([insurance2, shareHolder2, superstar2, hacker2, university2, skyscraper2, supplyTruck2, riotResponseVehicle2, innovate2, solidWorkforce2])
        allCardList.extend([insurance, shareHolder, superstar, hacker, university, skyscraper, supplyTruck, riotResponseVehicle, innovate, solidWorkforce])
        allCardList.extend([insurance2, shareHolder2, superstar2, hacker2, university2, skyscraper2, supplyTruck2, riotResponseVehicle2, innovate2, solidWorkforce2])

    def createCommonCollection(self, deckCardList, allCardList):
        bagOfCash = Card("Bag of Cash", 10, None, [Type.OBJECT])
        bigBagOfCash = Card("Big Bag of Cash", 20, None, [Type.OBJECT])
        deed = Card("Deed", 25, None, [Type.OBJECT])
        dollaDollaBills = Card("Dolla Dolla Bills", 7, None, [Type.OBJECT])
        mansion = Card("Mansion", 30, None, [Type.STRUCTURE])
        student = Card("Student", 5, None, [Type.PERSON])
        car = Card("Car", 15, None, [Type.VEHICLE])

        bagOfCash2 = Card("Bag of Cash", 10, None, [Type.OBJECT])
        bigBagOfCash2 = Card("Big Bag of Cash", 20, None, [Type.OBJECT])
        deed2 = Card("Deed", 25, None, [Type.OBJECT])
        dollaDollaBills2 = Card("Dolla Dolla Bills", 7, None, [Type.OBJECT])
        mansion2 = Card("Mansion", 30, None, [Type.STRUCTURE])
        student2 = Card("Student", 5, None, [Type.PERSON])
        car2 = Card("Car", 15, None, [Type.VEHICLE])

        deckCardList.extend([bagOfCash, bigBagOfCash, deed, dollaDollaBills, mansion, student, car])
        deckCardList.extend([bagOfCash2, bigBagOfCash2, deed2, dollaDollaBills2, mansion2, student2, car2])
        allCardList.extend([bagOfCash, bigBagOfCash, deed, dollaDollaBills, mansion, student, car])
        allCardList.extend([bagOfCash2, bigBagOfCash2, deed2, dollaDollaBills2, mansion2, student2, car2])

        #### COMMON WITH EFFECTS ###

        butler = Card("Butler", 10, None, [Type.PERSON])
        maid = Card("Maid", 5, None, [Type.PERSON])
        policeOfficer = Card("Police Officer", 15, None, [Type.PERSON])
        gangsters = Card("Gangsters", 3, None, [Type.PERSON, Type.BLACK])
        arsonist = Card("Arsonist", 0, None, [Type.PERSON, Type.BLACK])
        lemonadeStand = Card("Lemonade Stand", 5, None, [Type.STRUCTURE])
        parkingLot = Card("Parking Lot", 5, None, [Type.STRUCTURE])
        impoundLot = Card("Impound Lot", 5, None, [Type.STRUCTURE])
        junkyard = Card("Junkyard", 5, None, [Type.STRUCTURE])
        loanSlip = Card("Loan Slip", 0, None, [Type.SPELL])
        creditCard = Card("Credit Card", 0, None, [Type.SPELL])
        resurrect = Card("Resurrect", 0, None, [Type.SPELL])
        rebuild = Card("Rebuild", 0, None, [Type.SPELL])
        saboteur = Card("Saboteur", 0, None, [Type.SPELL])

        deckCardList.extend([butler, maid, policeOfficer, gangsters, arsonist, lemonadeStand, parkingLot, impoundLot, junkyard, loanSlip, creditCard, resurrect, rebuild, saboteur])
        allCardList.extend([butler, maid, policeOfficer, gangsters, arsonist, lemonadeStand, parkingLot, impoundLot, junkyard, loanSlip, creditCard, resurrect, rebuild, saboteur])
'''
class Type(Enum):
    SPELL = auto()
    BLACK = auto()
    STRUCTURE = auto()
    PERSON = auto()
    OBJECT = auto()
    VEHICLE = auto()
    ANIMAL = auto()