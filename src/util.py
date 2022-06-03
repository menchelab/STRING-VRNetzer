import os
import subprocess as sp
import sys
import time

import networkx as nx
import numpy as np
import psutil
import requests
from matplotlib import pyplot as plt
from PIL import ImageColor
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


def colorize_nodes(
    G: nx.Graph,
    color_mapping: dict,
) -> nx.Graph:
    """Colorizes the nodes of a networkx graph using a color mapping. Works for discrete, continuous, and passthrough mappings."""
    if color_mapping["type"] == "discrete":
        """For each node a color is assigned, if not it get the default color value."""
        for node in G.nodes:
            name = G.nodes[node]["name"]
            if name in color_mapping:
                color = color_mapping[name]
            else:
                color = color_mapping["default"]
            G.nodes[node]["color"] = color
    elif color_mapping["type"] == "continuous":
        """Uses the Value which is stored respective column a defines the color respectively."""
        default_color = color_mapping["default"]
        column = color_mapping["column"]
        for node in G.nodes:
            color = default_color
            mapping_points = {
                k: v for k, v in color_mapping.items() if isinstance(k, float)
            }
            if column in G.nodes[node].keys():
                node_value = float(G.nodes[node][column])
                for point in mapping_points:
                    color = color_mapping["default"]
                    flag = False
                    if node_value < point:
                        color = mapping_points[point][0]
                        flag = True
                    elif node_value == point:
                        color = mapping_points[point][1]
                        flag = True
                    elif node_value > point:
                        color = mapping_points[point][2]
                    if flag:
                        break
            G.nodes[node]["color"] = color
    elif color_mapping["type"] == "passthrough":
        """Uses the Value which is stored respective column."""
        column = color_mapping["column"]
        for node in G.nodes:
            if column in G.nodes[node]:
                color = G.nodes[node][column]
                # Color values are most likely hex values. We convert them to RGBA values.
                color = ImageColor.getcolor(color, "RGB") + (255,)
                G.nodes[node]["color"] = color
    return G


if __name__ == "__main__":
    G = nx.Graph()
    G.add_edge("O15552", "Q76EI6")
    print(prepare_networkx_network(G))
