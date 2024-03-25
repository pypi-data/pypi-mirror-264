from cuckoo.base import Observer, Subject
from cuckoo.utils import LOGGER, get_pretty_number


class WatcherHandler(Observer):
    def update(self, subject: Subject) -> None:
        for _, token in subject.tokens.items():
            LOGGER.info(f"{token.symbol.upper()}: {get_pretty_number(token.price)}")
