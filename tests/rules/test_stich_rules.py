import pytest

from schieber.rules.stich_rules import stich_rules, card_allowed, allowed_cards, is_trumpf_under, does_under_trumpf, \
    is_chosen_card_best_trumpf
from schieber.rules.trumpf import Trumpf
from jass.card import Card
from schieber.players.random_player import RandomPlayer
from schieber.stich import PlayedCard
from jass.suit import Suit


@pytest.fixture(scope="module", autouse=True)
def players():
    random_players = [RandomPlayer(), RandomPlayer(), RandomPlayer(), RandomPlayer()]
    for i, player in enumerate(random_players):
        player.id = i
    return random_players


@pytest.fixture(scope="module", autouse=True)
def played_cards(players):
    return [PlayedCard(player=players[0], card=Card(Suit.EICHEL, 6)),
            PlayedCard(player=players[1], card=Card(Suit.SCHELLE, 10)),
            PlayedCard(player=players[2], card=Card(Suit.SCHELLE, 13)),
            PlayedCard(player=players[3], card=Card(Suit.SCHELLE, 9))]


@pytest.mark.parametrize("trumpf, index,", [
    (Trumpf.OBE_ABE, 0),
    (Trumpf.UNDE_UFE, 0),
    (Trumpf.SCHELLE, 3),
    (Trumpf.EICHEL, 0),
])
def test_stich(trumpf, index, played_cards):
    stich = stich_rules[trumpf](played_cards=played_cards)
    assert stich.player.id == index


@pytest.mark.parametrize("table_cards, chosen_card, hand_cards, trumpf, result", [
    ([Card(Suit.EICHEL, 12)], Card(Suit.SCHELLE, 12), [Card(Suit.EICHEL, 11), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 11)],
     Trumpf.OBE_ABE, False),
    ([Card(Suit.SCHELLE, 12)], Card(Suit.SCHELLE, 12), [Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 11)], Trumpf.SCHELLE, True),
    (None, Card(Suit.SCHELLE, 12), [Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 11)], Trumpf.SCHELLE, True),
    ([Card(Suit.SCHELLE, 12)], Card(Suit.SCHELLE, 12), [Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 11)], Trumpf.OBE_ABE, True),
    ([Card(Suit.EICHEL, 12)], Card(Suit.SCHELLE, 12), [Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 11)], Trumpf.OBE_ABE, True),
    ([Card(Suit.EICHEL, 11)], Card(Suit.SCHELLE, 12), [Card(Suit.EICHEL, 12), Card(Suit.SCHELLE, 11), Card(Suit.SCHELLE, 12)],
     Trumpf.EICHEL, False),
    ([Card(Suit.EICHEL, 11)], Card(Suit.EICHEL, 11), [Card(Suit.SCHELLE, 12), Card(Suit.EICHEL, 11), Card(Suit.EICHEL, 12)],
     Trumpf.UNDE_UFE, True),
    ([Card(Suit.EICHEL, 11)], Card(Suit.EICHEL, 11), [Card(Suit.SCHELLE, 12), Card(Suit.EICHEL, 12)], Trumpf.UNDE_UFE, False),
    ([Card(Suit.ROSE, 6)], Card(Suit.EICHEL, 11), [Card(Suit.ROSE, 10), Card(Suit.EICHEL, 11)], Trumpf.ROSE, False),
    ([Card(Suit.ROSE, 6)], Card(Suit.EICHEL, 11), [Card(Suit.ROSE, 11), Card(Suit.EICHEL, 11)], Trumpf.ROSE, True),
    ([Card(Suit.ROSE, 7)], Card(Suit.ROSE, 6), [Card(Suit.ROSE, 6), Card(Suit.EICHEL, 11)], Trumpf.ROSE, True),
    ([Card(Suit.EICHEL, 6), Card(Suit.ROSE, 7)], Card(Suit.ROSE, 6), [Card(Suit.ROSE, 6), Card(Suit.EICHEL, 11)],
     Trumpf.ROSE, False),
    ([Card(Suit.ROSE, 12), Card(Suit.SCHILTE, 11)], Card(Suit.ROSE, 8),
     [Card(Suit.ROSE, 6), Card(Suit.ROSE, 8), Card(Suit.SCHILTE, 12), Card(Suit.EICHEL, 11), Card(Suit.SCHILTE, 14),
      Card(Suit.SCHILTE, 8), Card(Suit.SCHELLE, 11), Card(Suit.SCHELLE, 10)], Trumpf.ROSE, True),
    ([Card(Suit.SCHILTE, 6), Card(Suit.ROSE, 6), Card(Suit.ROSE, 9)], Card(Suit.ROSE, 10),
     [Card(Suit.ROSE, 10), Card(Suit.SCHELLE, 11)], Trumpf.ROSE, False),
    ([Card(Suit.SCHILTE, 13), Card(Suit.EICHEL, 6), Card(Suit.SCHILTE, 10)], Card(Suit.ROSE, 8),
     [Card(Suit.SCHILTE, 8), Card(Suit.SCHILTE, 9), Card(Suit.SCHELLE, 13), Card(Suit.ROSE, 12), Card(Suit.ROSE, 13),
      Card(Suit.ROSE, 8), Card(Suit.EICHEL, 6), Card(Suit.SCHELLE, 6), Card(Suit.SCHELLE, 14)], Trumpf.ROSE, True),

])
def test_card_allowed(table_cards, chosen_card, hand_cards, trumpf, result):
    assert card_allowed(table_cards=table_cards, chosen_card=chosen_card, hand_cards=hand_cards,
                        trumpf=trumpf) == result


