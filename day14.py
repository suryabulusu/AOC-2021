from pathlib import Path
from collections import Counter, defaultdict

TEST = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

def read_inp2(inp : str, steps : int) -> int:
    template, lines = inp.split("\n\n")
    rules : dict[str, str] = {}
    pair_counts : defaultdict[str, int] = defaultdict(int)
    char_cnt : defaultdict[str, int] = defaultdict(int)

    for line in lines.split("\n"):
        pair, c = line.split(" -> ")
        rules[pair] = c 

    # init state
    for t1, t2 in zip(template, template[1:]): 
        pair_counts[t1 + t2] += 1
    for c in template: char_cnt[c] += 1

    for t in range(steps):
        temp = defaultdict(int)
        for k, v in pair_counts.items():
            if not v: continue
            c = rules[k]
            char_cnt[c] += v
            a, b = k
            temp[a + c] += v 
            temp[c + b] += v 
            # temp[k] = 0
        pair_counts = temp 
    print(char_cnt)
    return max(char_cnt.values()) - min(char_cnt.values())

# brute force
def read_inp(inp : str, steps : int) -> int:
    template, lines = inp.split("\n\n")

    rules : dict[str, str] = {}

    for line in lines.split("\n"):
        pair, c = line.split(" -> ")
        rules[pair] = c 

    for t in range(steps):
        # print(t)
        new_temp = ""
        for a, b in zip(template, template[1:]):
            if a+b in rules: new_temp += (a + rules[a+b])
            else: new_temp += a
        new_temp += template[-1]
        # print(new_temp)
        template = new_temp

    d : dict[str, int] = dict(Counter(template))

    print(max(d.values()) - min(d.values()))
    return max(d.values()) - min(d.values())

assert read_inp(TEST, steps = 10) == 1588
print(read_inp2(TEST, steps = 10))
# assert read_inp2(TEST, steps = 1) == 1588


if __name__ == "__main__":
    datfile = Path("day14.txt").read_text()
    steps = 40
    ans = read_inp2(datfile, steps)
    print(ans)
