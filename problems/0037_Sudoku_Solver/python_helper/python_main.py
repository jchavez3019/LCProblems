from typing import *

class Solution:
    def solveSudoku(self, board: List[List[str]], verbose: bool = False) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        rbm = [0] * 9
        cbm = [0] * 9
        gbm = [0] * 9
        is_fixed = [False] * 81
        gbm_idx = lambda i, j : (i//3)*3 + (j//3)
        first_bit_mask = 0x0001

        # fill in the bit-masks with the fixed numbers on the board
        for k in range(81):
            i = k // 9
            j = k % 9
            char = board[i][j]
            if char != ".":
                g = gbm_idx(i, j)
                num = int(char) - 1
                is_fixed[k] = True
                rbm[i] |= 0x0001 << num
                cbm[j] |= 0x0001 << num
                gbm[g] |= 0x0001 << num

        # lambda function that applies the bit mask
        # the returned number will be 1 or 0
        gv = lambda num, idx, bitset : (bitset[idx] >> num) & first_bit_mask

        def backtracking(k):
            if k >= 81:
                # base case, we are out of range of the board
                return True

            if is_fixed[k]:
                return backtracking(k+1)

            nonlocal rbm, cbm, gbm
            i = k // 9
            j = k % 9
            g = gbm_idx(i, j)
            for e in range(9):
                if (gv(e, i, rbm) | gv(e, j, cbm) | gv(e, g, gbm)) == 0:
                    rbm[i] |= 0x0001 << e
                    cbm[j] |= 0x0001 << e
                    gbm[g] |= 0x0001 << e
                    if backtracking(k+1):
                        board[i][j] = str(e + 1)
                        return True
                    else:
                        rbm[i] &= ~(0x0001 << e)
                        cbm[j] &= ~(0x0001 << e)
                        gbm[g] &= ~(0x0001 << e)
            return False
        backtracking(0)

def main():
    test_cases = {
        "1": {
            "board": [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]],
            "expected": [["5","3","4","6","7","8","9","1","2"],["6","7","2","1","9","5","3","4","8"],["1","9","8","3","4","2","5","6","7"],["8","5","9","7","6","1","4","2","3"],["4","2","6","8","5","3","7","9","1"],["7","1","3","9","2","4","8","5","6"],["9","6","1","5","3","7","2","8","4"],["2","8","7","4","1","9","6","3","5"],["3","4","5","2","8","6","1","7","9"]],
        },
    }

    solution = Solution()

    for tk, targs in test_cases.items():
        expected = targs.pop("expected", None)
        solution.solveSudoku(**targs, verbose=True)
        ret = targs["board"]
        if expected is not None:
            passed = ret == expected
        else:
            passed = None
        print(f"test case {tk}: {targs}\nReturned: {ret}, Expected: {expected}\nPassed:{passed}\n")

if __name__ == '__main__':
    main()