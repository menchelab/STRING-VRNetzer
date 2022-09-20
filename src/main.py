#! python3
import os
import sys
from ast import literal_eval

from cytoscape_parser import CytoscapeParser
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
    success = queries[argv["query_type"]](
        parser,
        argv["query"],
        cutoff=argv["cutoff"],
        limit=argv["limit"],
        species=argv["species"],
        taxonID=argv["taxonID"],
    )
    if success:
        choice = input("Want to export this network?\n")
        if choice == "y":
            argv = prepare_export()
            call_export(parser, argv)
    else:
        exit()


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
        "keep_tmp": True,
        "base_url": "http://127.0.0.1:1234/v1",
        "*": None,
        "overwrite_files": True,
    }
    argv = extract_arguments(argv, new_argv)
    return argv


def call_export(parser, argv=None):
    """Export the targeted network to a GraphML file."""
    if argv is None:
        argv = {
            "network": None,
            "filename": None,
            "keep_tmp": True,
            "base_url": "http://127.0.0.1:1234/v1",
            "*": None,
            "overwrite_files": True,
        }
        argv = extract_arguments(argv, sys.argv[2:])

    # Export Network as GraphML
    layouter, filename = export_network(
        parser,
        argv["filename"],
        argv["network"],
        keep_output=argv["keep_tmp"],
        overwrite_file=argv["overwrite_files"],
    )
    print(isinstance(argv["network"], int))
    # Create VRNetzer Project
    skip_exists = not argv["overwrite_files"]
    state = create_project(
        layouter.graph, filename, skip_exists=skip_exists, keep_tmp=argv["keep_tmp"]
    )
    return state


def call_create_project():
    argv = {
        "network": None,
        "layout_algo": None,
        "keep_tmp": True,
        "skip_exists": False,
        "project_name": None,
        "gen_layout": True,
    }
    argv = extract_arguments(argv, sys.argv[2:])
    print(argv.items())
    if argv["project_name"] is None:
        argv["project_name"] = str(argv["network"].split("/")[-1]).replace(
            ".VRNetz", ""
        )
    layouter = apply_layout(argv["network"], argv["gen_layout"], argv["layout_algo"])
    graph = layouter.graph
    state = create_project(
        graph,
        project_name=argv["project_name"],
        keep_tmp=argv["keep_tmp"],
        skip_exists=argv["skip_exists"],
    )
    return state


def print_networks(parser: CytoscapeParser):
    print("Network\t\t\t SUID")
    for k, v in parser.get_network_list().items():
        print(f"{k}\t\t\t {v}")


def main():
    """Guides the user through the workflow."""

    if len(sys.argv) == 1:
        print(
            "Usage:\n"
            + "main.py query <query type=[protein/disease/compound/pubmed]> <query> <opt:cutoff> <opt:limit> <opt:species> <opt:taxonID>"
            + "\n"
            "or\n"
            + "main.py export <network> <filename> <opt:KeepTmp> <opt:*> <opt:overwrite_file>"
            + "\n"
            + "or\n"
            + "main.py project <network> <opt:layout_algo> <opt:KeepTmp> <opt:skip_exists> <opt:project_name> <opt:gen_layout>"
            + "\n"
            + "or\n"
            + "main.py names"
        )
        return
    keyword = sys.argv[1]
    if keyword in ["query", "export", "names"]:
        parser = CytoscapeParser()
        if keyword == "query":
            call_query(parser)
        elif keyword == "names":
            print_networks(parser)
        elif keyword == "export":
            state = call_export(parser)
            logging.debug(state)
    elif keyword == "project":
        state = call_create_project()
        logging.debug(state)


if __name__ == "__main__":
    main()
