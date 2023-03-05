from enum import Enum

from schieber.rules.suit import Suit


class Trumpf(Enum):
    ROSE = Suit.ROSE
    SCHELLE = Suit.SCHELLE
    EICHEL = Suit.EICHEL
    SCHILTE = Suit.SCHILTE
    OBE_ABE = "OBE_ABE"
    UNDE_UFE = "UNDE_UFE"
    SCHIEBEN = "SCHIEBEN"
