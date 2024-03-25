from typing import Tuple

from cuckoo.base import ConditionProcessor, Token
from cuckoo.processor.simple_processor import (
    EQUAL_PRICE,
    HIGH_PRICE,
    LOW_PRICE,
    WITHIN_PRICE,
    SimpleProcessor,
)

token_id = "AAA"
curr_price = 100
token = Token(token_id, curr_price)


def create(
    target_price: float, condition: SimpleProcessor.Condition
) -> ConditionProcessor:
    return SimpleProcessor(target_price, condition)


def exceed(
    target_price: float, condition: SimpleProcessor.Condition
) -> Tuple[bool, str]:
    return create(target_price, condition).exceed(token)


def test_over_price():
    target_price = 99
    b, t = exceed(target_price, SimpleProcessor.Condition.GREATER_THAN)
    assert b
    assert (
        t
        == f"{token_id.upper()} current price {curr_price} is {HIGH_PRICE} the set price {target_price}"
    )


def test_low_price():
    target_price = 101
    b, t = exceed(target_price, SimpleProcessor.Condition.LESS_THAN)
    assert b
    assert (
        t
        == f"{token_id.upper()} current price {curr_price} is {LOW_PRICE} the set price {target_price}"
    )


def test_equal_price():
    target_price = curr_price
    b, t = exceed(target_price, SimpleProcessor.Condition.LESS_OR_EQUAL)
    assert b
    assert (
        t
        == f"{token_id.upper()} current price {curr_price} is {EQUAL_PRICE} the set price {target_price}"
    )


def test_within_price():
    target_price = 101
    b, t = exceed(target_price, SimpleProcessor.Condition.GREATER_THAN)
    assert not b
    assert (
        t
        == f"{token_id.upper()} current price {curr_price} is {WITHIN_PRICE} the set price range"
    )
