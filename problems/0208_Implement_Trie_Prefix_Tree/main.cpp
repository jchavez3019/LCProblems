#include <iostream>
#include <vector>
#include <functional>
#include <memory>

using namespace std;

/**
 * @brief Represents a single character node within the Trie structure.
 */
class Node {
public:
    /**
     * @brief Constructs a new Node object.
     * @param value The character this node represents.
     * @param terminal Boolean indicating if this node marks the end of a valid word.
     */
    Node(const unsigned char& value, const bool terminal)
        : _value(value), _terminal(terminal), _children_nodes(26) {}

    /**
     * @brief Finds an existing child or creates a new one if it doesn't exist.
     * @param query The character to look for (must be 'a'-'z').
     * @return Node* A pointer to the child node.
     * @exception std::out_of_range Thrown if the query character is outside the 'a'-'z' range.
     */
    Node* getOrCreateChild(unsigned char query) {
        const auto idx = static_cast<size_t>(query - 'a');
        if (idx >= 26) throw std::out_of_range("Character out of a-z range");

        if (!(_children_characters & (1u << idx))) {
            _children_nodes[idx] = std::make_unique<Node>(query, false);
            _children_characters |= (1u << idx);
        }
        return _children_nodes[idx].get();
    }

    /**
     * @brief Safely retrieves a pointer to a child node without creating one.
     * @param query The character to look for.
     * @return Node* Pointer to the child node, or nullptr if it does not exist.
     */
    [[nodiscard]] Node* getChild(const unsigned char& query) const {
        const auto idx = static_cast<size_t>(query - 'a');
        if (idx >= 26 || !(_children_characters & (1u << idx))) return nullptr;
        return _children_nodes[idx].get();
    }

    /**
     * @brief Checks if this node represents the end of a complete word.
     * @return true If the node is terminal.
     * @return false If the node is just a prefix.
     */
    [[nodiscard]] bool isTerminal() const { return _terminal; }

    /**
     * @brief Updates the terminal status of the node.
     * @param terminal New terminal status.
     */
    void setTerminal(const bool terminal) { _terminal = terminal; }

private:
    unsigned char _value;
    bool _terminal;
    uint32_t _children_characters = 0;
    std::vector<std::unique_ptr<Node>> _children_nodes;
};

/**
 * @brief A Prefix Tree (Trie) for efficient string storage and lookup.
 */
class Trie {
public:
    /**
     * @brief Initializes the Trie with an empty root node.
     */
    Trie() : _root('_', false) {}

    /**
     * @brief Inserts a word into the Trie, creating nodes as necessary.
     * @param word The string to be stored.
     */
    void insert(string word) {
        // Create or get the node pointers of each child.
        Node* curr = &_root;
        for (const char& c : word) {
            curr = curr->getOrCreateChild(c);
        }
        // Set this node to terminal to mark the end of a word in the trie.
        curr->setTerminal(true);
    }

    /**
     * @brief Searches for a complete word in the Trie.
     * @param word The word to search for.
     * @return true If the exact word exists and is marked as terminal.
     * @return false Otherwise.
     */
    bool search(string word) const {
        const Node* node = _getNodePtr(word);
        return node && node->isTerminal();
    }

    /**
     * @brief Checks if any word in the Trie starts with the given prefix.
     * @param prefix The prefix string to look for.
     * @return true If the prefix exists in the tree.
     * @return false Otherwise.
     */
    bool startsWith(string prefix) const {
        return _getNodePtr(prefix) != nullptr;
    }

private:
    Node _root;

    /**
     * @brief Internal helper to traverse the tree and find the node for a given string.
     * @param word The string (word or prefix) to follow.
     * @return const Node* Pointer to the final node in the path, or nullptr if path breaks.
     */
    [[nodiscard]] const Node* _getNodePtr(const string& word) const {
        const Node* curr = &_root;
        for (unsigned char c : word) {
            curr = curr->getChild(c);
            if (!curr) return nullptr;
        }
        return curr;
    }
};

