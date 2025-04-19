from typing import List, Optional, Union, Tuple
import heapq
import numpy as np

INF = float('inf')

class Solution:
    def partitionString(self, s: str) -> int:
        visited = np.zeros(26)
        num_partitions = 1
        for i in range(len(s)):
            val = ord(s[i]) - ord('a')
            if visited[val] == 1:
                visited *= 0
                num_partitions += 1
            visited[val] = 1

        return num_partitions

    # FIXME:
    #  This solution is inefficient. This is not a dynamic programming problem. Since the objective is to have
    #  the least number of partitions, we should not consider the option of starting a new partition if a letter
    #  is not repeated. We should ONLY start a new partition if we have seen a character again.
    # def partitionString(self, s: str) -> int:
    #
    #     if len(s) == 1:
    #         # Only 1 element so there can only be 1 partition
    #         return 1
    #
    #     stack = []
    #     heapq.heappush(stack, (0, 0, 0))
    #     min_partitions = INF
    #     while len(stack) > 0:
    #         # p_idx := partition idx where p_idx + 1 is the number of partitions in this sub-problem
    #         # s_idx := index into the string
    #         # p_start_idx := the index in the string where this partition starts at
    #         p_idx, s_idx, p_start_idx = heapq.heappop(stack)
    #
    #         if p_idx + 1 > min_partitions:
    #             # This partition is already too long, terminate this sub-problem
    #             continue
    #
    #         if s_idx + 1 >= len(s):
    #             # base case where we have reached the end of the string
    #             min_partitions = min(min_partitions, p_idx + 1)
    #             break
    #
    #         next_char = s[s_idx + 1]
    #         is_repeated = next_char in s[p_start_idx:s_idx + 1]
    #         if not is_repeated:
    #             # This character was not repeated. One potential solution is to continue adding letters to this
    #             # partition.
    #             heapq.heappush(stack, (p_idx, s_idx + 1, p_start_idx))
    #         # Whether the character was repeated or not, a potential solution will always be to start a new partition.
    #         heapq.heappush(stack, (p_idx + 1, s_idx + 1, s_idx + 1))
    #
    #     return int(min_partitions)

def main():
    input_string = "abacaba"
    # input_string = "ssssss"
    # input_string = "lvkmzlaeaxbprczpfarnlaptfvmutkfsatyywnxpmkpduwoqeeiltbdjipwihqi"

    print(f"Input: \n{input_string}")

    sol_obj = Solution()
    ret = sol_obj.partitionString(input_string)

    print(f"Solution returned: {ret}")

if __name__ == '__main__':
    main()