//
// Created by jorgejc2 on 1/24/26.
//
#include <iostream>
#include <algorithm>
#include <vector>
#include <iterator>

using namespace std;

class Solution
{
public:
    Solution(){}

    static int largestPerimeter(const vector<int>& nums)
    {
        const int n = nums.size();
        int i, hypotenuse, opposite, adjacent;
        vector<int> sortedNums(nums);
        sort(sortedNums.begin(), sortedNums.end(), [](const int a, const int b)
        {
            // lambda function (equivalent to greater<int>() functional) to ensure the vector
            // is sorted in descending order
            return a > b;
        });

        for (i = 0; i < n - 2; ++i)
        {
            hypotenuse = sortedNums[i];
            adjacent = sortedNums[i + 1];
            opposite = sortedNums[i + 2];
            if (adjacent + opposite > hypotenuse)
            {
                // this forms a valid solution, return the total perimeter
                return adjacent + opposite + hypotenuse;
            }
        }

        // a valid solution could not be found
        return 0;
    }

};

int main(int argc, char*argv[])
{
    vector<vector<int>> test_cases = {
        {2, 1, 2},
        {1, 2, 1, 10}
    };

    int ret;
    for (const auto& test_case : test_cases)
    {
        cout << "Test Case [";
        copy(test_case.begin(), test_case.end(), ostream_iterator<int>(cout, ", "));
        cout << "]" << endl;
        ret = Solution().largestPerimeter(test_case);
        cout << "Maximal perimeter of " << ret << endl;
    }

}