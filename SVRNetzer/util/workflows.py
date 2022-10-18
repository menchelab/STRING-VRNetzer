import json
import logging
import os

import networkx as nx

from .converter import VRNetzConverter
from .cytoscape_parser import CytoscapeParser
from .layouter import Layouter
from .map_small_on_large import map_source_to_target
from .settings import _NETWORKS_PATH, _PROJECTS_PATH, UNIPROT_MAP
from .settings import VRNetzElements as VRNE
from .string_commands import (
    StringCompoundQuery,
    StringDiseaseQuery,
    StringProteinQuery,
    StringPubMedQuery,
)
from .uploader import Uploader

# from extract_colors_from_style import get_node_mapping


logger = logging.getLogger("VRNetzer Cytoscape App")
logger.setLevel(logging.DEBUG)


def protein_query_workflow(
    parser: CytoscapeParser, p_query: list[str], **kwargs
) -> None:
    """Fetches a network for given protein query."""
    query = StringProteinQuery(query=p_query, **kwargs)
    logger.info(f"Command as list:{query.cmd_list}")
    parser.exec_cmd(query.cmd_list)


def disease_query_workflow(parser: CytoscapeParser, disease: str, **kwargs) -> None:
    """Fetches a network for given disease query."""
    query = StringDiseaseQuery(disease=disease, **kwargs)
    logger.info(f"Command as list:{query.cmd_list}")
    parser.exec_cmd(query.cmd_list)


def compound_query_workflow(
    parser: CytoscapeParser, query: list[str], **kwargs
) -> None:
    """Fetches a network for given compound query."""
    query = StringCompoundQuery(query=query, **kwargs)
    logger.info(f"Command as list:{query.cmd_list}")
    parser.exec_cmd(query.cmd_list)


def pubmed_query_workflow(parser: CytoscapeParser, pubmed: list[str], **kwargs) -> None:
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
) -> tuple[Layouter, str]:
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

    # if keep_output is False, we remove the tmp GraphML file
    if not keep_output:
        os.remove(network_file)
        logger.info(f"Removed tmp file: {network_file}")

    return layouter, filename


def apply_layout_workflow(
    file_name: str,
    gen_layout: bool = True,
    layout_algo: str = None,
    cy_layout: bool = True,
    stringify: bool = True,
) -> Layouter:
    layouter = Layouter()
    layouter.read_from_vrnetz(file_name)
    logger.info(f"Network extracted from: {file_name}")

    if gen_layout:
        layouter.apply_layout(layout_algo)
        if layout_algo is None:
            layout_algo = "spring"
        logger.info(f"Layout algorithm {layout_algo} applied!")
    # Correct Cytoscape positions to be positive.
    if cy_layout:
        layouter.correct_cytoscape_pos()
        logger.info(f"2D layout created!")
    if stringify:
        layouter.gen_evidence_layouts()
    return layouter


# def apply_style_workflow(graph: nx.Graph, style: str) -> nx.Graph:
#     color_mapping = get_node_mapping(style)
#     if color_mapping is None:
#         return graph
#     mapping_type = color_mapping["type"]
#     logger.info(
#         f"Color mapping extracted from: {style}.xml. Mapping Type: {mapping_type}"
#     )
#     graph = colorize_nodes(graph, color_mapping)
#     logger.info(f"Colored nodes according to color mapping.")
#     return graph


def create_project_workflow(
    network: dict,
    project_name: str,
    projects_path: str = _PROJECTS_PATH,
    skip_exists: bool = False,
    keep_tmp: bool = False,
    cy_layout: bool = True,
    stringifiy: bool = True,
):
    """Uses a layout to generate a new VRNetzer Project."""
    uploader = Uploader(network, project_name, skip_exists, stringifiy, projects_path)
    state = uploader.upload_files(network)
    if keep_tmp:
        outfile = f"{_NETWORKS_PATH}/{project_name}_with_3D_Coords.VRNetz"
        print(f"OUTFILE:{outfile}")
        with open(outfile, "w") as f:
            json.dump(network, f)
        logging.info(f"Saved network as {outfile}")
    if stringifiy and cy_layout:
        uploader.stringify_project()
        logging.info(f"Layouts stringified: {project_name}")
    logging.info(f"Project created: {project_name}")
    return state


def map_workflow(small_net: str, large_net: str, destination: str) -> None:
    """Maps a small network onto a large network."""
    map_source_to_target(small_net, large_net, destination)


def convert_workflow(
    node_list: str, edge_list: str, uniprot_mapping=None, project=None
) -> str:
    """Converts a network from a edge and node list to a .VRNetz file."""
    if uniprot_mapping is None:
        uniprot_mapping = UNIPROT_MAP
    if project is None:
        project = "NA"
    output = os.path.join(_NETWORKS_PATH, project)
    converter = VRNetzConverter(node_list, edge_list, uniprot_mapping, project)
    converter.convert()
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
