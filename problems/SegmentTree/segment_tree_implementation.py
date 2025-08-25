from typing import *
from sys import getsizeof
from abc import ABC, abstractmethod

class SegmentTree(ABC):
    """
    Abstract base class for segment-tree implementations.
    """
    def __init__(self, global_interval: Tuple[int, int], initial_values: Optional[List[Union[int, float, bool]]] = None,
                 verbose_init: bool = False):
        """
        Initializes a segment tree. Over some interval range, integer points lying on the range can be assigned
        yes/no truth values. Queries over inclusive ranges can be answered regarding point intersection.

        Note that the segment tree best supports ranges that contain a number of integer points that are a power of 2.
        If the number of points in the given global interval is not a power of 2, the range will be expanded.

        :param global_interval:     1D range the segment tree will capture.
        :param initial_values:      Initial values of the segment tree.
        :param verbose_init:        When true, prints additional information during initialization.
        """
        start, end = global_interval
        o_num_points = end - start + 1

        # calculate how many bits it takes to reproduce the last index in our array
        self.num_bits: int = (o_num_points - 1).bit_length()
        # we need 2^{num_bits + 1} or 4^{num_bits} to produce a segment tree over this range
        self.size: int = 2 << self.num_bits
        # initialize the tree
        self.tree: List[bool] = [False] * self.size

        # If the global interval given does not yield a number of integer points that is a power of 2,
        # we will manually extend the range.
        # NOTE: The initial values are still expected to have length equal to the number of integer points in the
        # originally given global interval.
        self.num_points: int = 1 << self.num_bits
        self.start: int = start
        self.end: int = self.start + self.num_points - 1
        if verbose_init:
            print(f"Given [start, end]: [{start}, {end}].\n"
                  f"Updating range to [{self.start}, {self.end}].\n"
                  f"Now supporting {self.num_points} points from {o_num_points}.")

        # other notable attributes
        self.max_sd: int = self.num_bits # maximum split depth
        self.leaf_node_start_idx: int = 1 << self.num_bits # the idx of the first leaf node in the tree

        if initial_values:
            # use the initial values to update the tree
            assert o_num_points <= len(initial_values) <= self.num_points, ("The given initial values must initialize "
                                                                            "every integer point in the global "
                                                                            "interval.")

            # get the index of the last leaf node in the tree that will be initialized
            stop_idx = self.leaf_node_start_idx + len(initial_values)
            # initialize the values in the tree given these initial values
            self.tree[self.leaf_node_start_idx : stop_idx] = initial_values

            # We already initialized the leaf nodes at the last split depth.
            # Start at the second to last split depth.
            # For this tree, the maximum split depth is 2^{num_bits}.
            curr_split_depth = self.num_bits - 1
            curr_idx = self.leaf_node_start_idx
            for sd in range(curr_split_depth, -1, -1):

                # number of nodes at this split depth
                num_nodes = 1 << sd
                # we update our current index to point at the first node at our current split depth
                curr_idx -= num_nodes
                for i in range(curr_idx, curr_idx + num_nodes):
                    # for every node in this split depth, update if either child node is True
                    self.tree[i] = self._check(self.tree[i<<1], self.tree[(i<<1) + 1])

    def update(self, x: int, val: Union[int, float, bool]):
        """
        Given an integer point on the segment tree's range, update its truth value and the internal state of the tree.
        :param x:       Integer point in the tree's range.
        :param val:     The point's new truth value.
        :return:
        """

        assert self.start <= x <= self.end, f"{x} is not in the range [{self.start}, {self.end}]"

        # update the leaf node corresponding to point x
        x_idx = self.leaf_node_start_idx + x - self.start
        self.tree[x_idx] = val

        # update the segment tree
        x_idx >>= 1
        while x_idx > 0:
            # update this node by its children
            self.tree[x_idx] = self._check(self.tree[x_idx << 1], self.tree[(x_idx << 1) + 1])
            # move to the next parent node
            x_idx >>= 1

    def query(self, l: int, r: int) -> Union[int, float, bool]:
        """
        Given a range [l, r] ⊆ [start, end], check if the given range contains a point that has been stored
        in the segment tree. Note that [start, end] is the range that the segment tree supports.
        :param l:   Left endpoint of the given range.
        :param r:   Right endpoint of the given range.
        :return:    Truth value verifying or falsifying the existence of a point in the given range.
        """
        assert self.start <= l <= r <= self.end, (f"Please fix interval endpoints. Given range [{l}, {r}] but the tree "
                                                  f"only supports inclusive ranges in [{self.start}, {self.end}]")
        idx = 1 # first index into the segment tree
        return self._recurse_query(idx, l, r, self.start, self.end)

    def _recurse_query(self, idx: int, l: int, r: int, gl: int, gr: int) -> Union[int, float, bool]:
        """
        Recursive helper method which breaks the problem of verifying/falsifying the existence of a point in a
        given range into smaller subproblems.
        :param idx: Current tree node's index.
        :param l:   Left endpoint of the given query range.
        :param r:   Right endpoint of the given query range.
        :param gl:  Left endpoint of the tree node's range.
        :param gr:  Right endpoint of the tree node's range.
        :return:    Truth value verifying or falsifying the existence of a point in the given range.
        """
        if l == gl and r == gr:
            # the query range matches the range of the node in the tree, no need
            # to recurse further
            return self.tree[idx]

        # form the indices of the child nodes
        l_idx = idx << 1
        r_idx = l_idx + 1
        # the midpoint value of the tree node's range
        g_midpoint = (gr + gl) // 2

        if l <= g_midpoint and g_midpoint + 1 <= r:
            # Split the given range into two smaller ranges. Check on each range if it intersects a point.
            a = self._recurse_query(l_idx, l, g_midpoint, gl, g_midpoint)
            b = self._recurse_query(r_idx, g_midpoint + 1, r, g_midpoint + 1, gr)
            return self._check(a, b)
        elif r <= g_midpoint:
            # The given range inclusively belongs to the left subchild. Recurse left.
            return self._recurse_query(l_idx, l, r, gl, g_midpoint)
        elif g_midpoint + 1 <= l:
            # The given range inclusively belongs to the right subchild. Recurse right.
            return self._recurse_query(r_idx, l, r, g_midpoint + 1, gr)
        else:
            # Erroneous error with the given range and the subchild's range.
            raise AssertionError(f"Expected [l, r] ⊆ [gl, gr] but instead, given [l, r]: [{l}, {r}] and "
                                 f"[gl, gr]: [{gl}, {gr}].")

    @staticmethod
    @abstractmethod
    def _check(a: Union[int, float, bool], b: Union[int, float, bool]) -> Union[int, float, bool]:
        """
        Defines how the values between two nodes should be compared, e.g. 'or', 'max', and 'min'.
        :param a:   Value from node 'a'.
        :param b:   Value from node 'b'.
        :return:    Result from comparison check.
        """
        pass

    def __len__(self) -> int:
        """
        Returns the number of nodes in the segment tree. Note that this is one less than the length of the array
        allocated for the segment tree as the 0'th index is never used. This is common as 1-indexing is more
        intuitive and simpler for binary trees.
        """
        return self.size - 1

    def __sizeof__(self):
        """
        Return the memory footprint of the segment tree.
        """
        return getsizeof(self.tree)

    def __eq__(self, other):
        """
        Returns whether two segment trees are equal in values and range.
        :param other:   The other segment tree in the comparison.
        :return:        Comparison truth value.
        """
        return self.tree == other.tree and self.start == other.start and self.end == other.end

