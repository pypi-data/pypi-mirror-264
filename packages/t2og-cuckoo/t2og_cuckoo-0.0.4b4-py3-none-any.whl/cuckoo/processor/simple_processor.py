from enum import Enum, auto
from typing import Tuple

from cuckoo.base import ConditionProcessor, Token
from cuckoo.utils import get_pretty_number

HIGH_PRICE = "higher than"
LOW_PRICE = "lower than"
EQUAL_PRICE = "equal to"
WITHIN_PRICE = "within"


class SimpleProcessor(ConditionProcessor):
    class Condition(Enum):
        GREATER_THAN = auto()
        LESS_THAN = auto()
        GREATER_OR_EQUAL = auto()
        LESS_OR_EQUAL = auto()

    def __init__(self, target_value: float, condition: Condition) -> None:
        self.target_value = target_value
        self.condition = condition
        self.is_stopped = False

    def stopped(self) -> bool:
        return self.is_stopped

    def exceed(self, token: Token) -> Tuple[bool, str]:
        token_price = get_pretty_number(token.price)
        target_price = get_pretty_number(self.target_value)

        if self.condition in [
            SimpleProcessor.Condition.GREATER_THAN,
            SimpleProcessor.Condition.GREATER_OR_EQUAL,
        ]:
            if token.price >= self.target_value:
                self.is_stopped = True
                return (
                    True,
                    f"{token.symbol.upper()} {HIGH_PRICE if token.price > self.target_value else EQUAL_PRICE} {target_price}, now at {token_price}",
                )
        elif self.condition in [
            SimpleProcessor.Condition.LESS_THAN,
            SimpleProcessor.Condition.LESS_OR_EQUAL,
        ]:
            if token.price <= self.target_value:
                self.is_stopped = True
                return (
                    True,
                    f"{token.symbol.upper()} {LOW_PRICE if token.price < self.target_value else EQUAL_PRICE} {target_price}, now at {token_price}",
                )

        return (
            False,
            f"{token.symbol.upper()} {WITHIN_PRICE} the set price range, now at {token_price}",
        )
