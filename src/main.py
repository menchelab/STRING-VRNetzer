import sys
from ast import literal_eval

from cytoscape_parser import CytoscapeParser
from workflows import (call_compound_query, call_disease_query,
                       call_protein_query, call_pubmed_query, export_network)


def extract_arguments(argv, source):
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
    while True:
        new_argv = input(
            "Please enter <network> <filename> <opt:keep tmp> <opt:**kwargs>"
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
    if argv is None:
        argv = [
            None,  # Network
            None,  # Filename
            None,  # Keep temp Graph XML file
            "http://127.0.0.1:1234/v1",  # Base url
            None,  # *
            True,  # overwrite_file
        ]
        argv = extract_arguments(argv, sys.argv[2:])
    layouter = export_network(parser, argv[1], argv[0], argv[3], overwrite_file=argv[5])
    with open(f"{argv[0]}.json", "w") as outfile:
        outfile.write(f"{layouter.nodes_data}\n")
        outfile.write(f"{layouter.edges_data}")


def main():
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
    # parser = CytoscapeParser()
    # print(timeit.timeit(parser.check_for_string_app), number=10)
    # print(parser.get_network_list())
    # call_protein_query(parser, p_query=["ABC"], limit=2)
    # call_disease_query(parser, disease="breast cancer", limit=100)
    # layouter = export_network(
    #     parser,
    #     filename=filename,
    #     overwrite_file=True,
    #     type="graphML",
    # )


if __name__ == "__main__":
    main()
