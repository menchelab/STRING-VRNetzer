import json
import os

import numpy as np
import pandas as pd

from layouter import Layouter
from settings import _NETWORKS_PATH, UNIPROT_MAP, EdgeTags, NodeTags


class VRNetzConverter:
    """Converts a network from edge/link list to VRNetz format"""

    def __init__(
        self,
        nodes_file: str,
        links_file: str = None,
        uniprot_mapping_file: str = None,
        project_name: str = None,
    ):
        self.nodes_file = nodes_file
        self.links_file = links_file
        if uniprot_mapping_file is None:
            self.uniprot_mapping_file = UNIPROT_MAP
        else:
            self.uniprot_mapping_file = uniprot_mapping_file
        if project_name is None:
            self.project_name = "PPI.VrNetz"
        self.convert()

    def convert(self) -> None:
        """Construct the VrNetz from the links and nodes csv files"""

        links = self.gen_link_list()
        nodes = self.gen_node_layout()
        vr_netz = {"nodes": nodes, "edges": links}
        with open(os.path.join(_NETWORKS_PATH, self.project_name), "w+") as f:
            json.dump(vr_netz, f)

    def gen_node_layout(self) -> list:
        """Extract node list from a node csv file"""
        uniprot_map = pd.read_csv(uniprot_mapping_file, sep=",")
        nodes = pd.read_csv(
            self.nodes_file,
            sep=",",
            header=None,
            names=["ppi_id", "x", "y", "z"],
        ).to_dict(orient="records")
        points = []
        for node in nodes:
            points.append((node["x"], node["y"], node["z"]))
            index = uniprot_map.index[
                uniprot_map["NCBI Gene ID(supplied by NCBI)"] == node["ppi_id"]
            ].tolist()
            if len(index) > 0:
                display_name = uniprot_map.loc[
                    index[0], "UniProt ID(supplied by UniProt)"
                ]
            else:
                display_name = "NA"
            node[NodeTags.display_name] = display_name
            for col in ["x", "y", "z"]:
                del node[col]

        points = np.array(points)
        points = Layouter.to_positive(points, 3)
        points = Layouter.normalize_values(points, 3)
        res = {}
        for i, node in enumerate(nodes):
            node[NodeTags.vrnetzer_pos] = list(points[i])
            res[node["ppi_id"]] = node
        return res

    def gen_link_list(self) -> dict:
        """Extract edge dict from a edge csv file"""
        links = pd.read_csv(
            self.links_file, sep=",", header=None, names=["source", "sink"]
        ).to_dict(orient="records")
        res = {}
        for i, link in enumerate(links):
            link[EdgeTags.ppi_id] = i
            res[str(i)] = link
        return res


if __name__ == "__main__":
    link_list = "/Users/till/Documents/Playground/PPI_network/elists/PPI_full_elist.csv"
    node_list = "/Users/till/Documents/Playground/PPI_network/layouts/PPI_physical_eigenlayout_3D.csv"
    uniprot_mapping_file = (
        "/Users/till/Documents/Playground/STRING-VRNetzer/static/uniprot_mapping.csv"
    )
    VRNetzConverter(
        link_list,
        node_list,
        uniprot_mapping_file,
    )
