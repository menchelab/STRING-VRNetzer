import argparse
from optparse import OptionParser
from random import choices


def parse_mode():
    """Parse the mode for the main function."""
    parser = OptionParser(description="Cytoscape VRNetzer Exporter")
    parser.add_option(
        "-m",
        "--mode",
        help="Mode of the program.",
        type=str,
        options=["query", "export", "project", "names"],
        nargs=1,
    )
    return parser


def parse_query(parser):
    """_summary_"""
    # parser.add_argument("netType","-nt",help="Defines whether you want a full network or a physical subnetwork",
    # choices=["full","subnet"])
    parser.add_argument("query", "-q", help="Deine the Query")
    parser.add_option(
        "cutoff", "-c", help="Define the cutoff value.", type=float, default=0.4
    )
    parser.add_option(
        "limit",
        "-l",
        help="Defines the number of maximal Nodes.",
        type=int,
        default=100,
    )
    parser.add_option("species", "-s", help="Defines the species.", type=str)
    parser.add_option("taxonID", "-t", help="Defines the taxonID", type=str)


def parse_export(parser):
    parser.add_option(
        "network", "-n", help="Define which network to export", type=str, nargs=1
    )
    parser.add_option(
        "filename", "-f", help="Define which network to export", type=str, nargs=1
    )
    parser.add_option("tmp", "-kt", help="Keeps tmp files", type=str, default=True)
    parser.add_option(
        "overwrite",
        "-kt",
        help="Overwrite file if already existing",
        default=True,
        type=str,
    )


def main():
    main_parser = parse_mode()
    mode = main_parser.parse_args().mode[0]
    modes = {
        "export": parse_export,
        "query": parse_query,
    }
    modes[mode](main_parser)


if __name__ == "__main__":
    main()
