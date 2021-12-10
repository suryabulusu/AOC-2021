from pathlib import Path 
from collections import defaultdict

TEST = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

def read_input(inp : str) -> int:
    pathcnt : dict[tuple[int, int], int] = defaultdict(int)
    for line in inp.split("\n"):
        p1, p2 = line.split(" -> ")
        x1, y1 = [int(i) for i in p1.split(",")]
        x2, y2 = [int(i) for i in p2.split(",")]
        
        if x1 == x2: # vertical line
            if y1 > y2: y1, y2 = y2, y1 
            for y in range(y1, y2 + 1): pathcnt[(x1, y)] += 1
        elif y1 == y2: # horizontal line
            if x1 > x2: x1, x2 = x2, x1
            for x in range(x1, x2 + 1): pathcnt[(x, y1)] += 1
        else: # diagonal line - not swapping now coz not in mood
            if x1 > x2 and y1 > y2: 
                for m in range(x1 - x2 + 1): pathcnt[(x2 + m, y2 + m)] += 1
            elif x2 > x1 and y2 > y1:
                for m in range(x2 - x1 + 1): pathcnt[(x1 + m, y1 + m)] += 1
            elif x2 > x1 and y2 < y1:
                for m in range(x2 - x1 + 1): pathcnt[(x1 + m, y1 - m)] += 1
            elif x2 < x1 and y2 > y1:
                for m in range(x1 - x2 + 1): pathcnt[(x1 - m, y1 + m)] += 1

    ans = 0
    for k, v in pathcnt.items(): 
        if v >= 2: ans += 1

    print(ans)
    return ans
    # pass

assert read_input(TEST) == 12
assert read_input("1,2 -> 2,2") == 0


if __name__ == "__main__":
    datfile = Path("day05.txt").read_text()
    read_input(datfile)