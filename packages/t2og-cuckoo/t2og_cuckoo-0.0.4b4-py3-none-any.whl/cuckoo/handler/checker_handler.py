from typing import List

from cuckoo.base import ConditionProcessor, Messenger, Observer, Subject


class CheckerHandler(Observer):
    def __init__(
        self,
        symbol: str,
        processor: ConditionProcessor,
        messengers: List[Messenger],
    ) -> None:
        self.symbol = symbol
        self.processor = processor
        self.messengers = messengers

    def add(self, messenger: Messenger):
        self.messengers.append(messenger)

    def remove(self, messenger: Messenger):
        self.messengers.remove(messenger)

    def get_messengers(self) -> List[Messenger]:
        return self.messengers

    def update(self, subject: Subject) -> None:
        if self.symbol in subject.tokens:
            # Check price is out of range
            exceed, tips = self.processor.exceed(subject.tokens[self.symbol])
            if exceed:
                for m in self.messengers:
                    m.send(tips)
                # Check if it is necessary to continue reporting
                if self.processor.stopped():
                    subject.detach(self)
                    return
