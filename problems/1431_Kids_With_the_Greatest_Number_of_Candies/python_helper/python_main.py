from typing import *
import numpy as np

class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        largest_candies = max(candies)
        ret = [False] * len(candies)
        for i, c in enumerate(candies):
            if c + extraCandies >= largest_candies:
                ret[i] = True

        return ret

def main():
    test_cases = {
        "1": {
            "candies": [2, 3, 5, 1, 3],
            "extraCandies": 3
        }
    }

    solution = Solution()

    for tk, targs in test_cases.items():
        ret = solution.kidsWithCandies(**targs)
        print(f"test case {tk}: {targs}\nReturned: {ret}")

if __name__ == '__main__':
    main()