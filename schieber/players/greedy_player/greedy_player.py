from schieber.player import Player
from schieber.players.greedy_player import trumpf_decision
from schieber.rules.trumpf import Trumpf


class GreedyPlayer(Player):
    # TODO Does not fit base_player contract choose_trumpf(state: GameState)
    def choose_trumpf(self, geschoben):
        allowed = False
        while not allowed:
            trumpf, _ = trumpf_decision.choose_trumpf(cards=self.cards, geschoben=geschoben)
            if self.trumps == 'all':
                allowed = yield trumpf
            elif self.trumps == 'obe_abe':
                allowed = yield Trumpf.OBE_ABE
            if allowed:
                yield None

    # TODO Does not fit base_player contract choose_card(state: GameState)
    def choose_card(self, state=None):
        allowed_cards = self.allowed_cards(state=state)
        allowed = False
        while not allowed:
            card = greedy_card(allowed_cards, state.trumpf)
            allowed = yield card
            if allowed:
                yield None


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
