from pathlib import Path
# need to compute median essentially; find x such that min |x - x_i | over all i. 

# https://www.reddit.com/r/adventofcode/comments/rawxad/2021_day_7_part_2_i_wrote_a_paper_on_todays/
# L1 + L2 norm minimizer (only for integers).. we need to look for fewer terms (like 3-4 maybe)
# mean + 0.5, mean - 0.5 .. whatever integers lie in between 

TEST = "16,1,2,0,4,2,7,1,2,14"

# L1 + L2 Norm for Part 2
def find_ans(inp: str) -> int:
    inp = sorted(int(x) for x in inp.split(","))
    get_cost = lambda X, m: sum([
        (abs(x - m))*(abs(x - m) + 1)//2 
        for x in X
    ])
    return min([get_cost(inp, m) for m in range(min(inp), max(inp)+1)])

# brute force
def find_median(inp : str) -> int:
    inp = sorted([int(x) for x in inp.split(",")])

    get_sum = lambda X, m: sum([abs(x - m) for x in X])
    L = len(inp)
    ans = 0
    if L % 2:
        median = inp[L // 2]
        ans = get_sum(inp, median)
    else:
        med_1, med_2 = inp[L // 2 ], inp[L // 2 + 1]
        ans_1, ans_2 = get_sum(inp, med_1), get_sum(inp, med_2)    
        ans = min(ans_1, ans_2)
    
    return ans 

# print(sorted([int(x) for x in TEST.split(",")]))
assert find_median(TEST) == 37
assert find_ans(TEST) == 168

if __name__ == "__main__":
    datfile = Path("day07.txt").read_text()
    print(find_median(datfile))
    print(find_ans(datfile))