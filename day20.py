from __future__ import annotations 
from pathlib import Path 
from typing import List, Dict, NamedTuple 
from collections import defaultdict 

STR_TO_INT = {"#" : 1, "." : 0}
INT_TO_STR = {1 : "#", 0 : "."}

class Point(NamedTuple):
    x : int 
    y : int 

class Map:
    def __init__(self, inf_val : int = 0):
        self.rows = 0
        self.cols = 0
        self.inf_val = inf_val 
        self.mapper : Dict[Point, int] = defaultdict(lambda : inf_val)
        self.algo : List[int] = []
        
    
    def get_avg_val(self, p : Point) -> int:
        bitstring = ""
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                bitstring += str(self.mapper[Point(p.x + dx, p.y + dy)])
                # mapper is defaultdict.. gives either 0 or 1
        return self.algo[int(bitstring, 2)] 
        
    def next_map(self, step : int):
        inf_val = 0
        if not step % 2:
            if self.algo[0] == 0:
                inf_val = 0
            elif self.algo[0] == 1 and self.algo[-1] == 0:
                inf_val = 1
            else: 
                ValueError(f"your algo input is fishy, can't have 1 on both 0 and max positions")
            # elif self.algo[0] == 1 and self.algo[-1] == 1:
            # note the above cond wont be possible -- coz after step0 there will be infinite lights always
        next_m = Map(inf_val = inf_val) 
        # we are setting the next inf val to be 1 -- if self.algo[0] == 1 ... 
        # and in next iteratoin it will be zero ... and so on...
        next_m.rows = self.rows + 2 # padding
        next_m.cols = self.cols + 2
        next_m.algo = self.algo 
        for ridx in [-1] + list(range(self.rows + 1)):
            for cidx in [-1] + list(range(self.cols + 1)):
                p = Point(ridx, cidx)
                p_new = Point(ridx + 1, cidx + 1)
                next_m.mapper[p_new] = self.get_avg_val(p)
        return next_m 

    @classmethod 
    def parse(cls, lines : str, algo : List[int]) -> Map:
        m = Map() 
        m.rows, m.cols = len(lines.split("\n")), len(lines.split("\n")[0])
        m.algo = algo 
        for ridx, line in enumerate(lines.split("\n")):
            for cidx, s in enumerate(line):
                m.mapper[Point(ridx, cidx)] = STR_TO_INT[s]
        return m

    def print_map(self) -> str:
        printer = ""
        for ridx in range(self.rows):
            for cidx in range(self.cols):
                printer += INT_TO_STR[self.mapper[Point(ridx, cidx)]]
            printer += "\n"
        return printer 

    @property
    def lit_pixels(self) -> int:
        return sum(self.mapper.values())

def read_inp(inp : str, total_steps : int) -> int:
    ans = 0
    algo, lines = inp.split("\n\n")
    algo = [STR_TO_INT[s] for s in algo]
    m = Map.parse(lines, algo)
    maps : List[Map] = [m]
    print(maps[-1].lit_pixels)
    for step in range(total_steps):
        maps.append(maps[-1].next_map(step = step))
        # print(maps[-1].print_map())
        print(maps[-1].lit_pixels)
    return maps[-1].lit_pixels

TEST = Path("day20_test.txt").read_text()
assert read_inp(TEST, total_steps = 2) == 35

if __name__ == "__main__":
    datfile = Path("day20.txt").read_text()
    ans = read_inp(datfile, total_steps = 50) 