import json
import sys

file = sys.argv[1]
network = json.load(open(file))
for node in network["nodes"]:
    node = network["nodes"][node]
    if isinstance(node, dict):
        if "node_Cytoscape_pos" in node:
            print(node["node_Cytoscape_pos"])
