import json
import sys

file = sys.argv[1]
network = json.load(open(file))
with open("../Cytoscape_pos.txt", "w") as f:
    for node in network["nodes"]:
        node = network["nodes"][node]
        if isinstance(node, dict):
            if "node_Cytoscape_pos" in node:
                pos = node["node_Cytoscape_pos"]
                f.write(f"{pos}\n")
with open("../VrNetzer_pos.txt", "w") as f:
    for node in network["nodes"]:
        node = network["nodes"][node]
        if isinstance(node, dict):
            if "VRNetzer_pos" in node:
                pos = node["VRNetzer_pos"]
                f.write(f"{pos}\n")
