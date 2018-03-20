import pygame, math
from enum import Enum, auto
from .FontObj import FontObj

class Card(object):
    def __init__(self, id="", name="Generic", base_val = 0, effect="", type=None, heroOwner="Generic", card_art_path= "assets\\cards\\card_art\\chicken.png"):

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
        self.id = id

        self.owner = heroOwner      #owner of the card

        self.typeDictionary = {Type.SPELL: "SPELL",
                                Type.BLACK: "BLACK",
                                Type.STRUCTURE: "STRUCTURE",
                                Type.PERSON: "PERSON",
                                Type.OBJECT: "OBJECT",
                                Type.VEHICLE: "VEHICLE",
                                Type.ANIMAL: "ANIMAL"}

        self.typeText = "["
        for type in self.type:
            if self.type.index(type) != 0:
                self.typeText += ", "
            self.typeText += self.typeDictionary[type]
        self.typeText += "]"

        self.fontDictionary = {"King": 'POORICH.TTF',
                          "Billy": 'GARA.TTF',
                          "Victoria": 'big_noodle_titling_oblique.ttf',
                          "Generic": 'OLDENGL.TTF'}

        self.fontSizeDictionary = {"King": 17,
                               "Billy": 18,
                               "Victoria": 20,
                               "Generic": 20}
        self.fontChoice = self.fontDictionary[self.owner]
        self.fontSizeChoice = self.fontSizeDictionary[self.owner]

        self.card_art = pygame.image.load(card_art_path).convert_alpha()
        self.name_surf = FontObj.surface_factory(str(self.name), self.fontChoice, 30, (0, 0, 0))
        self.currval_surf = FontObj.surface_factory(str(self.current_val), self.fontChoice, 40, (0, 0, 0))
        self.typeText_surf = FontObj.surface_factory(self.typeText,self.fontChoice, self.fontSizeChoice, (0, 0, 0))
        # self.baseval_surf = FontObj.surface_factory(str(self.base_val), fontChoice, 25, (0, 0, 0))

        self.frontImg = pygame.image.load("assets\\cards\\cardDemoWithFrame.png").convert_alpha()
        self.frontImg.blit(self.name_surf, (self.frontImg.get_rect().size[0] *0.08, self.frontImg.get_rect().size[1] *0.82))
        self.frontImg.blit(self.currval_surf, (self.frontImg.get_rect().size[0] *0.745,self.frontImg.get_rect().size[1] *0.535))
        self.frontImg.blit(self.typeText_surf, (self.frontImg.get_rect().size[0] *0.08,self.frontImg.get_rect().size[1] *0.55))
        self.frontImg.blit(self.card_art, (self.frontImg.get_rect().size[0] * 0.085, self.frontImg.get_rect().size[1] * 0.04))

        # self.frontImg.blit(self.effect_surf, (self.frontImg.get_rect().size[0] * 0.05, self.frontImg.get_rect().size[1] * 0.60))
        self.blit_text(self.frontImg, self.effect, (self.frontImg.get_rect().size[0] * 0.08, self.frontImg.get_rect().size[1] * 0.645), pygame.font.Font('assets/fonts/' + self.fontChoice, self.fontSizeChoice))

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

        # scale factors
        self.is_scaling = False
        self.new_width = 0
        self.new_height = 0
        self.scalespeed = 10  # more of a tick delay
        self.scalexfactor = 4
        self.scalexstack = 0  # a separate tracker
        self.scaleyfactor = 5
        self.scaleystack = 0


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

    def scale_to(self, newxy):
        self.is_scaling = True
        self.new_width = newxy[0]
        self.new_height = newxy[1]

    def scaleanim(self, waitTick):
        currentTick = pygame.time.get_ticks()
        if currentTick - waitTick >= self.scalespeed:
            waitTick = currentTick
            if self.is_scaling:
                # print("Scaling like a dog")
                # self.surface = pygame.transform.smoothscale(self.surface, (round(50), round(50))).convert_alpha()
                if self.surface.get_rect().size[0] > self.new_width or self.surface.get_rect().size[1] > self.new_height:  # shrinking block
                    self.scalexstack = (self.scalexstack + self.scalexfactor) if self.surface.get_rect().size[0] > self.new_width else 0
                    self.scaleystack = (self.scaleystack + self.scaleyfactor) if self.surface.get_rect().size[1] > self.new_height else 0
                    self.surface = pygame.transform.smoothscale(self.original_surface, (self.original_surface.get_rect().size[0] - self.scalexstack, self.original_surface.get_rect().size[1] - self.scaleystack)).convert_alpha()
                else:
                    self.is_scaling = False

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

    def blit_text(self, surface, text, pos, font, color=(0, 0, 0)):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        max_width -= 6
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 14, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width * 0.95:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

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
        pass

    def rebuildFront(self):
        color = (0, 0, 0) #black
        if self.current_val > self.base_val:
            color = (0, 128, 0) #green
        elif self.current_val < self.base_val:
            color = (255, 0, 0) #red
        newFrontImg = pygame.image.load("assets\\cards\\cardDemoWithFrame.png").convert_alpha()
        newFrontImg.blit(self.name_surf, (self.frontImg.get_rect().size[0] *0.08, self.frontImg.get_rect().size[1] *0.82))
        self.currval_surf = FontObj.surface_factory(str(self.current_val), self.fontChoice, 40, color)
        newFrontImg.blit(self.currval_surf, (self.frontImg.get_rect().size[0] * 0.75, self.frontImg.get_rect().size[1] * 0.535))
        newFrontImg.blit(self.typeText_surf, (self.frontImg.get_rect().size[0] *0.08,self.frontImg.get_rect().size[1] *0.55))
        newFrontImg.blit(self.card_art, (self.frontImg.get_rect().size[0] * 0.085, self.frontImg.get_rect().size[1] * 0.04))
        self.blit_text(newFrontImg, self.effect, (self.frontImg.get_rect().size[0] * 0.05, self.frontImg.get_rect().size[1] * 0.575), pygame.font.Font('assets/fonts/' + self.fontChoice, self.fontSizeChoice))

        self.frontImg = newFrontImg
    def apply_buff(self, target):
        target.receive_buff(self.effect)

class Type(Enum):
    SPELL = auto()
    BLACK = auto()
    STRUCTURE = auto()
    PERSON = auto()
    OBJECT = auto()
    VEHICLE = auto()
    ANIMAL = auto()