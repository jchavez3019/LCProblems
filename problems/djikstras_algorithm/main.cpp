#include <iostream>
#include <utility>
#include <vector>
#include <queue>
#include <sstream>
#include <fstream>
#include <string>
#include <algorithm>
#include <Python.h>

using namespace std;
const int INF = 1e9;

struct Node {
    int id;
    vector<Node*> other_nodes;
    vector<int> other_dists;
    Node* prev_node;
    int smallestDist;
    Node(int _id, vector<Node*> _other_nodes, vector<int> _other_dists) : id(_id), other_nodes(std::move(_other_nodes)),
    other_dists(std::move(_other_dists)), prev_node(nullptr), smallestDist(INF) {}
    Node(int _id) : id(_id), prev_node(nullptr), smallestDist(INF) {}
};

class Djikstras {
public:

    Djikstras(Node* graph) {
        int min_dist = _main_djikstras(graph);
        _min_dist = min_dist;
    }

    void parse_new_graph(Node* graph) {
        int min_dist = _main_djikstras(graph);
        _min_dist = min_dist;
    }

    int get_min_dist() {
        return _min_dist;
    }

private:
    vector<bool> _already_visited;
    int _min_dist;

    struct _CustomCompare
    {
        bool operator()(const pair<pair<Node*, Node*>, int> l, const pair<pair<Node*, Node*>, int> r) const
        {
            if (l.first.first == nullptr) {
                // first pair does not have a source node, it has the smallest distance
                return true;
            }
            else if (r.first.first == nullptr) {
                // second pair does not have a source node, it has the smallest distance
                return false;
            }
            else
                // compare distances
                return l.second < r.second;
        }
    };

    int _main_djikstras(Node* graph) {
        /**
         * @brief Main method for running Djikstra's algorithm
         * @param graph -- the source node in the graph
         * @return ret -- the minimum distance to reach the end of the graph
         */

        // create a min-heap and push in the source node
        priority_queue<pair<pair<Node*, Node*>, int>, vector<pair<pair<Node*, Node*>, int>>, _CustomCompare> pq;
        pq.emplace(pair<Node*, Node*>(nullptr, graph), 0);
        Node* sink_node = nullptr;

        while (!pq.empty()) {

            // get an element from the min-heap
            pair<pair<Node*, Node*>, int> curr_pair = pq.top();
            pq.pop();

            // handle source node case
            Node* firstNode = curr_pair.first.first;
            Node* secondNode = curr_pair.first.second;
            int dist = curr_pair.second;

            // update the distance to this node
            if (dist < secondNode->smallestDist) {
                secondNode->smallestDist = dist;
                secondNode->prev_node = firstNode;
            }

            // append all neighboring nodes
            int secondSmallestDist = secondNode->smallestDist;  // smallest distance to this node
            vector<Node*> other_nodes = secondNode->other_nodes;    // list to neighboring nodes
            vector<int> other_dists = secondNode->other_dists;  // distances to neighboring nodes
            for (int i = 0; i < other_nodes.size(); ++i) {
                // calculate distance from source to this node to the neighbor
                int other_dist = other_dists[i] + secondSmallestDist;
                Node* other_node = other_nodes[i];

                // only if the distance is smaller do we push this to the min-heap
                if (other_dist < other_node->smallestDist) {
                    pq.emplace(pair<Node*, Node*>(secondNode, other_node), other_dist);
                }
            }

            if (other_nodes.size() == 0) {
                if (sink_node != nullptr)
                    throw std::runtime_error("An error occurred: Multiple sink nodes in the graph!");
                sink_node = secondNode;
            }
        }

        if (sink_node == nullptr)
            throw std::runtime_error("An error occurred: A sink node was never found in the graph!");

        int ret = sink_node->smallestDist;
        return ret;
    }
};

int run_create_graph(int argc, char* argv[]) {
    /**
     * @brief Runs create_graph.py
     * @param argc -- Number of command line arguments
     * @param argv -- The command line arguments themselves
     *
     * This function calls the create_graph.py script with the passed arguments. This script
     * helps create a randomized graph that can be tested with this program.
     */
    // Initialize the Python interpreter
    Py_Initialize();

    // Import the sys module
    PyObject* sysModule = PyImport_ImportModule("sys");

    // Create a Python list for sys.argv (add program name as argv[0])
    PyObject* sysArgv = PyList_New(argc);
    for (int i = 0; i < argc; ++i) {
        PyList_SetItem(sysArgv, i, PyUnicode_FromString(argv[i]));
    }

    // Set sys.argv in the Python interpreter
    PyObject_SetAttrString(sysModule, "argv", sysArgv);

    // Run the Python script
    FILE* file = fopen("python_helper/create_graph.py", "r");
    if (!file) {
        std::cerr << "Error: Could not open script.py\n";
        Py_Finalize();
        return 1;
    }

    PyRun_SimpleFile(file, "create_graph.py");

    // Clean up and finalize
    fclose(file);
    Py_Finalize();

    return 0;
}

