from typing import *
import numpy as np

class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int, verbose: bool = False) -> bool:

        n = len(matrix)
        m = len(matrix[0])
        matrix = np.array(matrix)

        def _bisect_1D(arr: List[int])->bool:
            n = len(arr)
            i = n // 2
            last_i = None
            while i != last_i:
                last_i = i
                if arr[i] == target:
                    return True
                elif arr[i] < target and i+1 < n and arr[i+1] > target:
                    return False
                elif arr[i] < target:
                    i = (i + n) // 2
                elif arr[i] > target:
                    i = i // 2
                else:
                    raise ValueError
            return False

        def _bisect_2D(start_pos: Tuple[int, int], stop_pos: Tuple[int, int]) -> bool:
            i_start, j_start = start_pos
            i_stop, j_stop = stop_pos
            i, j = (i_start + i_stop)//2, (j_start + j_stop)//2

            if i_stop == i_start + 1:
                return _bisect_1D(matrix[i_start, j_start:j_stop])
            elif j_stop == j_start + 1:
                return _bisect_1D(matrix[i_start:i_stop, j_start])

            last_pos = None
            while (i, j) != last_pos:
                last_pos = (i, j)

                if matrix[i, j] == target:
                    return True

                if matrix[i, j] < target and (i+1 < i_stop and j+1 < j_stop) and matrix[i+1, j+1] > target:
                    a_start_pos = (i+1, j_start)
                    a_stop_pos = (i_stop, j+1)
                    b_start_pos = (i_start, j+1)
                    b_stop_pos = (i+1, j_stop)
                    a = _bisect_2D(a_start_pos, a_stop_pos)
                    b = _bisect_2D(b_start_pos, b_stop_pos)
                    return a or b

                elif matrix[i, j] < target:
                    i, j = (i+i_stop)//2, (j+j_stop)//2

                elif matrix[i, j] > target:
                    i, j = (i_start + i) // 2, (j_start + j) // 2
                else:
                    raise ValueError

            return False

        return _bisect_2D((0, 0), (n, m))

def main():
    test_cases = {
        "1": {
            "matrix": [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]],
            "target": 5,
            "expected": True,
        },
        "2": {
            "matrix": [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]],
            "target": 20,
            "expected": False,
        },
        "3": {
            "matrix": [[-1,3]],
            "target": -1,
            "expected": True,
        },
        "4": {
            "matrix": [[4,6,9,10,15],[9,12,13,15,16]],
            "target": 14,
            "expected": False
        }
    }

    solution = Solution()

    for tk, targs in test_cases.items():
        expected = targs.pop("expected", None)
        ret = solution.searchMatrix(**targs, verbose=True)
        if expected is not None:
            passed = ret == expected
        else:
            passed = None
        print(f"test case {tk}: {targs}\nReturned: {ret}, Expected: {expected}\nPassed:{passed}")


if __name__ == '__main__':
    main()