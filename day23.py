from __future__ import annotations 
from pathlib import Path
from typing import Dict, List, Tuple, NamedTuple, DefaultDict
from dataclasses import dataclass
from itertools import chain 
from copy import deepcopy
import heapq
from collections import defaultdict

TEST = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

TEST_LARGE = """#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########"""

POSINF = 1000000000000

class Point(NamedTuple):
    x : int
    y : int

    def __repr__(self):
        return f"({self.x}, {self.y})"

accepted_positions : Dict[str, list] = {
    "A": [Point(2, 3), Point(3, 3)],
    "B": [Point(2, 5), Point(3, 5)],
    "C": [Point(2, 7), Point(3, 7)],
    "D": [Point(2, 9), Point(3, 9)]
} # has to change for part2


AMPHIPOD_TYPES = ["A", "B", "C", "D"]
ENERGY : Dict[str, int] = {"A" : 1, "B" : 10, "C" : 100, "D" : 1000}
BAD_HALLWAY : List[Point] = [Point(1, 3), Point(1, 5), Point(1, 7), Point(1, 9)]

# this class was not at all needed imo
# should've instead prepared a class for ROOM STACK
# popping from room stack -> leaving room at the top
# pushing to room stack -> entering room at the top
# nah i'm burned out now won't update this code
@dataclass
class Amphipod: 
    typ : str 
    loc : Point 

    def __repr__(self):
        return f"[{self.typ}, {self.loc}]"

    @property
    def is_done(self):
        return self.loc in accepted_positions[self.typ]

