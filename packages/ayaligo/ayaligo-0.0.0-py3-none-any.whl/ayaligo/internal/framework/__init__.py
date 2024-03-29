import abc


class Framework(abc.ABC):

    def __repr__(self) -> str:
        return f"Framework(name={self.get_name()!r})"

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        raise NotImplementedError
