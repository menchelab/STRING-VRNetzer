import time

import networkx as nx
import numpy as np
import psutil
import requests
from matplotlib import pyplot as plt


def get_pid_of_process(process: str):
    """Get the PID of a running process addressed by name."""
    processes = [proc for proc in psutil.process_iter()]
    for p in processes:
        if p.name().lower() == process:
            pid = p.pid
            return pid
    return None


def wait_until_ready(url, time_limit=30):
    """Waits until an response is successful. Waits repeats until a certain time limit has passed."""
    response = requests.Response()
    start = time.time()
    while response.status_code != 200:
        try:
            response = requests.get(url)
        except ConnectionError:
            pass
        if time.time() - start > time_limit:
            raise TimeoutError
        time.sleep(1)


def prepare_networkx_network(G: nx.Graph):
    """Transforms a basic networkx graph into a correct data structure to be uploaded by the Cytoscape uploader."""
    nodes_data = {}
    edges_data = {}
    for node in G.nodes():
        nodes_data[node] = {
            "pos": (0, 0, 0),
            "uniprotid": node,
            "display name": "Gene Name of the Protein",
        }
    for edge in G.edges():
        edges_data[edge] = {"source": edge[0], "target": edge[1]}
    return nodes_data, edges_data


if __name__ == "__main__":
    G = nx.Graph()
    G.add_edge("O15552", "Q76EI6")
    print(prepare_networkx_network(G))
