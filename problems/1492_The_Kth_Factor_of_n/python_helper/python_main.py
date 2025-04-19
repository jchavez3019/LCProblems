from typing import List, Union, Tuple, Optional

class Solution:
    def kthFactor(self, n: int, k: int) -> int:

        if n == 1:
            # base case where n is 1
            if k == 1:
                return 1
            else:
                return -1

        a = []  # will hold factors starting from 1 in ascending order
        b = []  # will hold factors starting from n in descending order
        k = k - 1 # offset k so that it is zero-indexing our final arrays

        i = 1
        stop_idx = n
        while i < stop_idx:

            if n % i == 0:
                # n is divisible, so we must break up the factors
                j = n // i
                if j == i:
                    # if the factors are equal, we only append to a and break
                    # since we have found all factors at this point
                    a.append(i)
                    break
                else:
                    # Break the factors up and append them to their appropriate lists.
                    # We always have i <= j, so i will always belong to a and j will belong to b.
                    a.append(i)
                    b.append(j)
                    # Update the stop_idx since it is now impossible for the larger factor to be larger than j
                    # in future iterations
                    stop_idx = j

            i += 1

        # Lists a and b can be thought of as a single list holding all the factors where a has the first half
        # of factors in ascending order and list b has the rest of the factors in descending order. Because they are
        # in different orders, we must be careful with indexing.
        total_len = len(a) + len(b)
        if k >= total_len:
            # k is out of range
            return -1
        elif k < len(a):
            return a[k]
        else:
            k = k - len(a)  # offset k to properly index list b
            return b[len(b) - k - 1]  # indexing accounts for descending order

def main():

    # n = 12
    # k = 3
    n=7
    k=2
    n=4
    k=4
    n=1
    k=1

    sol_obj = Solution()
    ret = sol_obj.kthFactor(n, k)
    print(f"n: {n}")
    print(f"k: {k}")
    print(f"Solution returned: {ret}")

if __name__ == '__main__':
    main()