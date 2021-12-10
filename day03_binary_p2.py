from pathlib import Path
# import bisect

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

def get_b(low, high, idx, L):
    JUMP = L - 1
    b = low
    while JUMP > 0:
        while JUMP + b < high and inp[JUMP + b][idx] == "0":
            b += JUMP
        JUMP //= 2
    return b

if __name__ == "__main__":
    datfile = Path("day03_p1.txt").read_text()
    inp : list[str] = sorted(datfile.split("\n"))
    Path("day03_sorted.txt").write_text("\n".join(inp))
    # inp : list[str] = sorted(TEST.split("\n"))
    # gotta do bin search-ish 
    low, high = 0, len(inp) - 1
    oxy, scrub = 0, 0
    idx = 0

    k = len(inp[0]) # length of any string
    while idx < k:
        print(idx, low, high)
        if high == low:
            break

        if inp[low][idx] == inp[high][idx]:
            # range has same digit throughout (regretting this bin search code)
            idx += 1
            continue

        med = (low + high + 1) // 2
        if inp[med][idx] == "0":
             # [low, med + ___]
            # search for the last "0"
            high = get_b(low, high, idx, len(inp))
        else:
            # [med - ___, high]
            low = get_b(low, high, idx, len(inp)) + 1
        
        idx += 1
    # print(idx, low, high)

    oxy = int(inp[(low + high + 1) // 2], 2)

    print("*****")
    idx = 0
    low, high = 0, len(inp) - 1
    while idx < k:
        print(idx, low, high)
        if high == low:
            break
        if inp[low][idx] == inp[high][idx]:
            # range has same digit throughout (regretting this bin search code)
            idx += 1
            continue 
        med = (low + high + 1) // 2
        if inp[med][idx] == "0":
             # [med + ___, high]
            # search for the last "0"
            low = get_b(low, high, idx, len(inp)) + 1
        else:
            # [low, med - ___]
            high = get_b(low, high, idx, len(inp))
        idx += 1

    scrub = int(inp[(low + high) // 2], 2)

    print(oxy, scrub, oxy * scrub)