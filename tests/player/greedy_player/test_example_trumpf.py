import pytest

from schieber.card import Card
from schieber.player.greedy_player.trumpf_decision import choose_trumpf, TrumpfType
from schieber.rules.suit import Suit
from schieber.rules.trumpf import Trumpf


@pytest.mark.parametrize("cards, trumpf, trumpf_type", [
    ([Card(Suit.SCHELLE, 13), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 11), Card(Suit.SCHELLE, 8), Card(Suit.EICHEL, 12),
      Card(Suit.EICHEL, 11), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], Trumpf.SCHELLE,
     TrumpfType.UNDER_4),
    ([Card(Suit.SCHELLE, 14), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 9), Card(Suit.SCHELLE, 8), Card(Suit.SCHELLE, 6),
      Card(Suit.EICHEL, 11), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], Trumpf.SCHELLE,
     TrumpfType.NELL_ASS_5),
    ([Card(Suit.SCHELLE, 14), Card(Suit.SCHELLE, 11), Card(Suit.SCHELLE, 9), Card(Suit.EICHEL, 12), Card(Suit.EICHEL, 12),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], Trumpf.SCHELLE,
     TrumpfType.UNDER_NELL_ASS),
    ([Card(Suit.SCHELLE, 11), Card(Suit.SCHELLE, 9), Card(Suit.SCHELLE, 6), Card(Suit.EICHEL, 14), Card(Suit.EICHEL, 12),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 14), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], Trumpf.SCHELLE,
     TrumpfType.UNDER_NELL_3_2_ASS),
    ([Card(Suit.SCHELLE, 14), Card(Suit.SCHELLE, 13), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 10), Card(Suit.SCHELLE, 6),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], Trumpf.OBE_ABE,
     TrumpfType.STICHE_5),
    ([Card(Suit.SCHELLE, 6), Card(Suit.SCHELLE, 7), Card(Suit.SCHELLE, 8), Card(Suit.SCHELLE, 10), Card(Suit.EICHEL, 6),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], Trumpf.UNDE_UFE,
     TrumpfType.STICHE_5),
])
def test_choose_trumpf_no_schieben(cards, trumpf, trumpf_type):
    evaluate_trumpf, evaluate_trumpf_type = choose_trumpf(cards=cards, geschoben=False)
    assert (evaluate_trumpf, evaluate_trumpf_type) == (trumpf, trumpf_type)


@pytest.mark.parametrize("cards, trumpf, trumpf_type", [
    ([Card(Suit.SCHELLE, 10), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 6), Card(Suit.SCHELLE, 8), Card(Suit.EICHEL, 12),
      Card(Suit.EICHEL, 11), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], Trumpf.EICHEL,
     TrumpfType.HAVE_TO_DECIDE),
    ([Card(Suit.SCHELLE, 10), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 6), Card(Suit.SCHELLE, 7), Card(Suit.EICHEL, 12),
      Card(Suit.EICHEL, 11), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], Trumpf.UNDE_UFE,
     TrumpfType.HAVE_TO_DECIDE),
])
def test_choose_trumpf_schieben(cards, trumpf, trumpf_type):
    evaluate_trumpf, evaluate_trumpf_type = choose_trumpf(cards=cards, geschoben=True)
    assert (evaluate_trumpf, evaluate_trumpf_type) == (trumpf, trumpf_type)
