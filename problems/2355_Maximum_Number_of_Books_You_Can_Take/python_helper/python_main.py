from typing import Tuple, Union, List, Dict, Optional

class Solution:
    def maximumBooks(self, books: List[int]) -> int:

        n = len(books)
        next_idx_attempt = n - 1

        global_max = 0

        while(next_idx_attempt is not None):

            curr_sum = 0  # initialize your running sum
            start_idx = next_idx_attempt
            next_idx_attempt = None
            prior_books = None
            for i in range(start_idx, -1, -1):

                if prior_books is None:
                    curr_sum += books[i]
                    prior_books = books[i]
                else:
                    if next_idx_attempt is None:
                        next_idx_attempt = i

                    curr_books = min(books[i], prior_books - 1)
                    if curr_books <= 0:
                        break

                    curr_sum += curr_books
                    prior_books = curr_books



            global_max = max(global_max, curr_sum)

        return global_max


def main():
    input_books = [8,5,2,7,9]
    input_books = [7,0,3,4,5]
    input_books = [8,2,3,7,3,4,0,1,4,3]
    input_books = [2, 3, 2, 0]
    input_books = [0,5,1]
    print(f"Input: \n{input_books}")

    sol_obj = Solution()
    ret = sol_obj.maximumBooks(input_books)
    print(f"Solution returned: {ret}")

if __name__ == '__main__':
    main()