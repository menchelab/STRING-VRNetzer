import os
import sys
from ast import literal_eval

from create_network import Layouter
from cytoscape_parser import CytoscapeParser
from workflows import (
    call_compound_query,
    call_disease_query,
    call_protein_query,
    call_pubmed_query,
    create_project,
    export_network,
)


def extract_arguments(argv: list[str], source: list[str]) -> list[any]:
    """Extract argument literals from list of strings."""
    for i, arg in enumerate(source):
        try:
            arg = literal_eval(arg)
        except (ValueError, SyntaxError):
            arg = str(arg)
            if "," in arg:
                arg = arg.split(",")
        argv[i] = arg
    return argv


def call_query(parser: CytoscapeParser):
    """Calls either a protein query, disease query, compound query or a PubMed query."""
    argv = [
        None,  # Query Type
        None,  # Query (Protein, Disease, Compound, PubMed)
        None,  # Cutoff
        None,  # Limit
        None,  # Species
        None,  # TaxonID
    ]
    argv = extract_arguments(argv, sys.argv[2:])
    queries = {
        "protein": call_protein_query,
        "disease": call_disease_query,
        "compound": call_compound_query,
        "pubmed": call_pubmed_query,
    }
    # Call the desired Query
    queries[argv[0]](
        parser,
        argv[1],
        cutoff=argv[2],
        limit=argv[3],
        species=argv[4],
        taxonID=argv[5],
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
    argv = [
        None,  # Network
        None,  # Filename
        None,  # Keep temp Graph XML file
        None,  # Base url
        None,  # *
        None,  # overwrite_file
    ]
    argv = extract_arguments(argv, new_argv)
    return argv


def call_export(parser, argv=None):
    """Export the targeted network to a GraphML file."""
    if argv is None:
        argv = [
            None,  # 0: Network
            None,  # 1: Filename
            False,  # 2: Keep temp GraphML file
            "http://127.0.0.1:1234/v1",  # 3: Base url
            None,  # 4: *
            True,  # 5: overwrite_file
        ]
        argv = extract_arguments(argv, sys.argv[2:])
    layouter, filename = export_network(
        parser, argv[1], argv[0], argv[3], overwrite_file=argv[5]
    )
    create_project(layouter.graph, filename, skip_exists=argv[5])


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
        call_export(parser)
    elif keyword == "names":
        print("Network\t\t\t SUID")
        for k, v in parser.get_network_list().items():
            print(f"{k}\t\t\t {v}")


if __name__ == "__main__":
    main()
