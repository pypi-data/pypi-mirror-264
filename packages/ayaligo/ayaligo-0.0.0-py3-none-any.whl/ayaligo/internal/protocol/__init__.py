import abc


class Protocol(abc.ABC):

    def __repr__(self) -> str:
        return f"Protocol(name={self.get_name()!r})"

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        raise NotImplementedError
