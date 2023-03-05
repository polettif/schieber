import pytest

from schieber.card import Card
from schieber.rules.suit import Suit
from schieber.player.challenge_player.strategy.mode.top_down_mode import TopDownMode


@pytest.fixture
def tdm():
    return TopDownMode()

@pytest.mark.parametrize("cards, score", [
    ([Card(Suit.SCHELLE, 13), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 11), Card(Suit.SCHELLE, 8), Card(Suit.EICHEL, 12),
      Card(Suit.EICHEL, 11), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], 0),
    ([Card(Suit.SCHELLE, 14), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 9), Card(Suit.SCHELLE, 8), Card(Suit.SCHELLE, 6),
      Card(Suit.EICHEL, 11), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], 13),
    ([Card(Suit.SCHELLE, 14), Card(Suit.SCHELLE, 11), Card(Suit.SCHELLE, 9), Card(Suit.EICHEL, 12), Card(Suit.EICHEL, 12),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], 13),
    ([Card(Suit.SCHELLE, 11), Card(Suit.SCHELLE, 9), Card(Suit.SCHELLE, 6), Card(Suit.EICHEL, 14), Card(Suit.EICHEL, 12),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 14), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], 26),
    ([Card(Suit.SCHELLE, 14), Card(Suit.SCHELLE, 13), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 10), Card(Suit.SCHELLE, 6),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], 72),
    ([Card(Suit.SCHELLE, 6), Card(Suit.SCHELLE, 7), Card(Suit.SCHELLE, 8), Card(Suit.SCHELLE, 10), Card(Suit.EICHEL, 6),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], 13),
])
def test_calculate_score_top_down(tdm, cards, score):
    s = tdm.calculate_mode_score(cards, geschoben=False)
    assert s == score


@pytest.mark.parametrize("cards, highest, lowest", [
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
def test_sort_by_rank_bottom_up(tdm, cards, lowest, highest):
    sorted = tdm.sort_by_rank(cards)
    assert sorted[-1] in lowest and sorted[0] == highest