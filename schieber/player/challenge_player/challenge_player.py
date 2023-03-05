import random

from schieber.game import GameState
from schieber.player.base_player import BasePlayer
from schieber.player.challenge_player.strategy.jass_strategy import JassStrategy
from schieber.card import Card
from schieber.rules.trumpf_rules import trumpf_allowed
from schieber.trumpf import Trumpf


class ChallengePlayer(BasePlayer):
    def set_card(self, card):
        self.cards.append(card)
        if len(self.cards) == 9:
            self.strategy = JassStrategy(self)

    def choose_trumpf(self, state: GameState):
        allowed = False
        while not allowed:
            trumpf = self.strategy.chose_trumpf(self.cards, state)
            if trumpf_allowed(chosen_trumpf=trumpf, geschoben=state.geschoben):
                return trumpf

    def choose_card(self, state:GameState=None):
        if len(state.stiche) == 0:
            if len(state.table) == 0:
                if state.geschoben:
                    self.role = 'Partner'
                else:
                    self.role = 'Trumpf'

            elif len(state.table) == 2:
                if state.geschoben:
                    self.role = 'Trumpf'
                else:
                    self.role = 'Partner'

            else:
                self.role = 'Off'

        cards = self.allowed_cards(state=state)

        allowed = False
        while not allowed:
            card = self.strategy.choose_card(cards, state, self.role)
            if not isinstance(card, Card):
                random.seed(self.seed)
                card = random.choice(cards)
            allowed = yield card
            if allowed:
                yield None

    def move_made(self, player_id, card, state):
        self.strategy.move_made(player_id, card, state)
