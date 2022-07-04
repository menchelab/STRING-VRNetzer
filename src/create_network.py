import json
from ast import literal_eval

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class Layouter:
    """Simple class to apply a 3D layout algorithm to a Graph extracted from a GraphML file."""

    graph: nx.Graph = nx.Graph()

    def read_from_json(self, file: str):
        network = literal_eval(open(file).read().strip("\n"))
        nodes = network["nodes"]
        edges = network["edges"]
        nodes.pop("data_type")
        nodes.pop("amount")
        edges.pop("data_type")
        edges.pop("amount")
        self.graph = nx.Graph()
        self.graph.add_nodes_from(
            [(node, {k: v for k, v in data.items()}) for (node, data) in nodes.items()]
        )
        for edge in edges:
            self.graph.add_edge(
                (str(edges[edge]["source"])), str(edges[edge]["sink"]), data=edges[edge]
            )
        return self.graph

    def read_from_grahpml(self, file: str):
        self.graph = nx.read_graphml(file)
        return self.graph

    def create_spring_layout(self) -> dict:
        return nx.spring_layout(self.graph, dim=3)

    def create_kamada_kawai_layout(self) -> dict:
        return nx.kamada_kawai_layout(self.graph, dim=3)

    def apply_layout(self, layout_algo: str = None) -> nx.layout:
        """Applies a networkx layout algorithm and adds the node positions to the self.nodes_data dictionary."""
        if layout_algo is None:
            layout_algo = "spring"
        layouts = {"spring": self.create_spring_layout}
        layout = layouts[layout_algo]()
        points = np.array(list(layout.values()))
        min_values = [min(points[:, i]) for i in range(3)]
        max_values = [max(points[:, i]) for i in range(3)]
        # Move everything into positive space
        for i, point in enumerate(points):
            for d, dim in enumerate(point):
                points[i, d] += abs(min_values[d])

        # Normalize Values between 0 and 1
        min_values = [min(points[:, i]) for i in range(3)]
        max_values = [max(points[:, i]) for i in range(3)]
        norms = [max_values[i] - min_values[i] for i in range(3)]
        for i, point in enumerate(points):
            for d, dim in enumerate(point):
                points[i, d] /= norms[d]

        # write points to node and add position to node data.
        for i, key in enumerate(layout):
            layout[key] = points[i]
        for node, position in layout.items():
            self.graph.nodes[node]["VRNetzer_pos"] = tuple(position)
        return layout


if __name__ == "__main__":
    import os

    layouter = Layouter()
    layouter.read_from_json(
        os.path.abspath(
            f"{__file__}/../../static/networks/STRING_network_-_Alzheimer's_disease.VRNetz"
        )
    )
    layouter.apply_layout()
    print(layouter.graph)
