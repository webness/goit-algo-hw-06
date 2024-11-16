import json
import os
import networkx as nx
from networkx.readwrite import json_graph
import heapq

# Load the graph from the JSON file
current_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_directory, "graph.json")

with open(json_file_path, "r") as json_file:
    graph_data = json.load(json_file)

# Reconstruct the graph from JSON data
network_graph = json_graph.node_link_graph(graph_data, edges="edges")


# Implement Dijkstra's algorithm for finding the shortest path
def dijkstra_shortest_path(graph, start, goal):
    # Priority queue to store (distance, node) pairs
    priority_queue = [(0, start)]
    # Dictionary to track the shortest distance to each node
    shortest_distances = {node: float('inf') for node in graph.nodes}
    shortest_distances[start] = 0
    # Dictionary to store the path
    previous_nodes = {node: None for node in graph.nodes}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # If we reach the goal, reconstruct the path
        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = previous_nodes[current_node]
            return path[::-1], shortest_distances[goal]  # Return path and total distance

        # Skip if we found a shorter way to this node already
        if current_distance > shortest_distances[current_node]:
            continue

        # Explore neighbors
        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor].get('weight', 1)
            distance = current_distance + weight

            # If a shorter path to the neighbor is found
            if distance < shortest_distances[neighbor]:
                shortest_distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # If no path is found, return None
    return None, float('inf')


# Example usage
if __name__ == "__main__":
    # Replace with desired start and goal nodes
    start_node = 'PC_F1_C1_1'
    end_node = 'CentralRouter'

    path, total_weight = dijkstra_shortest_path(network_graph, start_node, end_node)

    if path:
        print(f"Shortest path from '{start_node}' to '{end_node}': {' -> '.join(path)}")
        print(f"Total path weight: {total_weight}")
    else:
        print(f"No path found from '{start_node}' to '{end_node}'")
