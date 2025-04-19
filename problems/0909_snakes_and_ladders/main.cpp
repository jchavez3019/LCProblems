#include <iostream>
#include <vector>
//#include <algorithm>

using namespace std;

class Solution {
public:
    int snakesAndLadders(vector<vector<int>>& board) {

        return 12;
    }
};

int main() {

    // initializes 15x12 vector
    vector<vector<int>> board = vector<vector<int>>(15, vector<int>(12,5));
    Solution sol;
    int result = sol.snakesAndLadders(board);
    printf("Result: %d", result);

    return 0;
}
