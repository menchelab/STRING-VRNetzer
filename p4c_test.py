# exec(
#     requests.get(
#         "https://raw.githubusercontent.com/cytoscape/jupyter-bridge/master/client/p4c_init.py"
#     ).text
# )
# IPython.display.Javascript(_PY4CYTOSCAPE_BROWSER_CLIENT_JS)
import logging
import os
import platform
import shutil
import subprocess
import sys
from abc import ABC, abstractclassmethod
from dataclasses import dataclass
from enum import Enum, auto
from time import sleep
from typing import List, Optional, Union

import psutil
import py4cytoscape as p4c


class NetworkType(Enum):
    fullNetwork = auto
    pyhsicalSubnetwork = auto


class CytoscapeParser:
    def __init__(self, cytoscape=None):
        self.cytoscape = cytoscape
        # Start cytoscape, if it is not already running
        if self.cytoscape is None:
            print(self.check_for_cytoscape())
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
        print(self.cytoscape)
        try:
            self.cytoscape_proc = subprocess.Popen(
                f"{self.cytoscape}", stdout=subprocess.PIPE
            )
            print("Cytoscape started!")
            return self.cytoscape_proc.pid
        except Exception as e:
            print(e)

        if platform.system() == "Windows":
            raise Exception("Not yes implemented to work with Windows.")
            # TODO How to start cytoscape with subprocess on windows if it is not running.
        return None

    def export_network(self, filename):
        """Export the current network."""
        p4c.export_network(filename)


@dataclass
class StringCmd(ABC):
    network_type: str = None  # type: ignore
    cutoff: float = None  # type: ignore
    limit: int = None  # type: ignore
    species: str = None  # type: ignore
    taxonID: str = None  # type: ignore

    def __post_init__(self):
        self.verifications = {
            self.network_type: NetworkType.__dict__,
            self.cutoff: range(0, 1),
            self.limit: range(0, 100),
            self.species: [None],
            self.taxonID: [None],
        }
        self.cmd_list = [None]

    def verify(self) -> bool:
        # TODO Verify values
        for i, (value, boundaries) in enumerate(self.verifications.items()):
            if value is not None:
                if value not in boundaries:
                    variable = ""
                    for k, v in self.__dict__.items():
                        if value == v:
                            variable = k
                    raise ValueError(f"{variable} = {value} is not a valid!")
        return True

    def fetch_network(self) -> bool:
        """Fetch a network using the StringApp."""
        self.add_optional_attributes()
        cmd = " ".join(self.cmd_list)  # type: ignore
        try:
            p4c.commands.commands_run(cmd)
            return True
        except p4c.exceptions.CyError:  # type: ignore
            logging.warning(f"Error running command")
        return False

    def add_optional_attributes(self) -> None:
        """Adds additional attributes needed for the corresponding query."""
        for optional_atr in [self.cutoff, self.limit, self.species, self.taxonID]:
            if optional_atr is not None:
                self.cmd_list.append(f"{object(optional_atr).__name__}={optional_atr}")  # type: ignore


@dataclass
class StringDieseaseQuery(StringCmd):
    disease: str = None  # type: ignore

    def __post_init__(self):
        StringCmd.__post_init__(self)
        self.query_type = "disease query"
        if self.disease is None:
            raise ValueError("Please define a disease for the query!")
        self.verifications[
            self.disease
        ] = (
            []
        )  # TODO find boundaries or all allowed diseases or catch Errors from Query
        # self.verify()

    def get_cmd_list(self):
        """Creates the command which will be executed."""
        self.cmd_list.append(f"disease={self.disease}")  # type: ignore


@dataclass
class StringProteinQuery(StringCmd):
    query: List[str] = None  # type: ignore

    def __post_init__(self):
        StringCmd.__post_init__(self)
        self.query_type = "protein query"
        if self.query is None:
            raise ValueError("Please define proteins to query with!")

    def get_cmd_list(self):
        """Creates the command which will be executed."""
        self.cmd_list = ["string {disease query}", f"query={self.query}"]


if __name__ == "__main__":
    # pd.options.mode.chained_assignment = None
    # string_cmd_list = ["string disease query", 'disease="sadcer"', "cutoff=0.1"]
    # string_cmd = " ".join(string_cmd_list)
    # try:
    #     p4c.commands.commands_run(string_cmd)
    # except p4c.exceptions.CyError:
    #     print(f"Error running command")
    parser = CytoscapeParser()
    pass
    # p4c.export_network("./HIV-human PPI.sif")
    # cmd = StringDieseaseQuery(disease="cancer", network_type=NetworkType.pyhsicalSubnetwork)  # type: ignore