std::vector<int> parseIntList(const std::string& str) {
    /**
     * @brief Extracts list from string into a vector
     * @param str -- The string to parse
     * @return result -- the vector of ints from the string
     */
    std::vector<int> result;
    // Remove the square brackets and split by commas
    std::string trimmed = str.substr(1, str.length() - 2); // Remove leading and trailing '[' and ']'
    std::stringstream ss(trimmed);
    std::string item;
    while (std::getline(ss, item, ',')) {
        // Convert each item to integer
        if (!item.empty()) {
            result.push_back(std::stoi(item));
        }
    }
    return result;
}

int get_graph(vector<Node*>** get_node_table) {
    /**
     * @brief Returns a graph table
     * @param get_node_table -- pointer to be modified, will point to new node_table
     * @return num_nodes -- number of nodes in the graph
     *
     * This function will parse the last_graph.txt file which must be generated by the create_graph.py
     * script. The file follows a specific format which this function takes advantage of. The node_table
     * MUST be freed outside of this function.
     */
    std::ifstream file("python_helper/last_graph.txt"); // Open the file
    if (!file.is_open()) {
        std::cerr << "Error opening file!" << std::endl;
        return 1;
    }

    std::string line;
    int num_nodes;

    // Iterate through each line in the file
    bool firstLine = true;
    vector<Node*>* node_table = nullptr;
    while (std::getline(file, line)) {
        // remove white spaces in the string
        line.erase(std::remove_if(line.begin(), line.end(), ::isspace),
              line.end());
        // Use stringstream to split by semicolons
        std::stringstream ss(line);
        std::string part;

        if (firstLine) {
            num_nodes = std::stoi(line);
            firstLine = false;
            node_table = new vector<Node*>();
            for (int i = 0; i < num_nodes; ++i) {
                node_table->push_back(new Node(i));
            }
            continue;
        }

        std::vector<int> id_list, other_list, weight_list;

        // Read the first part (before the first semicolon)
        std::getline(ss, part, ';');
        id_list = parseIntList(part);
        int id = id_list[0];

        // Read the second part (between the first and second semicolons)
        std::getline(ss, part, ';');
        other_list = parseIntList(part);

        // Read the third part (after the second semicolon)
        std::getline(ss, part, ';');
        weight_list = parseIntList(part);

        Node* curr_node = node_table->at(id);
        curr_node->other_dists = weight_list;
        vector<Node*> other_nodes = vector<Node*>(weight_list.size(), nullptr);
        int idx;
        for (int i = 0; i < other_list.size(); ++i){
            idx = other_list[i];
            other_nodes[i] = node_table->at(idx);
        }
        curr_node->other_nodes = other_nodes;
    }

    file.close(); // Close the file after reading

    *get_node_table = node_table;

    return num_nodes;
}

int main(int argc, char* argv[]) {

    // run the create_path.py script
    run_create_graph(argc, argv);

    // get the node table representing the randomly generated graph
    vector<Node*>* node_table;
    int num_nodes = get_graph(&node_table);
    if (node_table == nullptr) {
        throw std::runtime_error("An error occurred: node_table was null");
    }
    Node* source_node = node_table->at(0);

    // run Djikstra's algorithm and print its results
    Djikstras obj(source_node);
    int min_dist = obj.get_min_dist();
    Node* sink_node = node_table->at(num_nodes - 1);
    vector<int> node_path = vector<int>();
    while (sink_node != nullptr) {
        node_path.push_back(sink_node->id);
        sink_node = sink_node->prev_node;
    }
    reverse(node_path.begin(), node_path.end());
    std::cout << "Node path: ";
    for (int num : node_path) std::cout << num << " -> ";
    printf("\nThe minimum distance to reach the end is %d\n", min_dist);

    // free all objects
    for (auto node : *node_table) {
        delete node;
    }
    delete node_table;

    return 0;
}
