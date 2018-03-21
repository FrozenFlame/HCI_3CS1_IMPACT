from .Card import Card, Type

class DeckBuilder(object):

    def build_deck(hero_name):
        return {
            'King': DeckCatalogue.get_deck_king(hero_name),
            'Victoria': DeckCatalogue.get_deck_victoria(hero_name),
            'Billy': DeckCatalogue.get_deck_billy(hero_name)
        }.get(hero_name, DeckCatalogue.get_deck_generic(hero_name))  # generic is default if hero_name not found

    build_deck = staticmethod(build_deck)




class DeckCatalogue(object):

    def get_deck_generic(hero_name):  # TEMPORARILY FILLED WITH STATIC DATA
        # common pool 28, unique pool ~20
        deck = [Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5),  # common 28
                Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5),  #

                Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), # unique 20
                Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5), Card(hero_name, 5)] #
        return deck
    get_deck_generic = staticmethod(get_deck_generic)

    def get_deck_tutorial(hero_name):
        reap = Card("reap", "Reap", 0, "Gain all the values of your 'Farm' cards on board, then send them to graveyard", [Type.SPELL], hero_name, "assets\\cards\\card_art\\billy\\reap.png")
        farm = Card("farm", "Farm", 15, "", [Type.STRUCTURE], hero_name)
        farmBoy = Card("farmboy", "Farm Boy", 5, "+3C to 'Farm' cards, +1C to ANIMAL cards on this boardfield", [Type.PERSON], hero_name, "assets\\cards\\card_art\\billy\\farmboy.png")
        butler = Card("butler", "Butler", 10, "+5C to card left of the Butler", [Type.PERSON], hero_name,"assets\\cards\\card_art\\commons\\butler.png")
        bagOfCash = Card("bagofcash", "Bag of Cash", 10, "", [Type.OBJECT], hero_name, "assets\\cards\\card_art\\commons\\Money bag.png")
        student = Card("student", "Student", 5, "", [Type.PERSON], hero_name,"assets\\cards\\card_art\\commons\\student.png")
        car = Card("car", "Car", 15, "", [Type.VEHICLE], hero_name)
        resurrect = Card("resurrect", "Resurrect", 0, "Restore 1 PERSON card from your graveyard.", [Type.SPELL], hero_name,"assets\\cards\\card_art\\commons\\resurrect.png")
        house = Card("house", "House", 10, "", [Type.STRUCTURE], hero_name)
        saboteur = Card("saboteur", "Saboteur", 0, "Destroy 1 random opponent card", [Type.SPELL], hero_name,"assets\\cards\\card_art\\commons\\saboteur.png")

        deck = [reap, farm, farmBoy, butler, bagOfCash, student, car, resurrect, house, saboteur]
        return deck
    get_deck_tutorial = staticmethod(get_deck_tutorial)


    def get_deck_king(hero_name):

        blackMarket = Card("blackmarket", "Black Market", 15, "Give half of their base value to OBJECT cards on this boardfield", [Type.STRUCTURE, Type.CRIME], hero_name)
        pickPocket = Card("pickpocket", "Pick Pocket", 3, "Give SELF a half the current value of each PERSON card on opposite boardfield", [Type.PERSON, Type.CRIME], hero_name, "assets\\cards\\card_art\\king\\pickpocket.png")
        graveDigger = Card("gravedigger", "Gravedigger", 2, "Give SELF a half the base value of each PERSON card in both graveyards", [Type.PERSON, Type.CRIME], hero_name, "assets\\cards\\card_art\\king\\gravedigger.png")
        robinHood = Card("robinhood", "Robin Hood", 10, "Take and Give to PLAYER BANK a quarter of the current value of -cash- cards on opposite boardfield", [Type.PERSON, Type.CRIME], hero_name, "assets\\cards\\card_art\\king\\robin hood.png")
        slums = Card("slums", "Slums", 5, "", [Type.STRUCTURE], hero_name)
        kingpin = Card("kingpin", "Kingpin", 10, "+2C for every CRIME card on this boardfield", [Type.PERSON, Type.CRIME], hero_name, "assets\\cards\\card_art\\king\\kingpin.png")
        bodyDouble = Card("bodydouble", "Body Double", 0, "Give SELF the current value of a random PERSON object on both boards", [Type.PERSON], hero_name, "assets\\cards\\card_art\\king\\double.png")
        junker = Card("junker", "Junker", 7, "", [Type.VEHICLE], hero_name)
        beg = Card("beg", "Beg", 0, "Take and Give 1C to the lowest value PERSON card on your board for every PERSON card on enemy board", [Type.SPELL], hero_name, "assets\\cards\\card_art\\king\\beg.png")
        scam = Card("scam", "Scam", 0, "Take all C from one random non-CRIME PERSON card on both boards", [Type.SPELL], hero_name)

        blackMarket2 = Card("blackmarket", "Black Market", 15, "", [Type.STRUCTURE, Type.CRIME], hero_name)
        pickPocket2 = Card("pickpocket", "Pick Pocket", 3, "", [Type.PERSON, Type.CRIME], hero_name, "assets\\cards\\card_art\\king\\pickpocket.png")
        graveDigger2 = Card("gravedigger", "Gravedigger", 5, "", [Type.PERSON, Type.CRIME], hero_name, "assets\\cards\\card_art\\king\\gravedigger.png")
        robinHood2 = Card("robinhood", "Robin Hood", 10, "", [Type.PERSON, Type.CRIME], hero_name, "assets\\cards\\card_art\\king\\robin hood.png")
        slums2 = Card("slums", "Slums", 5, "", [Type.STRUCTURE], hero_name)
        kingpin2 = Card("kingpin", "Kingpin", 10, "", [Type.PERSON, Type.CRIME], hero_name, "assets\\cards\\card_art\\king\\kingpin.png")
        bodyDouble2 = Card("bodydouble", "Body Double", 0, "", [Type.PERSON], hero_name, "assets\\cards\\card_art\\king\\double.png")
        junker2 = Card("junker", "Junker", 7, "", [Type.VEHICLE], hero_name)
        beg2 = Card("beg", "Beg", 0, "Take and Give 1C to the lowest value PERSON card on your board for every PERSON card on enemy board", [Type.SPELL], hero_name, "assets\\cards\\card_art\\king\\beg.png")
        scam2 = Card("scam", "Scam", 0, "Take all C from one random non-CRIME PERSON card on both boards", [Type.SPELL], hero_name)

        deck = [blackMarket, pickPocket, strangeGravedigger, robinHood, slums, kingpin, bodyDouble, junker, beg, scam,
                blackMarket2, pickPocket2, strangeGravedigger2, robinHood2, slums2, kingpin2, bodyDouble2, junker2, beg2, scam2]
        deck.extend(DeckCatalogue.get_deck_common(hero_name))
        return deck
    get_deck_king = staticmethod(get_deck_king)

    def get_deck_victoria(hero_name):
        insurance = Card("insurance", "Insurance", -2, "Restore 1 random undervalued card to its base value", [Type.OBJECT], hero_name, "assets\\cards\\card_art\\victoria\\insurance.png")
        shareHolder = Card("shareholder", "Share Holder", 10, "-1C to SELF per STRUCTURE and +2C to each STRUCTURE card on this boardfield", [Type.PERSON], hero_name, "assets\\cards\\card_art\\victoria\\business people.png")
        superstar = Card("superstar", "Superstar", 15, "+2C per PERSON card on both boards", [Type.PERSON], hero_name, "assets\\cards\\card_art\\victoria\\superstar.png")
        hacker = Card("hacker", "Hacker", 15, "-1C to all non-SPELL cards on enemy board", [Type.PERSON, Type.CRIME], hero_name, "assets\\cards\\card_art\\victoria\\hacker.png")
        university = Card("university", "University", 15, "", [Type.STRUCTURE], hero_name)
        skyscraper = Card("skyscraper", "Skyscraper", 20, "", [Type.STRUCTURE], hero_name)
        supplyTruck = Card("supplytruck", "Supply Truck", 8, "", [Type.VEHICLE], hero_name)
        riotResponseVehicle = Card("riotresponsevehicle", "Riot Response Vehicle", 10, "", [Type.VEHICLE], hero_name)
        innovate = Card("innovate", "Innovate", 0, "Draw a card", [Type.SPELL], hero_name, "assets\\cards\\card_art\\victoria\\innovation.png")
        solidWorkforce = Card("solidworkforce", "Solid Workforce", 0, "+3C to all non-CRIME PERSON cards on your board", [Type.SPELL], hero_name)

        insurance2 = Card("insurance", "Insurance", -2, "Restore 1 random undervalued card to its base value", [Type.OBJECT], hero_name, "assets\\cards\\card_art\\victoria\\insurance.png")
        shareHolder2 = Card("shareholder", "Share Holder", 10, "-1C to SELF per STRUCTURE and +2C to each STRUCTURE card on this boardfield", [Type.PERSON], hero_name, "assets\\cards\\card_art\\victoria\\business people.png")
        superstar2 = Card("superstar", "Superstar", 15, "+2C per PERSON card on both boards", [Type.PERSON], hero_name, "assets\\cards\\card_art\\victoria\\superstar.png")
        hacker2 = Card("hacker", "Hacker", 15, "-1C to all non-SPELL cards on enemy board", [Type.PERSON, Type.CRIME], hero_name, "assets\\cards\\card_art\\victoria\\hacker.png")
        university2 = Card("university", "University", 15, "", [Type.STRUCTURE], hero_name)
        skyscraper2 = Card("skyscraper", "Skyscraper", 20, "", [Type.STRUCTURE], hero_name)
        supplyTruck2 = Card("supplytruck", "Supply Truck", 8, "", [Type.VEHICLE], hero_name)
        riotResponseVehicle2 = Card("riotresponsevehicle", "Riot Response Vehicle", 10, "", [Type.VEHICLE], hero_name)
        innovate2 = Card("innovate", "Innovate", 0, "Draw a card", [Type.SPELL], hero_name, "assets\\cards\\card_art\\victoria\\innovation.png")
        solidWorkforce2 = Card("solidworkforce", "Solid Workforce", 0, "+3C to all non-CRIME PERSON cards on your board", [Type.SPELL], hero_name)

        deck = [insurance, shareHolder, superstar, hacker, university, skyscraper, supplyTruck, riotResponseVehicle, innovate, solidWorkforce,
                insurance2, shareHolder2, superstar2, hacker2, university2, skyscraper2, supplyTruck2, riotResponseVehicle2, innovate2, solidWorkforce2]
        deck.extend(DeckCatalogue.get_deck_common(hero_name))
        return deck
    get_deck_victoria = staticmethod(get_deck_victoria)


    def get_deck_billy(hero_name):
        slaughterHouse = Card("slaughterhouse", "Slaughter House", 5, "+3C for every ANIMAL card on your board", [Type.STRUCTURE], hero_name)
        cropDuster = Card("cropduster", "Crop Duster", 10, "+7C for every 'FARM' card on your board", [Type.VEHICLE], hero_name)
        farm = Card("farm", "Farm", 15, "", [Type.STRUCTURE], hero_name)
        farmBoy = Card("farmboy", "Farm Boy", 5, "+3C to 'Farm' cards, +1C to ANIMAL cards on this boardfield", [Type.PERSON], hero_name, "assets\\cards\\card_art\\billy\\farmboy.png")
        barn = Card("barn", "Barn", 5, "+3C to ANIMAL cards on this boardfield", [Type.STRUCTURE], hero_name)
        cow = Card("cow", "Cow", 7, "", [Type.ANIMAL], hero_name, "assets\\cards\\card_art\\billy\\cow.png")
        chicken = Card("chicken", "Chicken", 5, "", [Type.ANIMAL], hero_name, "assets\\cards\\card_art\\chicken.png")
        farmDog = Card("farmdog", "Farm Dog", 3, "", [Type.ANIMAL], hero_name, "assets\\cards\\card_art\\billy\\dog.png")
        reap = Card("reap", "Reap", 0, "Gain all the values of your 'Farm' cards on board, then send them to graveyard", [Type.SPELL], hero_name, "assets\\cards\\card_art\\billy\\reap.png")
        drought = Card("drought", "Drought", 0, "-5C to 'Farm', -2C to ANIMAL and PERSON, +10C to 'Water Purifier' on your board", [Type.SPELL], hero_name, "assets\\cards\\card_art\\billy\\drought.png")
        waterPurifier = Card("waterpurifier", "Water Purifier", 5, "+1C to all ANIMAL or PERSON cards on this boardfield", [Type.OBJECT], hero_name)

        slaughterHouse2 = Card("slaughterhouse", "Slaughter House", 5, "+3C for every ANIMAL card on your board", [Type.STRUCTURE], hero_name)
        cropDuster2 = Card("cropduster", "Crop Duster", 10, "+7C for every 'FARM' card on your board", [Type.VEHICLE], hero_name)
        farm2 = Card("farm", "Farm", 15, "", [Type.STRUCTURE], hero_name)
        farmBoy2 = Card("farmboy", "Farm Boy", 5, "+3C to 'Farm' cards, +1C to ANIMAL cards on this boardfield", [Type.PERSON], hero_name, "assets\\cards\\card_art\\billy\\farmboy.png")
        barn2 = Card("barn", "Barn", 0, "+3C to ANIMAL cards on this boardfield", [Type.STRUCTURE], hero_name)
        cow2 = Card("cow", "Cow", 7, "", [Type.ANIMAL], hero_name, "assets\\cards\\card_art\\billy\\cow.png")
        chicken2 = Card("chicken", "Chicken", 5, "", [Type.ANIMAL], hero_name, "assets\\cards\\card_art\\chicken.png")
        farmDog2 = Card("farmdog", "Farm Dog", 3, "", [Type.ANIMAL], hero_name, "assets\\cards\\card_art\\billy\\dog.png")
        reap2 = Card("reap", "Reap", 0, "Gain all the values of your 'Farm' cards on board, then send them to graveyard", [Type.SPELL], hero_name, "assets\\cards\\card_art\\billy\\reap.png")
        drought2 = Card("drought", "Drought", 0, "-5C to 'Farm' cards, +2C to ANIMAL cards on your board", [Type.SPELL], hero_name, "assets\\cards\\card_art\\billy\\drought.png")
        waterPurifier2 = Card("waterpurifier", "Water Purifier", 5, "+1C to all ANIMAL or PERSON cards on your board", [Type.OBJECT], hero_name)


        deck = [slaughterHouse, cropDuster, farm, farmBoy, barn, cow, chicken, farmDog, reap, drought, waterPurifier,
                slaughterHouse2, cropDuster2, farm2, farmBoy2, barn2, cow2, chicken2, farmDog2, reap2, drought2, waterPurifier2]
        deck.extend(DeckCatalogue.get_deck_common(hero_name))
        return deck
    get_deck_billy = staticmethod(get_deck_billy)

    def get_deck_common(hero_name):
        bagOfCash = Card("bagofcash", "Bag of Cash", 10, "", [Type.OBJECT], hero_name, "assets\\cards\\card_art\\commons\\Money bag.png")
        bigBagOfCash = Card("bigbagofcash", "Big Bag of Cash", 20, "", [Type.OBJECT], hero_name, "assets\\cards\\card_art\\commons\\big money bag.png")
        deed = Card("deed", "Deed", 25, "", [Type.OBJECT], hero_name, "assets\\cards\\card_art\\commons\\deed.png")
        dollaDollaBills = Card("dolladollabills", "Dolla Dolla Bills", 7, "", [Type.OBJECT], hero_name,"assets\\cards\\card_art\\commons\\dollars.png")
        mansion = Card("mansion", "Mansion", 30, "", [Type.STRUCTURE], hero_name)
        house = Card("house", "House", 10, "", [Type.STRUCTURE], hero_name)
        student = Card("student", "Student", 5, "", [Type.PERSON], hero_name,"assets\\cards\\card_art\\commons\\student.png")
        car = Card("car", "Car", 15, "", [Type.VEHICLE], hero_name)

        bagOfCash2 = Card("bagofcash", "Bag of Cash", 10, "", [Type.OBJECT], hero_name,"assets\\cards\\card_art\\commons\\Money bag.png")
        bigBagOfCash2 = Card("bigbagofcash", "Big Bag of Cash", 20, "", [Type.OBJECT], hero_name, "assets\\cards\\card_art\\commons\\big money bag.png")
        deed2 = Card("deed", "Deed", 25, "", [Type.OBJECT], hero_name, "assets\\cards\\card_art\\commons\\deed.png")
        dollaDollaBills2 = Card("dolladollabills", "Dolla Dolla Bills", 7, "", [Type.OBJECT], hero_name,"assets\\cards\\card_art\\commons\\dollars.png")
        mansion2 = Card("mansion", "Mansion", 30, "", [Type.STRUCTURE], hero_name)
        house2 = Card("house", "House", 10, "", [Type.STRUCTURE], hero_name)
        student2 = Card("student", "Student", 5, "", [Type.PERSON], hero_name,"assets\\cards\\card_art\\commons\\student.png")
        car2 = Card("car", "Car", 15, "", [Type.VEHICLE], hero_name)

        #### COMMON WITH EFFECTS ###
        butler = Card("butler", "Butler", 10, "+5C to card left of the Butler", [Type.PERSON], hero_name,"assets\\cards\\card_art\\commons\\butler.png")
        maid = Card("maid", "Maid", 5, "+3C to your 'Mansion' cards.", [Type.PERSON], hero_name,"assets\\cards\\card_art\\commons\\maid.png")
        policeOfficer = Card("policeofficer", "Police Officer", 15, "Send one random enemy PERSON, CRIME card to graveyard", [Type.PERSON], hero_name,"assets\\cards\\card_art\\commons\\police.png")
        gangsters = Card("gangsters", "Gangsters", 5, "", [Type.PERSON, Type.CRIME], hero_name,"assets\\cards\\card_art\\commons\\gangsters.png")
        arsonist = Card("arsonist", "Arsonist", 3, "Destroy Opposing Column's STRUCTURE cards", [Type.PERSON, Type.CRIME], hero_name,"assets\\cards\\card_art\\commons\\arsonist.png")
        lemonadeStand = Card("lemonadestand", "Lemonade Stand", 5, "+3C to SELF per PERSON card on this boardfield", [Type.STRUCTURE], hero_name)
        parkingLot = Card("parkinglot", "Parking Lot", 10, "+3C to SELF per VEHICLE card on this boardfield.", [Type.STRUCTURE], hero_name)
        impoundLot = Card("impoundlot", "Impound Lot", 5, "-2C to VEHICLE cards on enemy board", [Type.STRUCTURE], hero_name)
        junkyard = Card("junkyard", "Junkyard", 5, "+2C to SELF per VEHICLE card on both graveyards.", [Type.STRUCTURE], hero_name)
        loanSlip = Card("loanslip", "Loan Slip", 0, "-15C to PLAYER BANK; Draw 2 cards", [Type.SPELL], hero_name, "assets\\cards\\card_art\\commons\\loan slip.png")
        creditCard = Card("creditcard", "Credit Card", 0, "+2C to PERSON cards and -3C to OBJECT cards on your board", [Type.SPELL], hero_name,"assets\\cards\\card_art\\commons\\credit card.png")
        resurrect = Card("resurrect", "Resurrect", 0, "Restore 1 PERSON card from your graveyard.", [Type.SPELL], hero_name,"assets\\cards\\card_art\\commons\\resurrect.png")
        rebuild = Card("rebuild", "Rebuild", 0, "Restore 1 STRUCTURE or VEHICLE from your grave.", [Type.SPELL], hero_name,"assets\\cards\\card_art\\commons\\rebuild.png")
        saboteur = Card("saboteur", "Saboteur", 0, "Destroy 1 random opponent card", [Type.SPELL], hero_name,"assets\\cards\\card_art\\commons\\saboteur.png")

        deck = [bagOfCash, bigBagOfCash, deed, dollaDollaBills, mansion, student, car, bagOfCash2, bigBagOfCash2, deed2, dollaDollaBills2, mansion2, student2, car2,
                butler, maid, policeOfficer, gangsters, arsonist, lemonadeStand, parkingLot, impoundLot, junkyard, loanSlip, creditCard, resurrect, rebuild, saboteur]
        return deck
    get_deck_common = staticmethod(get_deck_common)


    '''
    REMEMBER: "Special" cards which are made by other cards (ie. not in deck)
    [Commons Cards]
    // let's start with raw Gold val cards w/no effect
    1) Bag of Cash [10C]
        - Effect: None
    2) Deed [30C]
        - Effect: None
    3) Big Bag of Cash [20C]
        - Effect: None
    4) Dolla dolla bills [7C]
        - Effect: None
    5) Mansion [30C] <Structure>
        - Effect: None
    6) Student [5C]  <Person>
        - Effect: None
    7) Car [15C]
        - Effect: None
    // cards w/ effect/s
    
    1) Loan Slip [Spell]
        - Effect: Draw 2 cards, after 2 turns lose 15C
    
    2) Lemonade Stand [5C]
        - Effect: Increase C value by 3 per start of turn.
    
    3) Credit Card [Spell] //could be opaf BUT ITS GWENT
        - Effect: Play as many cards as you can this turn. Gold values increasingly 	diminish by 2. e.g. -2 -> -4 -> -6 ...
    
    4) Butler [10C]
        - Effect: Adjacent cards increase in value by 5C
    5) Arsonist [0C] <Black>
        - Effect: Destroy Opposing Column's Structures
    6) Saboteur [Spell] <Black>
        - Effect: 1 bomb card is placed into each player's deck. The first player that draws this card, discards one card from their hand.
    7) Maid [5C]
        - Effect: Increases your Mansion cards by 3C.
    8) Police Officer [15C]
        - Effect: Silences 1 random black card (illegal activity cards).
    9) Parking Lot [5C]
        - Effect: Increase self value by 2 per Vehicle on board (all).
    10) Impound Lot [5C]
        - Effect: Decrease <vehicle> card values by 2 on board (all).
    11) Junkyard [5C]
        - Effect: Destroy all <Vehicle> cards in both player's grave, increase self value by 3.
    12) Resurrect [Spell]
        - Effect: Restore 1 <Person> card from your grave.
    13) Rebuild [Spell]
        - Effect: Restore 1 <Structure> or <Vehicle> from your grave.
    14) Gangsters [3C] <Black>
        - Effect: Selects 2 random cards from both sides, only one card survives.
    
    [Unique Cards]
    Ruling:
    3 Units
    3 Objects
    2 Spells
    2 Structs
    1 Hero Power
    
    <King of Beggars> {Beggar} - Hero Power: Humility - If round ends in draw, take victory.
    
    1) Black Market[15C] <Black, Structure>
        - Effect: Increase C value by X per start of turn. X is determined by no. of 
            Objects played on your field.
    
    2) Pickpocket [2C] <Person, Black>
        - Effect: reduce 1C from all <Person> cards on opponent's board, add to self.
    
    3) Strange Gravedigger [5C] <Person, Black> //omg hard to code idk if time
        - Effect: Select 1 <Person> card from the opponent's grave, inherit its effects.
    4) Robin Hood [10C] <Person, Black>
        - Effect: Takes away the highest value structures, and gives to Unique Person cards.
    5) Slums[0C] <Structure>
        - Effect: People/Object cards will be protected by this card. (This card will receive debuffs/elimination on their behalf.
    6) Kingpin[10C] <Person, Black>
        - Effect: Summons 3 random <Black> cards from your deck onto the board. Their effects do not trigger.
    7) Body Double [15C] <Person>
        - Effect: The body double of the King of Beggars himself. Immune from any effect.
    8) Junker [7C] <Vehicle>
        - Effect: Collects debuffed <Object/Vehicle> cards on the board. Increase in 2C per
        card.
    9) Beg [Spell]
        - Effect: Draw a card from opponent's deck.
    10) Scam [Spell] <Black>
        - Effect: Generate a duplicate of the targeted <Object> card, its current value
            will become its base value.
    ----------------------------------------------------
    Ruling:
    3 Units
    3 Objects
    2 Spells
    2 Structs
    1 Hero Power
    
    <Uncle Billy> {Farmer - Blue Collar} Hero Power: All vehicles/structures cards values will be multiply 1.5 (round only)
    1) Slaughterhouse [0C] <Structure1>
        - Effect: Remove all livestock from the board, gain their C value +1. Overrides other effects.
    
    2) Crop duster [10C] <Vehicle1>
        - Effect: Farm cards are boosted 2 per turn.
    
    3) Farm [15C] <Building1>
        - Effect: None
    4) Farmboy [5C] <Person1>
        - Effect: Tends to farms/barns/slaughterhouses by increasing their value by 2C
    5) Barn [10C] <Building2>
        - Effect: Animal cards are protected from elimination.
    6) Cow [7C] <Animal1>
        - Effect: None
    7) Chicken [5C] <Animal2>
        - Effect: None
    8) Farmdog [3C] <Animal3>
        - Effect: Upon playing, summons other Farmdogs on deck.
    9) Reap [Spell] <Spell1>
        - Effect: Farmboy required on your board. Your farmboy, and a random card 
                      with value higher than the farmboy's value will be removed from the board.
    10) Drought [Spell] <Spell2>
        - Effect: Farms/Barns and Animals will lose half their total value.
    11) Water Purifier [5C] <Object>
        - Effect: Cleanses adjacent cards from buffs/debuffs.
    ----------------------------------------------------
    Ruling:
    3 Units
    3 Objects
    2 Spells
    2 Structs
    1 Hero Power
    
    <Victoria> {Professional - White Collar} Hero Power: Expertise - All Person cards on board will double in value. (round only)
    1) Shareholder[10C] <Person>
        - Effect: Battlecry: Select an Office to link any bonuses and reductions that either receives is reflected to the other. //fatal bonds.
    
    2) Hacker [15C] <Black, Person>
        - Effect: Increases in value for every building played by the opponent.
    
    3) University [15C] <Structure>
        - Effect: +3C for every <Person> card active on the field. (+5C for Students)
    4) Insurance [0C] <Object>
        - Effect: Once played, your <Structures> receive only half of debuff effects.
    5) Solid Workforce [Spell]
        - Effect: Adjacent <Person> cards' values will be added then halved, and will be their current value.
        // aka 3 cards -> (10, 2, 2, = Total14) vs (10,2,2 => 14/2 => 7 thus 7,7,7 => Total21)
    6) Supply Truck [8C]
        - Effect: Deploy 1 random card from deck, triggering its effects.
    7) Innovate [Spell]
        - Effect: Targeted <Object> card will transform into higher C-value card.
    8) Superstar [15C] <Person>
        - Effect: <Person> cards on opposing board will flock in front of your superstar.
    9) Riot Response Vehicle [10C] <Vehicle>
        - Effect: Opposing <Person> cards which exceed 3 and are adjacent, will
                  become Detainee[1C]<Person> cards.
    10) Skyscraper [20C] <Structure>
        - Effect: Unaffected by buffs/debuffs.
        
        
    '''
