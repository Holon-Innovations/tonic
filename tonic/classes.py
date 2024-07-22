from datetime import datetime

class Bucket:
    def __init__(self, name: str, creation_date: datetime | None = None):
        self._name = name
        self._creation_date = creation_date

    @property
    def name(self) -> str:
        return self._name

    @property
    def creation_date(self) -> datetime | None:
        return self._creation_date

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self.name}')"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool | NotImplementedError:
        if isinstance(other, Bucket):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other
        return NotImplementedError

    def __hash__(self) -> int:
        return hash(self.name)

class Object:
    def __init__(self, name: str, creation_date: datetime | None = None):
        self._name = name
        self._creation_date = creation_date

    @property
    def name(self) -> str:
        return self._name

    @property
    def creation_date(self) -> datetime | None:
        return self._creation_date

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self.name}')"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool | NotImplementedError:
        if isinstance(other, Bucket):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other
        return NotImplementedError

    def __hash__(self) -> int:
        return hash(self.name)