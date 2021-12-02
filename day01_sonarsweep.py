from pathlib import Path

def depth_inc(depths: list[int], jump: int = 1) -> int:
    cnt = 0
    for d1, d2 in zip(depths, depths[jump:]):
        if d2 > d1: cnt += 1

    return cnt

TEST = """199
200
208
210
200
207
240
269
260
263"""
TEST = [int(x) for x in TEST.split("\n")]
assert depth_inc(TEST) == 7
assert depth_inc([1,2,3]) == 2
assert depth_inc([1,2,1]) == 1
assert depth_inc(TEST, 3) == 5

if __name__ == "__main__":
    datfile_1 = Path("day01_p1.txt") # same for p2
    inp = [int(x) for x in datfile_1.read_text().split("\n")]
    ans = depth_inc(inp)

    ans2 = depth_inc(inp, jump = 3)

    print(ans, ans2)
