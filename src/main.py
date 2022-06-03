#! python3
import os
import sys
from ast import arg, literal_eval
from re import S

from scipy.fft import skip_backend

from create_network import Layouter
from cytoscape_parser import CytoscapeParser
from util import colorize_nodes
from workflows import *


def extract_arguments(argv: list[str], source: list[str]) -> list[any]:
    """Extract argument literals from list of strings."""
    keys = list(argv.keys())
    for i, arg in enumerate(source):
        if arg == "":
            continue
        try:
            arg = literal_eval(arg)
        except (ValueError, SyntaxError):
            arg = str(arg)
            if "," in arg:
                arg = arg.split(",")
        argv[keys[i]] = arg
    return argv


def call_query(parser: CytoscapeParser):
    """Calls either a protein query, disease query, compound query or a PubMed query."""
    argv = {
        "query_type": None,
        "query": None,
        "cutoff": None,
        "limit": None,
        "species": None,
        "taxonID": None,
    }
    argv = extract_arguments(argv, sys.argv[2:])
    queries = {
        "protein": call_protein_query,
        "disease": call_disease_query,
        "compound": call_compound_query,
        "pubmed": call_pubmed_query,
    }
    # Call the desired Query
    queries[argv["query_type"]](
        parser,
        argv["query"],
        cutoff=argv["cutoff"],
        limit=argv["limit"],
        species=argv["species"],
        taxonID=argv["taxonID"],
    )
    choice = input("Want to export this network?\n")
    if choice == "y":
        argv = prepare_export()
        call_export(parser, argv)


def prepare_export():
    """Prepares the arguments for the export function."""
    while True:
        new_argv = input(
            "Please enter <network> <filename> <opt:keep tmp> <opt:**kwargs>\n"
        ).split(" ")
        if len(new_argv) > 1:
            break
    argv = {
        "network": None,
        "filename": None,
        "keep_tmp": None,
        "base_url": "http://127.0.0.1:1234/v1",
        "*": None,
        "overwrite_file": None,
    }
    argv = extract_arguments(argv, new_argv)
    return argv


def call_export(parser, argv=None):
    """Export the targeted network to a GraphML file."""
    if argv is None:
        argv = {
            "network": None,
            "filename": None,
            "keep_tmp": None,
            "base_url": "http://127.0.0.1:1234/v1",
            "*": None,
            "overwrite_file": None,
        }
        argv = extract_arguments(argv, sys.argv[2:])

    # Export Network as GraphML
    layouter, filename = export_network(
        parser,
        argv["network"],
        argv["filename"],
        keep_output=argv["keep_tmp"],
        overwrite_file=argv["overwrite_file"],
    )

    # Create VRNetzer Project
    skip_exists = not argv[5]
    state = create_project(layouter.graph, filename, skip_exists=skip_exists)
    return state


def call_create_project():
    argv = {
        "network": None,
        "style": None,
        "layout_algo": None,
        "keep_tmp": None,
        "skip_exists": None,
        "project_name": None,
    }
    argv = extract_arguments(argv, sys.argv[2:])
    if argv["project_name"] is None:
        argv["project_name"] = str(argv["network"].split("/")[-1]).strip(".graphml")
    layouter = apply_layout(argv["network"], argv["layout_algo"])
    graph = apply_style(layouter.graph, argv["style"])
    state = create_project(
        graph,
        project_name=argv["project_name"],
        keep_tmp=argv["keep_tmp"],
        skip_exists=argv["skip_exists"],
    )
    return state


def main():
    """Guides the user through the workflow."""
    if len(sys.argv) == 1:
        print(
            "Usage:\n"
            + "main.py query <query type=[protein/disease/compound/pubmed]> <query> <opt:cutoff> <opt:limit> <opt:species> <opt:taxonID>"
            + "\n"
            "or\n"
            + "main.py export <network> <filename> <opt:KeepTmp> <opt:*> <opt:overwrite_file>"
        )
        return
    keyword = sys.argv[1]
    parser = CytoscapeParser()
    if keyword == "query":
        call_query(parser)
    elif keyword == "export":
        state = call_export(parser)
        print(state)
    elif keyword == "project":
        state = call_create_project()
        print(state)
    elif keyword == "names":
        print("Network\t\t\t SUID")
        for k, v in parser.get_network_list().items():
            print(f"{k}\t\t\t {v}")


if __name__ == "__main__":
    main()
