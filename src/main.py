import json
import logging
import os
from typing import List

import networkx as nx
from black import out
from matplotlib import pyplot as plt

from create_network import Layouter
from cytoscape_parser import CytoscapeParser
from graphml_parser import parse_graphml
from string_commands import (
    StringCompoundQuery,
    StringDiseaseQuery,
    StringProteinQuery,
    StringPubMedQuery,
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def call_protein_query(parser: CytoscapeParser, p_query: List[str], **kwargs):
    """Fetches a network for given protein query."""
    query = StringProteinQuery(query=p_query, **kwargs)
    logger.info(f"Command as list:{query.cmd_list}")
    parser.exec_cmd(query.cmd_list)


def call_disease_query(parser: CytoscapeParser, disease: str, **kwargs):
    """Fetches a network for given disease query."""
    query = StringDiseaseQuery(disease=disease, **kwargs)
    logger.info(f"Command as list:{query.cmd_list}")
    parser.exec_cmd(query.cmd_list)


def call_compound_query(parser: CytoscapeParser, query: List[str], **kwargs):
    """Fetches a network for given compound query."""
    query = StringCompoundQuery(query=query, **kwargs)
    logger.info(f"Command as list:{query.cmd_list}")
    parser.exec_cmd(query.cmd_list)


def call_pubmed_query(parser: CytoscapeParser, pubmed: List[str], **kwargs):
    """Fetches a network for given pubmed query."""
    query = StringPubMedQuery(pubmed=pubmed, **kwargs)
    logger.info(f"Command as list:{query.cmd_list}")
    parser.exec_cmd(query.cmd_list)


def export_network(parser: CytoscapeParser, filename, keep_output=True, **kwargs):
    networks = parser.get_network_list()
    network = list(networks.keys())[0]
    logger.info(f"Network exported:{network}")
    parser.export_network(filename=filename, network=network, **kwargs)
    nodes, edges = parse_graphml(f"{filename}.graphml")
    layouter = Layouter(nodes, edges)
    layouter.apply_layout()
    if not keep_output:
        os.remove(f"{filename}.graphml")

    with open("sample.json", "w") as outfile:
        outfile.write("from numpy import array\n")
        outfile.write(f"nodes_data={layouter.nodes_data}\n")
        outfile.write(f"edge_data={layouter.edges_data}\n")


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


def export_style():
    # TODO implement exporting of network style
    pass


def main():
    # pd.options.mode.chained_assignment = None
    # string_cmd_list = ["string disease query", 'disease="sadcer"', "cutoff=0.1"]
    # string_cmd = " ".join(string_cmd_list)
    # try:
    #     p4c.commands.commands_run(string_cmd)
    # except p4c.exceptions.CyError:
    #     print(f"Error running command")
    # parser = CytoscapeParser()

    # p4c.export_network("./HIV-human PPI.sif")
    # cmd = StringDiseaseQuery(
    #     disease="cancer", network_type=NetworkType.physicalSubnetwork
    # )
    parser = CytoscapeParser()
    parser.check_for_string_app()
    # call_protein_query(parser, p_query=["ABC"], limit=2)
    # call_disease_query(parser, disease="breast cancer", limit=1000)
    export_network(
        parser,
        filename="test",
        overwrite_file=True,
        type="graphML",
    )


if __name__ == "__main__":
    main()
