import os

import cartoGRAPHs as cg
import numpy as np

from layouter import Layouter


def cartoGRAHP_global_umap(G):
    layout = cg.generate_layout(G, dim=3, layoutmethod="global", dimred_method="umap")
    points = np.array(list(layout.values()))
    points = Layouter.to_positive(points, 3)
    points = Layouter.normalize_values(points, 3)
    # write points to node and add position to node data.
    for i, key in enumerate(layout):
        layout[key] = points[i]
    for node, position in layout.items():
        G.nodes[node]["VRNetzer_pos"] = tuple(position)
        # print(G.nodes[node]["VRNetzer_pos"])
    return layout
