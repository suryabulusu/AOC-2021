from __future__ import annotations 
from pathlib import Path
from typing import List, Tuple
import numpy as np 

# there are 24 matrices ... to represent orientations
from scipy import spatial 
orientations = spatial.transform.Rotation.create_group("O").as_matrix().astype(int)
assert orientations.shape[0] == 24, "computed the wrong orientations"
############################

class Scanner:
    def __init__(self, scan_id : int, loc , rel_points : List[Tuple[int]], 
                    orientation : int = None) -> None:
        self.loc = loc
        self.id = scan_id 
        self.rel_points = np.array(rel_points) # (Ns, 3)
        self.num_points = len(rel_points)
        self.orientation = np.eye(3)
        self.orig_loc = np.array([0, 0, 0])
        self.orig_orientation = np.eye(3)

    def get_pairwise_dist(self):
        """returns array of differences; of shape (Ns, Ns)"""
        x_sq = np.square(self.rel_points).sum(axis = 1)
        return  x_sq + x_sq[:, np.newaxis]  - 2 * self.rel_points @ self.rel_points.T

    def get_difference(self):
        diffs = []
        for row in self.rel_points:
            diffs.append(self.rel_points - row)
        diffs = np.array(diffs)
        assert diffs.shape == (self.num_points, self.num_points, 3), "check your diffs array size, maybe subtraction is wrong"
        return diffs

    def convert_to_abs(self):
        """converts to abs to ease computation / once loc and orientation are known"""
        self.rel_points = self.rel_points @ self.orientation + self.loc
        self.orig_loc = self.loc 
        self.loc = np.array([0, 0, 0])
        self.orig_orientation = self.orientation
        self.orientation = np.eye(3)


class Map:
    def __init__(self, scanners : List[Scanner]):
        self.scanners = scanners 
        self.num_scanners = len(scanners)
        self.len_scanners = [s.num_points for s in scanners]
        self.scanner_ori = np.zeros((len(scanners), len(orientations)))
        self.same_beacons = set() # relative to scanner 0
    
    def find_overlap_beacons(self, a : int, b : int):
        """assumes that a's orientation is known -- and is equal to np.eye(3)"""
        found = False 

        rel_dist_a = self.scanners[a].get_pairwise_dist()
        rel_dist_b = self.scanners[b].get_pairwise_dist()

        if len(set(rel_dist_a.flatten()).intersection(set(rel_dist_b.flatten()))) < 67:
            return found


        rel_diff_a = self.scanners[a].get_difference()
        rel_diff_b = self.scanners[b].get_difference()
        # distance is a good shortlisting way
        same_beacons = set()

        for o_id, ori in enumerate(orientations):
            
            iter_a = list(np.ndindex(self.len_scanners[a], self.len_scanners[a]))
            iter_b = list(np.ndindex(self.len_scanners[b], self.len_scanners[b]))
            rel_diff_b_ori = rel_diff_b @ ori

            for ia, ja in iter_a:
                if ia == ja: continue 
                # print(ia, ja, rel_diff_a[ia, ja])
                for ib, jb in iter_b:
                    if ib == jb: continue 
                    # print("***")
                    if rel_dist_a[ia, ja] != rel_dist_b[ib, jb]: continue
                    # print("*****")
                    # flag = 1
                    # print(rel_diff_a[ia, ja].shape)
                    # print(rel_diff_b_ori[ib, jb].shape)
                    # print((rel_diff_a[ia, ja] == rel_diff_b_ori[ib, jb]))
                    if (rel_diff_a[ia, ja] == rel_diff_b_ori[ib, jb]).all():
                        # print("y")
                        # cnt += 1 
                        same_beacons.add((ia, ib))
                        same_beacons.add((ja, jb))
                    # if flag == 1: break
            # print(len(same_beacons))
            if len(same_beacons) >= 12:
                self.scanner_ori[b, o_id] += 1
                # vec x + vec y = vec z
                z, y = next(iter(same_beacons)) # just to access an elem in set
                self.scanners[b].orientation = ori 
                self.scanners[b].loc = self.get_rel_beacon(a, z) - self.get_rel_beacon(b, y) @ ori # x = z - y
                if a == 4:
                    print(self.scanners[b].loc)

                cnt = 0
                for i, j in same_beacons:
                    if not (self.get_abs_beacon(a, i) == self.get_abs_beacon(b, j)).all():
                        cnt += 1
                        # print("bad")
                        # print(a, self.get_abs_beacon(a, i), self.get_rel_beacon(a, i))
                        # print(b, self.get_abs_beacon(b, j), self.get_rel_beacon(b, j))
                        # bad_loc = True 
                        # break  
                        # this happens when the 12 matched beacons are not actually in the same relative angle
                        # its a spurious case that 12 have matched
                    else: self.same_beacons.add((a, i)) # which is same as j
                    # print(self.get_beacon(a, i), self.get_beacon(b, j))
                
                print("bad ones - ", len(same_beacons), cnt)
                if len(same_beacons) - cnt < 12:
                    same_beacons = set()
                    continue 
                
                found = True 
                return found
            
            # break

        return found 

    def get_rel_beacon(self, a : int, idx : int):
        """returns idx^th relative pos of beacon of scanner with id a"""
        return self.scanners[a].rel_points[idx]

    def get_abs_beacon(self, a : int, idx : int):
        """returns idx^th beacon of scanner with id a"""
        rel_beacon = self.get_rel_beacon(a, idx)
        return rel_beacon @ self.scanners[a].orientation + self.scanners[a].loc

