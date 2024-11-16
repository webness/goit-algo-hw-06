import networkx as nx
import matplotlib.pyplot as plt
import json
import os
from networkx.readwrite import json_graph
import random

network_graph = nx.Graph()

central_router = 'CentralRouter'

for floor in range(1, 4):  # Floors 1, 2, and 3
    floor_switch = f'FloorSwitch_{floor}'
    network_graph.add_node(floor_switch)

    for cabinet in range(1, 4):  # Cabinets 1, 2, and 3 on each floor
        cabinet_switch = f'Switch_F{floor}_C{cabinet}'
        network_graph.add_node(cabinet_switch)

        weight_floor_switch = random.randint(1, 10)  # Random weight for demonstration
        network_graph.add_edge(cabinet_switch, floor_switch, weight=weight_floor_switch)

        for comp in range(1, 5):  # Computers 1, 2, 3, and 4 in each cabinet
            computer = f'PC_F{floor}_C{cabinet}_{comp}'
            network_graph.add_node(computer)

            weight_cabinet_switch = random.randint(1, 5)  # Random weight for demonstration
            network_graph.add_edge(computer, cabinet_switch, weight=weight_cabinet_switch)

for floor in range(1, 4):
    floor_switch = f'FloorSwitch_{floor}'
    weight_to_router = random.randint(5, 15)  # Higher weight to central router
    network_graph.add_edge(floor_switch, central_router, weight=weight_to_router)

# Add a custom indirect path to create different paths for DFS and BFS
# Assign higher weights to the indirect path to differentiate it
network_graph.add_edge('PC_F1_C1_1', 'Node_A', weight=12)
network_graph.add_edge('Node_A', 'Node_B', weight=10)
network_graph.add_edge('Node_B', 'CentralRouter', weight=8)  # Longer, higher-weighted indirect path

# Shorter, lower-weighted direct path
network_graph.add_edge('PC_F1_C1_1', 'Switch_F1_C1', weight=3)  # Direct path with a lower weight

plt.figure(figsize=(20, 12))
layout = nx.spring_layout(network_graph, seed=42)  # Define layout for positioning
edge_labels = nx.get_edge_attributes(network_graph, 'weight')
nx.draw_networkx(network_graph, layout, with_labels=True, node_color='lightblue', edge_color='gray', node_size=700,
                 font_size=8)
nx.draw_networkx_edge_labels(network_graph, layout, edge_labels=edge_labels)
plt.title("Three-Story Office LAN with Custom Weighted Paths for DFS and BFS Comparison")
plt.show()

total_devices = network_graph.number_of_nodes()
total_connections = network_graph.number_of_edges()
device_degrees = dict(network_graph.degree())

print(f"Total devices (nodes): {total_devices}")
print(f"Total connections (edges): {total_connections}")
print("Device connection degrees:")
for device, degree in device_degrees.items():
    print(f"  {device}: {degree}")

graph_data = json_graph.node_link_data(network_graph, edges="edges")

current_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_directory, "graph.json")

with open(json_file_path, "w") as json_file:
    json.dump(graph_data, json_file, indent=4)

print(f"Graph saved to '{json_file_path}'")
