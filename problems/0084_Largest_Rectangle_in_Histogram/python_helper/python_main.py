"""
The stack should never be empty. The stack should contain rectangles that are strictly increasing.
"""

from typing import Tuple, Optional, List, Union

class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        n = len(heights)
        if n == 1:
            return heights[0]

        # Ensure last element is 0 in order to process last elements in stack
        n += 1
        heights = heights + [0]
        # Similar to saying we already processed the first element with index of -1 and height of 0;
        # Allows us to start processing the list correctly.
        stack = [(-1, 0)] # (index, height)
        max_area = 0
        for i in range(n):
            h = heights[i]

            if h > stack[-1][1]:
                # can add element while not violating rule
                # that stack must contain strictly increasing rectangles
                stack.append((i, h))

            # no h == stack[-1][1] case since this is redundant

            elif h < stack[-1][1]:
                # Appending this will violate stack rule. Must process elements
                # in stack by calculating their areas then removing them.
                while True:
                    if stack[-1][1] > h:
                        # rectangle is greater, must calculate area then remove it
                        s_i, s_h = stack.pop()
                        a = (i - s_i) * s_h
                        max_area = max(max_area, a)
                    elif stack[-1][1] == h:
                        # same height, don't need to push and done processing
                        break
                    elif stack[-1][1] < h:
                        # Top element is valid. Now we can finally push this element
                        # onto the stack. Since the previously popped element was greater
                        # than our current element, we can use its starting index, but
                        # use our height
                        stack.append((s_i, h))
                        break

        return max_area

def main():
    test_cases = [
        [2, 1, 5, 6, 2, 3],
        [2, 4],
        [4, 2, 0, 3, 2, 5]
    ]
    solutions = [10, 4, 6]
    sol_obj = Solution()
    for i, test_case, sol in zip(range(len(test_cases)), test_cases, solutions):
        print(f"Test case {i}: {test_case}\nSolution: {sol}")
        ret = sol_obj.largestRectangleArea(test_case)
        print(f"Returned: {ret}\nTest case: {'passed' if ret == sol else 'failed'}\n")

if __name__ == "__main__":
    main()