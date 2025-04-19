from typing import List, Optional, Tuple, Union
from math import log2

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        k_idx = 0
        kth_smallest = None
        stack = [(root, 0)]
        processed_nodes = {}
        while len(stack) > 0:
            curr_node, curr_idx = stack.pop()

            sd = int(log2(curr_idx + 1))
            i = curr_idx - (2**sd - 1)
            l_idx = 2**(sd+1) + 2*i - 1
            r_idx = 2**(sd+1) + 2*i

            if curr_node.left is not None and l_idx not in processed_nodes.keys():
                # Left node hasn't been processed, push this node to be processed
                # later as well as the left child nodel
                stack.append((curr_node, curr_idx))
                stack.append((curr_node.left, l_idx))
            elif curr_idx not in processed_nodes.keys():
                processed_nodes[curr_idx] = None  # this node is now processed

                # update the curr smallest and return if we have the kth smallest
                kth_smallest = curr_node.val
                k_idx += 1
                if k_idx == k:
                    break

                # If we are not done, we must traverse down the right child node if it exists. If it does not exist,
                # we must re-traverse from the ancestor node, but they are already in the stack, so we do not need to
                # push anything to the stack here.
                if curr_node.right is not None and r_idx not in processed_nodes.keys():
                    stack.append((curr_node.right, r_idx))

        return kth_smallest

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
    input_node_list = [5,3,6,2,4,None, None,1]
    root = create_tree(input_node_list)

    sol_obj = Solution()
    ret = sol_obj.kthSmallest(root, 3)
    print(f"Input: \n{input_node_list}")
    print(f"Solution returned: {ret}")

if __name__ == '__main__':
    main()