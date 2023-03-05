from schieber.player import Player
from itertools import count


def test_base_player_counter():
    Player.class_counter = count(0)
    base_player = [Player(name=i) for i in range(4)]

    for i, player in enumerate(base_player):
        assert player.name == i
