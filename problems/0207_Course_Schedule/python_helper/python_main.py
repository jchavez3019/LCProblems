from typing import List, Tuple, Optional, Union
GraphType = dict[int, dict[str, Union[int, list[int]]]]
from queue import Queue

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:

        # create the graph
        graph = {}
        for curr_pair in prerequisites:
            course_id, prereq_id = curr_pair

            if course_id not in graph:
                graph[course_id] = {
                    'incoming_edges': 1,
                    'outgoing_edges': []
                }
            else:
                graph[course_id]['incoming_edges'] += 1

            if prereq_id not in graph:
                graph[prereq_id] = {
                    'incoming_edges': 0,
                    'outgoing_edges': [course_id]
                }
            else:
                graph[prereq_id]['outgoing_edges'].append(course_id)

        # the root nodes will be the start of the queue
        root_nodes = [node_id for node_id, vals in graph.items() if vals['incoming_edges'] == 0]

        # check to see if cycles exist in the graph
        isCyclic = self.is_cyclic(graph, root_nodes)

        # if no cycles exist, it is possible to take the courses
        return not isCyclic

    def is_cyclic(self, graph: GraphType, root_nodes: List[int]) -> bool:
        """
        Kahn's algorithm for finding cycles in a directed graph. It may also be used for topologically sorting
        a DAG if it is indeed a DAG.
        :param graph:
        :param root_nodes:
        :return:
        """
        num_nodes = len(graph.keys())
        q = Queue()  # queue for DFS
        for root in root_nodes:
            q.put(root)

        visited = 0
        while not q.empty():
            curr_node = q.get()
            visited += 1

            for neighbor in graph[curr_node]['outgoing_edges']:
                graph[neighbor]['incoming_edges'] -= 1
                if graph[neighbor]['incoming_edges'] == 0:
                    q.put(neighbor)

        return not (num_nodes == visited)

def main():
    numCourses = 2
    prerequisites = [[1,0]]

    sol_obj = Solution()
    ret = sol_obj.canFinish(numCourses, prerequisites)
    print(f"numCourses: {numCourses}")
    for curr_pair in prerequisites:
        course_id, prereq_id = curr_pair
        print(f"{prereq_id} -> {course_id}")
    print(f"Solution returned: \n{ret}")

if __name__ == '__main__':
    main()