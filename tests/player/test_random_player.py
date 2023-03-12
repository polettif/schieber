import pytest
from timeit import default_timer as timer
from math import sqrt, floor

from schieber.players.random_player import RandomPlayer
from schieber.tournament import Tournament


@pytest.mark.statistical
def test_is_random():
    """
    This test may fail sometimes if the number of tournaments is too low. But for performance reasons, this number is set low.
    :return:
    """
    point_limit = 1000
    number_of_tournaments = 10
    mean = number_of_tournaments * 0.5  # assume that a RandomPlayer has a 50% chance to win
    variance = mean * (1 - 0.5)
    standard_deviation = int(floor(sqrt(variance)))

    random_players = [RandomPlayer(name=i) for i in range(4)]
    tournament = Tournament(random_players, point_limit=point_limit, seed=1)

    team_wins = [0, 0]

    start = timer()

    for _ in range(number_of_tournaments):
        tournament.play()
        team_wins[tournament.get_winning_team().team_index] += 1

    end = timer()
    print("\nTo run {0} tournaments it took {1:.2f} seconds.".format(number_of_tournaments, end - start))

    difference = abs(team_wins[0] - team_wins[1])
    print("Difference: ", difference)
    print("Team 1: ", team_wins[0])
    print("Team 2: ", team_wins[1])
    assert difference in range(0, 4 * standard_deviation)  # if a harder constraint is required replace 4 by 2 or 1
