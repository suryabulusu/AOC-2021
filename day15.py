from __future__ import annotations
from pathlib import Path
from typing import MutableMapping, NamedTuple, List, Dict, Any
from collections import defaultdict
import heapq

TEST = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

TEST_2 = """311
111
111"""

class Point(NamedTuple):
    x: int
    y: int

class Graph:
    def __init__(self, multiplier : int = 1):
        self.risks : list[list[int]] = []
        # need to put Any -- if Point is not yet considered, its distance is infinity
        self.smallest_dist : defaultdict[Point, Any[int, float]] = defaultdict(lambda : float("inf"))
        self.multiplier = multiplier
        self.rows = 0
        self.cols = 0

    def get_risk(self, p : Point) -> int:
        """"incorporates tiling for part2"""
        add_x, add_y = p.x // self.rows, p.y // self.cols 
        dx, dy = p.x % self.rows, p.y % self.cols 
        ans = (self.risks[dx][dy] + add_x + add_y) % 9
        if ans == 0: return 9
        else: return ans

    def neighbors(self, p : Point) -> List[Point]:
        """incorporates tiling for part2"""
        neigh = []
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            if 0 <= p.x + dx < self.rows * self.multiplier and 0 <= p.y + dy < self.cols * self.multiplier:
                neigh.append(Point(p.x + dx, p.y + dy))
        return neigh

    def compute_shortest_paths(self) -> None: 
        """implements dijkstra algorithm with heapq
        Note: I did not change this implementation at all for Part-2
        I suppose these are the gains of object-oriented programming
        
        Like in a diagram (periodic table, subway maps); with OOP it becomes easier 
        to identify patterns, areas that need attention, and overall info dissemination

        I might not have quickly realized this with a crude dijkstra implementation
        """
        start = Point(0, 0)
        self.smallest_dist[start] = 0
        Q : list[tuple[int, Point]] = [(self.smallest_dist[start], start)]
        while Q:
            dist, u = heapq.heappop(Q)
            # u is done - its shortest path is stored
            # now, we relax its neighbors when possible
            for v in self.neighbors(u):
                # if v is done -- we should not relax
                # but note: had v been done -- it won't even be relaxed
                # so the next check is sufficient -- thereby avoiding done[] array totally
                if dist + self.get_risk(v) < self.smallest_dist[v]:
                    self.smallest_dist[v] = dist + self.get_risk(v)
                    heapq.heappush(Q, (self.smallest_dist[v], v))

    @classmethod 
    def parse(cls, inp : str, m : int) -> Graph:
        g = cls(multiplier = m)
        for line in inp.split("\n"):
            g.risks.append([int(i) for i in line])
        g.rows = len(g.risks)
        g.cols = len(g.risks[0])
        return g 

def read_inp(inp : str, m : int = 1) -> int:
    """shortest path problem with non negative edges => dijkstra"""
    g = Graph.parse(inp, m = m)
    g.compute_shortest_paths()
    
    end = Point(g.rows * g.multiplier - 1, g.cols * g.multiplier- 1)
    print(g.smallest_dist[end])
    return g.smallest_dist[end]


# looks DP? -- actually isn't!! we can move left or up too
# only diagonal is not allowed
# DP accounts only for down and right movements
def DP(inp : str) -> int:
    risks : list[list[int]] = []
    for line in inp.split("\n"):
        risks.append([int(i) for i in line])
    M, N = len(risks), len(risks[0])
    memo : dict[tuple[int, int], int] = {}

    # init states
    memo[(0, 0)] = 0
    for m_idx in range(1, M): memo[(m_idx, 0)] = memo[(m_idx - 1, 0)] + risks[m_idx][0]
    for n_idx in range(1, N): memo[(0, n_idx)] = memo[(0, n_idx - 1)] + risks[0][n_idx]

    # iters -- ensure correct dependency
    for m_idx in range(1, M):
        for n_idx in range(1, N):
            memo[(m_idx, n_idx)] = min(memo[m_idx - 1, n_idx], memo[m_idx, n_idx - 1]) + risks[m_idx][n_idx]

    print(memo[M - 1, N - 1])
    return memo[M - 1, N - 1]

assert read_inp(TEST) == 40
assert read_inp(TEST_2) == 4
assert read_inp(TEST, m = 5) == 315 #part2

if __name__ == "__main__":
    datfile = Path("day15.txt").read_text()
    ans1 = read_inp(datfile, m = 1)
    ans2 = read_inp(datfile, m = 5)
    print(ans1, ans2)