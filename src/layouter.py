from ast import literal_eval

import networkx as nx
import numpy as np

from settings import LayoutAlgroithms as LA


class Layouter:
    """Simple class to apply a 3D layout algorithm to a Graph extracted from a GraphML file."""

    graph: nx.Graph = nx.Graph()

    def read_from_json(self, file: str) -> nx.Graph:
        network = literal_eval(open(file).read().strip("\n"))
        nodes = network["nodes"]
        edges = network["edges"]
        self.graph.add_nodes_from(
            [(node, {k: v for k, v in data.items()}) for (node, data) in nodes.items()]
        )
        for edge in edges:
            self.graph.add_edge(
                (str(edges[edge]["source"])), str(edges[edge]["sink"]), data=edges[edge]
            )
        return self.graph

    def read_from_grahpml(self, file: str) -> nx.Graph:
        self.graph = nx.read_graphml(file)
        return self.graph

    def create_spring_layout(self) -> dict:
        return nx.spring_layout(self.graph, dim=3)

    def create_kamada_kawai_layout(self) -> dict:
        return nx.kamada_kawai_layout(self.graph, dim=3)

    def create_cartoGRAPH_layout(self, layout_algo) -> dict:
        """Will pick the correct cartoGRAPH layout algorithm and apply it to the graph. If cartoGRAPH is not installed, it will ask the user whether to use networkx spring algorithm instead."""
        try:
            return self.pick_cg_layout_alogrithm(layout_algo)
        except ImportError:
            print("cartoGRAPHs is not installed.")
            use_spring = input("Use spring layout instead? [y/n]: ")
            if use_spring == "y":
                return self.create_spring_layout()
            else:
                exit()

    def pick_cg_layout_alogrithm(self, layout_algo):
        """Will pick the correct cartoGRAPH layout algorithm and apply it to the graph and return positions"""
        import cartoGRAPHs as cg

        _, layoutmethod, dimred_method = layout_algo.split("_")
        return cg.generate_layout(
            self.graph, dim=3, layoutmethod=layoutmethod, dimred_method=dimred_method
        )

    def apply_layout(self, layout_algo: str = None) -> nx.layout:
        """Applies a networkx layout algorithm and adds the node positions to the self.nodes_data dictionary."""
        if layout_algo is None:
            layout_algo = LA.spring
        if LA.cartoGRAPH in layout_algo:
            layout = self.create_cartoGRAPH_layout(layout_algo)
        else:
            layouts = {
                LA.spring: self.create_spring_layout,
                LA.kamada_kawai: self.create_kamada_kawai_layout,
            }
            layout = layouts[layout_algo]()  # Will use the desired layout algorithm
        points = np.array(list(layout.values()))
        points = self.to_positive(points, 3)
        points = self.normalize_values(points, 3)
        # write points to node and add position to node data.
        for i, key in enumerate(layout):
            layout[key] = points[i]
        for node, position in layout.items():
            self.graph.nodes[node]["VRNetzer_pos"] = tuple(position)
            self.graph.nodes[node]["node_new_2d_pos"] = (position[0], position[1], 0.0)
        return layout

    def correct_cytoscape_pos(self) -> np.array:
        """Corrects the Cytoscape positions to be positive and between 0 and 1."""
        cytoscape_nodes = [
            node
            for node in self.graph.nodes
            if "node_Cytoscape_pos" in self.graph.nodes[node]
        ]
        points = [
            self.graph.nodes[node]["node_Cytoscape_pos"] for node in cytoscape_nodes
        ]
        points = np.array(points)
        points = self.to_positive(points, 2)
        points = self.normalize_values(points, 2)
        # Write new formated node positions on the xz axis
        for node, position in zip(cytoscape_nodes, points):
            self.graph.nodes[node]["node_Cytoscape_pos"] = tuple(
                (position[0], position[1], 0.0)
            )
        return points

    @staticmethod
    def to_positive(points, dims=3) -> np.array:
        min_values = [min(points[:, i]) for i in range(dims)]
        # Move everything into positive space
        for i, point in enumerate(points):
            for d, _ in enumerate(point[:dims]):
                points[i, d] += abs(min_values[d])
        return points

    @staticmethod
    def normalize_values(points, dims=3) -> np.array:
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
