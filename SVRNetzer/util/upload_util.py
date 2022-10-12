import csv
import json
import os

import networkx as nx
from SVRNetzer.util.settings import _PROJECTS_PATH, NT, EdgeTags
from SVRNetzer.util.uploader import upload_files


def upload_network_from_file(filename: str, project_name: str, **kwargs) -> None:
    """Loads nodes data and edge data from json file in which all nodes have 3D coordinates."""
    with open(filename, "r") as f:
        network = json.load(f)
    print(upload_files(project_name, project_name, network, **kwargs))


def prepare_networkx_network(G: nx.Graph, positions: dict = None) -> tuple[dict, dict]:
    """Transforms a basic networkx graph into a correct data structure to be uploaded by the Cytoscape uploader. If the positions are not given, the positions are calculated using the spring layout algorithm of networkx."""
    if positions is None:
        positions = nx.spring_layout(G, dim=3)
    for node in G.nodes():
        nx.set_node_attributes(
            G,
            {
                "pos": positions[node],
                "uniprotide": node,
                "display_name": "Gene Name of the Protein",
            },
        )
    return G


def convert_csv_to_json(node_file: str, project_name: str, **kwargs) -> None:
    """Loads a csv network file and translates it to the new json format."""
    nodes = []
    edges = []
    # exract nodes
    with open(node_file, "r") as csvfile:
        network = csv.reader(csvfile, delimiter=",")
        for i, row in enumerate(network):
            annot = row[7].split(";")
            suid = annot[1]
            nodes[suid] = {
                NT.vrnetzer_pos: row[:2],
                NT.node_color: row[4:6],
                NT.display_name: annot[0],
                NT.suid: suid,
                NT.description: annot[2],
            }
    # extract edges
    with open(node_file, "r") as csvfile:
        network = csv.reader(csvfile, delimiter=",")
        for i, row in enumerate(network):
            suid = str(i)
            edges[suid] = {
                EdgeTags.source: row[0],
                EdgeTags.sink: row[1],
                EdgeTags.color: row[2:],
            }
    network = {"nodes": nodes, "edges": edges}
    dest = os.path.join(_PROJECTS_PATH, "f{project_name}.VRNetz")
    with open(dest, "w") as f:
        json.dump(network, f)


if __name__ == "__main__":
    # upload_network_from_file(
    #     "/Users/till/Documents/Playground/STRING-VRNetzer/static/networks/STRING_network_-_Alzheimer's_disease.VRNetz",
    #     "STRING_network_-_Alzheimer's_disease",
    # )
    convert_csv_to_json(
        "/Users/till/Desktop/VRNetzer_Backend/static/csv/1_spring3.csv", "1_spring3"
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
