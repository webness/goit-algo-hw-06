import json
from networkx.readwrite import json_graph
from collections import deque
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_directory, "graph.json")

with open(json_file_path, "r") as json_file:
    graph_data = json.load(json_file)

network_graph = json_graph.node_link_graph(graph_data, edges="edges")


def dfs_path(graph, start, goal):
    stack = [(start, [start])]  # Stack of (node, path_to_node)
    while stack:
        (node, path) = stack.pop()
        if node == goal:
            return path
        for neighbor in set(graph.neighbors(node)) - set(path):
            stack.append((neighbor, path + [neighbor]))
    return None  # No path found


def bfs_path(graph, start, goal):
    queue = deque([(start, [start])])  # Queue of (node, path_to_node)
    while queue:
        (node, path) = queue.popleft()
        if node == goal:
            return path
        for neighbor in set(graph.neighbors(node)) - set(path):
            queue.append((neighbor, path + [neighbor]))
    return None  # No path found


def find_paths(graph, start_node, end_node):
    print(f"Finding paths from '{start_node}' to '{end_node}'\n")

    dfs_result = dfs_path(graph, start_node, end_node)
    if dfs_result:
        print("DFS Path:", " -> ".join(dfs_result))
    else:
        print("DFS Path: No path found")

    bfs_result = bfs_path(graph, start_node, end_node)
    if bfs_result:
        print("BFS Path:", " -> ".join(bfs_result))
    else:
        print("BFS Path: No path found")

    if dfs_result == bfs_result:
        print("\nBoth algorithms found the same path.")
    else:
        print("\nThe paths found by DFS and BFS are different.")


if __name__ == "__main__":
    start_node = 'PC_F1_C1_1'
    end_node = 'CentralRouter'

    find_paths(network_graph, start_node, end_node)
