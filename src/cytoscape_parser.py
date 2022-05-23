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
import timeit
from time import sleep, time
from typing import Union

import psutil
import py4cytoscape as p4c
import requests
from requests.exceptions import ConnectionError


def wait_until_ready(time_limit=30):
    response = requests.Response()
    start = time()
    while response.status_code != 200:
        try:
            response = requests.get("http://127.0.0.1:1234")
        except ConnectionError:
            pass
        if time() - start > time_limit:
            raise TimeoutError
        sleep(1)


class CytoscapeParser:
    """Class that serves as a parser for Cytoscapes cyREST API."""

    def __init__(self, cytoscape=None):
        self.cytoscape = cytoscape
        # Start cytoscape, if it is not already running
        if self.cytoscape is None:
            pid = self.check_for_cytoscape()
            logging.debug(f"pid of Cytoscape is:{pid}")
        # self.networks_names = p4c.get_network_list()

    def check_for_cytoscape(self) -> Union[int, None]:
        """Will check whether cytoscape is already running, if not, it will setup path to cytoscape.sh/cytoscape.bat and execute it. Will return the process id of"""
        processes = [proc for proc in psutil.process_iter()]
        procs = {"Darwin": "javaapplicationstub", "Linux": "NA", "Windows": "NA"}
        system = platform.system()
        pid = None
        for p in processes:
            if p.name().lower() == procs[system]:
                pid = p.pid
        if pid is None:
            paths = {
                "Darwin": "/Applications/Cytoscape_v3.9.1/cytoscape.sh",
                "Linux": "NA",  # TODO implement path to cytoscape.sh on Linux.
                "Windows": "NA",  # TODO implement path to cytoscape.bat on Windows.
            }
            # TODO Other versions of Cytoscape?
            if paths[system] == "NA":
                raise Exception(f"Not yet implemented to work with {system}.")

            self.cytoscape = paths[system]
            if not os.access(self.cytoscape, os.X_OK):
                raise Exception(
                    f"cytoscape.sh can not be found at given path:{self.cytoscape}"
                )
            pid = self.start_cytoscape()
        return pid

    def start_cytoscape(self) -> Union[int, None]:
        """Will start cytoscape as a subprocess and return the corresponding process id."""
        # Uses Java Version 11
        try:
            self.cytoscape_proc = subprocess.Popen(
                f"{self.cytoscape}", stdout=subprocess.PIPE
            )
            print("Cytoscape is booting!")
            print(self.cytoscape_proc.pid)
            return self.cytoscape_proc.pid
        except Exception as e:
            print(e)

        if platform.system() == "Windows":
            raise Exception("Not yes implemented to work with Windows.")
            # TODO How to start cytoscape with subprocess on windows if it is not running.
        return None

    def export_network(self, filename, **kwargs):
        """Export the current network."""
        p4c.export_network(filename=filename, **kwargs)

    def exec_cmd(self, cmd_list) -> bool:
        """Executes a given command command."""
        cmd = " ".join(cmd_list)  # type: ignore
        wait_until_ready()  # Waits until the REST API is ready to be used.
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
