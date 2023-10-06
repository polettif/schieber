from schieber.game import Game
from schieber.players.random_player import RandomPlayer
from schieber.team import Team
from schieber.tournament import Tournament
import math as m, re

if __name__ == "__main__":
    board = list(open('D:/Nextcloud/advent-of-code/debug.txt'))
    chars = {(r, c): [] for r in range(6) for c in range(140)
             if board[r][c] not in '01234566789.'}

    for r, row in enumerate(board):
        for n in re.finditer(r'\d+', row):
            edge = {(r, c) for r in (r - 1, r, r + 1)
                    for c in range(n.start() - 1, n.end() + 1)}

            for o in edge & chars.keys():
                chars[o].append(int(n.group()))

    print(sum(sum(p) for p in chars.values()),
          sum(m.prod(p) for p in chars.values() if len(p) == 2))