@pytest.mark.parametrize("hand_cards, table_cards, trumpf, result", [
    ([Card(Suit.SCHELLE, 12)], [Card(Suit.SCHELLE, 11)], Trumpf.SCHELLE, [Card(Suit.SCHELLE, 12)]),
    ([Card(Suit.SCHELLE, 12), Card(Suit.ROSE, 12)], [Card(Suit.SCHELLE, 11)], Trumpf.EICHEL, [Card(Suit.SCHELLE, 12)]),
    ([Card(Suit.SCHELLE, 12)], [Card(Suit.ROSE, 11)], Trumpf.EICHEL, [Card(Suit.SCHELLE, 12)]),
])
def test_allowed_cards(hand_cards, table_cards, trumpf, result):
    assert allowed_cards(hand_cards=hand_cards, table_cards=table_cards, trumpf=trumpf) == result


@pytest.mark.parametrize("trumpf, card, result", [
    (Trumpf.SCHELLE, Card(Suit.SCHELLE, 12), False),
    (Trumpf.SCHELLE, Card(Suit.SCHELLE, 11), True),
    (Trumpf.ROSE, Card(Suit.SCHELLE, 11), False),
    (Trumpf.OBE_ABE, Card(Suit.SCHELLE, 11), False),
    (Trumpf.ROSE, Card(Suit.ROSE, 11), True),
])
def test_is_trumpf_under(trumpf, card, result):
    assert is_trumpf_under(trumpf=trumpf, card=card) == result


@pytest.mark.parametrize("table_cards, chosen_card, hand_cards, trumpf, result", [
    ([Card(Suit.EICHEL, 12)], Card(Suit.SCHELLE, 12), [Card(Suit.SCHELLE, 12)], Trumpf.OBE_ABE, False),
    ([Card(Suit.EICHEL, 12)], Card(Suit.EICHEL, 6), [Card(Suit.EICHEL, 6), Card(Suit.SCHELLE, 6)], Trumpf.EICHEL, True),
    ([Card(Suit.EICHEL, 12)], Card(Suit.EICHEL, 13), [Card(Suit.EICHEL, 13)], Trumpf.EICHEL, False),
    ([Card(Suit.SCHELLE, 12)], Card(Suit.SCHELLE, 13), [Card(Suit.SCHELLE, 13)], Trumpf.SCHELLE, False),
    ([Card(Suit.SCHELLE, 12)], Card(Suit.SCHELLE, 6), [Card(Suit.SCHELLE, 6), Card(Suit.ROSE, 6)], Trumpf.SCHELLE, True),
    ([Card(Suit.SCHELLE, 12)], Card(Suit.SCHELLE, 6), [Card(Suit.SCHELLE, 6), Card(Suit.SCHELLE, 7)], Trumpf.SCHELLE, False),
])
def test_does_under_trumpf(table_cards, chosen_card, hand_cards, trumpf, result):
    assert does_under_trumpf(table_cards, chosen_card, hand_cards, trumpf) == result


@pytest.mark.parametrize("table_cards, chosen_card, trumpf, result", [
    ([Card(Suit.EICHEL, 12)], Card(Suit.EICHEL, 11), Trumpf.EICHEL, True),
    ([Card(Suit.EICHEL, 11)], Card(Suit.EICHEL, 12), Trumpf.EICHEL, False),
    ([Card(Suit.EICHEL, 13), Card(Suit.EICHEL, 14)], Card(Suit.EICHEL, 6), Trumpf.EICHEL, False),
    ([Card(Suit.EICHEL, 13), Card(Suit.EICHEL, 14)], Card(Suit.EICHEL, 11), Trumpf.EICHEL, True),
])
def test_is_chosen_card_best_trumpf(table_cards, chosen_card, trumpf, result):
    assert is_chosen_card_best_trumpf(table_cards, chosen_card, trumpf) == result
