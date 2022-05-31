import sys

from cytoscape_parser import CytoscapeParser
from src.workflows import (call_compound_query, call_disease_query,
                           call_protein_query, call_pubmed_query)
from workflows import export_network


def call_query(parser:CytoscapeParser):
    arguments = [
        None,  # Query Type
        None,  # Query (Protein, Disease, Compound, PubMed)
        None,  # Cutoff
        None,  # Limit
        None,  # Species
        None,  # TaxonID
    ]
    for i, arg in enumerate(sys.argv[2:]):
        if "," in arg:
            arg = arg.split(",")
        arguments[i] = arg
    queries = {
        "protein": call_protein_query,
        "disease": call_disease_query,
        "compound": call_compound_query,
        "pubmed": call_pubmed_query,
    }
    queries[parser,arguments[0]](
        arguments[1],
        cutoff=arguments[2],
        limit=arguments[3],
        species=arguments[4],
        taxonID=arguments[5],
    )
    choice = input("Want to export this network?\n")
    if choice is "y":
        return prepare_export()
    return None

def prepare_export():
    new_argv = input(
            "Please enter <filename> <network> <keep tmp> **kwargs"
        ).split(" ")
    arguments = [
        None,  # Network
        None,  # Filename
        None,  # Keep temp Graph XML file
        None,  # Base url
        None,  # *
        None,  # overwrite_file
    ]
    for i, arg in enumerate(new_argv):
        arguments[i] = arg
    sys.argv = sys.argv[:2]+arguments
    return sys.argv

def call_export(parser,argv=sys.argv[2:]):
    


def main(filename):
    if len(sys.argv) == 1:
        print(
            "Usage:\n"
            + "main.py query <query type=[protein/disease/compound/pubmed]> <query> <opt:cutoff> <opt:limit> <opt:species> <opt:taxonID>"
            + "\n"
            "or\n"
            + "main.py export <network> <filename> <opt:KeepTmp> <opt:baseUrl> <opt:*> <opt:overwrite_file>"
        )
        return
    keyword = sys.argv[1]
    parser = CytoscapeParser()
    if keyword is "query":
        sys.argv = call_query(parser)
        if sys.argv is None:
            return
    elif keyword is "export":
        call_export(parser)
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
    # print(timeit.timeit(parser.check_for_string_app), number=10)
    print(parser.get_network_list())
    # call_protein_query(parser, p_query=["ABC"], limit=2)
    # call_disease_query(parser, disease="breast cancer", limit=100)
    layouter = export_network(
        parser,
        filename=filename,
        overwrite_file=True,
        type="graphML",
    )
    with open(f"{filename}.json", "w") as outfile:
        outfile.write(f"{layouter.nodes_data}\n")
        outfile.write(f"{layouter.edges_data}")


if __name__ == "__main__":
    main()
