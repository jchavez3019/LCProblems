#include <iostream>
#include <vector>

using namespace std;

/**
 * @brief A solution to LeetCode problem 1094, "Car Pooling".
 */
class Solution {
public:
    /**
     * Determines whether a car can carry out all trips given that it only travels in one direction
     * and with a given capacity.
     *
     * We are given constraints:
     * - \f$ 1 \le trips.length \le 1000 \f$
     * - \f$ trips[i].length == 3 \f$
     * - \f$ 1 \le numPassengers_i \le 100 \f$
     * - \f$ 0 \le from_i < to_i \le 1000 \f$
     * - \f$ 1 \le capacity \le 10^5 \f$
     * @param trips Number of trips to make.
     * @param capacity The capacity of the car transporting the passengers.
     * @return True when the car can take all the passengers in a continuous drive.
     * @return False when the car does not have the capacity to take all the passengers.
     */
    bool carPooling(vector<vector<int>>& trips, int capacity) {
        vector<int> buckets(1001, 0);

        // For each unit of the trip, mark the number of passengers that the car will add during that unit.
        // This number may be 0 or negative (in which, we drop off passengers at this unit).
        for (const auto& trip : trips)
        {
            const auto passengers = trip[0];
            const auto src = trip[1];
            const auto dst = trip[2];

            buckets[src] += passengers;
            buckets[dst] -= passengers;
        }

        // Create a running total of the passengers that have been picked thus far per unit of the
        // trip. If the capacity is exceeded, terminate early.
        int total_passengers = 0;
        for (size_t i = 0; i < buckets.size(); ++i)
        {
            total_passengers += buckets[i];
            if (total_passengers > capacity)
            {
                return false;
            }
        }
        return true;
    }
};

/**
 * Helper function to run a Car Pooling test case and validate against expected outputs.
 */
void runTestCase(int test_num, const vector<vector<int>>& trips, int capacity, bool expected) {
    Solution sol;

    // Create a copy because carPooling takes a non-const reference
    vector<vector<int>> trips_copy = trips;

    cout << "Running Test Case " << test_num << "...\n";

    bool result = sol.carPooling(trips_copy, capacity);

    if (result == expected) {
        cout << "  [PASSED] Result: " << (result ? "true" : "false") << "\n";
    } else {
        cout << "  [FAILED] Expected " << (expected ? "true" : "false")
             << ", got " << (result ? "true" : "false") << "\n";
    }
    cout << "----------------------------------------\n";
}

int main(int argc, char* argv[]) {
    // ---------------------------------------------------------
    // Test Case 1
    // trips = [[2,1,5],[3,3,7]], capacity = 4, expected = false
    // ---------------------------------------------------------
    vector<vector<int>> tc1_trips = {{2, 1, 5}, {3, 3, 7}};
    int tc1_capacity = 4;
    bool tc1_expected = false;
    runTestCase(1, tc1_trips, tc1_capacity, tc1_expected);

    // ---------------------------------------------------------
    // Test Case 2
    // trips = [[2,1,5],[3,3,7]], capacity = 5, expected = true
    // ---------------------------------------------------------
    vector<vector<int>> tc2_trips = {{2, 1, 5}, {3, 3, 7}};
    int tc2_capacity = 5;
    bool tc2_expected = true;
    runTestCase(2, tc2_trips, tc2_capacity, tc2_expected);

    return 0;
}