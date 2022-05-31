import logging
import os

from create_network import Layouter
from cytoscape_parser import CytoscapeParser
from graphml_parser import parse_graphml_network
from string_commands import (
    StringCompoundQuery,
    StringDiseaseQuery,
    StringProteinQuery,
    StringPubMedQuery,
)

logger = logging.getLogger()
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
    parser: CytoscapeParser, filename, network=None, keep_output=True, **kwargs
) -> Layouter:
    networks = parser.get_network_list()
    if network is None:
        network = list(networks.keys())[0]
    logger.info(f"Network exported:{network}")
    parser.export_network(filename=filename, network=network, **kwargs)
    nodes, edges = parse_graphml_network(f"{filename}.graphml")
    layouter = Layouter(nodes, edges)
    layouter.apply_layout()
    if not keep_output:
        os.remove(f"{filename}.graphml")

    return layouter


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
