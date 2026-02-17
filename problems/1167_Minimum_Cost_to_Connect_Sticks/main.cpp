#include <iostream>
#include <vector>
#include <queue>
#include <functional>

using namespace std;
using test_t = vector<vector<int>>;
using min_heap_t = priority_queue<int, vector<int>, greater<int>>;

class Solution
{
public:
    Solution() {}

    static int connectSticks(vector<int> &sticks, bool verbose)
    {
        size_t n = sticks.size();
        if (n == 1) return 0;

        int x, y;
        int cost = 0;
        min_heap_t pq(sticks.begin(), sticks.end(), greater<int>());

        if (verbose)
        {
            printPQ(pq);
        }

        while (pq.size() >= 2)
        {
            x = pq.top();
            pq.pop();
            y = pq.top();
            pq.pop();

            cost += x + y;
            pq.push(x + y);
        }

        return cost;
    }
private:
    static void printPQ(min_heap_t pq)
    {
        for (; !pq.empty(); pq.pop())
        {
            printf("%d ", pq.top());
        }
        printf("\n");
    }

};

int main(int argc, char* argv[])
{
    test_t test_cases = {
        {2, 4, 3},
        {1, 8, 3, 5},
        {5}
    };
    vector<int> solutions = {14, 30, 0};
    size_t n = test_cases.size();

    int solution, result;
    for (size_t i = 0; i < n; i++)
    {
        solution = solutions[i];
        result = Solution().connectSticks(test_cases[i], false);
        if (solution == result)
        {
            printf("Test case %lu passed with a result of %d", i, result);
        } else
        {
            printf("Test case %lu failed, returned %d with expected gt %d.", i, result, solution);
        }
        printf("\n");
    }
}