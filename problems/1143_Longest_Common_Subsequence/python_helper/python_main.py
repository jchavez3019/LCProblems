from typing import Tuple, Union, List, Dict, Optional

class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str, verbose=False) -> int:
        # row_text refers to the string we iterate over w.r.t. i
        # col_text refers to the string we iterate over w.r.t. j
        # we care about length in order to minimize space when we store our sub-problems
        if len(text1) < len(text2):
            row_text = text2
            col_text = text1
        else:
            row_text = text1
            col_text = text2

        # Holds our solutions. Since we only need to hold space for the current row and the row below,
        # we use only O(2min(m, n) + 1) space, or O(min(m,n)).
        # We use +1 so that we do not have to explicitly handle out of range errors when indexing the
        # cols.
        # Since prior_row is initialized with 0s, we don't experience out of range errors when indexing
        # the rows.
        prior_row = [0] * (len(col_text) + 1)
        curr_row = [0] * (len(col_text) + 1)

        # iterate through all rows
        for i in range(len(row_text) - 1, -1, -1):

            # now process each element in the row
            for j in range(len(col_text) - 1, -1, -1):
                a = prior_row[j]  # element below this one
                b = curr_row[j+1]  # element to the right
                # bottom-right only valid if the current characters match
                c = 1 + prior_row[j+1] if row_text[i] == col_text[j] else 0
                # take the best solution
                curr_row[j] = max(a, b, c)

            # now swap curr_row and prior_row
            prior_row, curr_row = curr_row, prior_row
        # final solution is stored in the top left index
        return prior_row[0]
    # def longestCommonSubsequence(self, text1: str, text2: str, verbose=False) -> int:
    #     """
    #     This solution seems to be correct, but it exceeds the time limit.
    #     You have become too comfortable writing recursion problems as a tree like structure with a while-loop
    #     and a stack. This dynamic programming problem can be written iteratively using a for-loop instead of a
    #     while-loop. Further, the solutions can be stored in a matrix, not a dictionary/tree.
    #     :param text1:
    #     :param text2:
    #     :param verbose:
    #     :return:
    #     """
    #
    #     if len(text1) < len(text2):
    #         main_string = text2
    #         dp_string = text1
    #     else:
    #         main_string = text1
    #         dp_string = text2
    #
    #     stack = [dp_string]
    #     solution_dict = {}
    #     maximum_subsequence = 0
    #     max_substring = ""
    #     while len(stack) > 0:
    #
    #         curr_substring = stack.pop()
    #
    #         if curr_substring in solution_dict.keys():
    #             # we have already solved this substring before, continue
    #             continue
    #
    #         if len(curr_substring) == 1:
    #             # this is a single character, find where it exists in the main_string if it does
    #             curr_char = curr_substring[0]
    #             found_char = False
    #             for i, c in enumerate(main_string):
    #                 if c == curr_char:
    #                     solution_dict[curr_substring] = i
    #                     found_char = True
    #                     if 1 > maximum_subsequence:
    #                         maximum_subsequence = 1
    #                         max_substring = curr_substring
    #                     break
    #             if found_char is False:
    #                 solution_dict[curr_substring] = -1
    #
    #             continue
    #
    #         substring_a = curr_substring[:-1]
    #         substring_b = curr_substring[-1]
    #         if substring_a in solution_dict.keys():
    #             # First substrings have been processed, we can now solve this current substring
    #             a_val = solution_dict[substring_a]
    #             if a_val == -1:
    #                 # This substring does not exist. We still need to say that its solution DNE
    #                 solution_dict[curr_substring] = -1
    #             else:
    #                 b_val = -1
    #                 for i, c in enumerate(main_string[a_val + 1:]):
    #                     if c == substring_b:
    #                         b_val = i + a_val + 1
    #                         break
    #
    #                 if b_val == -1:
    #                     # This substring does not exist. We still need to say that its solution DNE
    #                     solution_dict[curr_substring] = -1
    #                 else:
    #                     # Substring_a and substring_b exist, and substring_a comes before substring_b. Therefore,
    #                     # this substring exists. Put in its solution and update the maximum subsequence
    #                     solution_dict[curr_substring] = b_val
    #                     if len(curr_substring) > maximum_subsequence:
    #                         maximum_subsequence = len(curr_substring)
    #                         max_substring = curr_substring
    #
    #         else:
    #             # append this substring back into the stack so that it can be processed later
    #             stack.append(curr_substring)
    #
    #         # It may be possible that this substring may have been solved without having to explore all of its children.
    #         # However, we want to make sure that all of its children are eventually solved since other subproblems
    #         # may depend on them. Therefore, we always check if we can append the children into the stack.
    #
    #         # get all subsequences of length - 1 with the first character fixed
    #         first_char = curr_substring[0]
    #         rest_seq = curr_substring[1:]
    #         for i in range(len(rest_seq)):
    #             subproblem = first_char + rest_seq[:i] + rest_seq[i+1:]
    #             if subproblem not in solution_dict.keys():
    #                 stack.append(subproblem)
    #         # get the last subsequence
    #         if curr_substring[1:] not in solution_dict.keys():
    #             stack.append(curr_substring[1:])
    #
    #     if verbose:
    #         print(solution_dict)
    #         print(f"Maximum subsequence: {max_substring}")
    #     return maximum_subsequence

def main():
    text1 = "abcde"
    text2 = "ace"
    text1 = "abc"
    text2 = "abc"
    text1 = "abc"
    text2 = "def"
    # text1 = "hofubmnylkra"
    # text2 = "pqhgxgdofcvmr"
    # text1 = "abcba"
    # text2 = "abcbcba"
    # text1 = "bsbininm"
    # text2 = "jmjkbkjkv"
    # text1 = "mhunuzqrkzsnidwbun"
    # text2 = "szulspmhwpazoxijwbq"
    print(f"Inputs: \n{text1}\n{text2}")

    sol_obj = Solution()
    ret = sol_obj.longestCommonSubsequence(text1, text2, True)
    print(f"Solution returned: {ret}")

if __name__ == '__main__':
    main()