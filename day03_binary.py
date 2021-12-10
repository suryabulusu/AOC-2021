from pathlib import Path
from collections import defaultdict

TEST = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

if __name__ == "__main__":
    datfile = Path("day03_p1.txt").read_text()
    # datfile = TEST
    inp_dic : dict[int, int] = defaultdict(int)
    linecnt = 0
    for line in datfile.split("\n"):
        linecnt += 1
        for idx, i in enumerate(line): inp_dic[idx] += int(i)
    linelen = len(line)
    
    gamma = ["1" if val > linecnt // 2 else "0" for _, val in inp_dic.items()]
    gamma = int("".join(gamma), 2)
    eps = gamma ^ (2**linelen - 1)

    print(gamma, eps, gamma * eps)
        

    # print(inp[0], inp.shape)