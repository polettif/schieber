import random

from schieber.card import Card
from schieber.game import GameState
from schieber.player import Player
from schieber.players.greedy_player import trumpf_decision
from schieber.rules.trumpf import Trumpf


class GreedyPlayer(Player):
    def choose_trumpf(self, state: GameState) -> 'Trumpf':
        trumpf, _ = trumpf_decision.decide_trumpf(cards=self.cards, geschoben=state.geschoben)
        return trumpf

    def choose_card(self, state: GameState) -> 'Card':
        cards = self.allowed_cards(state=state)
        return random.choice(cards)


def greedy_card(allowed_cards, trumpf):
    sorted(allowed_cards)
    if trumpf == Trumpf.OBE_ABE:
        return allowed_cards[-1]
    elif trumpf == Trumpf.UNDE_UFE:
        return allowed_cards[0]
    else:
        trumpf_cards = [card for card in allowed_cards if card.suit.name == trumpf.name]
        if trumpf_cards:
            return trumpf_cards[-1]
        return allowed_cards[-1]