class Map:
    def __init__(self, amphipods : List[Amphipod], mapper : Dict[Point, str], 
                hallway : List[Point], rows : int, cols : List[int], energy : int = 0):
        self.mapper = mapper 
        self.amphipods : List[Amphipod] = amphipods 
        self.hallway : List[Point] = hallway 
        self.rows : int = rows
        self.cols : List[int] = cols 
        self.energy = energy

    def __repr__(self):
        return f"(Amphipods={self.amphipods}, Hallway={self.hallway})"

    @classmethod
    def parse(cls, inp : str) -> Map:
        """assumes hallway is free"""
        mapper = {}
        hallway = []
        amphipods = [] # to init
        rows = len(inp.split("\n"))
        cols = []
        for ridx, line in enumerate(inp.split("\n")):
            cols.append(len(line))
            for cidx, s in enumerate(line):
                p = Point(ridx, cidx)
                mapper[p] = s 
                if s == "." and p not in BAD_HALLWAY: 
                    hallway.append(p)                    
                elif s in AMPHIPOD_TYPES:
                    amphipods.append(Amphipod(s, p))
        return cls(mapper = mapper, hallway = hallway, amphipods = amphipods, rows = rows, cols = cols)

    def is_empty(self, room : Point) -> bool:
        """checks if room in current map is empty"""
        return self.mapper[room] == "."

    @staticmethod
    def compute_energy(p1 : Point, p2 : Point, typ : str) -> int:
        dy = abs(p1.y - p2.y) # for part1 its true
        x_check = abs(p1.x - p2.x)
        dx = 0
        # sorry...
        if p1.x == 1 or p2.x == 1:
            dx = x_check 
        else:
            dx = (p1.x - 1) + (p2.x - 1)

        return ENERGY[typ] * (dx + dy)

    def move(self, amphipod : Amphipod, p : Point) -> Map:
        """moves amphipod to p
        p - could be a room or hallway point
        """
        _hallway = deepcopy(self.hallway)
        _mapper = deepcopy(self.mapper)
        _amphipods = deepcopy(self.amphipods) # time taking; could have been a list 
        excess_energy = 0
        if p not in ROOMS: _hallway.remove(p) # remove only if p is hallway point
        if amphipod.loc not in ROOMS: _hallway.append(amphipod.loc) # only append if its not a room
        _amphipods.remove(amphipod) # remove amphi at old pos
        _amphipods.append(Amphipod(typ = amphipod.typ, loc = p)) # create new amphi with new pos
        _mapper[p] = amphipod.typ # if amphi goes to p, put that letter there
        _mapper[amphipod.loc] = "." # if amphipod leaves any place, it gets empty
        
        excess_energy = self.compute_energy(p, amphipod.loc, amphipod.typ)
        
        return Map(hallway = _hallway, amphipods = _amphipods, mapper = _mapper, 
                    energy = excess_energy, rows = self.rows, cols = self.cols)

    def __hash__(self):
        # useful to compare in dijkstra
        return hash(f"{self.print_map()}") 

    def __eq__(self, other : Map) -> bool:
        # useful for dijkstra -- to have class as key
        return self.print_map() == other.print_map()

    def __lt__(self, other : Map) -> bool:
        # needed for dijkstra -- although i don't see a point
        # if heapq uses only the first item, why __lt__ for second item
        return self.energy < other.energy
    
    def next_maps(self) -> List[Map]:
        maps : List[Map] = []
        if self.is_done: return []
        # we can move amphipods out of a room into hallway
        # print("looping over pods", self.amphipods)
        for amphipod in self.amphipods:
            # print("out of room", amphipod.typ, amphipod.loc)
            # if amphipod not in ROOMS => its in hallway already -- so ignore
            if amphipod.loc not in ROOMS: continue
            room = amphipod.loc
            # if anything under amphipod is correct.. dont move out -- dont move out!
            if amphipod.is_done and self.all_under_done(room, amphipod.typ): continue 
            for h in self.hallway:
                # have to check if we can move from amphipod.loc to h
                # h is guaranteed to be empty and not in BAD_HALLWAY
                # only need to check if path to h is not blocked
                # vertical check -- only for rooms down:
                v_check_fail = False 
                for x in range(room.x - 1, 1, -1): 
                    if not self.is_empty(Point(x, room.y)): v_check_fail = True 
                if v_check_fail: continue 
                # horizontal check - room.y is empty, h.y is empty (thats why its in hallway)
                h_check_fail = False 
                h_direction = 1 if h.y > room.y else -1 
                for y in range(room.y + h_direction, h.y, h_direction):
                    assert h.x == 1, "you messed the hallway" # h.x == 1 always
                    if not self.is_empty(Point(h.x, y)):
                        h_check_fail = True
                        break
                if h_check_fail: continue 

                maps.append(self.move(amphipod, h))
                # print(maps[-1].print_map())

        # we can move amphipods into a room - from hallway OR from another room      
        for room in ROOMS:
            # print(room)
            # can't move into a room if it is not empty
            if not self.is_empty(room): continue 
            for amphipod in self.amphipods:
                # you can't move to wrong rooms
                if room not in accepted_positions[amphipod.typ]: continue
                # you cant move if the ones underneath are wrong 
                if not self.all_under_done(room, amphipod.typ): continue
                # vertical path to room has to be free
                v_check_fail = False 
                for x in range(room.x - 1, 1, -1): 
                    if not self.is_empty(Point(x, room.y)): v_check_fail = True 
                if v_check_fail: continue 
                # if room underneath is free, no point in moving to top room
                for x in range(room.x + 1, self.rows):
                    if self.is_empty(Point(x, room.y)): v_check_fail = True 
                if v_check_fail: continue 
                # vertical path from amphipod (if in room) has to be free
                amphi_loc = amphipod.loc
                for x in range(amphi_loc.x - 1, 1, -1):
                    if not self.is_empty(Point(x, amphi_loc.y)): v_check_fail = True 
                    # no point in moving to the room gap above it.. if any
                    if x == room.x: v_check_fail = True 
                if v_check_fail: continue 
                # horizontal path between room and amphipod has to be free
                h_check_fail = False 
                h_direction = 1 if room.y > amphi_loc.y else -1 
                for y in range(amphi_loc.y + h_direction, room.y, h_direction): # just above room is empty anyway
                    if not self.is_empty(Point(1, y)): # need to check only hallway
                        h_check_fail = True
                        break
                if h_check_fail: continue 
            
                maps.append(self.move(amphipod, room))
                # print(maps[-1].print_map())

        return maps

    @property
    def is_done(self) -> bool:
        return all(a.is_done for a in self.amphipods)

    def all_under_done(self, room : Point, typ :str) -> bool:
        for x in range(room.x + 1, self.rows - 1):
            if self.mapper[Point(x, room.y)] != typ: 
                return False 
        return True 

    def print_map(self) -> str:
        printer = ""
        for row in range(self.rows):
            for col in range(self.cols[row]):
                p = Point(row, col)
                # this structure makes it easy to print (not optimal)
                printer += self.mapper[p]
            printer += "\n"
        return printer

