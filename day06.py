from pathlib import Path
from collections import deque, defaultdict

TEST = "3,4,3,1,2"

class PopStats:
    def __init__(self, rate : int) -> None:
        self.rate = rate
        self.count_1 = defaultdict(int) # old fish dynamics
        self.count_2 = defaultdict(int) # new fish dynamics
        self.r1 = rate - 1
        self.r2 = rate + 1
        self.max_T = 500

    def build_pop(self):
        for t in range(self.max_T):
            if t <= self.r1: self.count_1[t] = 1
            if t > self.r1: self.count_1[t] = self.count_1[t - self.r1 - 1] + self.count_2[t - self.r1- 1]
            
            if t <= self.r2: self.count_2[t] = 1
            if t > self.r2: self.count_2[t] = self.count_1[t - self.r2 - 1] + self.count_2[t - self.r2 - 1]

    def get_count(self, stage : int, T : int) -> int: 
        if T <= stage: return 1
        else: return self.count_1[T - stage - 1] + self.count_2[T - stage - 1]

def get_popu_dp(inp : str, T : int, rate : int) -> int:
    fishes = [int(x) for x in inp.split(",")]
    ans = 0
    pops = PopStats(rate = rate)
    pops.build_pop()
    # print(pops.count_1, pops.count_2)

    for fish in fishes: 
        # print(ans)
        ans += pops.get_count(fish, T)
    print(ans)
    return ans

# brute force; bad
def get_popu(inp : str, T : int, rate : int) -> int:
    fishes = deque([int(x) for x in inp.split(",")])

    t = 0
    while t < T:
        print(t)
        curr_pop = len(fishes)
        idx = 0
        while idx < curr_pop:
            # print(fishes)
            curr_fish_time = fishes.pop()
            if curr_fish_time == 0:
                fishes.appendleft(rate - 1)
                fishes.appendleft(rate + 1)
            else:
                fishes.appendleft(curr_fish_time - 1)
            idx += 1

        t += 1

    # print(len(fishes))
    return len(fishes)


# assert get_popu(TEST, 1, rate = 7) == 5
# assert get_popu(TEST, 2, rate = 7) == 6
# assert get_popu(TEST, 18, rate = 7) == 26
# assert get_popu(TEST, 80, rate = 7) == 5934

# assert get_popu_dp(TEST, 1, rate = 7) == 5
assert get_popu_dp(TEST, 2, rate = 7) == 6
assert get_popu_dp(TEST, 18, rate = 7) == 26
assert get_popu_dp(TEST, 80, rate = 7) == 5934
assert get_popu_dp(TEST, 256, rate = 7) == 26984457539

if __name__ == "__main__":
    datfile = Path("day06.txt").read_text()
    print(get_popu_dp(datfile, 256, rate = 7))

# later found a much better and concise code: https://www.youtube.com/watch?v=sRMfENjvTnE
