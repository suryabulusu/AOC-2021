from __future__ import annotations
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass

@dataclass 
class Dimension:
    low: int
    high: int 

    @staticmethod
    def intersection(a : Dimension, b : Dimension) -> Optional[Dimension]:
        if a.low < b.high and a.high > b.low:
            return Dimension(low = max(a.low, b.low), high = min(a.high, b.high))
        else: return None 

    @property
    def length(self):
        return self.high - self.low

    @property
    def get_range(self):
        return (self.low, self.high)

    @classmethod
    def create(cls, low : int, high : int):
        if low > high: low, high = high, low 
        return cls(low = low, high = high)

class Cuboid:
    """a cuboid consists of six markers"""
    def __init__(self, x_range : Dimension, y_range : Dimension, z_range : Dimension):
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range

    def volume(self):
        return self.x_range.length * self.y_range.length * self.z_range.length

    def __repr__(self):
        return f"Cuboid({self.x_range}, {self.y_range}, {self.z_range})"

    def intersection(self, cuboid_b : Cuboid):
        """intersection of cuboids creates 6 new cuboids
        think rectangles -- 
        """
        cuboid_a = self
        x_int = Dimension.intersection(cuboid_a.x_range, cuboid_b.x_range)
        y_int = Dimension.intersection(cuboid_a.y_range, cuboid_b.y_range)
        z_int = Dimension.intersection(cuboid_a.z_range, cuboid_b.z_range)

        if x_int is None or y_int is None or z_int is None:
            """if no intersection in any one dimension"""
            yield cuboid_a 
        else:
            new_cuboid = Cuboid(x_int, y_int, z_int)

            # this leads to six new cuboids 
            # (assume new_cuboid is fully inside cuboid_a)

            # full width, full depth cuboids -- 2
            full_x_d_1 = cuboid_a.x_range, Dimension.create(cuboid_a.y_range.low, new_cuboid.y_range.low), cuboid_a.z_range
            yield Cuboid(*full_x_d_1)
            full_x_d_2 = cuboid_a.x_range, Dimension.create(new_cuboid.y_range.high, cuboid_a.y_range.high), cuboid_a.z_range
            yield Cuboid(*full_x_d_2)
            
            # full height, full depth cuboids
            full_y_d_1 = Dimension.create(cuboid_a.x_range.low, new_cuboid.x_range.low), new_cuboid.y_range, cuboid_a.z_range
            yield Cuboid(*full_y_d_1)
            full_y_d_2 = Dimension.create(new_cuboid.x_range.high, cuboid_a.x_range.high), new_cuboid.y_range, cuboid_a.z_range
            yield Cuboid(*full_y_d_2)
            
            # full height of new cuboid, full width of new cuboid, restricted depth
            small_d_1 = new_cuboid.x_range, new_cuboid.y_range, Dimension.create(cuboid_a.z_range.low, new_cuboid.z_range.low)
            yield Cuboid(*small_d_1)
            small_d_2 = new_cuboid.x_range, new_cuboid.y_range, Dimension.create(new_cuboid.z_range.high, cuboid_a.z_range.high)
            yield Cuboid(*small_d_2)

TEST = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682"""

def get_indices(s : str) -> tuple[int, int]:
    a, b = tuple(int(i) for i in s.split("=")[1].split(".."))
    b += 1
    return (a, b)

# hacky... 
def restrict(a : int, b : int):
    return (-100, -100) if (abs(a) > 50 or abs(b) > 50) else (a, b)

def read_inp(inp : str, part2 : bool = False) -> int:
    all_cuboids : List[Cuboid] = []
    for line in inp.split("\n"):
        action, indices = line.split(" ")
        
        x_range, y_range, z_range = map(get_indices, indices.split(","))
        if not part2:
            x_range = restrict(*x_range)
            y_range = restrict(*y_range)
            x_range = restrict(*z_range)
            if (-100, -100) in [x_range, y_range, z_range]:
                continue

        x_dim, y_dim, z_dim = Dimension.create(*x_range), Dimension.create(*y_range), Dimension.create(*z_range)
        cuboid = Cuboid(x_dim, y_dim, z_dim)

        temp : List[Cuboid] = []
        for cub in all_cuboids:
            for c in cub.intersection(cuboid):
                # print(c, c.volume())
                if c.volume() > 0:
                    temp.append(c)

        all_cuboids = temp.copy()
        if action == "on":
            all_cuboids.append(cuboid)
        # off cuboids will just intersect / remove -- and not append!

        print("*****", len(all_cuboids))
        # break

    return sum(x.volume() for x in all_cuboids)

# assert read_inp(TEST) == 590784

TEST_2 = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507"""
assert read_inp(TEST_2, part2 = True) == 2758514936282235


if __name__ == "__main__":
    datfile = Path("day22.txt").read_text()
    ans = read_inp(datfile)
    print(ans)
    ans2 = read_inp(datfile, part2 = True)
    print(ans2)