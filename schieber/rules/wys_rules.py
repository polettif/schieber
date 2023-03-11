from enum import Enum

Wys = Enum('Wys', ['SEQUENCE_3', 'SEQUENCE_4', 'SEQUENCE_5', '4_SAME', '4_UNDER', '4_NAELL'])

points_wys = {Wys.SEQUENCE_3: 20, Wys.SEQUENCE_4: 50, Wys.SEQUENCE_5: 100, '4_NAELL': 150, '4_UNDER': 200}


# TODO: Implement Wys (way down on the list)

def wys_allowed(wys, hand_cards):
    allowed = False
    if not len(wys) >= 3:
        return False
    if not set(wys) < set(hand_cards):
        return False
    return allowed
