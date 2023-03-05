import pytest

from schieber.rules.deck import Deck

from schieber.rules.trumpf import Trumpf

from schieber.player.random_player import RandomPlayer

from schieber.game import Game, get_player_index
from schieber.team import Team


@pytest.mark.parametrize("start_key, last_key", [
    (0, 3),
    (1, 0),
    (2, 1),
    (3, 2),
])
def test_get_player_key(start_key, last_key):
    key = 0
    count = 0
    for i in get_player_index(start_key):
        key = i
        count += 1
    assert count == 3
    assert last_key == key


def test_game():
    random_players = [RandomPlayer(name=i) for i in range(4)]
    team_1 = Team(players=[random_players[0], random_players[1]])
    team_2 = Team(players=[random_players[1], random_players[2]])
    teams = [team_1, team_2]
    game = Game(teams=teams, point_limit=1500)
    game.play()

    for player in random_players:
        assert len(player.cards) == 0


def test_reset_points():
    random_players = [RandomPlayer(name=i) for i in range(4)]
    team_1 = Team(players=[random_players[0], random_players[1]])
    team_2 = Team(players=[random_players[1], random_players[2]])
    teams = [team_1, team_2]
    game = Game(teams=teams, point_limit=1500)
    game.play()

    game.reset_points()

    for team in game.teams:
        assert team.points == 0


@pytest.mark.parametrize("start_key, next_key", [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
])
def test_get_player_index(start_key, next_key):
    generator = get_player_index(start_index=start_key)
    current_key = next(generator)
    assert current_key == next_key


@pytest.mark.parametrize("trumpf", list(Trumpf)[:6])
def test_add_points(trumpf):
    round_points = 152
    deck = Deck()
    random_players = [RandomPlayer(name=i) for i in range(4)]
    team_1 = Team(players=[random_players[0], random_players[1]])
    team_2 = Team(players=[random_players[1], random_players[2]])
    teams = [team_1, team_2]
    game = Game(teams=teams)
    game.trumpf = trumpf
    game.add_points(team_index=0, cards=deck.cards, last=False)
    assert team_1.points == round_points * game.counting_factors[trumpf]
    game.counting_factors = {Trumpf.ROSE: 1, Trumpf.EICHEL: 1, Trumpf.SCHELLE: 1, Trumpf.SCHILTE: 1,
                             Trumpf.OBE_ABE: 1, Trumpf.UNDE_UFE: 1}
    game.add_points(team_index=1, cards=deck.cards, last=False)
    assert team_2.points == round_points
