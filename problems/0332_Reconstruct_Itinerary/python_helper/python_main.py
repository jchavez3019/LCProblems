from typing import Union, Tuple, List
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
from general_python_utils import my_networkx as my_nx

def plot_semi_euler_path(itinerary: List[str]):
    """
    Plots a semi-Euler path using matplotlib and networkx.

    :param itinerary: Semi-Euler path in lexicographic order with start node 'JFK'.
    """
    G = nx.DiGraph()

    # Add nodes using the edge method in order to calculate the spring layout
    for i in range(len(itinerary) - 1):
        u = itinerary[i]
        v = itinerary[i + 1]
        G.add_edge(u, v)

    # Compute positions for all nodes using a layout algorithm.
    pos = nx.spring_layout(G)

    # create the matplotlib figure
    plt.figure(figsize=(8, 6))
    fig, ax = plt.subplots()

    # Draw nodes and labels.
    node_size = 350
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=node_size)
    nx.draw_networkx_labels(G, pos, font_size=10)

    # Highlight the source (first node) and sink (last node).
    source_node = itinerary[0]
    sink_node = itinerary[-1]
    nx.draw_networkx_nodes(G, pos, nodelist=[source_node], node_color="green", node_size=node_size)
    nx.draw_networkx_nodes(G, pos, nodelist=[sink_node], node_color="red", node_size=node_size)

    # now draw the edges one by one as to retain their label orders
    visited_edges = defaultdict(int)
    arc_rad = 0.1
    for i in range(len(itinerary) - 1):
        u = itinerary[i]  # source node
        v = itinerary[i + 1]  # destination node
        # create a key using the node names in Lexicographic order
        ordered_pair = [u, v]
        ordered_pair.sort()
        node_key = ordered_pair[0] + ordered_pair[1]
        # gradually increase curvature by number of times this key is seen
        weight = visited_edges[node_key] * arc_rad
        visited_edges[node_key] += 1
        edge_labels = {(u, v): i}
        edge_list = [(u, v)]
        if weight == 0:
            # first edge, leave it straight
            nx.draw_networkx_edges(G, pos, edgelist=edge_list)
            nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels,
                                         rotate=False)
        else:
            # repeated edge, increase its curvature
            nx.draw_networkx_edges(G, pos, edgelist=edge_list, connectionstyle=f'arc3, rad = {weight}')
            my_nx.my_draw_networkx_edge_labels(G, pos, ax=ax,
                                           edge_labels=edge_labels, rotate=False,
                                           rad=weight)

    plt.title("Semi-Euler Path with Ordered Edges")
    plt.axis('off')
    plt.show()

class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        """
        Computes a semi-Euler path in Lexicographic order for a graph whose start node is fixed as 'JFK'. Note that
        this function assumes the tickets admits a valid solution and we does not check to see if a semi-euler path
        is possible.

        The check (which is not done here) for determining if a graph admits a semi-euler path is as follows:

        * The starting node of the semi-euler path has one more outgoing edge than incoming edges.
        * The final node of the semi-euler path has one more incoming edge than outgoing edges.
        * All other nodes in the path have the same number of incoming edges and outgoing edges.

        :param tickets: Uni-directional edges of the graph
        :return:        Semi-Euler path in lexicographic order with start node 'JFK'
        """

        nodes = defaultdict(list)  # by default, each node should have an empty list
        for (source, dest) in tickets:
            # for each node, append all of its destinations
            nodes[source].append(dest)

        for destinations in nodes.values():
            # sort destinations in lexicographic order so that smaller destinations
            # are visited first
            destinations.sort(reverse=True)

        itinerary = []  # will hold our semi-euler path in reverse order
        stack = ['JFK']  # the starting node will always be JFK airport
        while len(stack) > 0:
            node = stack.pop()
            destinations = nodes[node]  # get the destinations of this node

            if len(destinations) > 0:
                # if we still have destinations left, we must append this node so that it's
                # tracked as an ancestor as well as append the next smallest neighbor
                stack.append(node)
                stack.append(destinations.pop())
            else:
                # we no longer have out-going edges, we can append this node to the solution
                itinerary.append(node)

        # reverse the path in place
        itinerary.reverse()

        return itinerary

def main():
    # input_tickets = [["JFK","KUL"],["JFK","NRT"],["NRT","JFK"]]
    # input_tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
    # input_tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
    input_tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"], ["JFK","ATL"], ["ATL","JFK"]]

    sol_obj = Solution()
    ret = sol_obj.findItinerary(input_tickets)
    print(f"Input: \n{input_tickets}")
    print(f"Solution returned: \n{ret}")

    plot_semi_euler_path(ret)

if __name__ == '__main__':
    main()