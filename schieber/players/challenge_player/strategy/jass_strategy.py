from schieber.players.challenge_player.strategy.card_counter import *
from schieber.rules.trumpf import Trumpf


class JassStrategy:
    def __init__(self, player):
        self.me = player
        self.card_counter = CardCounter(player)

    def chose_trumpf(self, cards, state):
        scores = []

        if not state.geschoben:
            scores.append((Trumpf.SCHIEBEN, 54))

        tdm = TopDownMode()
        scores.append((Trumpf.OBE_ABE, tdm.calculate_mode_score(cards, state.geschoben)))

        bum = BottomUpMode()
        scores.append((Trumpf.UNDE_UFE, bum.calculate_mode_score(cards, state.geschoben)))

        for suit in Suit:
            tcm = TrumpfColorMode(suit)
            scores.append((Trumpf[suit.name], tcm.calculate_mode_score(cards, state.geschoben)))

        return max(scores, key=lambda x: x[1])[0]

    def choose_card(self, allowed_cards, state, role):
        mode = get_mode(state.trumpf)
        return mode.get_card_to_play(allowed_cards, self.card_counter, state, role)

    def move_made(self, player_id, card, state):
        self.card_counter.card_played(player_id, card, state)
