from typing import *


class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:

        # NOTE: Even though a triangle is like a binary tree, it is NOT a binary tree, so careful with trying
        # to index it like a binary tree

        max_split_depth = len(triangle)

        # We use O(d + 1) memory where is the number of split depths in the triangle
        # However, we use fewer elements in these arrays as we iterate upwards.
        # Naively, we could use a O(d x d + 1) matrix to hold our solutions. But we save memory by realizing
        # we don't need to save results from "two split depths ago".
        curr_arr = [0] * (max_split_depth + 1)      # solutions for current split depth
        prior_arr = [0] * (max_split_depth + 1)     # solutions for below split depth

        # first iterate in reverse via the split depths
        for i in range(max_split_depth - 1, -1, -1):

            # iterate through each element in the level
            for j in range(i, -1, -1):
                # our result depends on our element plus the minimum value of the left and right triangle
                # since prior_arr is initialized with 0s, our results are still sound on the first split depth iteration
                curr_arr[j] = triangle[i][j] + min(prior_arr[j], prior_arr[j+1])

            # swap arrays
            curr_arr, prior_arr = prior_arr, curr_arr

        return prior_arr[0]

def main():
    triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]
    triangle = [[-1]]
    print(f"Input: \n{triangle}")

    sol_obj = Solution()
    ret = sol_obj.minimumTotal(triangle)
    print(f"Solution returned: {ret}")

if __name__ == '__main__':
    main()