import json
import os

from .settings import _NETWORKS_PATH
from .settings import Evidences as EV
from .settings import LayoutTags as LT
from .settings import NodeTags as NT
from .settings import StringTags as ST
from .settings import VRNetzElements as VRNE

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


def add_link_evidences(source_link: dict, target_net: dict) -> dict:
    """Add the link evidences from the string network to the ppi network"""
    for link in source_link:
        target_net[VRNE.links].append(link)
    return target_net[VRNE.links]


def gen_name_suid_map(source_net: dict) -> tuple[dict, dict]:
    all_dis_names = {}
    all_canoncial_names = {}
    for s_node in source_net[VRNE.nodes]:
        all_dis_names[s_node[NT.name]] = s_node
        if ST.stringdb_canoncial_name in s_node:
            all_canoncial_names[s_node[ST.stringdb_canoncial_name]] = s_node
    return all_dis_names, all_canoncial_names


def map_values(
    source_node: dict, target_node: dict, highlight_color: list = [255, 0, 0]
) -> dict:
    """Adds the values from the String Network onto the node in the PPI"""
    for k, v in source_node.items():
        if (
            k not in target_node
        ):  # Add all keys which are not yet in the node informations
            target_node[k] = v
    for l, _ in enumerate(target_node[NT.layouts]):
        target_node[NT.layouts][l][LT.color] = highlight_color
    return target_node


def map_source_to_target(
    source: str, target: str, output_name: str = "PPI_out.VRNetz"
) -> None:
    """Map the smaller network onto the larger network"""
    arbitrary_color = [255, 255, 255, 255]
    with open(source, "r") as f:
        source_net = json.load(f)

    with open(target, "r") as f:
        target_net = json.load(f)

    all_dis_names, all_canoncial_names = gen_name_suid_map(source_net)
    # ppi_to_suid = {}
    for idx, t_node in enumerate(target_net[VRNE.nodes]):
        t_node[NT.node_color] = arbitrary_color
        id = t_node[NT.id]
        node_identifiers = t_node[NT.name].split(",")
        for identifier in node_identifiers:
            if identifier != "NA":
                if identifier in all_dis_names:
                    s_node = all_dis_names[identifier]
                    target_net[VRNE.nodes][idx] = map_values(s_node, t_node)
                elif identifier in all_canoncial_names:
                    s_node = all_canoncial_names[identifier]
                    target_net[VRNE.nodes][idx] = map_values(s_node, t_node)
    target_net[VRNE.links] = add_link_evidences(source_net[VRNE.links], target_net)
    for ev in EV.get_default_scheme().keys():
        target_net[VRNE.link_layouts].append(ev)
    if not output_name.endswith(".VRNetz"):
        output_name = f"{output_name}.VRNetz"
    with open(os.path.join(_NETWORKS_PATH, output_name), "w+") as f:
        json.dump(target_net, f)


if __name__ == "__main__":
    string_network = "/Users/till/Desktop/2000_alzheimer.VRNetz"
    PPI_VrNet = (
        "/Users/till/Documents/Playground/STRING-VRNetzer/static/networks/PPI.VrNetz"
    )
    map_source_to_target(string_network, PPI_VrNet)
    # /opt/homebrew/bin/python3 /Users/till/Documents/Playground/STRING-VRNetzer/src/main.py project '/Users/till/Documents/Playground/STRING-VRNetzer/static/networks/PPI_out.VrNetz' None None False 2000_alz_map_ppi_with_ev False False
