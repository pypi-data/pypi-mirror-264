import warnings
from typing import Optional
from ayaligo.context import Context
from ayaligo.protocols import Protocol

warnings.warn("ayaligo is still in development and cannot be used.")

_context = Context()
_protocol: Optional[type[Protocol]] = None


def get_context() -> Context:
    return _context


def set_protocol(protocol: type[Protocol]) -> None:
    global _protocol
    _protocol = protocol
    for board in _context.get_boards().values():
        board.set_protocol(protocol)
