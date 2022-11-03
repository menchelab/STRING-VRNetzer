from dataclasses import dataclass
from enum import Enum, auto
from typing import Union

from .cytoscape_commands import AbstractCommand


class NetworkType(Enum):
    fullNetwork = auto
    physicalSubnetwork = auto


@dataclass
class StringCmd(AbstractCommand):
    """Abstract Class to build a string command which can be executed using the CyREST API. CyRest API is accessed using the py4cytoscape package."""

    network_type: NetworkType = NetworkType.fullNetwork
    cutoff: Union[float, None] = None
    limit: Union[int, None] = None
    species: Union[str, None] = None
    taxonID: Union[str, None] = None

    def __post_init__(self) -> None:
        # self.verifications = {
        #     self.network_type: NetworkType.__dict__,
        #     self.cutoff: range(0, 1),
        #     self.limit: range(0, 100),
        #     self.species: [None],
        #     self.taxonID: [None],
        # }
        self.cmd_list = ["string"]
        self.query_type = "NA"
        self.arguments = [self.cutoff, self.limit, self.species, self.taxonID]


@dataclass
class StringProteinQuery(StringCmd):
    """Class to build a string protein query command which can be executed using the CyREST API. CyRest API is accessed using the py4cytoscape package."""

    query: Union[list[str], None] = None

    def __post_init__(self) -> None:
        StringCmd.__post_init__(self)
        self.query_type = "protein query"
        if self.query is None:
            raise ValueError("Please define proteins to query with!")
        self.arguments.append(self.query)
        self.add_arguments(self.query_type)


@dataclass
class StringDiseaseQuery(StringCmd):
    """Class to build a string disease query command which can be executed using the CyREST API. CyRest API is accessed using the py4cytoscape package."""

    disease: str = None  # type: ignore

    def __post_init__(self) -> None:
        StringCmd.__post_init__(self)
        self.query_type = "disease query"
        if self.disease is None:
            raise ValueError("Please define a disease for the query!")
        self.arguments.append(self.disease)
        self.add_arguments(self.query_type)


@dataclass
class StringCompoundQuery(StringCmd):
    """Class to build a string compound query command which can be executed using the CyREST API. CyRest API is accessed using the py4cytoscape package."""

    query: str = None  # type: ignore

    def __post_init__(self) -> None:
        StringCmd.__post_init__(self)
        self.query_type = "compound query"
        if self.query is None:
            raise ValueError("Please define a compounds/proteins for the query!")
        self.arguments.append(self.query)
        self.add_arguments(self.query_type)


@dataclass
class StringPubMedQuery(StringCmd):
    """Class to build a string compound query command which can be executed using the CyREST API. CyRest API is accessed using the py4cytoscape package."""

    pubmed: str = None  # type: ignore

    def __post_init__(self) -> None:
        StringCmd.__post_init__(self)
        self.query_type = "pubmed query"
        if self.pubmed is None:
            raise ValueError("Please define a compounds/proteins for the query!")
        self.arguments.append(self.pubmed)
        self.add_arguments(self.query_type)
