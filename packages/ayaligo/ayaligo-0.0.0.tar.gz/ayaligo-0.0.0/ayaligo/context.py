from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from ayaligo.platforms import Board, Server
    from ayaligo.components import Component


class Context:
    _server: Optional["Server"] = None
    _boards: Dict[str, "Board"] = {}
    _components: Dict[str, "Component"] = {}

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def set_server(self, server: "Server"):
        self._server = server

    def get_server(self) -> Optional["Server"]:
        return self._server

    def add_board(self, board: "Board"):
        if board.id in self._boards.keys():
            raise ValueError(f"Board with name {board.id} already exists")
        self._boards[board.id] = board

    def get_board(self, name: str) -> Optional["Board"]:
        return self._boards.get(name)

    def get_boards(self) -> Dict[str, "Board"]:
        return self._boards

    def add_component(self, component: "Component"):
        if component.id in self._components.keys():
            raise ValueError(f"Component with name {component.id} already exists")
        self._components[component.id] = component

    def get_component(self, name: str) -> Optional["Component"]:
        return self._components.get(name)

    def get_components(self) -> Dict[str, "Component"]:
        return self._components
