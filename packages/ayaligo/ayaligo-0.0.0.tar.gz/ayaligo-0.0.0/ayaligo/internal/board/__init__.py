import abc
from typing import Set, Optional

from ayaligo import get_context
from ayaligo.frameworks import Framework
from ayaligo.protocols import Protocol
from ayaligo.components import Component


class Board(abc.ABC):

    def __init__(self, id: str) -> None:
        self.id: str = id
        self.framework: Optional[type[Framework]] = None
        self.protocol: Optional[type[Protocol]] = None
        self.components: Set[str] = set()
        get_context().add_board(self)

    def __repr__(self) -> str:
        return f"Board(id={self.id!r}, name={self.get_name()!r}, framework={self.framework.get_name() if self.framework else None!r}, protocol={self.protocol.get_name() if self.protocol else None!r}, components={self.components!r})"

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        raise NotImplementedError

    def set_framework(self, framework: type[Framework]) -> None:
        self.framework = framework

    def set_protocol(self, protocol: type[Protocol]) -> None:
        self.protocol = protocol

    def attach(self, component: Component) -> None:
        self.components.add(component.id)
        component.add_board(self.id)
