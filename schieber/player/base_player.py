import inspect

from schieber.card import from_string_to_card, Card
from schieber.game import GameState
from schieber.rules.trumpf import Trumpf
from schieber.rules.stich_rules import allowed_cards


class BasePlayer:
    def __init__(self, name='unknown', seed=None):
        """
        :param name:
        :param seed:
        """
        self.name = name
        self.cards = []
        self.trumpf_list = list(Trumpf)
        self.id = name
        self.seed = seed

    def get_dict(self):
        """
        Returns a dictionary containing:
        - the name
        - the type (RandomPlayer, GreedyPlayer, etc.)
        :return:
        """
        return dict(name=self.name, type=type(self).__name__)

    def take_card(self, card):
        self.cards.append(card)

    def choose_trumpf(self, state: GameState) -> 'Trumpf':
        raise NotImplementedError(str(inspect.stack()[1][3]))

    def choose_card(self, state: GameState) -> 'Card':
        raise NotImplementedError(str(inspect.stack()[1][3]))

    def move_made(self, player_id, card, state):
        pass

    def stich_over(self, state=None):
        pass

    def allowed_cards(self, state: GameState):
        return self.allowed_cards_with_hand_cards(state, self.cards)

    def allowed_cards_with_hand_cards(self, state: GameState, hand_cards):
        """
        Returns the cards on the hand of the player which he/she is allowed to play in the current state according to the rules
        :param hand_cards:
        :param state:
        :return:
        """
        table_cards = [from_string_to_card(entry['card']) for entry in state.table]
        return allowed_cards(hand_cards=hand_cards, table_cards=table_cards, trumpf=state.trumpf)

    def __str__(self):
        return '<Player:{}>'.format(self.name)