/**
 * Your Trie object will be instantiated and called as such:
 * Trie* obj = new Trie();
 * obj->insert(word);
 * bool param_2 = obj->search(word);
 * bool param_3 = obj->startsWith(prefix);
 */

/**
 * Helper function to run a sequence of Trie commands and validate against expected outputs.
 */
void runTestCase(const int test_num, const vector<string>& commands, const vector<vector<string>>& args, const vector<string>& expected) {
    Trie* obj = nullptr;
    bool all_passed = true;

    cout << "Running Test Case " << test_num << "...\n";

    for (size_t i = 0; i < commands.size(); ++i) {
        const string& cmd = commands[i];
        string arg = args[i].empty() ? "" : args[i][0];
        const string& exp = expected[i];
        string result_str = "null";

        try {
            if (cmd == "Trie") {
                delete obj; // Clean up previous instance if it exists
                obj = new Trie();
            } else if (cmd == "insert") {
                obj->insert(arg);
            } else if (cmd == "search") {
                bool res = obj->search(arg);
                result_str = res ? "true" : "false";
            } else if (cmd == "startsWith") {
                bool res = obj->startsWith(arg);
                result_str = res ? "true" : "false";
            } else {
                result_str = "Unknown Command";
            }

            if (result_str != exp) {
                cout << "  [FAILED] Op " << i << " (" << cmd << " '" << arg << "'): expected " << exp << ", got " << result_str << "\n";
                all_passed = false;
            }
        } catch (const std::exception& e) {
            // Catch exceptions (like std::out_of_range) to see if we expected them
            result_str = string("Exception: ") + e.what();
            if (result_str != exp) {
                cout << "  [FAILED] Op " << i << " (" << cmd << " '" << arg << "'): expected " << exp << ", got " << result_str << "\n";
                all_passed = false;
            }
        }
    }

    if (all_passed) {
        cout << "  [PASSED] All " << commands.size() << " operations returned expected results.\n";
    }
    delete obj;
    cout << "----------------------------------------\n";
}

int main(int argc, char* argv[]) {
    // ---------------------------------------------------------
    // Test Case 1: LeetCode sequence
    // ---------------------------------------------------------
    const vector<string> tc1_cmds = {"Trie", "insert", "search", "search", "startsWith", "insert", "search"};
    const vector<vector<string>> tc1_args = {{}, {"apple"}, {"apple"}, {"app"}, {"app"}, {"app"}, {"app"}};
    const vector<string> tc1_expected = {"null", "null", "true", "false", "true", "null", "true"};

    runTestCase(1, tc1_cmds, tc1_args, tc1_expected);

    // ---------------------------------------------------------
    // Test Case 2: Overlapping prefixes and separate branches
    // ---------------------------------------------------------
    const vector<string> tc2_cmds = {"Trie", "insert", "insert", "search", "startsWith", "search", "startsWith"};
    const vector<vector<string>> tc2_args = {{}, {"hello"}, {"help"}, {"hell"}, {"hell"}, {"help"}, {"cat"}};
    // "hell" is not a full word, but it is a prefix. "cat" doesn't exist at all.
    const vector<string> tc2_expected = {"null", "null", "null", "false", "true", "true", "false"};

    runTestCase(2, tc2_cmds, tc2_args, tc2_expected);

    // ---------------------------------------------------------
    // Test Case 3: Edge Cases (Empty strings and Invalid Characters)
    // ---------------------------------------------------------
    const vector<string> tc3_cmds = {"Trie", "search", "insert", "search", "insert"};
    const vector<vector<string>> tc3_args = {{}, {""}, {""}, {""}, {"A"}}; // "A" is uppercase, out of bounds
    // Searching an empty string before insertion should be false.
    // Inserting an empty string marks root as terminal. Searching it should now be true.
    // Inserting 'A' should trigger the std::out_of_range exception built into getOrCreateChild
    const vector<string> tc3_expected = {"null", "false", "null", "true", "Exception: Character out of a-z range"};

    runTestCase(3, tc3_cmds, tc3_args, tc3_expected);

    return 0;
}