def dijkstra(init_map : Map) -> int:
    """computes shortest path wherein nodes are map configs and edges are excess energies"""
    """there won't be cycles in this setting; and non negative edges only"""
    Q : List[Tuple[int, Map]] = [(init_map.energy, init_map)] # int | float coz initially -float(inf)
    # types can get very irritating at times
    heapq.heapify(Q)
    final_energies : DefaultDict[Map, int] = defaultdict(lambda : POSINF)
    cnt = 0
    flag = 0
    map_done : DefaultDict[Map, bool] = defaultdict(bool) # not necessary - but i dont want to create new map objects
    # only to discard them later anyway
    while Q:
        cnt += 1
        # if cnt > 10: break
        energy, m = heapq.heappop(Q)
        if map_done[m]: continue
        map_done[m] = True
        if m.is_done: break  
        next_maps : List[Map] = m.next_maps()
        print(len(Q), len(next_maps))
        if cnt > 100000000000: # max loops -- stop after this, save RAM
            for n in next_maps:
                print(n.print_map())
                print(final_energies[n], "*****")
            if flag: print(flag, "dlfd")
            break
        # print(next_maps)
        for n in next_maps:
            # relax function
            if energy + n.energy < final_energies[n]:
                final_energies[n] = energy + n.energy 
                heapq.heappush(Q, (final_energies[n], n))
        
        # break
    
    min_energy : int = POSINF
    min_map = None 
    for m, e in final_energies.items():
        if not m.is_done: continue
        # m.print_map()
        print(e, "****")
        if e < min_energy:
            min_energy = e
            min_map = m 

    if min_map: print(min_map.print_map())
    return min_energy


def read_inp(inp : str) -> int:
    """reads input map and returns least energy"""
    m = Map.parse(inp)
    # m.print_map()
    ans = dijkstra(m)
    return ans

TEST_2 = """#############
#...........#
###A#B#D#C###
  #A#B#C#D#
  #########"""

TEST_3 = """#############
#...........#
###A#B#D#C###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########"""

part2 = True 
if part2:
    accepted_positions["A"].extend([Point(4, 3), Point(5, 3)])
    accepted_positions["B"].extend([Point(4, 5), Point(5, 5)])
    accepted_positions["C"].extend([Point(4, 7), Point(5, 7)])
    accepted_positions["D"].extend([Point(4, 9), Point(5, 9)])
ROOMS : List[Point] = list(chain(*accepted_positions.values()))

# ans = read_inp(TEST)
# ans = read_inp(TEST_LARGE)

# testing the path for old code
# m = Map.parse(TEST)
# nm = m.next_maps()
# for idx, n in enumerate(nm):
#     print(idx)
#     print(n.print_map())
# print(len(nm))
# n = nm[16]
# print(n.print_map(), n.energy)
# print("1. --------------------------------------------")
# nn = n.next_maps()
# n_2 = nn[-1]
# print(n_2.print_map(), n_2.energy)
# n22 = n_2.next_maps()
# n_3 = n22[-5]
# print(n_3.print_map(), n_3.energy)
# print("2. --------------------------------------------")
# n33 = n_3.next_maps()
# n_4 = n33[-1]
# print(n_4.print_map(), n_4.energy)
# print("3. --------------------------------------------")
# n44 = n_4.next_maps()
# n_5 = n44[-1]
# print(n_5.print_map(), n_5.energy)
# print("4. --------------------------------------------")
# n55 = n_5.next_maps()
# n_6 = n55[0]
# print(n_6.print_map(), n_6.energy)
# print("5. --------------------------------------------")
# n66 = n_6.next_maps()
# n_7 = n66[-3]
# print(n_7.print_map(), n_7.energy)
# print("6. --------------------------------------------")
# n77 = n_7.next_maps()
# n_8 = n77[-1]
# print(n_8.print_map(), n_8.energy)
# print("7. --------------------------------------------")
# n88 = n_8.next_maps()
# n_9 = n88[-1]
# print(n_9.print_map(), n_9.energy)
# print("8. --------------------------------------------")
# n99 = n_9.next_maps()


# for n_ in nn:
    
    # print(n_.print_map())
    # break 
if __name__ == "__main__":
    datfile = Path("day23_2.txt").read_text()
    ans = read_inp(datfile)
    # print(ans)