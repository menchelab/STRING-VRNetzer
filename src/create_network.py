import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


class Layouter:
    def __init__(self, file: str):
        self.graph = nx.read_graphml(file)

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
            self.graph.nodes[node]["pos"] = tuple(position)
        return layout


if __name__ == "__main__":
    import os

    layouter = Layouter(
        os.path.abspath(
            f"{__file__}/../../static/networks/STRING network - Alzheimer's disease.graphml"
        )
    )
    layouter.apply_layout()
    print(list(layouter.graph.edges(data=True))[0])
