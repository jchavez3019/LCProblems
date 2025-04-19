import numpy as np
from typing import List, Tuple, Optional, Union
import sys

class Solution:

    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        # # This old implementation uses recursion which Python does not like
        # self.rows: int = len(board)
        # self.cols: int = len(board[0])
        # self.board = board
        # self.adjacent_indices = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        #
        # if self.rows < 3 or self.cols < 3:
        #     return
        #
        # self.visited = np.zeros((self.rows, self.cols), dtype=bool)
        #
        # for i in range(1, self.rows - 1):
        #     for j in range(1, self.cols - 1):
        #
        #         if self.board[i][j] == 'X' or self.visited[i, j]:
        #             continue
        #
        #         self.curr_region = [(i, j)]
        #         is_region = self.traverse_region(i, j)
        #
        #         if not is_region:
        #             oi, oj = zip(*self.curr_region)
        #             self.board[oi][oj] = 'O'
        #
        # board = self.board

        # This new implementation uses a stack. Some things to consider when using a stack instead of function recursion:
        # 1) Does the current subproblem's solution depend on the next subproblem's solution? If so, then you should
        #       create a hash table recording these dependencies and at the end, travel through this table
        #       to update the final solution for all the subproblems that have been encountered
        # 2) Does the overall solution only depend on one subproblem? If so, we can greedily predict the solution to
        #       subrpoblems and track the ones we have encountered in a list. If a subproblem encounters a base case
        #       that affects all subproblems, we should update a global flag to tell us this global result. Finally,
        #       we should update the solutions to all subproblems. In this scenario, the subproblems do not depend
        #       directly on the next subproblem, but rather, every subproblem depends on one subproblem. This problem
        #       is an example of this case.

        rows: int = len(board)
        cols: int = len(board[0])
        adjacent_indices = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        if rows < 3 or cols < 3:
            return

        visited = np.zeros((rows, cols), dtype=bool)

        for i in range(1, rows - 1):
            for j in range(1, cols - 1):

                if board[i][j] == 'X' or visited[i, j]:
                    continue

                curr_region = [(i, j)]
                is_region = True
                stack = [(i, j)]

                while len(stack) > 0:
                    curr_i, curr_j = stack.pop()
                    visited[curr_i, curr_j] = True
                    curr_region.append((curr_i, curr_j))
                    board[curr_i][curr_j] = 'X'

                    if curr_i == 0 or curr_i == rows - 1 or curr_j == 0 or curr_j == cols - 1:
                        is_region = False
                        continue

                    for m, n in adjacent_indices:
                        if board[curr_i + m][curr_j + n] == 'O':
                            stack.append((curr_i + m, curr_j + n))

                if not is_region:
                    for oi, oj in curr_region:
                        board[oi][oj] = 'O'

        self.board = board

    # def traverse_region(self, i, j):
    #
    #     self.visited[i, j] = True
    #     self.curr_region.append((i, j))
    #     if i == 0 or i == self.rows - 1 or j == 0 or j == self.cols - 1:
    #         return False
    #
    #     for m, n in self.adjacent_indices:
    #         if self.board[i + m][j + n] == 'O':
    #             other_ret = self.traverse_region(i + m, j + n)
    #
    #             if not other_ret:
    #                 return False
    #
    #     self.board[i][j] = 'X'
    #
    #     return True

def main():
    input_board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]
    input_board = [["O","O","O"],["O","O","O"],["O","O","O"]]
    # output_board = [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]
    sol_obj = Solution()
    sol_obj.solve(input_board)
    print(f"Input: \n{input_board}")
    # print(f"Ground truth: \n{output_board}")
    print(f"Output: \n{sol_obj.board}")

if __name__ == '__main__':
    main()