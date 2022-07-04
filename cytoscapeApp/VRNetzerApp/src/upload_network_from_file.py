import os
import sys
from ast import literal_eval

from settings import _PROJECTS_PATH
from uploader_cytoscape_network import upload_files


def upload_network_from_file(filename: str, project_name: str, **kwargs):
    """Loads nodes data and edge data from a file containing 2 dicts, one for nodes and one for edges."""
    with open(filename, "r") as f:
        content = f.readlines()
        nodes_data = literal_eval(content[0].strip("\n"))
        edge_data = literal_eval(content[1].strip("\n"))
    print(upload_files(project_name, project_name, nodes_data, edge_data, **kwargs))


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        skip_exists = True
        if len(sys.argv) == 4:
            skip_exists = literal_eval(sys.argv[3])
        upload_network_from_file(
            sys.argv[1],
            sys.argv[2],
            projects_path=_PROJECTS_PATH,
            skip_exists=skip_exists,
        )
    else:
        print("Usage: upload_network_from_file.py <filename> <project_name>")
