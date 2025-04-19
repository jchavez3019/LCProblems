from typing import List, Tuple, Optional, Union
from queue import Queue
from math import log2

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:

        if root is None:
            return []

        q = Queue()
        q.put((root, 0))
        node_list = []
        curr_sd = 0 # current split depth
        curr_node_list = [] # node list for current split depth

        while not q.empty():
            curr_node, idx = q.get()

            # Calculate split depth and indices of potential children
            sd = int(log2(idx + 1))
            i = idx - (2**sd - 1)
            l_idx = 2**(sd + 1) + 2*i - 1
            r_idx = 2**(sd + 1) + 2*i

            # Check the split depth to see if we put this in the current
            # split depth list or if we need to create a new split depth list
            if sd == curr_sd:
                curr_node_list.append(curr_node.val)
            else:
                curr_sd = sd
                node_list.append(curr_node_list)
                curr_node_list = [curr_node.val]

            # Appends children nodes to the queue if they exist
            if curr_node.left is not None:
                q.put((curr_node.left, l_idx))
            if curr_node.right is not None:
                q.put((curr_node.right, r_idx))

        # Append the final curr_node_list to the node_list
        node_list.append(curr_node_list)

        return node_list

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

        if l_idx < len(node_values) and node_values[l_idx] is not None:
            l_node = TreeNode(node_values[l_idx])
            curr_node.left = l_node
            stack.append((l_node, l_idx))

        if r_idx < len(node_values) and node_values[r_idx] is not None:
            r_node = TreeNode(node_values[r_idx])
            curr_node.right = r_node
            stack.append((r_node, r_idx))

    return root_node

def main():
    input_node_list = [3,9,20,None,None,15,7]
    root = create_tree(input_node_list)

    sol_obj = Solution()
    ret = sol_obj.levelOrder(root)
    print(f"Input: \n{input_node_list}")
    print(f"Solution returned: \n{ret}")

if __name__ == '__main__':
    main()