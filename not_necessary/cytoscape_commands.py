from abc import ABC


class AbstractCommand(ABC):
    cmd_list: list[str] = []
    arguments: list[str] = []

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

    def add_arguments(self, task) -> None:
        """Adds additional attributes needed for the corresponding query."""
        self.cmd_list.append(task)
        for arg in self.arguments:
            if arg is not None:
                arg_name = [i for i, a in self.__dict__.items() if a == arg][
                    0
                ]  # get the name of the variable as string.
                print(arg_name, arg)
                self.cmd_list.append(f"{arg_name}={arg}")
