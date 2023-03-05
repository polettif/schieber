import pytest

from schieber.card import Card
from schieber.game import Game
from schieber.suit import Suit
from schieber.trumpf import Trumpf
from schieber.player.challenge_player.strategy.jass_strategy import JassStrategy
from schieber.player.challenge_player.challenge_player import ChallengePlayer


@pytest.fixture
def js():
    p = ChallengePlayer()
    p.id = 0
    return JassStrategy(p)


@pytest.mark.parametrize("cards, trumpf", [
    ([Card(Suit.SCHELLE, 13), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 11), Card(Suit.SCHELLE, 8),
      Card(Suit.EICHEL, 12),
      Card(Suit.EICHEL, 11), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], Trumpf.SCHELLE),
    ([Card(Suit.SCHELLE, 14), Card(Suit.SCHELLE, 13), Card(Suit.SCHELLE, 9), Card(Suit.EICHEL, 8), Card(Suit.EICHEL, 6),
      Card(Suit.EICHEL, 11), Card(Suit.SCHILTE, 12), Card(Suit.SCHILTE, 7), Card(Suit.ROSE, 9)], Trumpf.EICHEL),
    ([Card(Suit.SCHELLE, 14), Card(Suit.SCHELLE, 11), Card(Suit.EICHEL, 9), Card(Suit.SCHILTE, 13),
      Card(Suit.SCHILTE, 12),
      Card(Suit.SCHILTE, 10), Card(Suit.SCHILTE, 8), Card(Suit.SCHILTE, 9), Card(Suit.SCHILTE, 6)], Trumpf.SCHILTE),
    ([Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 9), Card(Suit.SCHELLE, 6), Card(Suit.EICHEL, 14), Card(Suit.ROSE, 12),
      Card(Suit.ROSE, 7), Card(Suit.ROSE, 6), Card(Suit.ROSE, 14), Card(Suit.ROSE, 9)], Trumpf.ROSE),
    ([Card(Suit.SCHELLE, 14), Card(Suit.SCHELLE, 13), Card(Suit.SCHELLE, 12), Card(Suit.SCHELLE, 10),
      Card(Suit.SCHELLE, 6),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], Trumpf.OBE_ABE),
    ([Card(Suit.SCHELLE, 6), Card(Suit.SCHELLE, 7), Card(Suit.SCHELLE, 8), Card(Suit.SCHELLE, 10), Card(Suit.EICHEL, 6),
      Card(Suit.EICHEL, 7), Card(Suit.SCHILTE, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], Trumpf.UNDE_UFE),
    ([Card(Suit.SCHELLE, 6), Card(Suit.SCHELLE, 7), Card(Suit.SCHELLE, 9), Card(Suit.EICHEL, 10), Card(Suit.EICHEL, 8),
      Card(Suit.SCHILTE, 7), Card(Suit.SCHILTE, 10), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], Trumpf.SCHIEBEN),
])
def test_calculate_score_top_down(js, cards, trumpf):
    t = js.chose_trumpf(cards, Game().get_state())
    assert t == trumpf
