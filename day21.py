from pathlib import Path
from itertools import cycle, product
from typing import List, Iterable, DefaultDict
from collections import defaultdict, Counter
from copy import deepcopy

TEST = """Player 1 starting position: 4
Player 2 starting position: 8"""

class DiceGame:
    def __init__(self, sides : int = 100):
        self.sides = sides 
        self.deterministic_die = cycle(range(1, self.sides + 1)) # can iterate over this
        # the type of cycle() is ____
        self.die_rolls = 0
        self.player_scores : defaultdict[int, int] = defaultdict(int) 

    def deterministic_die_roll(self) -> List[int]:
        """yields 3 consecutive numbers between 1-100"""
        self.die_rolls += 3
        return [self.deterministic_die.__next__() for _ in range(3)]

    @staticmethod
    def next_player(current_player : int) -> int:
        """returns next player in a 2 game setup"""
        return (current_player + 1) % 2 # could just make a cycle(range(1,3)) too
        
    def play_game(self, p_start : List[int], deterministic : bool = True, verbose : bool = True) -> int:
        """returns when the score of any player hits 1000
        Player positions can move from 1-10; hence %10
        """
        current_player = 0 # 0 --> Player 1; 1 --> Player 2
        while all(i < 1000 for i in self.player_scores.values()):
            p_start[current_player] = (p_start[current_player] + sum(self.deterministic_die_roll()) - 1) % 10 + 1
            self.player_scores[current_player] += p_start[current_player]
            current_player = self.next_player(current_player)
        
        # if we broke out of loop, current player has lost [previous player won]
        if verbose:
            print("Player Scores:", self.player_scores)
            print("Die rolls:", self.die_rolls)
            print("Losing Player:", current_player)
        
        return self.player_scores[current_player] * self.die_rolls

def print_matrix(matrix : List[List[int]]) -> None:
    for row in matrix:
        print(" ".join(str(x).rjust(3) for x in row))

def count_universes(matrix : List[List[int]]) -> int:
    ans = 0
    for row in matrix:
        ans += sum(row)
    return ans

def quantum_die(p_start : List[int], score : int) -> int:
    """universe splits; must be one of those metaverse companies that sponsored this nonsense"""
    # trying some DP -- this is init
    transition_matrix = [[0] * 11 for _ in range(11)] # to enable 1-indexing
    for start in range(1, 11):
        new_pos = [
            (start + a + b + c  - 1) % 10 + 1
            for a, b, c in product(range(1, 4), repeat = 3)
        ]
        for k, v in Counter(new_pos).items():
            transition_matrix[start][k] = v

    score_pos_mat1 = [[0] * 11 for _ in range(score + 1)]
    score_pos_mat2 = [[0] * 11 for _ in range(score + 1)] 
    score_pos_mat1[0][p_start[0]] += 1 
    score_pos_mat2[0][p_start[1]] += 1

    score_pos : dict[int, List[List[int]]] = {0 : score_pos_mat1, 1 : score_pos_mat2}

    # print_matrix(transition_matrix)
    current_player = 0
    c1, c2 = count_universes(score_pos[0]), count_universes(score_pos[1])
    ans = {0 : 0, 1 : 0}
    flag = 0
    while True:
        # need n3 loop matmul
        new_mat = [[0] * 11 for _ in range(score + 2)]
        for s in range(0, score + 1):
            for final_pos in range(1, 11):
                for curr_pos in range(1, 11):
                    adder = score_pos[current_player][s][curr_pos] * transition_matrix[curr_pos][final_pos] * c1 // c2
                    if s + final_pos >= score: 
                        ans[current_player] += adder
                        continue
                    new_mat[s + final_pos][final_pos] += adder
        score_pos[current_player] = new_mat

        print("*****", ans[0], ans[1])
        # print_matrix(score_pos[0])
        # print("num universe", count_universes(score_pos[0]))

        next_player = (current_player + 1) % 2

        if count_universes(score_pos[current_player]) == 0 or count_universes(score_pos[next_player]) == 0:
            break

        c1, c2 = count_universes(score_pos[current_player]), count_universes(score_pos[next_player])
        # print("current player ", current_player + 1)
        current_player = next_player
    return ans[0]


def read_inp(inp : str, quantum = False) -> int:
    vals = [int(line.split(": ")[1]) for line in inp.split("\n")]
    if quantum:
        return quantum_die(p_start = vals, score = 21)

    game = DiceGame()
    ans = game.play_game(p_start = vals)

    return ans 

assert read_inp(TEST) == 739785
assert read_inp(TEST, quantum = True) == 444356092776315

if __name__ == "__main__":
    datfile = Path("day21.txt").read_text()
    print(read_inp(datfile))

    print(read_inp(datfile, quantum = True))
    pass 
