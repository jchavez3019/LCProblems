from typing import *
from math import log2, ceil

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def create_binary_tree(tree_list: List[int]) -> Optional[TreeNode]:
    """
    Given a list representation of a binary tree, we flesh out the binary tree and return its root.
    :param tree_list: List representation of the binary tree.
    :return:          Root of the newly created binary tree.
    """
    if len(tree_list) == 0:
        # empty tree
        return None

    root = TreeNode(tree_list[0])
    q: List[Optional[TreeNode]] = [root] # queue for creating nodes (queue over stack as it is easier to track indices)
    idx = 0

    # Since we enqueue None nodes for proper index updating, the queue may potentially never be empty
    # as we are allowed to push None to it. Therefore, instead of checking queue size, we should check
    # if the current index is in range.
    while idx < len(tree_list):

        node = q.pop(0) # dequeue from the front

        # get the idx into the list of the left/right child node
        l_idx = idx*2 + 1
        r_idx = idx*2 + 2
        # true if the left/right node is not None
        l_valid = (l_idx < len(tree_list)) and (tree_list[l_idx] is not None)
        r_valid = (r_idx < len(tree_list)) and (tree_list[r_idx] is not None)

        # create the left/right child nodes (set them as None if they don't exist)
        left_node = TreeNode(tree_list[l_idx]) if l_valid else None
        right_node = TreeNode(tree_list[r_idx]) if r_valid else None

        if node is not None:
            # if our current node is not None, then set its left and right children
            node.left = left_node
            node.right = right_node
        else:
            # as a precaution, ensure the children are None as well if the current node is None
            assert left_node is None and right_node is None, "Current node is None, its children should also be None."

        # enqueue the left and right child nodes to be processed later (even if they are None for proper idx updating)
        q.extend([left_node, right_node])
        idx +=1

    return root

def binary_tree_to_list(root: Optional[TreeNode], verbose: bool = False)->List[int]:
    """
    Given the root to a binary tree, we return its list representation.

    TODO:   I employ some interesting logic in order to ensure the returned list is of the appropriate length. However,
            another alternative would have been to modify the while loop to include None children and their indices.
            Therefore, we would not need to append the list. Instead, we can sort the list, and then trim it appropriately.
            The trimming would be done by finding the largest index is the list whose value is not None. From this max index,
            use it to calculate what the correct length of the list should be. Finally, trim the list to this correct length.

    :param root:    The root of the binary tree.
    :param verbose: If true, print statements become enabled to help with debugging.
    :return:        List representation of the binary tree.
    """
    if root is None:
        return []

    def _sort_values_and_indices(v: List[int], i: List[int])->Tuple[List[int], List[int]]:
        """
        Helper function which sorts the values and indices based on the indices. We also return the sorted indices
        instead of range(len(v)) since some indices may be missing. E.g., the sorted indices for a sorted list of
        length 3 may be {1, 3, 6} instead of {0, 1, 2}.
        :param v: Values to sort.
        :param i: Indices which we used to sort the values and the indices themselves.
        :return:  Sorted values and indices.
        """
        sorted_tuples = sorted(zip(v, i), key=lambda x : x[1])
        return [t[0] for t in sorted_tuples], [t[1] for t in sorted_tuples]

    # since we do not know how many elements are in the tree, we must use a stack and only process non-empty nodes
    stack: List[Tuple[TreeNode, int]] = [(root, 0)]
    values = [] # we will push values as we encounter them
    indices = [] # we will push indices as we encounter them (used for reordering the values at the end)
    while len(stack) > 0:
        node, idx = stack.pop()
        values.append(node.val)
        indices.append(idx)
        if node.left is not None:
            stack.append((node.left, idx*2 + 1))
        if node.right is not None:
            stack.append((node.right, idx*2 + 2))

    if verbose:
        print("values and indices after processing the stack")
        print(f"values: {values}")
        print(f"indices: {indices}")

    # We need to ensure the returned list is of the appropriate length. If not, we need to include None elements
    # in to the list.
    max_idx = max(indices)
    len_list = 2**ceil(log2(max_idx+1)) - 1
    appended = False # indicator if we had to increase the length of values and indices
    if len(values) < len_list:
        # values and indices are not long enough, we need to include more values.
        # The values are currently sorted based on when we encountered them in the stack. We sort them
        # based on indices so that this if block runs in O(nlogn) instead of O(n^2)
        values, indices = _sort_values_and_indices(values, indices)
        new_indices = []
        ptr = 0
        for i in range(len_list):
            if ptr >= len(indices) or i < indices[ptr]:
                new_indices.append(i)
            else:
                ptr += 1
        values.extend([None] * len(new_indices))
        indices.extend(new_indices)
        appended = True

    if verbose:
        print("values and indices after extending the list to the appropriate length")
        print(f"values: {values}")
        print(f"indices: {indices}")
    if verbose: print(f"List should be of length {len_list} because of max index {max_idx}. Values len: {len(values)}, Indices len: {len(indices)}")

    if appended:
        # if we had to append values, we must sort the list again
        values, _ = _sort_values_and_indices(values, indices)

    return values

class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode], verbose: bool = False) -> List[List[int]]:
        if root is None:
            return []

        # helper functions to push/pop from the correct stack/queue based on the use_queue flag
        pop = lambda : q.pop(0) if use_queue else s.pop()
        push = lambda x : q.append(x) if not use_queue else s.append(x)

        q = [root] # queue
        s = [] # stack
        use_queue = True
        ret, curr = [], []
        while len(q) > 0 or len(s) > 0:
            if (use_queue and len(q) == 0) or (not use_queue and len(s) == 0):
                use_queue = not use_queue
                ret.append(curr)
                curr = []

            node = pop()
            curr.append(node.val)
            if node.left is not None:
                push(node.left)
            if node.right is not None:
                push(node.right)

        if len(curr) > 0:
            ret.append(curr)

        return ret

def main():
    test_cases = {
        "1": {
            "root": [3,9,20,None,None,15,7],
            # "expected": True,
        },
        "2": {
            "root": [1],
            # "expected": False,
        },
        "3": {
            "root": [],
            # "expected": ,
        }
    }

    solution = Solution()

    for tk, targs in test_cases.items():
        expected = targs.pop("expected", None)
        root = create_binary_tree(targs["root"])
        ret = solution.zigzagLevelOrder(root, verbose=True)
        if expected is not None:
            passed = ret == expected
        else:
            passed = None
        print(f"test case {tk}: {targs}\nReturned: {ret}, Expected: {expected}\nPassed:{passed}\n")

if __name__ == '__main__':
    main()
