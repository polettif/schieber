from schieber.game import Game
from schieber.players.random_player import RandomPlayer
from schieber.team import Team
from schieber.tournament import Tournament

if __name__ == "__main__":
    random_players = [RandomPlayer(name=i) for i in range(4)]
    tournament = Tournament(random_players)
    tournament.play()

