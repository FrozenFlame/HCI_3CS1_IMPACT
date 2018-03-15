from ...Card import Card
from enum import Enum, auto


class BlackMarket(Card):
    name = "Black Market"
    base_val = 15
    current_val = 15

    def __init__(self, name="Black Market", base_val=15, effect=None, type=[Type.BLACK, Type.STRUCTURE]):
        super.__init__(name,base_val,effect)
        self.type = type

class Type(Enum):
    BLACK = auto()
    STRUCTURE = auto()
