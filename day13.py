from pathlib import Path
from dataclasses import dataclass
from typing import NamedTuple, List

TEST = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

# @dataclass
class Point(NamedTuple):
    x: int
    y: int

    def __repr__(self):
        return f"Point({self.x}, {self.y})" 
        # this would've been rendered by NamedTuple

class Grid:
    def __init__(self):
        # self.rows = 0
        # self.cols = 0 -- no point.. since they keep on changing
        self.points : set[Point] = set() 

    def process_folds(self, lines : str) -> List[int]:
        ans = []
        for line in lines.split("\n"):
            # print(line)
            direction, val = line.split("=")
            val = int(val)
            print(direction[-1], val)
            if direction[-1] == "x":
                self.points = set([
                    Point(2 * val - p.x, p.y) if p.x > val else p for p in self.points 
                ])
            elif direction[-1] == "y":
                self.points = set([
                    Point(p.x, 2 * val - p.y) if p.y > val else p for p in self.points 
                ])
            else:
                raise ValueError(f"Wrong direction {direction[-1]}; direction should be x or y")

            ans.append(len(self.points))
        
        print(self)

        return ans

    def __str__(self) -> str:
        min_row = min(p.x for p in self.points)
        max_row = max(p.x for p in self.points)
        min_col = min(p.y for p in self.points)
        max_col = max(p.y for p in self.points)

        out = ""
        for y in range(min_col, max_col + 1):
            for x in range(min_row, max_row + 1):
                if Point(x, y) in self.points: out += "#"
                else: out += "."
            out += "\n"
        return out

    @classmethod
    def parse(cls, points : str) -> "Grid":
        grid = cls()
        for point in points.split("\n"):
            x, y = [int(i) for i in point.split(",")]
            grid.points.add(Point(x, y))

        return grid

def read_inp(inp : str) -> List[int]:
    points, lines = inp.split("\n\n")
    grid = Grid.parse(points)
    ans = grid.process_folds(lines)
    # ans = len(grid.points)
    # print(ans)
    return ans

assert read_inp(TEST) == [17, 16]

if __name__ == "__main__":
    datfile = Path("day13.txt").read_text()
    ans = read_inp(datfile)
    print(ans)

