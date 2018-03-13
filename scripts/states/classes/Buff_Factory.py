from enum import Enum, auto
'''
The Buff class, can generate.
'''


class BuffFactory(object):

    def factory(kind, operation, intensity):
        # example(buff, add, 20) -> current_vaL + 20
        # example(debuff, divide, 2) -> current_val / 2
        # example(constant, set, 15) -> current_val = 15

        # with this in mind, there must be some kind of operation priority within the Card class.
        if kind == Kind.BUFF:
            return Buff(operation, intensity)
        elif kind == Kind.DEBUFF:
            return Debuff(operation, intensity)
        elif kind == Kind.CONSTANT:
            return Constant(operation, intensity)
    factory = staticmethod(factory)


class Buff(object):
    def __init__(self, operation, intensity):
        self.operation = operation
        self.intensity = intensity

class Debuff(object):
    def __init__(self, operation, intensity):
        self.operation = operation
        self.intensity = intensity

class Constant(object):
    def __init__(self, operation, intensity):
        self.operation = operation
        self.intensity = intensity


class Operation(Enum):
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    SET = auto()

class Kind(Enum):
    BUFF = auto()
    DEBUFF = auto()
    CONSTANT = auto()

