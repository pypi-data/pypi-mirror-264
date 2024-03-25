from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from cuckoo.utils.request_helper import RequestHelper


class Token:
    def __init__(self, symbol: str, price: float) -> None:
        self.symbol = symbol
        self.price = price


class DataSource(ABC):
    """
    Attributes:
        name: datasource's name
        rate: limit /min
    """

    def __init__(self, name: str, rate: int) -> None:
        self.name = name
        self.rate = rate
        self.request_helper = RequestHelper()

    def set_rate(self, rate) -> None:
        self.rate = rate

    @abstractmethod
    def query(self) -> Dict[str, Token]:
        pass


class Observer(ABC):
    @abstractmethod
    def update(self, subject: "Subject") -> None:
        pass


class Subject(ABC):
    tokens: Dict[str, Token]
    _observers: List[Observer]
    datasource: DataSource

    def __init__(self, datasource: DataSource, observers: List[Observer] = []) -> None:
        self.datasource = datasource
        self.tokens = {}
        self._observers = observers

    def fetch(self) -> None:
        self.query()
        if self.is_change():
            self.notify()

    def is_change(self) -> bool:
        return True

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def set_datasource(self, datasource: DataSource) -> None:
        self.datasource = datasource

    def get_datasource_name(self) -> str:
        return self.datasource.name

    def get_observers(self) -> List[Observer]:
        return self._observers

    @abstractmethod
    def query(self) -> None:
        pass


class Messenger(ABC):
    @abstractmethod
    def send(self, text: str) -> None:
        pass


class ConditionProcessor(ABC):
    @abstractmethod
    def stopped(self) -> bool:
        pass

    @abstractmethod
    def exceed(self, token: Token) -> Tuple[bool, str]:
        pass
