from typing import Union, List, Tuple, Optional
import numpy as np

class FenwickTree:
    """
    Implementation of Fenwick Tree. Fenwick Tree is an efficient data structure when performing prefix operations
    on a fixed sized array where we frequently:
    * query the prefix operation
    * update the elements in the array
    The query and update operations are done in O(logn) time
    """
    def __init__(self, n):
        self.size = n
        self.tree = [0] * (n + 1)

    def update(self, i, delta):
        """
        To update, start at i and use update rule i += LSB(i).
        Add this value to BITree[i] while i is in range.
        :param i:       Starting index
        :param delta:   Value to add to BITree
        :return:
        """
        while i <= self.size:
            self.tree[i] += delta
            i += (i & -i)

    def query(self, i):
        """
        To query, start at i and use query rule i -= LSB(i).
        Start with sum = 0, and add BITree[i] while i is in range.
        :param i:   Starting index
        :return:
        """
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= (i & -i)
        return s

    def reset_frequency(self):
        """
        Maintains the tree structure but resets all values to back to 0.
        :return:
        """
        self.tree = [0] * (self.size + 1)

def count_less_than(arr):
    # Step 1: Coordinate Compression. Sort the numbers array, and give each element an index in increasing
    # order starting with index 1. Repeated values share the same index since we will be counting the frequency
    # a number appears in the array.
    sorted_vals = sorted(set(arr))  # Unique sorted values

    # Takes value from our original array as an index and maps it to its new compressed index.
    value_map = {val: idx + 1 for idx, val in enumerate(sorted_vals)}  # Map to [1, N] since Fenwick trees are 1-indexed

    # Step 2: Fenwick Tree
    n = len(arr)
    bit = FenwickTree(len(sorted_vals))
    # Result holds the number of elements before i that are smaller. Of course, the first element must be 0
    result = [0]

    for i in range(n - 1):
        # Add arr[i] to BIT, increasing its frequency by 1
        bit.update(value_map[arr[i]], 1)
        # Get compressed index for arr[i+1]
        val = value_map[arr[i + 1]]
        # Count elements < arr[i+1] by summing the frequency up numbers smaller than arr[i+1]
        count = bit.query(val - 1)
        # append the count
        result.append(count)

    return result


class Solution:
    def kBigIndices(self, nums: List[int], k: int) -> int:

        num_less_than = count_less_than(nums)
        num_greater_than = count_less_than(nums[::-1])[::-1]
        count = 0
        for i in range(len(nums)):
            if num_less_than[i] >= k and num_greater_than[i] >= k:
                # this element meets to k-big conditions
                count += 1

        return count
def main():
    # input_nums = [2,3,6,5,2,3]
    # input_k = 2
    # input_nums = [1,1,1]
    # input_k = 3
    input_nums = [7, 7, 8, 11, 7, 15, 16, 7, 7]
    input_k = 2
    # input_nums = [3, 8, 4, 2, 5, 3, 8, 6]
    # input_k = 1

    print(f"Input (k = {input_k}): \n{input_nums}")

    sol_obj = Solution()
    ret = sol_obj.kBigIndices(input_nums, input_k)
    print(f"Solution returned: {ret}")

if __name__ == '__main__':
    main()