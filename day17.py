# Referred in parts to this code: https://github.com/prscoelho/aoc2021/blob/main/a17.py
# added some rough figures to explain
from __future__ import annotations
from pathlib import Path
import math
from typing import Tuple, Optional, List

def sign(x : int) -> int:
    if x < 0: return -1
    return 1

TEST = """target area: x=20..30, y=-10..-5"""

class Trajectory:
    """
    This trajectory class assumes that x_min and x_max are greater than 0
    y_min and y_max are less than 0
    """
    def __init__(self, vx : int, vy : int):
        self.x = 0
        self.y = 0
        self.vx = vx
        self.vy = vy  

    @staticmethod
    def quadratic_sol(a : float, b : float, c : float) -> Optional[Tuple[float, float]]:
        s = b ** 2 - 4 * a * c
        left, right = 0.0, 0.0
        if s >= 0:
            left = (-b - math.sqrt(s)) / (2 * a)
            right = (-b + math.sqrt(s)) / (2 * a)
        else:
            return None 
        return left, right

    def time_low_limit(self, pos : int, v : int) -> Optional[float]:
        """returns a value of time given position"""
        """the first time it hits pos mark"""
        # ax**2 + bx + c <= 0 type situation
        a = -1 / 2
        b = v + 1 / 2
        c = - 1 * pos 

        result = self.quadratic_sol(a, b, c)
        if result:
            left, right = result 
            # need to return the one that is greater than 0
            # and minimum timepoint it crosses the limit [maximum root doesnt matter]
            get_pos_time = lambda t: t >= 0
            return  min(filter(get_pos_time, (left, right)))

    @staticmethod
    def pos_func(p : int, t : int) -> int:
        """a = x/y; t = time
        f(p, t) = (t*(2p+1)-t**2)/2
        """
        assert t >= 0
        num = t * (2 * p + 1) - t ** 2
        den = 2
        return num // den 


    def pos_x(self, t : int) -> int:
        """returns position of x at time t / for now"""
        assert t >= 0, "time cant be negative"
        if self.vx + 1 - t < 0:
            return sign(self.vx) * self.pos_func(self.vx, self.vx + 1)
        return sign(self.vx) * self.pos_func(self.vx, t)

    def pos_y(self, t : int) -> int:
        """returns position of y at time t"""
        assert t >= 0, "time can't be negative"
        return self.pos_func(self.vy, t)

    def pos_max_x(self) -> int:
        """returns max of position x / where it stays constant"""
        return self.pos_x(self.vx + 1)

    def pos_max_y(self) -> int:
        """returns max of position y"""
        if self.vy <= 0: return 0

        return ((2 * self.vy + 1) ** 2) // 8

    def range_for_x(self, x_min : int, x_max : int):
        """computes range of t for given velocity; such that they pass through [x_min, x_max]"""
        assert x_min >= 0
        assert x_max >= 0
        assert x_max >= x_min
        low = self.time_low_limit(x_min, v = self.vx)
        if low is None:
            # simply doesn't hit the required region
            # example; x_min = 10, (x**2 + x) / 2 < 10
            return math.inf, -math.inf # so that distinct condition t[0] <= t[1] fails

        high = self.time_low_limit(x_max, v = self.vx) # beyond this time, we are crossing x_max
        # sometimes we may not - when trajectory gets stuck in region

        low = math.ceil(low) # surely we are in region now, for given vx
        if not high:
            high = math.inf 
        else:
            high = math.floor(high)

        return low, high 

    def range_for_y(self, y_min : int, y_max : int):
        """returns time range for vy given [y_min, y_max]"""
        """or 0 is just to avoid typing errors / we will never get None for y [for our case]"""
        assert y_min <= 0
        assert y_max <= 0
        assert y_min <= y_max
        low = self.time_low_limit(y_max, v = self.vy) or 0 # it will hit y_max first
        # node that both y_min and y_max are negative
        high = self.time_low_limit(y_min, v = self.vy) or 0 # will then hit the lower val

        return math.ceil(low), math.floor(high)

    def does_range_intersect(self, x_range : Tuple[int, int], y_range : Tuple[int, int]) -> bool:
        low_x, high_x = self.range_for_x(*x_range)
        low_y, high_y = self.range_for_y(*y_range)

        return low_x <= high_y and high_x >= low_y 

def get_distinct_trajectories(x_range : Tuple[int, int], y_range : Tuple[int, int]) -> List[Trajectory]:
    """returns a list of valid trajectories"""
    x_min, x_max = x_range
    y_min, y_max = y_range 
    trajs : list[Trajectory] = []
    # for x -- at t = 1, pos_x = x; if that is greater than x_max, it simply doesn't fall in target area
    # so, move x from 0 to x_max
    # for y -- its lower limit in y < 0 zone? if y < 0, t = 0 is the right most root of curve 
    # then, at t = 1, its position is y.. which should not jump over y_min.. so.. y has to be >= y_min
    # its upper limit in y > 0 zone? t = 2 * y + 1 is right-most root. 
    # t = 2 * y + 2, its value is negative and equal to -(y+1); and it should not jump over y_min => 
    # -(y + 1) >= y_min .. y + 1 <= -y_min ; y <= -y_min - 1
    bad_x : set[int] = set()
    bad_y : set[int] = set()
    for vx in range(0, x_max + 1):
        if vx in bad_x: continue 
        for vy in range(y_min, -1 * y_min):
            if vy in bad_y: continue 
            traj = Trajectory(vx = vx, vy = vy)
            tx_low, tx_high = traj.range_for_x(x_min, x_max)
            if tx_low > tx_high: 
                bad_x.add(vx)
                del traj 
                break 
            ty_low, ty_high = traj.range_for_y(y_min, y_max)
            if ty_low > ty_high:
                bad_y.add(vy)
                del traj
                continue
            if traj.does_range_intersect(x_range, y_range):
                trajs.append(traj)
            else: del traj 

    print(bad_x)
    print(bad_y)
    return trajs        

def read_inp(inp : str) -> tuple[int, int]:
    ans = 0
    x_str, y_str = inp.split(", ")
    x_str = x_str.split("=")[1]
    y_str = y_str.split("=")[1]
    x_min, x_max = [int(i) for i in x_str.split("..")]
    y_min, y_max = [int(i) for i in y_str.split("..")]

    trajs = get_distinct_trajectories(x_range = (x_min, x_max), y_range = (y_min, y_max))

    max_y = -math.inf
    for traj in trajs:
        if traj.pos_max_y() > max_y:
            max_y = traj.pos_max_y()

    total_trajs = len(trajs)

    # for traj in trajs:
        # print(traj.vx, traj.vy)

    return int(max_y), total_trajs

print(read_inp(TEST))
# traj = Trajectory(8, -1)
# print(traj.range_for_x(20, 30))
# print(traj.range_for_y(-10, -5))

if __name__ == "__main__":
    datfile = Path("day17.txt").read_text()
    print(read_inp(datfile))
