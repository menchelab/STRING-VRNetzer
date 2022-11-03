import json
import random

import networkx as nx
import numpy as np

from . import util
from .settings import Evidences
from .settings import LayoutAlgroithms as LA
from .settings import LayoutTags as LT
from .settings import LinkTags as LiT
from .settings import NodeTags as NT
from .settings import VRNetzElements as VRNE


class Layouter:
    """Simple class to apply a 3D layout algorithm to a Graph extracted from a GraphML file."""

    graph: nx.Graph = nx.Graph()

    def gen_graph(self, nodes, links):
        for node_data in nodes:
            self.graph.add_node(node_data[NT.id], data=node_data)
            # self.node_map[node_data["id"]] = node_data
        for link in links:
            self.graph.add_edge(link[LiT.start], link[LiT.end], data=link)
            # self.edge_map[(str(edge["s"]), str(edge["e"]))] = edge
        return self.graph

    def read_from_vrnetz(self, file: str) -> nx.Graph:
        network = json.load(open(file))
        self.network = network
        nodes = network[VRNE.nodes]
        links = network[VRNE.links]
        return self.gen_graph(nodes, links)

    def get_node_data(self, node):
        if "data" not in self.graph.nodes[node]:
            self.graph.nodes[node]["data"] = {}
        return self.graph.nodes[node]["data"]

    def set_node_data(self, node, data):
        self.graph.nodes[node]["data"] = data

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
            return self.pick_cg_layout_algorithm(layout_algo)
        except ImportError:
            print("cartoGRAPHs is not installed.")
            use_spring = input("Use spring layout instead? [y/n]: ")
            if use_spring == "y":
                return self.create_spring_layout()
            else:
                exit()

    def pick_cg_layout_algorithm(self, layout_algo):
        """Will pick the correct cartoGRAPH layout algorithm and apply it to the graph and return positions"""
        import cartoGRAPHs as cg

        _, layoutmethod, dimred_method = layout_algo.split("_")
        return cg.generate_layout(
            self.graph, dim=3, layoutmethod=layoutmethod, dimred_method=dimred_method
        )

    def apply_layout(self, layout_algo: str = None) -> nx.layout:
        """Applies a layout algorithm and adds the node positions to nodes in the self.network[VRNE.nodes] list."""
        if layout_algo is None:
            """Select default layout algorithm"""
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

        if LT.string_3d not in self.network[VRNE.node_layouts]:
            self.network[VRNE.node_layouts].append(LT.string_3d)
        if LT.string_3d_no_z not in self.network[VRNE.node_layouts]:
            self.network[VRNE.node_layouts].append(LT.string_3d_no_z)

        idx = 0
        for node, pos in layout.items():
            node = self.network[VRNE.nodes][idx]
            color = [random.randint(0,255),random.randint(0,255),random.randint(0,255),255]
            size = 1

            # find the correct layout
            cy_layout, _ = util.find_cy_layout(node)
            if cy_layout:
                # extract color and (size) information
                size = cy_layout[LT.size]
                color = cy_layout[LT.color]

            if VRNE.node_layouts not in self.network:
                self.network[VRNE.node_layouts] = []

            if NT.layouts not in node:
                node[NT.layouts] = []

            node[NT.layouts].append(
                {
                    LT.name: LT.string_3d_no_z,
                    LT.position: (pos[0], pos[1], 0.0),
                    LT.color: color,
                    LT.size: size,
                }
            )  # Add 2D coordinates

            node[NT.layouts].append(
                {
                    LT.name: LT.string_3d,
                    LT.position: tuple(pos),
                    LT.color: color,
                    LT.size: size,
                }
            )  # Add 3D coordinates

            self.network[VRNE.nodes][idx] = node
            idx += 1

        return layout

    def correct_cytoscape_pos(self) -> np.array:
        """Corrects the Cytoscape positions to be positive and between 0 and 1."""
        # Only handle nodes which are contained in the cytoscape layout
        cytoscape_nodes = []
        points = []
        for node in self.graph.nodes:
            data = self.get_node_data(node)
            cy_layout, idx = util.find_cy_layout(data)
            if cy_layout is not None:
                cytoscape_nodes.append(node)

                # Get positions of only these
                points.append(cy_layout[LT.position])
                
        if len(points) == 0:
            return None
        # normalize positions between in [0,1]
        points = np.array(points)
        points = self.to_positive(points, 2)
        points = self.normalize_values(points, 2)

        # Write new formatted node positions on the xz axis
        for node, position in zip(cytoscape_nodes, points):
            data = self.get_node_data(node)
            data[NT.layouts][idx][LT.position] = tuple((position[0], position[1], 0.0))
            self.set_node_data(node, data)  # Update node data

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

    def gen_evidence_layouts(self, evidences: dict = None) -> dict:
        # Set up the colors for each evidence type
        if evidences is None:
            evidences = Evidences.get_default_scheme()

        links = self.network[VRNE.links]
        if VRNE.link_layouts not in self.network:
            self.network[VRNE.link_layouts] = []
        for ev in evidences:
            self.network[VRNE.link_layouts].append(ev)
            cur_links = links
            if not ev == Evidences.any:
                cur_links = [link for link in links if ev in link]
            # Skip This evidence if there are not edges for this evidence
            if len(cur_links) == 0:
                continue

            # Color each link with the color of the evidence
            for idx, link in enumerate(links):
                if link in cur_links:
                    if ev == Evidences.any:
                        color = evidences[ev]
                        # TODO extract the alpha value with the highest score.
                    else:
                        color = evidences[ev][:3] + (
                            int(link[ev] * 255),
                        )  # Alpha scales with score
                else:
                    color = (0, 0, 0, 0)  # No evidence
                if LiT.layouts not in self.network[VRNE.links][idx]:
                    self.network[VRNE.links][idx][LiT.layouts] = []
                self.network[VRNE.links][idx][LiT.layouts].append(
                    {LT.name: ev, LT.color: color}
                )
        return self.network[VRNE.links]


if __name__ == "__main__":
    import os

    layouter = Layouter()
    layouter.read_from_vrnetz(
        os.path.abspath(
            f"{__file__}/../../static/networks/STRING_network_-_Alzheimer's_disease.VRNetz"
        )
    )
    layouter.apply_layout()
