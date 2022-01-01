from __future__ import annotations
from pathlib import Path
from typing import NamedTuple, Tuple

class Point(NamedTuple):
    x: int
    y: int 

class CucumberMap:
    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.map_item : dict[Point, str] = {}
        self.num_steps = 0
        self.movement = False
    
    def get_neighbors(self, p : Point) -> Tuple[Point, Point]:
        p_h = Point(p.x, (p.y + 1) % self.cols)
        p_v = Point((p.x + 1) % self.rows, p.y)
        return p_h, p_v 

    def is_free(self, p : Point) -> bool:
        return self.map_item[p] == "."

    def move(self, p1 : Point, p2 : Point) -> None:
        """move from p1 to p2; p1 gets free"""
        self.map_item[p2] = self.map_item[p1]
        self.map_item[p1] = "."

    def step(self) -> None:
        # first reset
        move_store : list[tuple[Point, Point]]= []
        self.movement = False 
        for p in self.map_item.keys():
            p_h, _ = self.get_neighbors(p)
            if self.map_item[p] == ">" and self.is_free(p_h):
                # print(p, p_h)
                move_store.append((p, p_h))
        
        if len(move_store): self.movement = True 
        while move_store: self.move(*move_store.pop())

        for p in self.map_item.keys():
            _, p_v = self.get_neighbors(p)
            if self.map_item[p] == "v" and self.is_free(p_v):
                move_store.append((p, p_v))

        if len(move_store): self.movement = True 
        while move_store: self.move(*move_store.pop())

        self.num_steps += 1
        
    @classmethod
    def parse(cls, inp : str) -> CucumberMap:
        cmap = cls()
        cmap.rows = len(inp.split("\n"))
        cmap.cols = len(inp.split("\n")[0])
        
        for ridx, line in enumerate(inp.split("\n")):
            for cidx, s in enumerate(line):
                    cmap.map_item[Point(ridx, cidx)] = s 

        return cmap 

    def print_map(self):
        for ridx in range(self.rows):
            for cidx in range(self.cols):
                p = Point(ridx, cidx)
                print(self.map_item[p].rjust(2), end = "")
            print("")

# TEST = "...>>>>>..."
# cm = CucumberMap.parse(TEST)
# cm.step()
# cm.step()
# cm.print_map()

# TEST_2 = """..........
# .>v....v..
# .......>..
# .........."""
# cm = CucumberMap.parse(TEST_2)
# cm.step()
# cm.print_map()

TEST_3 = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

def read_inp(inp : str) -> int:
    cm = CucumberMap.parse(inp)
    while True:
        cm.step()
        if not cm.movement: break 

        print(cm.num_steps)
    return cm.num_steps

assert read_inp(TEST_3) == 58

if __name__ == "__main__":
    pass
    datfile = Path("day25.txt").read_text()
    print(read_inp(datfile))
