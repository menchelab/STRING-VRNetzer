import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


class Layouter:
    def __init__(self, nodes_data: dict, edges_data: dict):
        self.nodes_data = nodes_data
        self.edges_data = edges_data
        self.graph = None

    def create_spring_layout(self) -> dict:
        graph = nx.Graph()
        graph.add_nodes_from(self.nodes_data.keys())
        graph.add_edges_from(self.edges_data.keys())
        self.graph = graph
        return nx.spring_layout(graph, dim=3)

    def create_kamada_kawai_layout(self) -> dict:
        graph = nx.Graph()
        graph.add_nodes_from(self.nodes_data.keys())
        graph.add_edges_from(self.edges_data.keys())
        self.graph = graph
        return nx.kamada_kawai_layout(graph, dim=3)

    def apply_layout(self, layout_algo="spring") -> None:
        """Applies a networkx layout algorithm and adds the node positions to the self.nodes_data dictionary."""
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
            self.nodes_data[node]["pos"] = tuple(position)
        return layout


if __name__ == "__main__":
    from graphml_parser import parse_graphml

    nodes, edges = parse_graphml("test.graphml")
    layouter = Layouter(nodes, edges)
    pos = layouter.apply_layout()
    print(pos)
