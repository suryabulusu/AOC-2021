from __future__ import annotations
from pathlib import Path
# from typing import NamedTuple
from collections import defaultdict 

TEST = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

# digit_data = {
#     0: "abcefg", 1: "cf", 2: "acdeg", 3: "acdfg", 
#     4: "bcdf", 5: "abdfg",6: "abdefg", 
#     7: "acf", 8: "abcdefg", 9: "abcdfg"
# }

class Digits:
    def __init__(self):
        self.len_to_letters : dict[int, list[str]] = defaultdict(list)
        self.letters_to_digit : dict[str, int] = defaultdict(lambda : -1)
        self.digit_to_letters : dict[int, str] = defaultdict(str)

    def connector(self, num : int, letters : str):
        self.letters_to_digit[letters] = num
        self.digit_to_letters[num] = letters

    def prepare_digits(self, line : str):
        for l in line.split():
            self.len_to_letters[len(l)].append(l)
            if len(l) == 7:
                self.connector(8, l) 
            elif len(l) == 2:
                self.connector(1, l) 
            elif len(l) == 4:
                self.connector(4, l) 
            elif len(l) == 3:
                self.connector(7, l)   

    @staticmethod
    def find_difference(str1 : str, str2 : str) -> list[str]:
        ans = []
        for s in str1:
            if s not in str2: ans.append(s)
        return ans

    def get_digit(self, s : str) -> int:
        # print(s)
        for let in self.len_to_letters[len(s)]:
            if not self.find_difference(let, s): return str(self.letters_to_digit[let]) # str coz later we have to join

    def apply_rules(self): 
        # in those of len = 5, if all of 7 exist.. that number is 3
        idx_3 = 0
        for idx, let_3 in enumerate(self.len_to_letters[5]):
            if not self.find_difference(self.digit_to_letters[7], let_3):
                self.connector(3, let_3)
                idx_3 = idx
        
        idx_6 = 0
        for idx, let_6 in enumerate(self.len_to_letters[6]):
            if self.find_difference(self.digit_to_letters[8], let_6)[0] in self.digit_to_letters[7]:
                self.connector(6, let_6)
                idx_6 = idx

        char_for_c = self.find_difference(self.digit_to_letters[8], self.digit_to_letters[6])[0]
        for idx, let_2_5 in enumerate(self.len_to_letters[5]):
            if idx == idx_3: continue 
            if char_for_c in let_2_5: self.connector(2, let_2_5)
            else: self.connector(5, let_2_5)

        char_for_e = ""
        for c in self.find_difference(self.digit_to_letters[8], self.digit_to_letters[5]):
            if c != char_for_c: char_for_e = c 
        for idx, let_0_9 in enumerate(self.len_to_letters[6]):
            if idx == idx_6: continue
            if char_for_e in let_0_9: self.connector(0, let_0_9)
            else: self.connector(9, let_0_9)

def read_inp_2(inp : str) -> int:
    lines, nums = zip(*[line.split(" | ") for line in inp.split("\n")]) # no point of doing this tbf
    # just wanted to play around with zip*
    ans = 0
    for line, num in zip(lines, nums):
        digit_solver = Digits()
        digit_solver.prepare_digits(line)
        digit_solver.apply_rules()
        number = int("".join([digit_solver.get_digit(n) for n in num.split(" ")]))
        ans += number 

    return ans 
    # pass

def read_inp(inp : str) -> int:
    nums = [line.split("|")[1] for line in inp.split("\n")]
    unique = [2, 3, 4, 7]
    unique_counts = sum([
        1 if len(x) in unique else 0
        for num in nums
        for x in num.split()
    ])
    # print(unique_counts)
    return unique_counts
    
assert read_inp("be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe") == 2
assert read_inp(TEST) == 26

assert read_inp_2("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf") == 5353
assert read_inp_2(TEST) == 61229

if __name__ == "__main__":
    datfile = Path("day08.txt").read_text()
    print(read_inp_2(datfile))
    pass
