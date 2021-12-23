from __future__ import annotations 
from pathlib import Path 
from typing import Union, Optional, Iterator, Tuple
from dataclasses import dataclass
from math import floor, ceil 
import json 
import sys 
sys.setrecursionlimit(1000)


TEST = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

# with a named tuple, we cant assign stuff once node is created
# hence, dataclass a better choice here [infact a class would've worked too]
# there will be some nodes whose value does not exist.. 
@dataclass
class Node:
    left_child: Optional[Node] = None 
    right_child: Optional[Node] = None 
    val: Optional[int] = None 
    depth: int = 0
    side: Optional[str] = None 
    parent: Optional[Node] = None 

    @property
    def is_not_leaf(self):
        """It is a pair; not a leaf node!"""
        return self.left_child and self.right_child 

    @property 
    def has_value(self):
        return self.val is not None  

    @property
    def get_root(self) -> Node:
        node = self
        while node.parent:
            node = node.parent 
        return node 

    def string_rep(self) -> str:
        node = self 
        if node.has_value: return str(node.val)
        else:
            ans = "["
            ans += node.left_child.string_rep() 
            ans += ","
            ans += node.right_child.string_rep()
            ans += "]"
            return ans 

    @staticmethod
    def parse(inp_array : Union[list, int], parent : Optional[Node] = None, side : Optional[str] = None) -> Node:
        """creates a node
        args:
        inp_array: an array like [[9, 8], 7] or integer value (leaf)
        parent: the node that calls parse
        """
        depth = parent.depth + 1 if parent else 0 # helps during root node creation
        if isinstance(inp_array, int):
            return Node(val = inp_array, parent = parent, depth = depth, side = side)
        else:
            node = Node(parent = parent, depth = depth, side = side)
            node.left_child = Node.parse(inp_array[0], node, side = "left") # inp_array[0] == left
            node.right_child = Node.parse(inp_array[1], node, side = "right") # inp_array[1] == right
            return node 

def inorder_traversal(node : Node) -> Iterator[Node]:
    # given any node ; we produce inorder traversal
    if node.is_not_leaf:
        yield from inorder_traversal(node.left_child)
        yield node 
        yield from inorder_traversal(node.right_child)
    else:
        yield node 

# node1 == node2 --> giving recursion limit exceeded error
# unable to correct it even with sys.setrecursionlimit()
# maybe it helps to define __eq__ in dataclass
def node_equality(node1 : Node, node2 : Node) -> bool: 
    """assumes nodes are not None"""
    assert node1, "send a node; not None"
    assert node2, "send a node; not None"
    while True:
        if node1.side == node2.side and node1.string_rep() == node2.string_rep():
            node1 = node1.parent 
            node2 = node2.parent 
            # if both nodes are None -- we just called root's parent
            if not node1 and not node2:
                return True 
            elif not node1 or not node2: # if any one of them reached root's parent, say False
                return False 
        else:
            return False 

    return True # won't reach here ever 


def nearest_value_nodes(node : Node) -> Tuple[Node, Node]:
    """returns the surrounding regular/value nodes"""
    prev_node = None 
    next_node = None 
    # go through the inorder traversal...
    # if u come across a value and node is not seen; save it as prev_node
    is_node_seen = False 
    for n in inorder_traversal(node.get_root):
        # print("here", is_node_seen)
        # if prev_node and prev_node.has_value: print("prev val", prev_node.val)
        # if next_node and next_node.has_value: print("next val", next_node.val)
        # if n.has_value: 
        #     print_node(n.parent)
        #     print_node(n.parent.parent)
        #     print_node(node.parent.parent)
        #     print(n.parent.string_rep())
            # if n.parent.parent == node.parent.parent: print("yea so what")
            # print(node)
            # print(n)
        if n.parent and node_equality(n.parent, node):
            # print("gone here")
            continue
        # print("reached till here")
        if node_equality(n, node):
            is_node_seen = True
        if not is_node_seen and n.has_value:
            prev_node = n 
        elif is_node_seen and n.has_value:
            next_node = n
            break # we are done; want the immediate next 
        
    return prev_node, next_node

# p = [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
# tree = Node.parse(p)

