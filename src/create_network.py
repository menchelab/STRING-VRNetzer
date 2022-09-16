import json
from ast import literal_eval

import cartoGRAPHs
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from settings import LayoutAlgroithms as LA


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

    def create_cartoGRPAHS_spring(self) -> dict:
        return cartoGRAPHs.springlayout_3D(self.graph, itr=500)

    def apply_layout(self, layout_algo: str = None) -> nx.layout:
        """Applies a networkx layout algorithm and adds the node positions to the self.nodes_data dictionary."""
        if layout_algo is None:
            layout_algo = LA.SPRING
        layouts = {
            LA.spring: self.create_spring_layout,
            LA.kamada_kawai: self.create_kamada_kawai_layout,
            LA.cartoGRAPHS_spring: self.create_cartoGRPAHS_spring,
        }
        layout = layouts[layout_algo]()
        points = np.array(list(layout.values()))
        points = self.to_positive(points, 3)
        points = self.normalize_values(points, 3)
        # write points to node and add position to node data.
        for i, key in enumerate(layout):
            layout[key] = points[i]
        for node, position in layout.items():
            self.graph.nodes[node]["VRNetzer_pos"] = tuple(position)
        return layout

    def correct_cytoscape_pos(self):
        """Corrects the Cytoscape positions to be positive and between 0 and 1."""
        points = [
            self.graph.nodes[node]["node_Cytoscape_pos"] for node in self.graph.nodes
        ]
        points = np.array(points)
        points = self.to_positive(points, 2)
        points = self.normalize_values(points, 2)
        # Write new formated node positions on the xz axis
        for node, position in zip(self.graph.nodes, points):
            self.graph.nodes[node]["node_Cytoscape_pos"] = tuple(
                (0.0, position[0], position[1])
            )
        return points

    @staticmethod
    def to_positive(points, dims=3):
        min_values = [min(points[:, i]) for i in range(dims)]
        # Move everything into positive space
        for i, point in enumerate(points):
            for d, _ in enumerate(point[:dims]):
                points[i, d] += abs(min_values[d])
        return points

    @staticmethod
    def normalize_values(points, dims=3):
        # Normalize Values between 0 and 1
        min_values = [min(points[:, i]) for i in range(dims)]
        max_values = [max(points[:, i]) for i in range(dims)]
        norms = [max_values[i] - min_values[i] for i in range(dims)]
        for i, point in enumerate(points):
            for d, _ in enumerate(point[:dims]):
                points[i, d] /= norms[d]
        return points


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
