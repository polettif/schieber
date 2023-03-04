import pytest

from schieber.card import Card
from schieber.suit import Suit
from schieber.player.challenge_player.strategy.mode.bottom_up_mode import BottomUpMode


@pytest.fixture
def bum():
    return BottomUpMode()

@pytest.mark.parametrize("cards, score", [
    ([Card(Suit.SCHELLE, 13), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 11), Card(Suit.SCHELLE, 8), Card(Suit.EICHEL, 12),
      Card(Suit.EICHEL, 11), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], 0),
    ([Card(Suit.SCHELLE, 14), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 9), Card(Suit.SCHELLE, 8), Card(Suit.SCHELLE, 6),
      Card(Suit.EICHEL, 11), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], 13),
    ([Card(Suit.SCHELLE, 14), Card(Suit.SCHELLE, 11), Card(Suit.SCHELLE, 9), Card(Suit.EICHEL, 12), Card(Suit.EICHEL, 6),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], 26),
    ([Card(Suit.SCHELLE, 11), Card(Suit.SCHELLE, 9), Card(Suit.SCHELLE, 6), Card(Suit.EICHEL, 13), Card(Suit.EICHEL, 12),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 14), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], 13),
    ([Card(Suit.SCHELLE, 14), Card(Suit.SCHELLE, 13), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 10), Card(Suit.SCHELLE, 6),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 13), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], 13),
    ([Card(Suit.SCHELLE, 6), Card(Suit.SCHELLE, 7), Card(Suit.SCHELLE, 8), Card(Suit.SCHELLE, 10), Card(Suit.EICHEL, 6),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], 75),
])
def test_calculate_score_bottom_up(bum, cards, score):
    s = bum.calculate_mode_score(cards, geschoben=False)
    assert s == score


@pytest.mark.parametrize("cards, lowest, highest", [
    ([Card(Suit.SCHELLE, 13), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 11), Card(Suit.SCHELLE, 8), Card(Suit.EICHEL, 12),
      Card(Suit.EICHEL, 11), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], Card(Suit.SCHELLE, 13), [Card(Suit.SCHILTE, 7)]),
    ([Card(Suit.SCHELLE, 14), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 9), Card(Suit.SCHELLE, 8), Card(Suit.SCHELLE, 6),
      Card(Suit.EICHEL, 11), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], Card(Suit.SCHELLE, 14), [Card(Suit.SCHELLE, 6)]),
    ([Card(Suit.SCHELLE, 14), Card(Suit.SCHELLE, 11), Card(Suit.SCHELLE, 9), Card(Suit.EICHEL, 12), Card(Suit.EICHEL, 6),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], Card(Suit.SCHELLE, 14), [Card(Suit.EICHEL, 6)]),
    ([Card(Suit.SCHELLE, 11), Card(Suit.SCHELLE, 9), Card(Suit.SCHELLE, 6), Card(Suit.EICHEL, 13), Card(Suit.EICHEL, 12),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 14), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], Card(Suit.SCHILTE, 14), [Card(Suit.SCHELLE, 6)]),
    ([Card(Suit.SCHELLE, 14), Card(Suit.SCHELLE, 13), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 10), Card(Suit.SCHELLE, 6),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 13), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], Card(Suit.SCHELLE, 14), [Card(Suit.SCHELLE, 6)]),
    ([Card(Suit.SCHELLE, 6), Card(Suit.SCHELLE, 7), Card(Suit.SCHELLE, 8), Card(Suit.SCHELLE, 10), Card(Suit.EICHEL, 6),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], Card(Suit.SCHILTE, 14), [Card(Suit.EICHEL, 6), Card(Suit.SCHELLE, 6)]),
])
def test_sort_by_rank_bottom_up(bum, cards, lowest, highest):
    sorted = bum.sort_by_rank(cards)
    assert sorted[-1] == lowest and sorted[0] in highest