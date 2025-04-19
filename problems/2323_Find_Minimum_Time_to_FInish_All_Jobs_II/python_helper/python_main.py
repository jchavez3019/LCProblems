from typing import *
from math import ceil

class Solution:
    def minimumTime(self, jobs: List[int], workers: List[int]) -> int:
        jobs = sorted(jobs)
        workers = sorted(workers)
        allTimes = [ceil(j/w) for j, w in zip(jobs, workers)]
        minTime = max(allTimes)
        return minTime


def main():
    sol_obj = Solution()

if __name__ == '__main__':
    main()