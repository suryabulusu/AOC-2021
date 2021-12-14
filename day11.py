from pathlib import Path
from typing import List, Any, Tuple

TEST = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
TEST_SMALL = """11111
19991
19191
19991
11111"""

class LightGrid:
    def __init__(self, rows : int = 10, cols : int = 10):
        self.rows = rows
        self.cols = cols 
        self.lights : list[list[int]] = []
        self.flashed : list[list[bool]] = [[False] * self.cols for _ in range(self.rows)]

    def parse(self, inp : str) -> None:
        self.lights = [
            [int(x) for x in line]
            for line in inp.split("\n")
        ]
        # print(len(self.lights), len(self.lights[0]))
    
    def neighbors(self, r_idx : int, c_idx : int) -> List[Tuple[int, int]]:
        neigh = []
        for dr, dc in [(-1, -1), (-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (-1, 1), (1, -1)]:
            if 0 <= r_idx + dr < self.rows and 0 <= c_idx + dc < self.cols:
                neigh.append((r_idx + dr, c_idx + dc))
        # should have done yield .. but few points so chalega
        # print(neigh)
        return neigh

    def inc_val(self, r_idx : int, c_idx : int) -> None:
        # print(r_idx, c_idx)
        self.lights[r_idx][c_idx] += 1
    
    def get_val(self, r_idx : int, c_idx : int) -> int:
        return self.lights[r_idx][c_idx]

    def set_flash(self, r_idx : int, c_idx : int) -> None:
        self.flashed[r_idx][c_idx] = True

    def printer(self, arr : List[List[Any]]) -> None:
        for line in arr:
            print(" ".join(str(i).rjust(3) for i in line))
        print("\n")

    def step(self) -> Tuple[int, bool]:
        flashes = []
        for r_idx in range(self.rows):
            for c_idx in range(self.cols):
                self.inc_val(r_idx, c_idx)
                if self.get_val(r_idx, c_idx) > 9: 
                    flashes.append((r_idx, c_idx))
                    self.set_flash(r_idx, c_idx)
                    # self.printer(self.flashed)

        while flashes:
            # self.printer()
            # print(flashes)
            # self.printer(self.flashed)
            # self.printer(self.lights)
            i, j = flashes.pop()
            # check neighbors only if it flashes
            for a, b in self.neighbors(i, j):
                self.inc_val(a, b)
                if self.get_val(a, b) > 9 and not self.flashed[a][b]:
                    flashes.append((a, b))
                    self.set_flash(a, b)

        # self.printer(self.flashed)
        # self.printer(self.lights)
        ans, sync = self.count_flashes_and_reset()

        return ans, sync

    def count_flashes_and_reset(self) -> Tuple[int, bool]:
        ans = 0
        for r_idx in range(self.rows):
            for c_idx in range(self.cols):
                if self.flashed[r_idx][c_idx]:
                    ans += 1
                    self.flashed[r_idx][c_idx] = False 
                    self.lights[r_idx][c_idx] = 0
        
        sync = False 
        if ans == self.rows * self.cols: sync = True

        
        return ans, sync

def read_inp(inp : str, rows : int, cols : int, steps : int) -> int:
    grid = LightGrid(rows = rows, cols = cols)   
    grid.parse(inp)
    ans = 0
    for t in range(steps):
        inc, sync = grid.step()

        # if t == 193: grid.printer(grid.lights)

        if sync: print(t)
        ans += inc 
    
    # print(grid.printer(grid.lights))
    print(ans)
    return ans

assert read_inp(TEST_SMALL, 5, 5, 1) == 9
assert read_inp(TEST, 10, 10, 100) == 1656

if __name__ == "__main__":
    datfile = Path("day11.txt").read_text()
    # ans = read_inp(datfile, 10, 10, 1000)
    # print(ans)