from cuckoo.base import Messenger
from cuckoo.utils import LOGGER


class ConsoleSender(Messenger):
    def send(self, text: str) -> None:
        LOGGER.info(text)
