from typing import Union, List, Tuple, Optional
# from math import ceil


class Solution:
    def minSwaps(self, data: List[int]) -> int:

        total_ones = data.count(1)  # total ones in the entire array
        # pointers to track our sliding window
        left_ptr = 0
        right_ptr= 0
        num_ones = 0  # current number of ones in the sliding window
        max_ones = 0  # max number of ones found in any sliding window

        while right_ptr < len(data):
            # iterate until we have tried all valid sliding windows

            # include this new element and update the right ptr
            num_ones += data[right_ptr]
            right_ptr += 1
            if right_ptr - left_ptr > total_ones:
                # the sliding window is too large, remove the first element
                # by updating the left_ptr and the num_ones in this updated window
                num_ones -= data[left_ptr]
                left_ptr += 1
            max_ones = max(max_ones, num_ones)

        # The minimum number of zeros in a sub array is equivalent to the length of the sliding window
        # (which is the total number of ones in the array) minus the maximum number of ones in the sliding window.
        # We want the minimum number of zeros since this corresponds to the minimum number of swaps.
        return total_ones - max_ones

def main():
    # input_data = [1, 0, 1, 0, 1]
    # input_data = [1,0,1,0,1,0,0,1,1,0,1]
    input_data = [1,0,0,1,1,1]

    print(f"Input: \n{input_data}")
    sol_obj = Solution()

    ret = sol_obj.minSwaps(input_data)
    print(f"Solution returned: {ret}")

if __name__ == '__main__':
    main()