def explode(node : Node) -> None:
    assert node.is_not_leaf, "can't explode leaf node"
    assert node.left_child and node.left_child.has_value
    assert node.right_child and node.right_child.has_value

    prev, next = nearest_value_nodes(node)
    if prev: prev.val += node.left_child.val
    if next: next.val += node.right_child.val 
    # doubt: wont the prev node of 

    node.val = 0 # we are making a pair to leaf now
    node.left_child = None
    # node.left_child.parent = None # to avoid any garbage
    node.right_child = None
    # node.right_child.parent = None # to avoid any garbage


def split(node : Node) -> None:
    assert node.has_value, "can't split non-val node"
    assert node.val >= 10, "why did you send node with val less than 10"
    store_val = node.val
    node.val = None 
    node.left_child = Node(val = floor(store_val / 2), depth = node.depth + 1, parent = node, side = "left")
    node.right_child = Node(val = ceil(store_val / 2), depth = node.depth + 1, parent = node, side = "right")
    # node.val = None 

def print_node(node : Node) -> None:
    """assumes given node is root"""
    print(node.string_rep())
    
    # once printing is done
    # if node.get_root == node: print("\n")

# p = [7,[6,[5,[4,[3,2]]]]]
# tree = Node.parse(p)
## note: since tree is a class instance, its attributes can be changed by passing to function
## unlike, say x = 3, y = square(x), x is still 3 and not 9 regardless of what is done in square()

def reduce_node(node : Node) -> None:
    """assumes node is root"""
    flag = True
    # save_val = 0
    while flag:
        print_node(node)
        # print("\n")
        flag = False 
        for n in inorder_traversal(node):
            # if n.has_value: print(n.val, n.depth)
            if n.is_not_leaf and n.depth >= 4:
                print("exploding...")
                explode(n)
                flag = True 
                break 
        if flag: continue 
        for n in inorder_traversal(node):
            if n.has_value and n.val >= 10:
                # print(n.val, n.depth)
                print("splitting...")
                split(n)
                flag = True 
                break 

def add_nodes(node_1 : Node, node_2 : Node) -> Node:
    node = Node(parent = None, left_child = node_1, right_child = node_2)
    node_1.parent = node 
    node_1.side = "left"
    node_2.parent = node
    node_2.side = "right"
    for n in inorder_traversal(node):
        if n.parent is None: continue # dont increase depth of root
        n.depth += 1 
    return node

def compute_magnitude(node : Node) -> int:
    if node.has_value:
        return node.val
    else:
        left_val = compute_magnitude(node.left_child)
        right_val = compute_magnitude(node.right_child)
        return 3 * left_val + 2 * right_val 


def read_inp(inp : str, part2 : bool = False) -> int:
    snail_nums = [json.loads(line) for line in inp.split("\n")]

    if part2: 
        max_mag = 0
        for idx1, num1 in enumerate(snail_nums):
            for idx2, num2 in enumerate(snail_nums):
                if idx1 == idx2: continue 
                result = add_nodes(Node.parse(num1), Node.parse(num2))
                reduce_node(result)
                mag = compute_magnitude(result)
                if mag > max_mag: max_mag = mag
        return max_mag

    main_tree = Node.parse(snail_nums[0])
    for num in snail_nums[1:]:
        main_tree = add_nodes(main_tree, Node.parse(num))
        reduce_node(main_tree)
        print_node(main_tree)
        print("***************************************************")
    ans = compute_magnitude(main_tree)

    # print_node(main_tree)
    return ans 

### checks adddition
# p1 = [1,2]
# p2 = [[3,4],5]
# print_node(add_nodes(Node.parse(p1), Node.parse(p2)))

### checks magnitude computation
# assert compute_magnitude(Node.parse([[1,2],[[3,4],5]])) == 143
# assert compute_magnitude(Node.parse([[[[0,7],4],[[7,8],[6,0]]],[8,1]])) == 1384
# assert compute_magnitude(Node.parse([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])) == 3488

TEST_SMALL = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]"""

print(read_inp(TEST))
assert read_inp(TEST) == 4140

if __name__ == "__main__":
    datfile = Path("day18.txt").read_text()
    print(read_inp(datfile, part2 = True))