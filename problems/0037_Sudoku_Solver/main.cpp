#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <algorithm>

using namespace std;

// this lambda function returns the index to the gbm vector based on the current (i,j) position
inline auto gbm_idx = [](int i, int j) {
    return int(i / 3) * 3 + int(j / 3);
};

// this lambda function returns 1/0 based on if a bit is present
inline auto bit_present = [](int num, int idx, const vector<unsigned int>& bitset) {
    return (bitset[idx] >> num) & 0x0001;
};

/**
 * @brief   This is a helper function which fills in the cells of a Sudoku puzzle and allows us to backtrack if we
 *          detect infeasibility.
 * @param k:            the current position on the board, index in range [0, 80]
 * @param sudoku_table: reference the the sudoku board which we modify in place
 * @param rbm:          row bit mask where a 1 indicates that a value is present in the row
 * @param cbm:          column bit mask where a 1 indicates that a value is present in the column
 * @param gbm:          grid bit mask where a 1 indicates that a value is present in the grid
 * @param is_fixed:     vector where `true` indicates that the element on the board is fixed
 * @return
 */
bool _sudoku_backtracking(int k, vector<vector<int>> &sudoku_table, vector<unsigned int> &rbm, vector<unsigned int> &cbm, vector<unsigned int> &gbm, vector<bool> &is_fixed) {
    if (k >= 81) {
        // base case, we are out of range on the board
        return true;
    }
    if (is_fixed[k]) {
        // this is a fixed position, move onto the next element
        return _sudoku_backtracking(k+1, sudoku_table, rbm, cbm, gbm, is_fixed);
    }

    int i, j, g, c;
    i = int(k / 9);
    j = k % 9;
    g = gbm_idx(i, j);
    for (c = 0; c < 9; c++) {
        if ((bit_present(c, i, rbm) | bit_present(c, j, cbm) | bit_present(c, g, gbm)) == 0) {
            // it is currently valid to use this number in this cell w.r.t. previously filled cells
            rbm[i] |= 0x0001 << c;
            cbm[j] |= 0x0001 << c;
            gbm[g] |= 0x0001 << c;
            if (_sudoku_backtracking(k+1, sudoku_table, rbm, cbm, gbm, is_fixed)) {
                // setting this number does not make subsequent elements infeasible
                sudoku_table[i][j] = c + 1; // we 0-index in range [0, 8], but this maps to digits [1, 9]
                return true;
            }
            else {
                // this number produces an infeasible solution, reset the value
                rbm[i] &= ~(0x0001 << c);
                cbm[j] &= ~(0x0001 << c);
                gbm[g] &= ~(0x0001 << c);
            }
        }
    }
    return false;
}

/**
 * @brief   The main function which solves a sudoku puzzle in place.
 * @param sudoku_table: Vector reference to the sudoku puzzle to solve.
 * @return
 */
int solve_sudoku(vector<vector<int>> &sudoku_table) {
    int i, j, k, c, g;
    vector<unsigned int> rbm(9, 0x0000); // row bit mask
    vector<unsigned int> cbm(9, 0x0000); // column bit mask
    vector<unsigned int> gbm(9, 0x0000); // grid bit mask
    vector<bool> is_fixed(81, false);

    // fill in the bit masks and marked fixed numbers as visited
    for (k = 0; k < 81; k++) {
        i = int(k / 9);
        j = k % 9;
        c = sudoku_table[i][j];
        if (c > 0) {
            g = gbm_idx(i, j);
            c--; // sudoku digits in range [1, 9] but we zero index to range [0, 8]
            rbm[i] |= 0x0001 << c;
            cbm[j] |= 0x0001 << c;
            gbm[g] |= 0x0001 << c;
            is_fixed[k] = true;
        }
    }

    return static_cast<int>(_sudoku_backtracking(0, sudoku_table, rbm, cbm, gbm, is_fixed));
}

