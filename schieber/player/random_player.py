import random

from schieber.game import GameState
from schieber.player.base_player import BasePlayer
from schieber.rules.trumpf_rules import trumpf_allowed
from schieber.trumpf import Trumpf


def select_random_trumpf(geschoben: bool):
    choices = list(Trumpf)
    random.shuffle(choices)
    for choice in choices:
        if trumpf_allowed(chosen_trumpf=choice, geschoben=geschoben):
            return choice


class RandomPlayer(BasePlayer):
    def choose_trumpf(self, state: GameState):
        return select_random_trumpf(state.geschoben)

    def choose_card(self, state=None):
        cards = self.allowed_cards(state=state)
        random.shuffle(cards)
        return cards[0]
