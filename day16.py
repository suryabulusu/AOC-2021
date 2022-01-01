from __future__ import annotations
from pathlib import Path 
from typing import Dict, List, Tuple 
from functools import reduce

hexs = """0 = 0000
1 = 0001
2 = 0010
3 = 0011
4 = 0100
5 = 0101
6 = 0110
7 = 0111
8 = 1000
9 = 1001
A = 1010
B = 1011
C = 1100
D = 1101
E = 1110
F = 1111"""

hex_code : Dict[str, str] = {}
for line in hexs.split("\n"):
    k, v = line.split(" = ")
    hex_code[k] = v 

def get_bit_string(S : str) -> str:
    return "".join(hex_code[s] for s in S)

def parse(hexstr : str, start : int = 0) -> Tuple[Packet, int]:
    bit_string = get_bit_string(hexstr)
    packet = Packet()
    packet.bit_string = bit_string 
    packet.version = int(bit_string[start : start + 3], 2)
    packet.type_id = int(bit_string[start + 3 : start + 6], 2)

    # print(packet.version, packet.type_id)
    start += 6
    if packet.type_id == 4:
        # literal value
        digits = []
        while bit_string[start] == "1":
            digits.append(bit_string[start + 1 : start + 5])
            start += 5
        # last byte
        digits.append(bit_string[start + 1 : start + 5])
        start += 5
        packet.value = int("".join(digits), 2)
    else:
        # print(bit_string[start:])
        length_tid = bit_string[start]
        start += 1
        if length_tid == "0":
            total_length = int(bit_string[start : start + 15], 2)
            start += 15
            end = start + total_length 

            while True:
                subpack, start = parse(hexstr, start)
                packet.sub_packets.append(subpack)
                if start >= end: break 

        else:
            num_subpacks = int(bit_string[start : start + 11], 2)
            # immediately contained by this packet
            start += 11
            
            cnt = 0
            while cnt < num_subpacks:
                subpack, start = parse(hexstr, start)
                packet.sub_packets.append(subpack)
                cnt += 1
    
    packet.num_subpacks = len(packet.sub_packets)
    packet.set_value()
    # print(packet.sub_packets)
    return packet, start

# could have been dataclass/namedtuple
class Packet:
    def __init__(self) -> None:
        self.bit_string : str = ""
        self.version : int = 0
        self.type_id : int = 0
        self.sub_packets : List[Packet] = []
        self.num_subpacks : int = 0
        self.value : int = 0

    def set_value(self):
        if self.type_id == 4:
            # value is already set
            pass 
        elif self.type_id == 0:
            self.value = sum([p.value for p in self.sub_packets])
        elif self.type_id == 1:
            self.value = reduce(lambda a, b : a * b, [p.value for p in self.sub_packets])
        elif self.type_id == 2:
            self.value = min([p.value for p in self.sub_packets])
        elif self.type_id == 3:
            self.value = max([p.value for p in self.sub_packets])
        elif self.type_id == 5:
            p1, p2 = self.sub_packets # guaranteed to have 2 subpackets
            self.value = 1 if p1.value > p2.value else 0
        elif self.type_id == 6:
            p1, p2 = self.sub_packets
            self.value = 1 if p1.value < p2.value else 0
        elif self.type_id == 7:
            p1, p2 = self.sub_packets
            self.value = 1 if p1.value == p2.value else 0

    def sum_versions(self) -> int:
        ans = self.version + sum([p.sum_versions() for p in self.sub_packets])
        return ans

# hexstr = "EE00D40C823060"
# packet, _ = parse(hexstr = hexstr, start = 0)
# assert [packet.version, packet.type_id, packet.num_subpacks] == [7, 3, 3]
# assert [p.value for p in packet.sub_packets] == [1, 2, 3]

hexstr = "8A004A801A8002F478"
# print(get_bit_string(hexstr))
packet, _ = parse(hexstr, 0)
# print(packet.sum_versions())
assert packet.sum_versions() == 16

assert parse("9C0141080250320F1802104A08", 0)[0].value == 1

if __name__ == "__main__":
    datfile = Path("day16.txt").read_text()
    pack, _ = parse(datfile, 0)
    print(pack.sum_versions())
    print(pack.value)
