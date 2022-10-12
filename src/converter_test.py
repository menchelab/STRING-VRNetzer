import os
import sys

from . import util


def convert_csv_vrnetz(node_files: str, link_files: str):
    arg = [
        "",
        "convert",
        node_files,
        link_files,
        "None",
        "convert_test",
    ]
    util(arg=arg)


def create_project(network, stringify="False"):
    arg = [
        "",
        "project",  # Mode
        network,  # network
        "None",  # layout_algo
        "None",  # keep_temp
        "None",  # skip_exists
        "None",  # project_name
        "False",  # gen_layout
        "False",  # cy_layout
        stringify,  # stringify
    ]
    util(arg=arg)


def map_small_to_large(source, target, output_name):
    arg = ["", "map", source, target, output_name]
    util(arg=arg)


if __name__ == "__main__":
    node_files = "['/Users/till/Documents/Playground/PPI_network/layouts/PPI_direct_eigenlayout_3D.csv','/Users/till/Documents/Playground/PPI_network/layouts/PPI_full_eigenlayout_2D.csv','/Users/till/Documents/Playground/PPI_network/layouts/PPI_full_eigenlayout_3D.csv','/Users/till/Documents/Playground/PPI_network/layouts/PPI_physical_eigenlayout_2D.csv','/Users/till/Documents/Playground/PPI_network/layouts/PPI_physical_eigenlayout_3D.csv']"
    link_files = "['/Users/till/Documents/Playground/PPI_network/elists/PPI_direct_elist.csv','/Users/till/Documents/Playground/PPI_network/elists/PPI_full_elist.csv','/Users/till/Documents/Playground/PPI_network/elists/PPI_physical_elist.csv']"

    network = "/Users/till/Documents/Playground/STRING-VRNetzer/static/networks/convert_test.VRNetz"

    source = "/Users/till/Documents/Playground/STRING-VRNetzer/static/networks/2000_alzheimer.VRNetz"
    target = "/Users/till/Documents/Playground/STRING-VRNetzer/static/networks/convert_test.VRNetz"
    output_name = "2000_alzheimer_mapped_to_PPI_eigen.VRNetz"

    # convert_csv_vrnetz(node_files, link_files)

    # create_project(network)

    # map_small_to_large(source, target, output_name)

    network = "/Users/till/Documents/Playground/STRING-VRNetzer/static/networks/2000_alzheimer_mapped_to_PPI_eigen.VRNetz"

    create_project(network, stringify="True")
