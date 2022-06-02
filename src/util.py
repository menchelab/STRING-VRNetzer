import os
import subprocess as sp
import sys
import time

import networkx as nx
import numpy as np
import psutil
import requests
from matplotlib import pyplot as plt
from requests.exceptions import ConnectionError


def get_pid_of_process(process_names: list):
    """Get the PID of a running process addressed by name."""
    processes = [proc for proc in psutil.process_iter()]
    for p in processes:
        for name in process_names:
            if p.name().lower() == name:
                pid = p.pid
                return pid
    return None


def wait_until_ready(url, time_limit=30) -> bool:
    """Waits until an response is successful. Waits repeats until a certain time limit has passed."""
    response = requests.Response()
    start = time.time()
    while response.status_code != 200:
        try:
            response = requests.get(url)
        except ConnectionError as e:
            pass
        if time.time() - start > time_limit:
            raise TimeoutError
        # time.sleep(1)
    return True


def prepare_networkx_network(G: nx.Graph, positions: dict = None):
    """Transforms a basic networkx graph into a correct data structure to be uploaded by the Cytoscape uploader. If the positions are not given, the positions are calculated using the spring layout algorithm of networkx."""
    if positions is None:
        positions = nx.spring_layout(G, dim=3)
    nodes_data = {}
    edges_data = {}
    for node in G.nodes():
        nodes_data[node] = {
            "pos": positions[node],
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