import json

from settings import _PROJECTS_PATH
from uploader_cytoscape_network import upload_files


def upload_network_from_file(filename: str, project_name: str, **kwargs):
    """Loads nodes data and edge data from json file in which all nodes have 3D coordinates."""
    with open(filename, "r") as f:
        network = json.load(f)
    print(upload_files(project_name, project_name, network, **kwargs))


if __name__ == "__main__":
    upload_network_from_file(
        "/Users/till/Documents/Playground/STRING-VRNetzer/static/networks/STRING_network_-_Alzheimer's_disease.VRNetz",
        "STRING_network_-_Alzheimer's_disease",
    )
    # if len(sys.argv) >= 3:
    #     skip_exists = True
    #     if len(sys.argv) == 4:
    #         skip_exists = literal_eval(sys.argv[3])
    #     upload_network_from_file(
    #         sys.argv[1],
    #         sys.argv[2],
    #         projects_path=_PROJECTS_PATH,
    #         skip_exists=skip_exists,
    #     )
    # else:
    #     print("Usage: upload_network_from_file.py <filename> <project_name>")
