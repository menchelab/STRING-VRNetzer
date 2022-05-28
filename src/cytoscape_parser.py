# exec(
#     requests.get(
#         "https://raw.githubusercontent.com/cytoscape/jupyter-bridge/master/client/p4c_init.py"
#     ).text
# )
# IPython.display.Javascript(_PY4CYTOSCAPE_BROWSER_CLIENT_JS)
import logging
import os
import platform
import subprocess
from time import sleep, time
from typing import Union

import py4cytoscape as p4c
import requests
from requests.exceptions import ConnectionError

from util import get_pid_of_process, wait_until_ready

logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)
logging.getLogger("py4...").setLevel(logging.INFO)


class CytoscapeParser:
    """Class that serves as a parser for Cytoscapes cyREST API."""

    def __init__(self, CYTOSCAPE=None):
        self.CYTOSCAPE = CYTOSCAPE
        self.POSSIBLE_PROC_NAMES = {
            "Darwin": "javaapplicationstub",
            "Linux": "NA",
            "Windows": "NA",
        }
        self.CYTOSCAPE_INSTALLATION_PATHS = {
            "Darwin": "/Applications/Cytoscape_v3.9.1/cytoscape.sh",
            "Linux": "NA",  # TODO implement path to cytoscape.sh on Linux.
            "Windows": "NA",  # TODO implement path to cytoscape.bat on Windows.
        }
        self.SYSTEM = platform.system()
        self.PROC_NAME = self.POSSIBLE_PROC_NAMES[self.SYSTEM]
        self.URL = "http://127.0.0.1:1234"

        # Start Cytoscape, if it is not already running
        if self.CYTOSCAPE is None:
            # TODO Other versions of Cytoscape?
            if self.CYTOSCAPE_INSTALLATION_PATHS[self.SYSTEM] == "NA":
                raise Exception(f"Not yet implemented to work with {self.SYSTEM}.")
            self.CYTOSCAPE_INSTALLATION_PATHS[self.SYSTEM]
        self.pid = self.check_for_cytoscape()
        logging.debug(f"pid of Cytoscape is:{self.pid}")
        self.check_for_string_app()

    def check_for_cytoscape(self) -> Union[int, None]:
        """Will check whether cytoscape is already running, if not, it will setup path to cytoscape.sh/cytoscape.bat and execute it. Will return the process id of"""
        pid = get_pid_of_process(self.PROC_NAME)
        if pid is None:
            if not os.access(self.CYTOSCAPE, os.X_OK):
                raise Exception(
                    f"cytoscape.sh can not be found at given path:{self.CYTOSCAPE}"
                )
            pid = self.start_cytoscape()
        return pid

    def start_cytoscape(self) -> Union[int, None]:
        """Will start cytoscape as a subprocess and return the corresponding process id."""
        # Uses Java Version 11
        try:
            devnull = open(os.devnull, "wb")
            process = subprocess.Popen(
                self.CYTOSCAPE, stdout=devnull, stderr=devnull, start_new_session=True
            )
            pid = process.pid
            print("Cytoscape is booting!")
            wait_until_ready(url=self.URL)
            print(f"Cytoscape is booted! Pid is:{pid}")
            return pid
        except Exception as e:
            print(e)

        if platform.system() == "Windows":
            raise Exception("Not yes implemented to work with Windows.")
            # TODO How to start cytoscape with subprocess on windows if it is not running.
        return None

    def export_network(self, filename, network, **kwargs):
        """Export the current network."""
        column_names = p4c.get_table_column_names(network=network)
        if "stringdb::STRING style" in column_names:
            p4c.delete_table_column(column="stringdb::STRING style")
        if "stringdb::canonical name" in column_names:
            p4c.rename_table_column(
                column="stringdb::canonical name", new_name="uniprotid"
            )
        p4c.export_network(filename=filename, network=network, **kwargs)

    def get_networkx_network(self, network, **kwargs):
        return p4c.create_networkx_from_network(network)

    # FIXME: Does not work, they destroying it by using name_identifier to get SUIDs
    def export_table(self, network, **kwargs):
        all_node_names = p4c.get_all_nodes(network=network)
        all_edge_names = p4c.get_all_edges(network=network)

        node_table = {i: None for i, _ in enumerate(all_node_names)}
        edge_table = {i: None for i, _ in enumerate(all_edge_names)}

        node_columns = p4c.get_table_column_names(table="node", network=network)
        edge_columns = p4c.get_table_column_names(table="edge", network=network)
        for i, node in enumerate(node_table.keys()):
            row = {}
            for column in node_columns:
                row[column] = p4c.get_table_value("node", all_edge_names[i], column)
            node_table[i] = row
        for i, edge in enumerate(edge_table.keys()):
            row = {}
            for column in node_columns:
                row[column] = p4c.get_table_value("edge", all_edge_names[i], column)
            edge_table[i] = row
        return node_columns, edge_columns

    def exec_cmd(self, cmd_list) -> bool:
        """Executes a given command command."""
        cmd = " ".join(cmd_list)  # type: ignore
        wait_until_ready(url=self.URL)  # Waits until the REST API is ready to be used.
        try:
            p4c.commands.commands_run(cmd)
            logging.info(f"Executed command {cmd}.")
            return True
        except p4c.exceptions.CyError:  # type: ignore
            logging.warning(f"Error running command: {cmd}.")
        return False

    def close_cytoscape(self):
        # wait = input("Want to close Cytoscape?\n")
        # if wait == "y":
        os.kill(self.pid)

    def get_network_list(self):
        names = p4c.get_network_list()
        networks = {}
        for i, name in enumerate(names):
            networks[name] = p4c.get_network_suid(name)
        return networks

    def check_for_string_app(self):
        wait_until_ready(url=self.URL)
        if p4c.get_app_status("stringApp")["status"] != "Installed":
            print()
            raise Exception("StringApp is not installed!")
