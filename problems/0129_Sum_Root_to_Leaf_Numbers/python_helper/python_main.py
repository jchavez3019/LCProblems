import numpy as np
from math import log2
from typing import List, Tuple, Optional, Union

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:

        # values in stack are (TreeNode, None/current_value)
        stack = [(root, None)]
        sum = 0

        while len(stack) > 0:
            curr_node, curr_val = stack.pop()

            if curr_val is None:
                # handles case when root node gets pushed
                new_num = curr_node.val
            else:
                # concatenate values
                new_num = curr_node.val + curr_val * 10

            if curr_node.left == curr_node.right == None:
                # leaf node must be added to the sum
                sum += new_num
                continue

            # child nodes exist, append them
            if curr_node.left is not None:
                stack.append((curr_node.left, new_num))
            if curr_node.right is not None:
                stack.append((curr_node.right, new_num))

        return sum


def create_tree(node_values: List[int]) -> TreeNode:

    root_node = TreeNode(node_values[0])

    # values in stack are (TreeNode, idx of TreeNode in node_values)
    stack = [(root_node, 0)]

    while len(stack) > 0:
        curr_node, idx = stack.pop()

        sd = int(log2(idx + 1))
        i = idx - (2**sd - 1)
        l_idx = 2**(sd+1) + 2*i - 1
        r_idx = 2**(sd+1) + 2*i

        if l_idx < len(node_values):
            l_node = TreeNode(node_values[l_idx])
            curr_node.left = l_node
            stack.append((l_node, l_idx))

        if r_idx < len(node_values):
            r_node = TreeNode(node_values[r_idx])
            curr_node.right = r_node
            stack.append((r_node, r_idx))

    return root_node

def main():
    tree_list = [4,9,0,5,1]
    root_node = create_tree(tree_list)

    sol_obj = Solution()
    sum = sol_obj.sumNumbers(root_node)

    print(f"Tree List: \n{tree_list}")
    print(f"Solution returned: {sum}")

if __name__ == '__main__':
    main()