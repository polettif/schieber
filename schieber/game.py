import logging
from multiprocessing import Condition

from schieber.dealer import Dealer
from schieber.rules.stich_rules import stich_rules, card_allowed
from schieber.rules.trumpf_rules import trumpf_allowed
from schieber.rules.count_rules import count_stich
from schieber.stich import PlayedCard, stich_dict, played_card_dict
from schieber.team import Team
from schieber.rules.trumpf import Trumpf

logger = logging.getLogger(__name__)


class EmptyPlayer:  # circular reference via GameState if inheriting Player
    def __init__(self):
        super().__init__()
        self.name = "empty"


class Game:
    def __init__(self, teams=None, point_limit=1500,
                 counting_factors=None,
                 seed=None):
        if teams is None:
            team_1 = Team(players=[EmptyPlayer(), EmptyPlayer()])
            team_2 = Team(players=[EmptyPlayer(), EmptyPlayer()])
            teams = [team_1, team_2]
        if counting_factors is None:
            counting_factors = {Trumpf.ROSE: 1, Trumpf.EICHEL: 1, Trumpf.SCHELLE: 2, Trumpf.SCHILTE: 2,
                                Trumpf.OBE_ABE: 3, Trumpf.UNDE_UFE: 3}
        self.teams = teams
        self.point_limit = point_limit
        self.players = [teams[0].players[0], teams[1].players[0], teams[0].players[1], teams[1].players[1]]
        self.dealer = Dealer(players=self.players)
        self.geschoben = False
        self.trumpf = None
        self.stiche = []
        self.cards_on_table = []
        self.counting_factors = counting_factors
        self.seed = seed
        self.endless_play_control = Condition()  # used to control the termination of the play_endless method
        self.stop_playing = False  # has to be set to true in order to stop the endless play

    def play_endless(self, start_player_index=0, whole_rounds=True):
        # TODO move to tournament.play() with endless param
        """
        Plays one game after the other with no end. This can be used for training a RL Player. Like this we can reuse
        one game. When we are training with tournaments, each time we play a game, it is added to the list of games.
        This could result in very high unneeded memory usage.
        :param start_player_index:
        :param whole_rounds:
        :return:
        """
        while True:
            logger.debug("start playing game")
            self.play(start_player_index, whole_rounds)
            logger.debug("game finished")
            try:
                self.endless_play_control.acquire()
                # timeout in case something goes wrong in the reset, or reset is not called for any reason.
                # In the normal case we just want to continue playing
                received = self.endless_play_control.wait(0.01)
                if received:
                    logger.debug("endless play received control message")
                else:
                    logger.debug(
                        "endless play did not receive control message! Timeout occurred. Endless play resuming.")
                if self.stop_playing:
                    logger.debug("stopping endless play")
                    break
            finally:
                self.endless_play_control.release()
            logger.debug("reset game")
            self.reset()

    def reset(self):
        """
        Resets the game so that a new game can be started. Used in the endless mode
        :return:
        """
        self.reset_points()
        self.stiche = []

    def play(self, start_player_index=0, whole_rounds=False):
        """
        Plays a game from the start to the end in the following manner:
        1. The dealer shuffles the cards
        2. The dealer deals 9 cards to each player
        3. The player on the right side of the dealer chooses the trumpf. If he/she chooses 'geschoben' his/her partner
            can choose the trumpf.
        4. For 9 rounds/stichs let the players play their cards.
        5. After each stich count the points, update the starting player based on who won the stich and add the cards
            played in the stich to the already played stichs.
        6. Check if a team has reached the point limit
        :param start_player_index:
        :param whole_rounds:
        :return:
        """
        logging.basicConfig(level=logging.DEBUG)

        # TODO move seed increment to tournament class
        if self.seed is not None:
            # Increment seed by one so that each game is different.
            # But still the sequence of games is the same each time
            self.seed += 1

        self.dealer.shuffle_cards(self.seed)
        self.dealer.deal_cards()
        self.define_trumpf(start_player_index=start_player_index)
        logger.info('Chosen Trumpf: {0} \n'.format(self.trumpf))

        for i in range(9):
            stich = self.play_stich(start_player_index)
            self.count_points(stich, last=(i == 8))

            logger.info('\nStich: {0} \n'.format(stich.player))
            logger.info('{}{}\n'.format('-' * 35, self.trumpf))
            start_player_index = self.players.index(stich.player)
            self.stiche.append(stich)
            self.stich_over_information()

            if (self.teams[0].won(self.point_limit) or self.teams[1].won(self.point_limit)) and not whole_rounds:
                return True
        logger.info(self.teams[0].points)
        logger.info(self.teams[1].points)

        return False

    def define_trumpf(self, start_player_index):
        """
        Sets the trumpf based on the choice of the player assigned to choose the trumpf
        :param start_player_index: The player which is on the right side of the dealer
        :return:
        """
        chosen_trumpf = self.players[start_player_index].choose_trumpf(self.get_state())
        if chosen_trumpf == Trumpf.SCHIEBEN:
            self.geschoben = True
            chosen_trumpf = self.players[(start_player_index + 2) % 4].choose_trumpf(self.get_state())
            is_allowed_trumpf = trumpf_allowed(chosen_trumpf=chosen_trumpf, geschoben=self.geschoben)
            if not is_allowed_trumpf:
                raise Exception('Trumpf not allowed')
        self.trumpf = chosen_trumpf

    def play_stich(self, start_player_index):
        """
        Plays one entire stich
        :param start_player_index: the index of the player who won the last stich or was assigned to choose the trumpf
        :return: the stich containing the played cards and the winner
        """
        self.cards_on_table = []
        first_card = self.play_card(table_cards=self.cards_on_table, player=self.players[start_player_index])
        self.move_made(self.players[start_player_index].id, first_card)
        self.cards_on_table = [PlayedCard(player=self.players[start_player_index], card=first_card)]
        for i in get_player_index(start_index=start_player_index):
            current_player = self.players[i]
            card = self.play_card(table_cards=self.cards_on_table, player=current_player)
            self.move_made(current_player.id, card)
            self.cards_on_table.append(PlayedCard(player=current_player, card=card))
        stich = stich_rules[self.trumpf](played_cards=self.cards_on_table)
        return stich

    def play_card(self, table_cards, player):
        """
        Checks if the card played by the player is allowed. If yes removes the card from the player's hand.
        :param table_cards:
        :param player:
        :return: the card chosen by the player
        """
        cards = [played_card.card for played_card in table_cards]
        chosen_card = player.choose_card(state=self.get_state())
        if not card_allowed(table_cards=cards, chosen_card=chosen_card, hand_cards=player.cards, trumpf=self.trumpf):
            Exception("Card not allowed")
        logger.info('Table: {0}:{1}'.format(player, chosen_card))
        player.cards.remove(chosen_card)
        return chosen_card

    def move_made(self, player_id, card):
        for player in self.players:
            player.move_made(player_id, card, self.get_state())

    def stich_over_information(self):
        [player.stich_over(state=self.get_state()) for player in self.players]

    def count_points(self, stich, last):
        """
        Gets the team of the winner of the stich and counts the points.
        :param stich:
        :param last: True if it is the last stich of the Game, False otherwise
        :return:
        """
        stich_player_index = self.players.index(stich.player)
        cards = [played_card.card for played_card in stich.played_cards]
        self.add_points(team_index=(stich_player_index % 2), cards=cards, last=last)

    def add_points(self, team_index, cards, last):
        """
        Adds the points of the cards to the score of the team who won the stich.
        :param team_index:
        :param cards:
        :param last:
        :return:
        """
        points = count_stich(cards, self.trumpf, last=last)
        points = points * self.counting_factors[self.trumpf]
        self.teams[team_index].points += points

    def get_state(self) -> 'GameState':
        return GameState(
            stiche=[stich_dict(stich) for stich in self.stiche],
            trumpf=self.trumpf,
            geschoben=self.geschoben,
            point_limit=self.point_limit,
            table=[played_card_dict(played_card) for played_card in self.cards_on_table],
            teams=[dict(points=team.points) for team in self.teams],
            counting_factors=self.counting_factors
        )

    def reset_points(self):
        """
        Resets the points of the teams to 0. This is used when single games are played.
        :return:
        """
        [team.reset_points() for team in self.teams]


class GameState:
    """
    Returns the status of the game in a dictionary containing
    - the stiche
    - the trumpf
    - if it has been geschoben
    - the point limit
    - the cards currently on the table
    - the teams
    - counting factors
    :return:
    """

    def __init__(self, stiche, trumpf: Trumpf, geschoben: bool, point_limit: int, table, teams, counting_factors):
        self.stiche = stiche
        self.trumpf: Trumpf = trumpf
        self.geschoben: bool = geschoben
        self.point_limit: int = point_limit
        self.table = table
        self.teams = teams
        self.counting_factors = counting_factors


def get_player_index(start_index):
    for i in range(1, 4):
        yield (i + start_index) % 4
