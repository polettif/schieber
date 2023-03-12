import logging

from schieber.game import Game
from schieber.player import Player
from schieber.team import Team

logger = logging.getLogger(__name__)


class Tournament:
    def __init__(self, players: list[Player], point_limit=1500, seed=None):
        """
        Sets the point limit and initializes the players, teams and games arrays.
        :param point_limit:
        """
        assert len(players) == 4
        self.players = players
        self.point_limit = point_limit
        self.teams = []
        self.games = []
        self.seed = seed

    def check_players(self):
        """
        Checks if there are really 4 players in the array
        :return:
        """
        player_numbers = []
        for index, player in enumerate(self.players):
            player_numbers.append(index)
        assert {0, 1, 2, 3} == set(player_numbers)

    def register_player(self, player: Player, position: int):
        """
        Adds another player at the designated position (0-3)
        """
        assert 0 <= position <= 4
        player.id = position
        self.players[position] = player

    def build_teams(self):
        """
        Builds the teams based on the players array
        :return: the team list
        """
        self.check_players()
        team_1 = Team(players=[self.players[0], self.players[2]], team_index=0)
        team_2 = Team(players=[self.players[1], self.players[3]], team_index=1)
        self.teams = [team_1, team_2]
        assert team_1.team_index != team_2.team_index
        return self.teams

    def play(self, rounds=0):
        """
        Plays a tournament until one team reaches the point_limit.
        :param rounds:
        :return:
        """
        self.build_teams()
        logger.info('Tournament starts, the point limit is {}.'.format(self.point_limit))
        end = False
        whole_rounds = True if rounds > 0 else False
        round_counter = 0
        while not end:
            if self.seed is not None:
                # Increment seed by one so that each game is different.
                # But still the sequence of games is the same each time
                self.seed += 1
            game = Game(teams=self.teams, point_limit=self.point_limit, seed=self.seed)
            self.games.append(game)
            logger.info('-' * 200)
            logger.info('Round {} starts.'.format(len(self.games)))
            logger.info('-' * 200)
            end = game.play(start_player_index=((len(self.games) - 1) % 4), whole_rounds=whole_rounds)
            logger.info('Round {} is over.'.format(len(self.games)))
            logger.info('Points: Team 1: {0} , Team 2: {1}. \n'.format(self.teams[0].points, self.teams[1].points))
            round_counter += 1
            if whole_rounds and round_counter == rounds:
                end = True
        winning_team = self.get_winning_team()
        logger.info('Team {0} won! \n'.format(winning_team))
        self.reset()

    def get_winning_team(self) -> Team:
        if self.teams[0].points >= self.point_limit:
            return self.teams[0]
        elif self.teams[1].points >= self.point_limit:
            return self.teams[1]
        else:
            Exception()

    def get_status(self):
        """
        Returns the status of the tournament
        :return:
        """
        return {
            'games': [game.get_state() for game in self.games],
            'players': [player.get_dict() for player in self.players]
        }

    def reset(self):
        """
        Resets the tournament. Deletes the games array and deletes the cards of the players.
        :return:
        """
        self.games = []
        for player in self.players:
            player.cards = []
