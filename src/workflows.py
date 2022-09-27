import json
import logging
import os

import networkx as nx

from converter import VRNetzConverter
from cytoscape_parser import CytoscapeParser
from extract_colors_from_style import get_node_mapping
from layouter import Layouter
from map_small_on_large import map_source_to_target
from settings import _NETWORKS_PATH, _PROJECTS_PATH, UNIPROT_MAP, EdgeTags
from string_commands import (
    StringCompoundQuery,
    StringDiseaseQuery,
    StringProteinQuery,
    StringPubMedQuery,
)
from uploader_cytoscape_network import upload_files
from util import colorize_nodes

logger = logging.getLogger("VRNetzer Cytoscape App")
logger.setLevel(logging.DEBUG)


def protein_query_workflow(parser: CytoscapeParser, p_query: list[str], **kwargs):
    """Fetches a network for given protein query."""
    query = StringProteinQuery(query=p_query, **kwargs)
    logger.info(f"Command as list:{query.cmd_list}")
    parser.exec_cmd(query.cmd_list)


def disease_query_workflow(parser: CytoscapeParser, disease: str, **kwargs):
    """Fetches a network for given disease query."""
    query = StringDiseaseQuery(disease=disease, **kwargs)
    logger.info(f"Command as list:{query.cmd_list}")
    parser.exec_cmd(query.cmd_list)


def compound_query_workflow(parser: CytoscapeParser, query: list[str], **kwargs):
    """Fetches a network for given compound query."""
    query = StringCompoundQuery(query=query, **kwargs)
    logger.info(f"Command as list:{query.cmd_list}")
    parser.exec_cmd(query.cmd_list)


def pubmed_query_workflow(parser: CytoscapeParser, pubmed: list[str], **kwargs):
    """Fetches a network for given pubmed query."""
    query = StringPubMedQuery(pubmed=pubmed, **kwargs)
    logger.info(f"Command as list:{query.cmd_list}")
    parser.exec_cmd(query.cmd_list)
    print(query.cmd_list)


def export_network_workflow(
    parser: CytoscapeParser,
    filename: str = None,
    network: str = None,
    keep_output: bool = True,
    layout_algo: str = None,
    **kwargs,
) -> tuple[Layouter, dict, str]:
    """Exports a network as GraphML file, generates a 3D layout."""
    networks = parser.get_network_list()
    if network is None:
        network = list(networks.keys())[0]
    if filename is None:
        filename = network
    filename = filename.replace(" ", "_")
    network_loc = f"{_NETWORKS_PATH}/{filename}"
    network_file = f"{network_loc}.VRNetz"

    parser.export_network(filename=network_loc)
    logger.info(f"Network exported: {network}")

    # generate a 3D layout
    layouter = apply_layout_workflow(f"{network_loc}.VRNetz", layout_algo)

    # Export current style
    # parser.export_style(filename=style_loc, **kwargs)

    # logger.info(f"Style exported: {style_file}")
    # layouter.graph = apply_style(layouter.graph, style_file)
    # if keep_output is False, we remove the tmp GraphML file
    if not keep_output:
        os.remove(network_file)
        logger.info(f"Removed tmp file: {network_file}")
        # os.remove(style_file)
        # logger.info(f"Removed tmp file: {style_file}")
    return layouter, filename


def apply_layout_workflow(
    file_name: str, gen_layout=True, layout_algo=None, create_2d_layout=True
):
    layouter = Layouter()
    layouter.read_from_json(file_name)
    logger.info(f"Network extracted from: {file_name}")
    if gen_layout:
        layouter.apply_layout(layout_algo)
        if layout_algo is None:
            layout_algo = "spring"
        logger.info(f"Layout algorithm {layout_algo} applied!")
    # Correct Cytoscape positions to be positive.
    if create_2d_layout:
        layouter.correct_cytoscape_pos()
        logger.info(f"2D layout created!")
    return layouter


def apply_style_workflow(graph: nx.Graph, style: str):
    color_mapping = get_node_mapping(style)
    if color_mapping is None:
        return graph
    mapping_type = color_mapping["type"]
    logger.info(
        f"Color mapping extracted from: {style}.xml. Mapping Type: {mapping_type}"
    )
    graph = colorize_nodes(graph, color_mapping)
    logger.info(f"Colored nodes according to color mapping.")
    return graph


def create_project_workflow(
    graph: nx.Graph,
    project_name: str,
    projects_path=_PROJECTS_PATH,
    skip_exists=False,
    keep_tmp=False,
    create_2d_layout=True,
):
    nodes = dict(graph.nodes(data=True))
    edges = {tuple((edge[0], edge[1])): edge[2] for edge in graph.edges(data=True)}
    """Uses a layout to generate a new VRNetzer Project."""
    # if keep temp, we save the network as a file
    network = {"nodes": {}, "edges": {}}
    for node in nodes:
        network["nodes"][node] = nodes[node]
    network["nodes"]["data_type"] = "nodes"
    network["nodes"]["amount"] = len(nodes)
    for edge in edges:
        data = edges[edge]["data"]
        if EdgeTags.suid in data:
            suid = data[EdgeTags.suid]
        elif EdgeTags.ppi_id:
            suid = data[EdgeTags.ppi_id]
        network["edges"][suid] = edges[edge]["data"]
    network["edges"]["data_type"] = "edges"
    network["edges"]["amount"] = len(edges)
    state = upload_files(
        project_name,
        project_name,
        network,
        projects_path=projects_path,
        skip_exists=skip_exists,
        create_2d_layout=create_2d_layout,
    )
    if keep_tmp:
        outfile = f"{_NETWORKS_PATH}/{project_name}_with_3D_Coords.VRNetz"
        print(f"OUTFILE:{outfile}")
        with open(outfile, "w") as f:
            json.dump(network, f)
        logging.info(f"Saved network as {outfile}")

    logging.info(f"Project created: {project_name}")
    return state


def map_workflow(small_net: str, large_net: str, destination: str):
    """Maps a small network onto a large network."""
    map_source_to_target(small_net, large_net, destination)


def convert_workflow(node_list, edge_list, uniprot_mapping=UNIPROT_MAP, project=None):
    """Converts a network from a edge and node list to a .VRNetz file."""
    output = os.path.join(_NETWORKS_PATH, project)
    VRNetzConverter(node_list, edge_list, uniprot_mapping, project)
    return output


# TODO: Networkx export with separate table export. Does not work do fails in matching node/edge names to SUIDs
# def parse_network(parser: CytoscapeParser, network_index=None, **kwargs):
#     if network_index is None:
#         network_index = 0
#     networks = parser.get_network_list()
#     network = list(networks.keys())[network_index]
#     graph = parser.get_networkx_network(network)
#     # node_columns, edge_columns = parser.export_table(network)
#     nx.draw(graph)
#     plt.show()


# TODO directly create a networkx network
