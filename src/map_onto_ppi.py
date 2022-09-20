import json
import os

import numpy as np
import pandas as pd

from layouter import Layouter
from settings import _NETWORKS_PATH, EdgeTags, NodeTags


def genLinkList(filename: str) -> dict:
    """Extract edge dict from a edge csv file"""
    links = pd.read_csv(
        filename, sep=",", header=None, names=["source", "sink"]
    ).to_dict(orient="records")
    res = {}
    for i, link in enumerate(links):
        link[EdgeTags.suid] = i
        res[str(i)] = link
    return res


def genNodeLayout(filename: str, uniprot_mapping_file: str) -> list:
    """Extract node list from a node csv file"""
    uniprot_map = pd.read_csv(uniprot_mapping_file, sep=",")
    nodes = pd.read_csv(
        filename,
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
            display_name = uniprot_map.loc[index[0], "UniProt ID(supplied by UniProt)"]
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


def constructVrNetz(
    links_file: str,
    nodes_file: str,
    uniprot_mapping_file: str,
    project_name: str = "PPI.VrNetz",
) -> None:
    """Construct the VrNetz from the links and nodes csv files"""
    links = genLinkList(links_file)
    nodes = genNodeLayout(nodes_file, uniprot_mapping_file)
    vr_netz = {"nodes": nodes, "edges": links}
    with open(os.path.join(_NETWORKS_PATH, project_name), "w+") as f:
        json.dump(vr_netz, f)


def mapValues(source_node, target_node, highlight_color: list = [255, 0, 0]):
    """Adds the values from the String Network onto the node in the PPI"""
    for k, v in source_node.items():
        if k not in target_node:
            target_node[k] = v
    target_node[
        NodeTags.node_color
    ] = highlight_color  # Could also just use the color from the source network
    return target_node


def mapSourceToTarget(source: str, target: str) -> None:
    """Map the smaller network onto the larger network"""
    arbitrary_color = [255, 255, 255]
    with open(source, "r") as f:
        source_net = json.load(f)
    with open(target, "r") as f:
        target_net = json.load(f)
    source_nodes = {k: v for k, v in source_net["nodes"].items()}
    for target_node in target_net["nodes"]:
        target_net["nodes"][target_node][NodeTags.node_color] = arbitrary_color
        if target_net["nodes"][target_node][NodeTags.display_name] == "NA":
            continue
        for source_node in source_nodes:
            if (
                target_net["nodes"][target_node][NodeTags.display_name]
                == source_nodes[source_node][NodeTags.display_name]
            ):
                newNode = mapValues(
                    source_nodes[source_node], target_net["nodes"][target_node]
                )
                target_net["nodes"][target_node] = newNode
            if NodeTags.stringdb_canoncial_name in source_nodes[source_node]:
                if (
                    target_net["nodes"][target_node][NodeTags.display_name]
                    == source_nodes[source_node][NodeTags.stringdb_canoncial_name]
                ):
                    newNode = mapValues(
                        source_nodes[source_node], target_net["nodes"][target_node]
                    )
                    target_net["nodes"][target_node] = newNode

    with open(target, "w+") as f:
        json.dump(target_net, f)


if __name__ == "__main__":
    link_list = "/Users/till/Documents/Playground/PPI_network/elists/PPI_full_elist.csv"
    node_list = "/Users/till/Documents/Playground/PPI_network/layouts/PPI_physical_eigenlayout_3D.csv"
    uniprot_mapping_file = (
        "/Users/till/Documents/Playground/STRING-VRNetzer/static/uniprot_mapping.csv"
    )
    string_network = "/Users/till/Desktop/2000_alzheimer.VRNetz"
    PPI_VrNet = (
        "/Users/till/Documents/Playground/STRING-VRNetzer/static/networks/PPI.VrNetz"
    )
    constructVrNetz(
        link_list,
        node_list,
        uniprot_mapping_file,
    )
    mapSourceToTarget(string_network, PPI_VrNet)
