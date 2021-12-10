# find the lowest points
from pathlib import Path
from collections import defaultdict

TEST = """2199943210
3987894921
9856789892
8767896789
9899965678"""

def read_inp(inp : str) -> int:
    M, N = len(inp.split("\n")), len(inp.split("\n")[0]) # shape
    inp = [
        [int(i) for i in line]
        for line in inp.split("\n")
    ]

    valid_point = lambda M, N, i, j: 0 <= i < M and 0 <= j < N

    ans = 0
    # ugly looking code..
    low_points = []
    for m_idx in range(M):
        for n_idx in range(N):
            val = inp[m_idx][n_idx]
            flag = 0
            for a in [-1, 0, 1]:
                for b in [-1, 0, 1]:
                    if valid_point(M, N, m_idx + a, n_idx + b):
                        if inp[m_idx + a][n_idx + b] < val: 
                            flag = 1; break 
                if flag == 1: break 
            # print(m_idx, n_idx, flag, val)
            if not flag:
                low_points.append((m_idx, n_idx)) 
                ans += val + 1

    # finding basins
    # for some reason diagonal points not accepted here
    basin_vals = []
    for m_idx, n_idx in low_points:
        val = 0
        stack : list[tuple[int, int]] = [(m_idx, n_idx)] 
        visited : dict[tuple[int, int], bool] = defaultdict(bool)
        while stack:
            a, b = stack.pop()
            if visited[(a, b)]: continue
            visited[(a, b)] = True 
            
            if inp[a][b] != 9:
                val += 1
                for (i, j) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    if not valid_point(M, N, i + a, j + b): continue # regretting why I didn't make a class
                    stack.append((i + a, j + b))
        
        basin_vals.append(val)

    # print(low_points)
    # print(basin_vals)
    
    basin_vals = sorted(basin_vals, reverse = True)
    ans_2 = basin_vals[0] * basin_vals[1] * basin_vals[2] 

    print(ans_2)

    return ans, ans_2

assert read_inp(TEST) == (15, 1134)

if __name__ == "__main__":
    datfile = Path("day09.txt").read_text()
    print(read_inp(datfile))
    pass
