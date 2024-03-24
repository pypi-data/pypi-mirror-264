class Const:
    def __setattr__(self, name: str, value):
        raise ValueError("Cannot change %s.%s." % self.__class__.__name__, name)


class CommonConst(Const):
    OFF = 0
    ON = 1
    BLANK = ""
    SPACE = " "
    NEW_LINE = "\n"
    NA = "N/A"
    ZERO = 0
    ONE = 1
    TWO = 2
    ACTIVE = 1
    DEACTIVATED = 0
