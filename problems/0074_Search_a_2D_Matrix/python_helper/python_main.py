#%%
from typing import *
#%%
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int, verbose: bool = False) -> bool:
        m = len(matrix) # number of rows
        n = len(matrix[0]) # number of columns

        ptr = [m - 1, 0] # start our search at the bottom left

        while ptr[0] >= 0 and ptr[1] < n:
            # iterate while our pointer is in range

            # get the value of the current position we are in
            val = matrix[ptr[0]][ptr[1]]

            if val == target:
                # we have found our target, return True
                return True
            elif val < target:
                # Value is less than the target. It must be that all elements defined in the sub-matrix
                # with top-left corner (0, 0) and bottom-right corner (i, j) are less than our equal to
                # our value, so we should advance to the right.

                # In other words, we need to increase our value.
                ptr[1] += 1
            else:
                # Value is greater than the target. We already know that all elements defined in the
                # sub-matrix with top-left corner (0, 0) and bottom-right corner (i, j-1) are less than
                # our equal to our value. But our value at (i, j) is too large. We should move upwards
                # as that value is guaranteed to be smaller or equal to our current value.

                # In our words, we need to decrease our value.
                ptr[0] -= 1

        # Our pointer became out of range. The target value did not exist in the matrix.
        return False

def main():
    test_cases = {
        "1": {
            "matrix": [[1,3,5,7],[10,11,16,20],[23,30,34,60]],
            "target": 3,
            "expected": True,
        },
        "2": {
            "matrix": [[1,3,5,7],[10,11,16,20],[23,30,34,60]],
            "target": 13,
            "expected": False,
        },
    }

    solution = Solution()

    for tk, targs in test_cases.items():
        expected = targs.pop("expected", None)
        ret = solution.searchMatrix(**targs, verbose=True)
        if expected is not None:
            passed = ret == expected
        else:
            passed = None
        print(f"test case {tk}: {targs}\nReturned: {ret}, Expected: {expected}\nPassed:{passed}\n")


main()