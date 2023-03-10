import random

from schieber.game import GameState
from schieber.player import Player
from schieber.players.challenge_player.strategy.jass_strategy import JassStrategy
from jass.card import Card
from schieber.rules.trumpf import Trumpf
from schieber.rules.trumpf_rules import trumpf_allowed


class ChallengePlayer(Player):
    def take_card(self, card):
        self.cards.append(card)
        if len(self.cards) == 9:
            self.strategy = JassStrategy(self)

    def choose_trumpf(self, state: GameState) -> 'Trumpf':
        allowed = False
        while not allowed:
            trumpf = self.strategy.chose_trumpf(self.cards, state)
            if trumpf_allowed(chosen_trumpf=trumpf, geschoben=state.geschoben):
                return trumpf

    def choose_card(self, state: GameState) -> 'Card':
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

        return random.choice(cards)

    def move_made(self, player_id, card, state):
        self.strategy.move_made(player_id, card, state)
