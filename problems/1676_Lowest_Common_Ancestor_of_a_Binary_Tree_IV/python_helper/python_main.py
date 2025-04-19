from typing import Union, Tuple, List, Optional, Dict
from math import log2

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x: int):
        self.val: int = x
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', nodes: 'List[TreeNode]') -> 'TreeNode':

        if len(nodes) == 1:
            # simple case where a single node's LCA is itself
            return nodes[0]

        stack: List[Tuple[TreeNode, bool]] = [(root, False)]  # (node, is_processed)
        solutions: Dict[int, TreeNode] = {}
        while len(stack) > 0:
            node, is_processed = stack.pop()

            if node in nodes:
                solutions[node.val] = node
                continue

            if node.left is not None or node.right is not None:
                # This node has children. Either we 1) process this node or 2) push to the stack for future processing.

                if not is_processed:
                    # node was not processed, push this node and its children
                    stack.append((node, True))
                    if node.left is not None: stack.append((node.left, False))
                    if node.right is not None: stack.append((node.right, False))
                else:
                    # Node was processed and its children may have solutions.
                    # If the children do not have solutions, none of them are the LCA, and neither is this node.
                    # If one of the children has a solution, then so does this node.
                    left_key_exists = node.left is not None and node.left.val in solutions.keys()
                    right_key_exists = node.right is not None and node.right.val in solutions.keys()
                    if left_key_exists and right_key_exists:
                        # both children found a node in the list, this node is their LCA
                        solutions[node.val] = node
                    elif left_key_exists:
                        # only left child found a node in the list, let it remain the LCA
                        solutions[node.val] = solutions[node.left.val]
                    elif right_key_exists:
                        # only right child found a node in the list, let it remain the LCA
                        solutions[node.val] = solutions[node.right.val]

        # return the final solution
        return solutions[root.val]

def create_tree(node_values: List[int], node_int_list: Union[Tuple[int], List[int]] = ()) -> Tuple[TreeNode, List[TreeNode]]:

    root_node = TreeNode(node_values[0])

    # values in stack are (TreeNode, idx of TreeNode in node_values)
    stack = [(root_node, 0)]
    node_list = []

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

        if curr_node.val in node_int_list:
            node_list.append(curr_node)

    return root_node, node_list

def main():
    tree_list = [3,5,1,6,2,0,8,None,None,7,4]
    node_int_list = [4,7]
    root, node_list = create_tree(tree_list, node_int_list)
    print(f"Input tree list: \n{tree_list}")
    print(f"Input node list: \n{node_int_list}")

    sol_obj = Solution()
    ret = sol_obj.lowestCommonAncestor(root, node_list)

    print(f"Solution returned: \n{ret.val}")

if __name__ == '__main__':
    main()