import abc
from typing import Set

from ayaligo import get_context


class Component(abc.ABC):

    def __init__(self, id: str) -> None:
        self.id = id
        """
        Unique identifier of the component.
        """
        self.boards: Set[str] = set()
        """
        Set of board identifiers where the component is connected.
        """
        get_context().add_component(self)

    def __repr__(self) -> str:
        return f"Component(id={self.id!r}, name={self.get_name()!r}, boards={self.boards!r})"

    def add_board(self, board: str) -> None:
        self.boards.add(board)

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def extract(self):
        raise NotImplementedError
