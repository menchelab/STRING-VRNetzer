import sys
from ast import literal_eval

from . import workflows as wf
from .cytoscape_parser import CytoscapeParser


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


def call_query_workflow(parser: CytoscapeParser, arg=sys.argv) -> None:
    """Calls either a protein query, disease query, compound query or a PubMed query."""
    argv = {
        "query_type": None,
        "query": None,
        "cutoff": None,
        "limit": None,
        "species": None,
        "taxonID": None,
    }
    argv = extract_arguments(argv, arg[2:])
    queries = {
        "protein": wf.protein_query_workflow,
        "disease": wf.disease_query_workflow,
        "compound": wf.compound_query_workflow,
        "pubmed": wf.pubmed_query_workflow,
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
        wf.logger.info("Network fetched!")
        choice = input("Want to export this network?\n")
        if choice == "y":
            argv = prepare_export()
            call_export_workflow(parser, argv)
    else:
        exit()


def prepare_export() -> dict[str, any]:
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


def call_export_workflow(parser, argv=None, arg=sys.argv) -> None:
    """Export the targeted network to a .VRNetz file."""
    if argv is None:
        argv = {
            "network": None,
            "filename": None,
            "keep_tmp": True,
            "base_url": "http://127.0.0.1:1234/v1",
            "*": None,
            "overwrite_files": True,
        }
        argv = extract_arguments(argv, arg[2:])

    # Export Network as VRNetz
    layouter, filename = wf.export_network_workflow(
        parser,
        argv["filename"],
        argv["network"],
        keep_output=argv["keep_tmp"],
        overwrite_file=argv["overwrite_files"],
    )
    print(isinstance(argv["network"], int))
    # Create VRNetzer Project
    skip_exists = not argv["overwrite_files"]
    state = wf.create_project_workflow(
        layouter.graph, filename, skip_exists=skip_exists, keep_tmp=argv["keep_tmp"]
    )
    wf.logging.debug(state)
    wf.logger.info("Network exported!")


def print_networks_workflow(parser: CytoscapeParser) -> None:
    print("Network\t\t\t SUID")
    for k, v in parser.get_network_list().items():
        print(f"{k}\t\t\t {v}")


def call_map_workflow(arg=sys.argv) -> None:
    argv = {
        "source_network": None,
        "target_network": None,
        "output_name": None,
    }
    argv = extract_arguments(argv, arg[2:])
    if argv["output_name"] is None:
        overwrite = input(
            f"Output name is not give, overwrite {argv['target_network']}? [y/n]"
        )
        if overwrite == "y":
            argv["output_name"] = argv["target_network"]
        else:
            print("Aborting...")
            exit()
    output_dest = wf.map_workflow(
        argv["source_network"], argv["target_network"], argv["output_name"]
    )
    wf.logging.info(
        f"Smaller network mapped to larger network, output can be found at {output_dest}"
    )


def call_convert(arg=sys.argv) -> None:
    """Takes an node list and an link list and converts them to a .VRNetz file."""
    argv = {
        "node_list": None,
        "link_list": None,
        "uniprot_mapping_file": None,
        "project_name": None,
    }
    argv = extract_arguments(argv, arg[2:])
    print(argv)
    output = wf.convert_workflow(
        argv["node_list"],
        argv["link_list"],
        argv["uniprot_mapping_file"],
        argv["project_name"],
    )
    wf.logging.info(f"Network converted to {output}.")


def call_create_project_workflow(arg=sys.argv) -> None:
    """Creates a VRNetz project from a given .VRNetz file."""
    argv = {
        "network": None,
        "layout_algo": None,
        "keep_tmp": True,
        "skip_exists": False,
        "project_name": None,
        "gen_layout": True,
        "cy_layout": True,
        "stringify": True,
    }
    argv = extract_arguments(argv, arg[2:])
    if argv["project_name"] is None:
        argv["project_name"] = str(argv["network"].split("/")[-1]).replace(
            ".VRNetz", ""
        )
    layouter = wf.apply_layout_workflow(
        argv["network"],
        argv["gen_layout"],
        argv["layout_algo"],
        argv["cy_layout"],
        argv["stringify"],
    )
    network = layouter.network
    state = wf.create_project_workflow(
        network,
        project_name=argv["project_name"],
        keep_tmp=argv["keep_tmp"],
        skip_exists=argv["skip_exists"],
        cy_layout=argv["cy_layout"],
        stringifiy=argv["stringify"],
    )
    wf.logging.debug(state)
