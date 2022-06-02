import logging
import os

import networkx as nx

from create_network import Layouter
from cytoscape_parser import CytoscapeParser
from graphml_parser import parse_graphml_network
from settings import _NETWORKS_PATH, _PROJECTS_PATH
from string_commands import (
    StringCompoundQuery,
    StringDiseaseQuery,
    StringProteinQuery,
    StringPubMedQuery,
)
from uploader_cytoscape_network import upload_files

logger = logging.getLogger("cytoscape_workflows")
logger.setLevel(logging.DEBUG)


def call_protein_query(parser: CytoscapeParser, p_query: list[str], **kwargs):
    """Fetches a network for given protein query."""
    query = StringProteinQuery(query=p_query, **kwargs)
    logger.info(f"Command as list:{query.cmd_list}")
    parser.exec_cmd(query.cmd_list)


def call_disease_query(parser: CytoscapeParser, disease: str, **kwargs):
    """Fetches a network for given disease query."""
    query = StringDiseaseQuery(disease=disease, **kwargs)
    logger.info(f"Command as list:{query.cmd_list}")
    parser.exec_cmd(query.cmd_list)


def call_compound_query(parser: CytoscapeParser, query: list[str], **kwargs):
    """Fetches a network for given compound query."""
    query = StringCompoundQuery(query=query, **kwargs)
    logger.info(f"Command as list:{query.cmd_list}")
    parser.exec_cmd(query.cmd_list)


def call_pubmed_query(parser: CytoscapeParser, pubmed: list[str], **kwargs):
    """Fetches a network for given pubmed query."""
    query = StringPubMedQuery(pubmed=pubmed, **kwargs)
    logger.info(f"Command as list:{query.cmd_list}")
    parser.exec_cmd(query.cmd_list)


def export_network(
    parser: CytoscapeParser,
    filename: str = None,
    network: str = None,
    keep_output: bool = True,
    layout_algo: str = None,
    **kwargs,
) -> Layouter:
    """Exports a network as GraphML file, generates a 3D layout ."""
    networks = parser.get_network_list()
    if network is None:
        network = list(networks.keys())[0]
    if filename is None:
        filename = network
    save_loc = f"{_NETWORKS_PATH}/{filename}"
    parser.export_network(filename=save_loc, network=network, type="graphML", **kwargs)
    logger.info(f"Network exported: {network}")

    layouter = Layouter(f"{save_loc}.graphml")
    logger.info(f"Network extracted from: {save_loc}.graphml")
    layouter.apply_layout(layout_algo)
    logger.info(f"Layout algorithm {layout_algo} applied!")
    if not keep_output:
        os.remove(f"{filename}.graphml")
        logger.info(f"Removed tmp file: {filename}.graphml.")

    return layouter, filename


def create_project(
    graph: nx.Graph,
    project_name: str,
    projects_path=_PROJECTS_PATH,
    skip_exists=True,
    keep_tmp=False,
):
    """Uses a layout to generate a new VRNetzer Project."""
    state = upload_files(
        project_name,
        project_name,
        dict(graph.nodes(data=True)),
        list(graph.edges(data=True)),
        projects_path=projects_path,
        skip_exists=skip_exists,
    )
    # if keep temp, we save the network as a file
    if keep_tmp:
        outfile = f"{_NETWORKS_PATH}/{project_name}.network"
        with open(outfile, "w") as f:
            f.write(f"{graph.nodes(data=True)}\n")
            f.write(f"{graph.edges(data=True)}")
        logging.info(f"Saved network as {outfile}")
    logging.info(f"Project created: {project_name}")


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
