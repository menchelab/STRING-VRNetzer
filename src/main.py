import os
from typing import List

from commands import NetworkType, StringDiseaseQuery, StringProteinQuery
from cytoscape_parser import CytoscapeParser


def call_protein_query(parser: CytoscapeParser, p_query: List[str], **kwargs):
    """Fetches a network for given protein query."""
    query = StringProteinQuery(query=p_query, **kwargs)
    print(query.cmd_list)
    parser.exec_cmd(query.cmd_list)


def call_disease_query(parser: CytoscapeParser, disease: str, **kwargs):
    """Fetches a network for given disease query."""
    query = StringDiseaseQuery(disease=disease, **kwargs)
    print(query.cmd_list)
    parser.exec_cmd(query.cmd_list)


def export_network(parser: CytoscapeParser, **kwargs):
    parser.export_network(**kwargs)


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
    # call_protein_query(parser, query=["ABC"], limit=2)
    call_disease_query(parser, disease="breast cancer", limit=2)
    export_network(parser, filename="test.sif", overwrite_file=True)
    if "cytoscape_proc" in list(parser.__dict__.keys()):
        parser.cytoscape_proc.wait()


if __name__ == "__main__":
    main()
