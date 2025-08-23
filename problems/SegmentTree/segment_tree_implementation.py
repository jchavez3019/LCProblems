from typing import *

class AnySegmentTree:
    def __init__(self, global_interval: Tuple[int, int], initial_values: Optional[List[int]] = None):
        """

        :param global_interval:
        :param initial_values:
        """
        self.start, self.end = global_interval
        self.num_points = self.end - self.start + 1

        # calculate how many bits it takes to reproduce the last index in our array
        self.num_bits = (self.num_points - 1).bit_length()
        # we need 2^{num_bits + 1} or 4^{num_bits} to produce a segment tree over this range
        self.size = 2 << self.num_bits
        # initialize the tree
        self.tree = [False] * self.size

        # other notable attributes
        self.max_sd = self.num_bits # maximum split depth

        if initial_values:
            assert len(initial_values) == self.num_points, ("The given initial values must initialize every integer "
                                                            "point in the global interval.")
            # get the idx of the first leaf node in the tree
            self.leaf_node_start_idx = 1 << self.num_bits
            # get the index of the last leaf node in the tree
            stop_idx = self.leaf_node_start_idx + self.num_points
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
                    self.tree[i] = self.tree[i<<1] or self.tree[(i<<1) + 1]

    def update(self, x: int, val: bool):
        """

        :param x:
        :param val:
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
            self.tree[x_idx] = self.tree[x_idx << 1] or self.tree[(x_idx << 1) + 1]
            # move to the next parent node
            x_idx >>= 1

    def check(self, l: int, r: int) -> bool:
        """

        :param l:
        :param r:
        :return:
        """

        idx = 1 # first index into the segment tree
        return self._recurse_check(idx, l, r, self.start, self.end)

    def _recurse_check(self, idx: int, l: int, r: int, gl: int, gr: int):
        """

        :param idx:
        :param l:
        :param r:
        :param gl:
        :param gr:
        :return:
        """
        if idx >= self.leaf_node_start_idx:
            # the idx now belong to a leaf node, return its result
            return self.tree[idx]

        # form the indices of the child nodes
        l_idx = idx << 1
        r_idx = l_idx + 1
        g_midpoint = (gr + gl) // 2
        if l < g_midpoint < r:
            a = self._recurse_check(l_idx, l, g_midpoint, gl, g_midpoint)
            b = self._recurse_check(r_idx, g_midpoint, r, g_midpoint, gr)
            return a or b
        elif r <= g_midpoint:
            return self._recurse_check(l_idx, l, r, gl, g_midpoint)
        elif g_midpoint <= l:
            return self._recurse_check(r_idx, l, r, g_midpoint, gr)
        else:
            return False

    def __repr__(self) -> str:
        repr_strs = ["Segment Tree Values: "]
        curr_idx = 1
        for i in range(self.max_sd + 1):
            num_nodes = 1 << i
            repr_strs.append(f"Split Depth: {i} | \t" + "  ".join(
                map(lambda t : str(t), self.tree[curr_idx:curr_idx+num_nodes])
            ))
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


if __name__ == "__main__":
    sample_input = {
        "global_interval": (0, 9), # inclusive range
        "initial_values": [False, False, False, False, False, False, True, False, False, False],
    }
    g_start, g_end = sample_input["global_interval"]
    len_inputs = len(sample_input["initial_values"])
    assert g_end - g_start + 1 == len_inputs, f"Length of inputs ({len_inputs}) does not match range [{g_start}, {g_end}]"
    example(**sample_input)