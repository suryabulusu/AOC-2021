from __future__ import annotations
from pathlib import Path
from typing import NamedTuple

# Notice that: we achieved two things by having this cumbersome structure
# 1. Easy to add new updates when dealing with part2 (I had to make 3 changes max)
# 2. Pedagogical -- Revise ideas of NamedTuple, Classes
# (Probably would've taken fewer lines (and fewer changes for part2) with simple code too)

TEST = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""

class engine_move(NamedTuple):
    movement: str 
    amount: int

    @staticmethod
    def from_line(line: str) -> engine_move:
        m, a = line.split()
        return engine_move(movement=m, amount=int(a))

class Engine:
    def __init__(self, moves: list(engine_move)) -> None:
        self.moves = moves
        self.horiz = 0
        self.vert = 0
        self.aim = 0 # part2 
        self.idx = 0

    def execute_move(self) -> None:
        m, a = self.moves[self.idx]

        if m == "forward":
            self.horiz += a 
            self.vert += (self.aim * a) # part2
        elif m == "down":
            # self.vert += a
            self.aim += a
        elif m == "up":
            # self.vert -= a
            self.aim -= a 
        else:
            raise ValueError(f"unknown move: {m}")

    def execute(self) -> None:
        while self.idx < len(self.moves):
            self.execute_move() # very cumbersome way to do things
            self.idx += 1
            # idea is to learn classes; pedagogy


if __name__ == "__main__":
    datfile_1 = Path("day02_p1.txt")

    input = TEST
    inp = [engine_move.from_line(line) for line in input.split("\n")]
    submarine = Engine(inp)
    submarine.execute()
    print(submarine.horiz, submarine.vert)
    assert submarine.horiz == 15
    # assert submarine.vert == 10
    assert submarine.vert == 60 # part2
    
    input = datfile_1.read_text()
    inp = [engine_move.from_line(line) for line in input.split("\n")]
    submarine = Engine(inp)
    submarine.execute()
    print(submarine.horiz * submarine.vert)
