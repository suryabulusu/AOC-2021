from pathlib import Path 
from typing import Tuple

TEST = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

class SyntaxCheck:
    def __init__(self, points, auto_points):
        self.points = points
        self.auto_points = auto_points
        self.pairs = {"(" : ")", "[" : "]", "{" : "}", "<" : ">"}

    def get_score(self, line : str, verbose : bool) -> Tuple[int, int]:
        stack = []
        corrupt_score, auto_score = 0, 0
        corrupted = False
        for c in line:
            if c in self.pairs.keys():
                stack.append(c)
            else:
                in_stack = stack.pop()
                if self.pairs[in_stack] != c:
                    if verbose: print(f"Expected {self.pairs[in_stack]}, but found {c} instead.")
                    corrupt_score = self.points[c]
                    corrupted = True 
                    break 

        if corrupted == False:
            for s in stack[::-1]:
                # reverse order
                auto_score *= 5
                auto_score += self.auto_points[self.pairs[s]]

        return corrupt_score, auto_score

    

def read_inp(inp : str, verbose : bool = False) -> int:
    points = {")" : 3, "]" : 57, "}" : 1197, ">" : 25137}
    auto_points = {")" : 1, "]" : 2, "}" : 3, ">" : 4}
    checker = SyntaxCheck(points, auto_points)
    corrupt_ans, auto_ans = zip(*[checker.get_score(line, verbose = verbose) for line in inp.split("\n")])
    corrupt_ans = sum(corrupt_ans)
    auto_ans = [i for i in auto_ans if i != 0]
    # print(auto_ans)
    if auto_ans: auto_ans = sorted(auto_ans)[len(auto_ans) // 2]
    else: auto_ans = 0
    return corrupt_ans, auto_ans


assert read_inp("<<<", verbose = True)[0] == 0
assert read_inp("{([(<{}[<>[]}>{[]{[(<()>", verbose = True)[0] == 1197
assert read_inp(TEST, verbose = True)[0] == 26397

print(read_inp(TEST))
assert read_inp(TEST)[1] == 288957



if __name__ == "__main__":
    datfile = Path("day10.txt").read_text()
    print(read_inp(datfile))
    pass 