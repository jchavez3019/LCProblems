from typing import *

class Solution:

    def getCanJump(self, nums: List[int]):
        n = len(nums)
        can_jump = [[False for _ in range(n-i+1)] for i in range(n)]

        for j in range(n - 1, -1, -1):
            j_el = nums[j]
            sat_one = True
            sat_two = True
            minNum = 10 ** 5 + 1
            maxNum = -1
            for i in range(j - 1, -1, -1):
                i_el = nums[i]
                if sat_one:
                    if i_el <= j_el and maxNum < i_el:
                        can_jump[i][j] = True
                    elif i_el > j_el:
                        sat_one = False
                if sat_two:
                    if i_el > j_el and minNum >= i_el:
                        can_jump[i][j] = True
                    elif i_el < j_el:
                        sat_two = False

                if not sat_one and not sat_two:
                    break

                minNum = min(minNum, i_el)
                maxNum = max(maxNum, i_el)

        return can_jump

    def minCost(self, nums: List[int], costs: List[int], verbose:bool=False) -> int:
        can_jump = self.getCanJump(nums)
        n = len(nums)
        if n == 1:
            # base case
            return 0
        tab = [10 ** 5 + 1 for _ in range(n)]
        tab[-1] = costs[-1]
        costs[0] = 0

        for j in range(n - 1, -1, -1):
            j_cost = tab[j]
            for i in range(j - 1, -1, -1):
                if can_jump[i][j]:
                    curr_cost = tab[i]
                    new_cost = j_cost + costs[i]
                    tab[i] = min(curr_cost, new_cost)

        if verbose:
            print(f"can_jump:\n{can_jump}")
            print(f"tab:\n{tab}")

        return tab[0]

def main():
    test_cases = {
        "1": {
            "nums": [3,2,4,4,1],
            "costs": [3,7,6,4,2],
            "expected": 8
        },
        "2": {
            "nums": [5,0,2,2,1],
            "costs": [1,2,4,4,0],
            "expected": 6
        },
        "3": {
            "nums": [2,4,2,2],
            "costs": [0,2,1,5],
            "expected": 8
        }
    }

    solution = Solution()

    for tk, targs in test_cases.items():
        expected = targs.pop("expected", None)
        ret = solution.minCost(**targs, verbose=True)
        if expected is not None:
            passed = expected == ret
        else:
            passed = None
        print(f"test case {tk}: {targs}\nReturned: {ret}, Expected: {expected}\nPassed:{passed}")


if __name__ == '__main__':
    main()