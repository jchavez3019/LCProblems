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

    def maxPathSum(self, root: Optional[TreeNode]) -> int:

        stack: List[Tuple[TreeNode, int]] = [(root, 0)]
        best_sum = float('-inf')
        # initialize a solved_subproblems list to store the solutions to each subproblem
        self.solved_subproblems: dict[int, int] = {}

        while len(stack) > 0:
            curr_node, curr_idx = stack.pop()

            # Calculate the current split depth and the indices
            # of the potential child nodes. This allows us to hash each node.
            sd = int(log2(curr_idx + 1))
            i = curr_idx - (2**sd - 1)
            l_idx = 2**(sd + 1) + 2*i - 1
            r_idx = 2**(sd + 1) + 2*i

            if curr_node.left == curr_node.right == None:
                # Base case where this is a child node, therefore the sub-problem can be instantaneously solved
                # self.insert_subproblem(curr_idx, curr_node.val)
                self.solved_subproblems[curr_idx] = curr_node.val
                best_sum = max(best_sum, curr_node.val)
                continue

            # We can only solve this current node if the children nodes have been processed
            canSolveCurr_left = (curr_node.left is None or l_idx in self.solved_subproblems.keys())
            canSolveCurr_right = (curr_node.right is None or r_idx in self.solved_subproblems.keys())
            canSolveCurr = canSolveCurr_left and canSolveCurr_right

            if canSolveCurr:

                # Get the values of the children (could potentially be 0 if there is only one child)
                sum_left = self.solved_subproblems.get(l_idx, 0)
                sum_right = self.solved_subproblems.get(r_idx, 0)

                # The first potential solution is that we traverse from the left child node, to this node, down the
                # right child node
                potential_solution_one = max(best_sum, sum_left + curr_node.val + sum_right)
                # The second potential solution is that we traverse from one of the child nodes (or even start from
                # this node), and traverse upwards in the tree
                potential_solution_two = curr_node.val + max(sum_left, sum_right, 0)

                # Update the best possible sum using these potential solutions
                best_sum = max(best_sum, potential_solution_one, potential_solution_two)

                # Save the second potential solution into the hash table so that the ancestors can reference it
                # when they get processed (the first potential solution does not apply to the ancestors)
                self.solved_subproblems[curr_idx] = potential_solution_two
            else:
                # We cannot process this node because its children have not been processed. We push this node
                # back onto the stack as well as its children
                stack.append((curr_node, curr_idx))
                if curr_node.left is not None:
                    stack.append((curr_node.left, l_idx))
                if curr_node.right is not None:
                    stack.append((curr_node.right, r_idx))

        return int(best_sum)

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
    # input_list = [1, 2, 3]
    input_list = [2, -1]
    # input_list = [-10,9,20,None, None,15,7]
    # On this example, leetcode exceeds the memory limit. This means that we need to more carefully consider how the solutions
    # to the subproblems are stored.
    root = create_tree(input_list)

    sol_obj = Solution()
    ret = sol_obj.maxPathSum(root)
    print(f"Input: \n{input_list}")
    print(f"Solution returned: {ret}")

if __name__ == '__main__':
    main()