def get_max_dist(scanners : List[Scanner]) -> int:
    scan_iter = np.ndindex(len(scanners), len(scanners))

    maxdist = 0
    for a, b in scan_iter:
        if a == b: continue 
        curr_dist = np.abs(scanners[a].orig_loc - scanners[b].orig_loc).sum()
        maxdist = max(maxdist, curr_dist)

    return maxdist

def read_inp(inp : str) -> Tuple[int, int]:
    """reads input; returns total beacon count"""
    ans = 0
    scan_num = -1
    rel_points = []
    scanners = []
    for line in inp.split("\n"):
        if line[:3] == "---":
            if scan_num != -1:
                loc = None 
                if scan_num == 0: loc = (0, 0, 0) # dont think i'll use Point class at all
                scanners.append(Scanner(scan_id = scan_num, loc = loc, rel_points = rel_points))
            scan_num += 1
            rel_points = []
        elif "," in line: rel_points.append(tuple(int(i) for i in line.split(","))) # hackkkkyyyy
        else: continue 
    scanners.append(Scanner(scan_id = scan_num, loc = None, rel_points = rel_points)) # hackkky
    m = Map(scanners = scanners)
    
    done_scanners : List[bool] = [False] * len(scanners)
    # done_scanners[0] = True 
    done_stack = [0]
    done_scanners[0] = True 
    while not all(done_scanners):
        a = done_stack.pop()
        
        for b in range(len(scanners)):
            if b == a or done_scanners[b]: continue 
            print(f"Pair ({a},{b}) processing..")
            found = m.find_overlap_beacons(a, b) # sets angle of b etc
            if found:
                done_stack.append(b)
                print(f"done; same beacons = {len(m.same_beacons)}")
                # translate to base -- update orientation
                # this is to ease computations later on
                scanners[b].convert_to_abs()
                done_scanners[b] = True # meaning -- we found the angle/loc
    
    ans = np.unique(np.vstack([scan.rel_points for scan in scanners]), axis = 0).shape[0]
    maxdist = get_max_dist(scanners)

    return ans, maxdist  

TEST = Path("day19_test.txt").read_text()
ans, maxdist = read_inp(TEST)
assert ans == 79 

if __name__ == "__main__":
    datfile = Path("day19.txt").read_text()
    ans, maxdist = read_inp(datfile)
    print(ans, maxdist)
