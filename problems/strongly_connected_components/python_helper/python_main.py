from typing import Union, Tuple, List, Optional
from collections import defaultdict

def find_scc(graph: dict[str:list[str]], root: str) -> dict[int:list[str]]:
    """
    Given a graph dictionary and a root node to start from, this function finds all strongly connected components.
    :param graph:   A graph represented as a dictionary
    :param root:    The root node to start from
    :return:        A dictionary of strongly connected components
    """
    # holds the scc's that are found where 'low' is used as the unique indices
    scc = defaultdict(list)

    # TODO:
    #  Since 'low' and 'disc' share the same indices, it is more efficient to combine them into a single
    #  dictionary. However, we leave them separate for algorithmic clarity.
    # Holds the low values of all nodes. This is initially the time-step a node is discovered, but once a node is
    # processed, its 'low' value will be the smallest 'low' value found among all of its children.
    low = defaultdict(lambda: -1)
    # The time-step a node is discovered at. Unlike 'low', this never gets updated.
    disc = defaultdict(lambda: -1)

    time = 0  # used to determine the time-step a node was discovered at
    stack = [root]  # stack for nodes to be processed

    while len(stack) > 0:

        node = stack.pop()
        if disc[node] == -1:
            # this node has not been discovered before
            disc[node] = time
            low[node] = time
            time += 1

        smallest_low = low[node]
        is_processed = True  # remains true if 1) no neighbors or 2) all neighbors processed
        for n in graph[node]:
            # iterate through the neighbors
            if disc[n] == -1:
                # this neighbor has not been processed
                if is_processed:
                    # if we find a neighbor that has not been processed, we cannot
                    # process this node so we must append this node back to be
                    # processed later
                    is_processed = False
                    stack.append(node)
                # append neighbors that need to be processed
                stack.append(n)

            # Track the smallest low number found among descendants as this will be the key
            # for placing this node into an scc.
            # If neighbors have not been processed, this will become -1 but the 'is_processed' check later ensures
            # that we do not update 'low' or 'scc' with this index.
            smallest_low = min(smallest_low, low[n])

        if is_processed:
            # this node has been processed, we can update its low number and use it to append this node
            # to an scc
            low[node] = smallest_low
            scc[smallest_low].append(node)

    return scc

def main():
    graph = {
        'a': ['b'],
        'b': ['c'],
        'c': ['e', 'd'],
        'e': [],
        'd': ['b'],
    }
    scc = find_scc(graph, 'a')

    # Print the scc's in the order they were found, and reverse the nodes in each scc
    # so that the first element is now the first element found in the scc, and the last element is the last element
    # found in the scc.
    ordered_keys = sorted(scc.keys())
    i = 0
    for k in ordered_keys:
        val = scc[k]
        val.reverse()
        print(f"scc: {i} | {val}")
        i += 1

if __name__ == "__main__":
    main()