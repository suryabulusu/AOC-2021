"""
learned the approach from an incredibly well written explainer:
https://old.reddit.com/r/adventofcode/comments/rnl0vn/2021_day_24_had_me_for_a_sec/hpuvs50/
"""
from __future__ import annotations
from pathlib import Path 
from typing import List, Tuple

class ALU:
    def __init__(self):
        self.vars : dict[str, int] = {
            "w": 0, "x": 0, "y": 0, "z": 0
        }

    def read_inp(self, a : str, val : int) -> None:
        self.vars[a] = val 

    def add_vals(self, a : str, val : int) -> None:
        self.vars[a] = self.vars[a] + val 

    def mult_vals(self, a : str, val : int) -> None:
        self.vars[a] = self.vars[a] * val 

    def div_vals(self, a : str, val : int) -> None:
        self.vars[a] = self.vars[a] // val 

    def mod_vals(self, a : str, val : int) -> None:
        self.vars[a] = self.vars[a] % val 

    def eq_vals(self, a : str, val : int) -> None:
        if self.vars[a] == val:
            self.vars[a] = 1
        else: self.vars[a] = 0 

    @classmethod
    def parse(cls, inp : str, num : str) -> ALU:
        """by iterating over digits in num; we are assuming that 
        ALU can input single-digit numbers only"""
        alu = cls()
        inp_num_idx = 0 
        for line in inp.split("\n"):
            # go through each instruction
            command, *args = line.split(" ")
            if command == "inp":
                v = args[0] # only one arg
                alu.read_inp(v, int(num[inp_num_idx]))
                inp_num_idx += 1
            else:
                v1, v2 = args
                if v2 in ["w", "x", "y", "z"]: v2 = alu.vars[v2]
                else: v2 = int(v2)

                # go to the operation
                if command == "add":
                    alu.add_vals(v1, v2)
                elif command == "mul":
                    alu.mult_vals(v1, v2)
                elif command == "div":
                    alu.div_vals(v1, v2)
                elif command == "mod":
                    alu.mod_vals(v1, v2)
                elif command == "eql": # equality op
                    alu.eq_vals(v1, v2)
                else:
                    raise ValueError(f"Unknown operator: {command}")

            # print(alu.vars)
        return alu 
    
# testing
# TEST = """inp z
# inp x
# mul z 3
# eql z x"""
# num1 = "39"
# num2 = "37"
# assert ALU.parse(TEST, num1).vars["z"] == 1 # z = 1 if 3*z = x
# assert ALU.parse(TEST, num2).vars["z"] == 0 # z = 0 if 3*z != x

TEST_2 = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2"""
num = "9"
assert list(ALU.parse(TEST_2, num).vars.values()) == [1, 0, 0, 1]

"""Another krak question -- read the input txt and notice that operations are similar
w == input here
if z%26 + (adder_1) != w: x = 1 / else: x = 0
z = z // (divisor)
z = z * [(25*x) + 1]
z = z + (w + adder_2) * x

simplify to:
if z%26 + adder_1 != w: 
    z = z // divisor
    z = 26 * z
    z = z + w + adder_2
else: z = z // divisor

in the input instruction, divisor = 1 or 26, and there's mod26. 
so it makes sense to consider base 26.
z % 26 -> last bit of z -- z.last_bit 
z * 26 -> left shift z -- z.push(0)
z // 26 -> right shift z -- z.pop()

(now in base 26) 
if divisor == 0:
    if z.last_bit + adder_1 != w:
        z.push(0)
        z = z + w + adder_2
else:
    if z.last_bit + adder_1 != w:
        z.pop()
        z.push(0)
        z = z + w + adder_2
    else: z.pop()

we know 1 <= w <= 9, and 0 <= z.last_bit < 26
from input, in all cases where divisor = 0, adder_1 > 9. 
so.. can ignore the if statement in it (its always true)

also notice adder_2 is <= 16 always.. so w + adder_2 <= 25
z = z + w + adder_2 after the z.push(0).. is equivalent to
z.push(w + adder_2). so, 

if divisor == 0:
    z.push(w + adder_2)
else:
    z.pop()
    if z.last_bit + adder_1 != w:
        z.push(w + adder_2)

the surprising find is: Z IS NOTHING BUT A STACK. push/pop
For MONAD to accept input, we need z = 0 at the end of program. 
that is, the stack should be empty. divisor == 0 always pushes things. 
we need to ensure divisor == 1 always pops things. 

so.. at time t, if z.last_bit = P, and at time (t+1) we see a divisor == 1;
we need P + adder_1 == w. so that only z.pop() happens. 
"""

def get_solution(inp : List[str], part : int = 1) -> str:
    # init
    if part == 1:
        start = "9" * 14
    else: start = "1" * 14

    start = list(map(int, start))
    # instruction sets are of len 18. 
    # of them, line 4, 5, 15 are divisor, adder_1, and adder_2
    # 5, 6, 16 -- for my input!
    types = [4, 5, 15]
    z_stack : List[Tuple[int, int]] = [] # we always append start[x] + adder_2
    # better save x and adder_2 -- this will be used later on
    for i in range(14):
        req_vals = [inp[18 * i + typ].split(" ")[-1] for typ in types]
        divisor, adder_1, adder_2 = map(int, req_vals)
        
        if divisor == 1:
            z_stack.append((i, adder_2)) # equivalent to start[i] + adder_2 
        else:
            j, adder_2_old = z_stack.pop()
            # we require z.last_bit (start[j] + adder_2_old) + adder_1 
            # and current input to be equal
            start[i] = start[j] + adder_2_old + adder_1 

            if start[i] > 9:
                # the best we can do is have start[i] as 9
                # effectively subtracting (start[i] - 9) from start[i]
                # thats the least we can subtract
                start[j] = start[j] - (start[i] - 9) # to maintain equality
                start[i] = 9

            if start[i] < 1:
                # again, best is to have start[i] as 1
                # have to add 1 - start[i] 
                # not sure if this "1" is optimal... but note we won't be reaching here in highest case
                # we only reach in minima case.. and "1" in minima is the least
                print("do i even reach here", start[i], start[j])
                start[j] = start[j] + (1 - start[i])
                start[i] = 1

            """
            you can change start[j] as you wish -- becuase these are just pushed with
            no dependency issues. start[i] never gets pushed, so manipulate at your will
            """

    return "".join([str(i) for i in start]) # sending only one solution for now


def read_inp(inp : str, part : int = 1) -> str:
    num = get_solution(inp.split("\n"), part = 2)
    alu = ALU.parse(inp, num)
    assert alu.vars["z"] == 0, f"Got the wrong answer, {num}, with length {len(num)}"
    return num

if __name__ == "__main__":
    datfile = Path("day24.txt").read_text()
    print(read_inp(datfile))
