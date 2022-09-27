import json
import os

from settings import _NETWORKS_PATH, NodeTags

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


def add_edge_evidences(source_edges: dict, target_net: dict) -> dict:
    """Add the edge evidences from the string network to the ppi network"""
    next_id = len(target_net["edges"])
    for _, edge in source_edges.items():
        target_net["edges"][next_id] = edge
        next_id += 1
    return target_net["edges"]


def gen_name_suid_map(source_net: dict) -> tuple[dict, dict]:
    all_dis_names = {}
    all_canoncial_names = {}
    for suid, s_node in source_net["nodes"].items():
        all_dis_names[s_node[NodeTags.display_name]] = suid
        if NodeTags.stringdb_canoncial_name in s_node:
            all_canoncial_names[s_node[NodeTags.stringdb_canoncial_name]] = suid
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
    target_node[
        NodeTags.node_color
    ] = highlight_color  # Could also just use the color from the source network
    return target_node


def map_source_to_target(
    source: str, target: str, output_name: str = "PPI_out.VRNetz"
) -> None:
    """Map the smaller network onto the larger network"""
    arbitrary_color = [255, 255, 255]
    with open(source, "r") as f:
        source_net = json.load(f)
    with open(target, "r") as f:
        target_net = json.load(f)
    all_dis_names, all_canoncial_names = gen_name_suid_map(source_net)
    # ppi_to_suid = {}
    for id, t_node in target_net["nodes"].items():
        t_node[NodeTags.node_color] = arbitrary_color
        ppi_id = t_node[NodeTags.ppi_id]
        node_identifiers = t_node[NodeTags.display_name].split(",")
        for identifier in node_identifiers:
            if identifier != "NA":
                if identifier in all_dis_names:
                    suid = all_dis_names[identifier]
                    # ppi_to_suid[ppi_id] = suid
                    s_node = source_net["nodes"][suid]
                    target_net["nodes"][id] = map_values(s_node, t_node)
                elif identifier in all_canoncial_names:
                    suid = all_canoncial_names[identifier]
                    # ppi_to_suid[ppi_id] = suid
                    s_node = source_net["nodes"][suid]
                    target_net["nodes"][id] = map_values(s_node, t_node)
    # suid_to_ppi = {v: k for k, v in ppi_to_suid.items()}
    target_net["edges"] = add_edge_evidences(source_net["edges"], target_net)
    with open(os.path.join(_NETWORKS_PATH, output_name), "w+") as f:
        json.dump(target_net, f)


if __name__ == "__main__":
    string_network = "/Users/till/Desktop/2000_alzheimer.VRNetz"
    PPI_VrNet = (
        "/Users/till/Documents/Playground/STRING-VRNetzer/static/networks/PPI.VrNetz"
    )
    map_source_to_target(string_network, PPI_VrNet)
    # /opt/homebrew/bin/python3 /Users/till/Documents/Playground/STRING-VRNetzer/src/main.py project '/Users/till/Documents/Playground/STRING-VRNetzer/static/networks/PPI_out.VrNetz' None None False 2000_alz_map_ppi_with_ev False False
