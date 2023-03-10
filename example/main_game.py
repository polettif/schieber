from schieber.game import Game
from schieber.players.random_player import RandomPlayer
from schieber.team import Team

if __name__ == "__main__":
    random_players = [RandomPlayer(name=i) for i in range(4)]
    team_1 = Team(players=[random_players[0], random_players[1]])
    team_2 = Team(players=[random_players[1], random_players[2]])
    game = Game([team_1, team_2], seed=1)
    game.play()
