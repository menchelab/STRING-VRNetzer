import json
import os
from lib2to3.pytree import Node
from re import S

import numpy as np
import pandas as pd

from layouter import Layouter
from settings import _NETWORKS_PATH, EdgeTags, NodeTags


def gen_link_list(filename: str) -> dict:
    """Extract edge dict from a edge csv file"""
    links = pd.read_csv(
        filename, sep=",", header=None, names=["source", "sink"]
    ).to_dict(orient="records")
    res = {}
    for i, link in enumerate(links):
        link[EdgeTags.ppi_id] = i
        res[str(i)] = link
    return res


def gen_node_layout(filename: str, uniprot_mapping_file: str) -> list:
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


def construct_VRNetz(
    links_file: str,
    nodes_file: str,
    uniprot_mapping_file: str,
    project_name: str = "PPI.VrNetz",
) -> None:
    """Construct the VrNetz from the links and nodes csv files"""
    links = gen_link_list(links_file)
    nodes = gen_node_layout(nodes_file, uniprot_mapping_file)
    vr_netz = {"nodes": nodes, "edges": links}
    with open(os.path.join(_NETWORKS_PATH, project_name), "w+") as f:
        json.dump(vr_netz, f)


def map_values(source_node, target_node, highlight_color: list = [255, 0, 0]):
    """Adds the values from the String Network onto the node in the PPI"""
    for k, v in source_node.items():
        if (
            k not in target_node
        ):  # Add all keys which are not yet in the node informations
            target_node[k] = v
    target_node[
        NodeTags.node_color
    ] = highlight_color  # Could also just use the color from the source network
    return target_node


# def process_edge(source, sink, target_edge, source_edges):
#     edge_found = False
#     for id, edge in source_edges.items():
#         if (edge[EdgeTags.source] == source and edge[EdgeTags.sink] == sink) or (
#             edge[EdgeTags.source] == sink and edge[EdgeTags.sink] == source
#         ):
#             edge_found = True
#             for k, v in edge.items():
#                 if k not in edge:
#                     edge[k] = v
#             target_edge = edge
#             print("FOUND")
#     if not edge_found:
#         target_edge = None
#         # next_id = len(edges)
#         # source_edge[EdgeTags.source] = source
#         # source_edge[EdgeTags.sink] = sink
#         # target_net["edges"][next_id] = source_edge
#     return target_edge


def add_edge_evidences(ppi_to_suid, suid_to_ppi, source_edges, target_net):
    """Add the edge evidences from the string network to the ppi network"""
    next_id = len(target_net["edges"])
    for _, edge in source_edges.items():
        target_net["edges"][next_id] = edge
        next_id += 1
    return target_net["edges"]


def gen_name_suid_map(source_net):
    all_dis_names = {}
    all_canoncial_names = {}
    for suid, s_node in source_net["nodes"].items():
        all_dis_names[s_node[NodeTags.display_name]] = suid
        if NodeTags.stringdb_canoncial_name in s_node:
            all_canoncial_names[s_node[NodeTags.stringdb_canoncial_name]] = suid
    return all_dis_names, all_canoncial_names


def map_source_to_target(source: str, target: str) -> None:
    """Map the smaller network onto the larger network"""
    arbitrary_color = [255, 255, 255]
    with open(source, "r") as f:
        source_net = json.load(f)
    with open(target, "r") as f:
        target_net = json.load(f)
    all_dis_names, all_canoncial_names = gen_name_suid_map(source_net)
    ppi_to_suid = {}
    for id, t_node in target_net["nodes"].items():
        t_node[NodeTags.node_color] = arbitrary_color
        ppi_id = t_node[NodeTags.ppi_id]
        node_identifiers = t_node[NodeTags.display_name].split(",")
        for identifier in node_identifiers:
            if identifier != "NA":
                if identifier in all_dis_names:
                    suid = all_dis_names[identifier]
                    ppi_to_suid[ppi_id] = suid
                    s_node = source_net["nodes"][suid]
                    target_net["nodes"][id] = map_values(s_node, t_node)
                elif identifier in all_canoncial_names:
                    suid = all_canoncial_names[identifier]
                    ppi_to_suid[ppi_id] = suid
                    s_node = source_net["nodes"][suid]
                    target_net["nodes"][id] = map_values(s_node, t_node)
    suid_to_ppi = {v: k for k, v in ppi_to_suid.items()}
    target_net["edges"] = add_edge_evidences(
        ppi_to_suid, suid_to_ppi, source_net["edges"], target_net
    )
    with open(os.path.join(_NETWORKS_PATH, "PPI_out.VRNetz"), "w+") as f:
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
    # construct_VRNetz(
    #     link_list,
    #     node_list,
    #     uniprot_mapping_file,
    # )
    map_source_to_target(string_network, PPI_VrNet)
    # /opt/homebrew/bin/python3 /Users/till/Documents/Playground/STRING-VRNetzer/src/main.py project '/Users/till/Documents/Playground/STRING-VRNetzer/static/networks/PPI_out.VrNetz' None None False 2000_alz_map_ppi_with_ev False False