class MaxSegmentTree(SegmentTree):
    """
    Implementation of the "max" logic segment tree. These trees are capable of answering "max" types of queries
    on 1D ranges.
    """
    @staticmethod
    def _check(a, b):
        return max(a, b)

class MinSegmentTree(SegmentTree):
    """
    Implementation of the "min" logic segment tree. These trees are capable of answering "min" types of queries
    on 1D ranges.
    """
    @staticmethod
    def _check(a, b):
        return min(a, b)

class AnySegmentTree(SegmentTree):
    """
    Implementation of the "OR" logic segment tree. These trees are capable of answering "OR" types of queries
    on 1D ranges.
    """
    @staticmethod
    def _check(node_a: bool, node_b: bool) -> bool:
        return node_a or node_b

    def __repr__(self) -> str:
        """
        Returns a string representation of the segment tree's values.
        :return: String representation.
        """
        if self.size >= 10**4:
            print(f"Warning: Segment tree has {self.size} nodes which is at least 10^4 nodes. This may lead"
                  f"to strange printing behavior.")

        repr_strs = ["Segment Tree Values: "]
        curr_idx = 1
        for i in range(self.max_sd + 1):
            num_nodes = 1 << i # number of nodes at this split depth
            repr_strs.append(f"Split Depth: {i} | \t" + "  ".join(
                # Maps each value in the current split depth to a string.
                # Since the tree contains truth values, we pad the end of each string with spaces to a length of 5 (the
                # number of characters in 'False').
                map(lambda t : (f"[{curr_idx + t[0]:04d}]" + str(t[1])).ljust(11),
                    enumerate(self.tree[curr_idx:curr_idx+num_nodes]))
            ))
            # update to idx of the first node at the next split depth
            curr_idx += num_nodes

        return "\n".join(repr_strs)


def example(global_interval: Tuple[int, int], initial_values: List[int]):
    segment_tree = AnySegmentTree(global_interval, initial_values)

    print("Initial Segment Tree")
    print(segment_tree)

    update_args = {"x": 0, "val": True}
    segment_tree.update(**update_args)
    print(f"\nSegment Tree after updating with argument: {update_args}")
    print(segment_tree)

    check_range = (1, 3)
    check_result = segment_tree.query(*check_range)
    print(f"\nDoes range {check_range} contain a point? {check_result}")


if __name__ == "__main__":
    sample_input = {
        "global_interval": (0, 9), # inclusive range
        "initial_values": [False, False, False, False, False, False, True, False, False, False],
    }
    g_start, g_end = sample_input["global_interval"]
    len_inputs = len(sample_input["initial_values"])
    assert g_end - g_start + 1 == len_inputs, f"Length of inputs ({len_inputs}) does not match range [{g_start}, {g_end}]"
    example(**sample_input)