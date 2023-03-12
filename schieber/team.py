class Team:
    # TODO use list[Player] resolve circular dependency via GameState
    def __init__(self, players, team_index=None):
        self.points = 0
        self.players = players
        self.team_index = team_index

    def player_by_number(self, number):
        """
        Returns the players by the number in the team. The number should be either 0 or 1.
        :param number:
        :return:
        """
        for player in self.players:
            if player.number == number:
                return player
        return None

    def reset_points(self):
        """
        Resets the points to 0. This is used when single games and no tournaments are played.
        :return:
        """
        self.points = 0

    def __str__(self):
        if self.team_index is None:
            return "?"
        return str(self.team_index+1)
