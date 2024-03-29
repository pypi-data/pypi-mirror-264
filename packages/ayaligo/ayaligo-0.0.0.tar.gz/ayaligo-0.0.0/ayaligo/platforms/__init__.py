from typing import Optional, Set

from ayaligo import get_context
from ayaligo.components import Component
from ayaligo.protocols import Protocol
from ayaligo.frameworks import Framework


class Server:

    def __init__(self, id: str) -> None:
        self.id: str = id
        self.framework: Optional[type[Framework]] = None
        self.protocol: Optional[type[Protocol]] = None
        self.components: Set[str] = set()
        get_context().set_server(self)

    def __repr__(self) -> str:
        return f"Server(id={self.id!r}, name={self.get_name()!r}, framework={self.framework.get_name() if self.framework else None!r}, protocol={self.protocol.get_name() if self.protocol else None!r}, components={self.components!r})"

    @classmethod
    def get_name(cls) -> str:
        return "Server"

    def set_framework(self, framework: type[Framework]) -> None:
        self.framework = framework

    def set_protocol(self, protocol: type[Protocol]) -> None:
        self.protocol = protocol

    def attach(self, component: Component) -> None:
        self.components.add(component.id)
        component.add_board(self.id)


from ayaligo.internal.board import Board as Board
