from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Union


class NetworkType(Enum):
    fullNetwork = auto
    physicalSubnetwork = auto


@dataclass
class StringCmd(ABC):
    network_type: NetworkType = NetworkType.fullNetwork
    cutoff: Union[float, None] = None
    limit: Union[int, None] = None
    species: Union[str, None] = None
    taxonID: Union[str, None] = None

    def __post_init__(self):
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

    def add_arguments(self) -> None:
        """Adds additional attributes needed for the corresponding query."""
        self.cmd_list.append(self.query_type)
        for arg in self.arguments:
            if arg is not None:
                arg_name = [i for i, a in self.__dict__.items() if a == arg][
                    0
                ]  # get the name of the variable as string.
                self.cmd_list.append(f"{arg_name}={arg}")


@dataclass
class StringProteinQuery(StringCmd):
    query: Union[List[str], None] = None

    def __post_init__(self):
        StringCmd.__post_init__(self)
        self.query_type = "protein query"
        if self.query is None:
            raise ValueError("Please define proteins to query with!")
        self.arguments.append(self.query)
        self.add_arguments()


@dataclass
class StringDiseaseQuery(StringCmd):
    disease: str = None  # type: ignore

    def __post_init__(self):
        StringCmd.__post_init__(self)
        self.query_type = "disease query"
        if self.disease is None:
            raise ValueError("Please define a disease for the query!")
        self.arguments.append(self.disease)
        self.add_arguments()
