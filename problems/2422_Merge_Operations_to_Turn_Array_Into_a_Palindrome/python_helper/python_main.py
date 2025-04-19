from typing import List, Union, Tuple, Optional

class Solution:
    def minimumOperations(self, nums: List[int]) -> int:

        left_ptr = 0
        right_ptr = len(nums) - 1
        num_ops = 0  # track number of merge operations we perform
        while left_ptr <= right_ptr:
            l_el = nums[left_ptr]
            r_el = nums[right_ptr]
            if l_el == r_el:
                # these symmetric elements are the same, advance both pointers
                left_ptr += 1
                right_ptr -= 1
                continue

            # since values are non-negative, we should perform the merge operation
            # on the element that is smaller
            if l_el < r_el:
                left_ptr += 1
                nums[left_ptr] += l_el
            else:
                right_ptr -= 1
                nums[right_ptr] += r_el

            num_ops += 1

        return num_ops


def main():
    input_arr = [4,3,2, 1, 2, 3, 1]
    # input_arr = list(range(1, 5))
    print(f"Input: \n{input_arr}")

    sol_obj = Solution()

    ret = sol_obj.minimumOperations(input_arr)
    print(f"Solution returned: {ret}")


if __name__ == '__main__':
    main()