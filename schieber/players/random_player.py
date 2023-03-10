import random

from jass.card import Card
from schieber.game import GameState
from schieber.player import Player
from schieber.rules.trumpf_rules import trumpf_allowed
from schieber.rules.trumpf import Trumpf


class RandomPlayer(Player):
    def choose_trumpf(self, state: GameState) -> 'Trumpf':
        return select_random_trumpf(state.geschoben)

    def choose_card(self, state: GameState) -> 'Card':
        cards = self.allowed_cards(state=state)
        random.shuffle(cards)
        return cards[0]


def select_random_trumpf(geschoben: bool):
    choices = list(Trumpf)
    random.shuffle(choices)
    for choice in choices:
        if trumpf_allowed(chosen_trumpf=choice, geschoben=geschoben):
            return choice
