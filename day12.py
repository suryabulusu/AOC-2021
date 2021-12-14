from __future__ import annotations
from pathlib import Path
from collections import defaultdict
# from typing import NamedTuple

TEST = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

class Graph:
    def __init__(self):
        self.edges : dict[str, list[str]] = defaultdict(list)
    
    @staticmethod
    def is_caps(s : str) -> bool:
        return all([i.isupper() for i in s])

    def add_edge(self, a : str, b : str) -> None:
        self.edges[a].append(b)
        self.edges[b].append(a)

    def parse(self, inp : str):
        for line in inp.split("\n"):
            a, b = line.split("-")
            self.add_edge(a, b)

        self.edges["end"] = [] # yeah deal with it

    def condition_part_1(self, path : list[str], node : str) -> bool:
        return self.is_caps(node) or node not in path

    def condition_part_2(self, path : list[str], node : str) -> bool:
        more_than_1 = any(True if path.count(x) > 1 and not self.is_caps(x) else False for x in path)
        cond = node not in ["start", "end"] and node in path and not more_than_1

        return self.is_caps(node) or node not in path or cond 

    def count_paths(self) -> int:
        """counts paths from start to end"""
        """some really cool solutions on reddit; learned that you can't just do with dfs on nodes"""
        """need to maintain paths... pain"""
        stack : list[list[str]] = [["start"]]
        # cnt = 0
        # stack = ["start"]
        ans = 0
        while stack:
            # print(stack)
            curr_path = stack.pop()
            curr_node = curr_path[-1]

            for next_node in self.edges[curr_node]:
                if next_node == "end":
                    # stack.append(curr_path + ["end"]) 
                    # save only if you want paths
                    ans += 1
                elif self.condition_part_2(curr_path, next_node):
                    new_path = curr_path + [next_node]
                    stack.append(new_path)
        
        return ans

def read_inp(inp : str) -> int:
    g = Graph()
    g.parse(inp)
    # print(g.edges)
    ans = g.count_paths()
    print(g.count_paths())
    return ans 

assert read_inp(TEST) == 36

if __name__ == "__main__":
    datfile = Path("day12.txt").read_text()
    read_inp(datfile)
    