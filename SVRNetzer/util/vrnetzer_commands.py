from dataclasses import dataclass
from typing import Union

from cytoscape_commands import AbstractCommand


@dataclass
class VRNetzerAppCmd(AbstractCommand):
    """Abstract Class to build a VRNetzer command which can be executed using the CyREST API. CyRest API is accessed using the py4cytoscape package."""

    cmnd: Union[str, None] = None
    arguments: Union[dict, None] = None

    def __post_init__(self):
        self.cmd_list = ["vrnetzer"]


@dataclass
class VRNetzerAppExport(VRNetzerAppCmd):
    """Class to build a vrnetzer export command which can be executed using the CyREST API. CyRest API is accessed using the py4cytoscape package."""

    filename: str = None

    def __post_init__(self):
        VRNetzerAppCmd.__post_init__(self)
        self.command = "export"
        self.arguments = [self.filename]
        self.add_arguments(self.command)
