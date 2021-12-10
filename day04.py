from __future__ import annotations
from pathlib import Path
from collections import defaultdict
# from typing import NamedTuple 

TEST = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

class Board:
    def __init__(self, board : str, bingo_size : int):
        self.bingo_size = bingo_size 
        self.done = False 
        self.position = {}
        self.unmarked = 0
        self.read_string(board)
        self.rowsum = defaultdict(int)
        self.colsum = defaultdict(int)

    def read_string(self, board : str) -> dict[int, tuple[int, int]]:
        for ridx, row in enumerate(board.split("\n")):
            for cidx, val in enumerate(row.split()):
                self.position[int(val)] = (ridx, cidx)
                self.unmarked += int(val)

    def play(self, marker : int) -> None:
        if marker in self.position:
            r, c = self.position[marker]
        else: return
        self.unmarked -= marker 
        self.rowsum[r] += 1
        self.colsum[c] += 1

        if self.rowsum[r] == self.bingo_size or self.colsum[c] == self.bingo_size: #BINGO!
            self.done = True   
            self.ans = marker * self.unmarked


def read_input(inp: str) -> list[Board]:
    markers, *boards =  inp.split("\n\n")
    markers = [int(x) for x in markers.split(",")]
    boards = [Board(b, bingo_size = 5) for b in boards] # get the objects
    board_cnt = len(boards)

    flag = 0
    bidx_done = []
    for marker in markers:
        for bidx, board in enumerate(boards):
            board.play(marker)
            if board.done: 
                # print(board.ans)
                if bidx not in bidx_done: flag += 1
                bidx_done.append(bidx)
                if flag == board_cnt: 
                    print(bidx, board.ans)
                    return boards
                    # break 
                # continue 

    return boards
    
boards = read_input(TEST)

# tests for Part 1
# assert boards[0].done == False 
# assert boards[1].done == False 
# assert boards[2].done == True
# assert boards[2].unmarked == 188
# assert boards[2].ans == 188*24


if __name__ == "__main__":
    datfile = Path("day04.txt").read_text()
    boards = read_input(datfile)