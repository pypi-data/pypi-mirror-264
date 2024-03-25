from typing import List

from cuckoo.base import ConditionProcessor, Messenger, Observer, Subject
from cuckoo.handler.checker_handler import CheckerHandler
from cuckoo.processor.simple_processor import SimpleProcessor


class TokenTracker(Subject):
    def query(self) -> None:
        self.tokens = self.datasource.query()

    def get_processors(self, symbol: dict) -> List[ConditionProcessor]:
        processors: List[ConditionProcessor] = []
        for key, value in symbol.items():
            condition: SimpleProcessor.Condition | None = None
            match key:
                case "gte":
                    condition = SimpleProcessor.Condition.GREATER_OR_EQUAL
                case "gt":
                    condition = SimpleProcessor.Condition.GREATER_THAN
                case "lte":
                    condition = SimpleProcessor.Condition.LESS_OR_EQUAL
                case "lt":
                    condition = SimpleProcessor.Condition.LESS_THAN
                case _:
                    pass
            if isinstance(condition, SimpleProcessor.Condition):
                processors.append(SimpleProcessor(value, condition))

        return processors

    def get_price_checker(
        self, id: str, processors: List[ConditionProcessor], messengers: List[Messenger]
    ) -> List[Observer]:
        return [CheckerHandler(id, processor, messengers) for processor in processors]
