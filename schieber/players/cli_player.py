from schieber.game import GameState
from schieber.players.base_player import BasePlayer
from schieber.rules.trumpf_rules import trumpf_allowed


class CliPlayer(BasePlayer):
    def choose_trumpf(self, state: GameState) -> 'Trumpf':
        self._print_cards()
        print('\nTrumpf:')
        for i, trumpf in enumerate(self.trumpf_list):
            print('{0} : {1}'.format(i, trumpf))
        print('\nGeschoben: {0}\n'.format(state.geschoben))
        while True:
            chosen_trumpf = self._choose_trumpf_input()
            if trumpf_allowed(chosen_trumpf, state.geschoben):
                return chosen_trumpf

    def choose_card(self, state: GameState) -> 'Card':
        self._print_cards()
        allowed_cards = self.allowed_cards(state=state)
        while True:
            chosen_card = self._choose_card_input()
            if chosen_card in allowed_cards:
                return chosen_card

    def _choose_trumpf_input(self):
        while True:
            try:
                trumpf_index = int(
                    input("Please chose the trumpf by the number from 0 to {0}: \n".format(len(self.trumpf_list) - 1)))
                if trumpf_index in range(0, len(self.trumpf_list)):
                    return self.trumpf_list[trumpf_index]
                else:
                    print("Sorry, no valid trumpf number.\n")
                    continue
            except ValueError:
                print("Sorry, I didn't understand that.\n")
                continue

    def _choose_card_input(self):
        while True:
            try:
                card_index = int(
                    input("Please chose the card by the number from 0 to {0}: \n".format(len(self.cards) - 1)))
                if card_index in range(0, len(self.cards)):
                    print()
                    return self.cards[card_index]
                else:
                    print("Sorry, no valid trumpf number\n")
                    continue
            except ValueError:
                print("Sorry, I didn't understand that.\n")
                continue

    def _print_cards(self):
        print('Hand cards: \n')
        for i, card in enumerate(self.cards):
            print('{0} : {1}'.format(i, card))
        print('')


def move_allowed(move_function, message):
    allowed = False
    while not allowed:
        move = move_function()
        allowed = yield move
        if allowed:
            yield None
        else:
            print(message)