/**
 * @brief   Given the path to a text file, parses it to return a sudoku table as a vector of integers. Unfilled elements
 *          are marked with '.'.
 * @param filename:     Path to the text file to parse.
 * @param sudoku_table  Reference to the sudoku table we should fill.
 * @return
 */
int parse_sudoku_text(const string &filename, vector<vector<int>> &sudoku_table) {
    std::ifstream file(filename); // Open the file
    if (!file.is_open()) {
        std::cerr << "Error opening file!" << std::endl;
        return 1;
    }

    // iterate through the text file
    std::string line;
    char c;
    int line_count = 0;
    while (std::getline(file, line)) {
        // remove characters that are not a digit or '.' in the string
        line.erase(std::remove_if(line.begin(), line.end(),
                                  [](char c){return (!isdigit(c) && c != '.');}),
                   line.end());
        if (line.length() != 9) {
            cerr << "Line length is not 9!" << endl;
            file.close(); // Close the file after reading
            return 1;
        }
        // insert this row into the sudoku table
        for (int i = 0; i < 9; i++) {
            c = line[i];
            if (c != '.') {
                sudoku_table[line_count][i] = c - '0';
            }
        }
        line_count++;
    }

    file.close(); // Close the file after reading
    return 0;
}

/**
 * @brief   Prints a sudoku board to the terminal in a pretty format.
 * @param board: Sudoku board to print to the console.
 */
void printSudoku(const vector<vector<int>>& board) {
    for (int i = 0; i < 9; ++i) {
        if (i % 3 == 0 && i != 0) {
            cout << "------+-------+------\n";
        }
        for (int j = 0; j < 9; ++j) {
            if (j % 3 == 0 && j != 0) {
                cout << "| ";
            }
            if (board[i][j] == 0) {
                cout << ". ";  // Use '.' for empty cells
            } else {
                cout << board[i][j] << ' ';
            }
        }
        cout << '\n';
    }
    cout << '\n';
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        // recall argv[0] is the name of the C++ executable
        std::cerr << "Usage: " << argv[0] << " <input_file_path> <solution_file_path>\n";
        return 1;
    }

    // extract the input and solution filepath
    std::string inputFilePath = argv[1];
    std::string solutionFilePath = argv[2];

    std::cout << "Input file: " << inputFilePath << "\n";
    std::cout << "Solution file: " << solutionFilePath << "\n";

    // extract the tables from the text files
    vector<vector<int>> initial_sudoku_table(9, vector<int>(9, 0));
    vector<vector<int>> solution_sudoku_table(9, vector<int>(9, 0));
    int parse_init_ret = parse_sudoku_text(inputFilePath, initial_sudoku_table);
    int parse_sol_ret = parse_sudoku_text(solutionFilePath, solution_sudoku_table);;
    if (parse_init_ret > 0) {
        cerr << "Error parsing initial sudoku table!" << endl;
        return 1;
    }
    if (parse_sol_ret > 0) {
        cerr << "Error parsing solution sudoku table!" << endl;
        return 1;
    }
    printf("Initial Sudoku table: \n");
    printSudoku(initial_sudoku_table);
    printf("Solution Sudoku table: \n");
    printSudoku(solution_sudoku_table);

    // solve the sudoku board
    int solution_exists = solve_sudoku(initial_sudoku_table);

    if (solution_exists) {
        // check to see if the output matches the solution board
        int output_matches = true;
        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 9; j++) {
                if (initial_sudoku_table[i][j] != solution_sudoku_table[i][j]) {
                    output_matches = false;
                    break;
                }
            }
            if (!output_matches) {
                break;
            }
        }

        string match_string = output_matches ? "matches" : "does not match";
        printf("The Sudoku table was solved! The output %s the solution.\n", match_string.c_str());

        printf("Returned output: \n");
        printSudoku(initial_sudoku_table);

    }
    else {
        // we could not find a solution to the sudoku puzzle
        std::cerr << "The Sudoku table could not be solved!";
        return 1;
    }

    return 0;
}
