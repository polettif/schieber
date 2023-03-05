import pytest

from schieber.card import Card
from schieber.rules.suit import Suit
from schieber.player.challenge_player.strategy.mode.mode import Mode


@pytest.fixture
def mode():
    return Mode()

@pytest.mark.parametrize("cards, suits", [
    ([Card(Suit.SCHELLE, 13), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 11), Card(Suit.SCHELLE, 8), Card(Suit.EICHEL, 12),
      Card(Suit.EICHEL, 11), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], [Suit.SCHELLE, Suit.EICHEL, Suit.SCHILTE, Suit.ROSE]),
    ([Card(Suit.SCHELLE, 14), Card(Suit.EICHEL, 11), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)],
     [Suit.SCHELLE, Suit.EICHEL, Suit.SCHILTE, Suit.ROSE]),
    ([Card(Suit.SCHELLE, 14), Card(Suit.SCHELLE, 11), Card(Suit.SCHELLE, 9), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)],
     [Suit.SCHELLE, Suit.SCHILTE, Suit.ROSE]),
    ([Card(Suit.EICHEL, 13), Card(Suit.EICHEL, 12), Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 14), Card(Suit.SCHILTE, 7)],
     [Suit.EICHEL, Suit.SCHILTE]),
    ([Card(Suit.SCHELLE, 14), Card(Suit.SCHELLE, 13), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 10), Card(Suit.SCHELLE, 6)],
     [Suit.SCHELLE]),
    ([Card(Suit.SCHILTE, 7)],
     [Suit.SCHILTE]),
    ([], []),
])
def test_available_suits(mode, cards, suits):
    available_suits = mode.available_suits(cards)
    assert set(available_suits) == set(suits)


@pytest.mark.parametrize("round_color, cards, have_to_serve", [
    (Suit.ROSE,
     [Suit.SCHELLE, Suit.EICHEL, Suit.SCHILTE, Suit.ROSE],
     True),
    (Suit.ROSE,
     [Suit.SCHELLE, Suit.EICHEL],
     False),
    (Suit.SCHILTE,
     [Suit.SCHELLE],
     False),
    (Suit.SCHELLE,
     [Suit.SCHELLE, Suit.EICHEL, Suit.SCHILTE, Suit.ROSE],
     True),
    (Suit.EICHEL,
     [Suit.SCHELLE, Suit.SCHILTE, Suit.ROSE],
     False),
    (None,
     [Suit.SCHELLE, Suit.EICHEL, Suit.SCHILTE, Suit.ROSE],
     False),
])
def test_have_to_serve(mode, cards, round_color, have_to_serve):
    assert have_to_serve == mode.have_to_serve(cards, round_color)