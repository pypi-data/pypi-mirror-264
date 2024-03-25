from typing import List

from cuckoo.base import Messenger, Observer
from cuckoo.datasource.coingecko import Coingecko
from cuckoo.tracker.token_tracker import TokenTracker
from cuckoo.utils import TOKEN_SYMBOL_ID


class CoingeckoTracker(TokenTracker):

    def __init__(
        self, symbols: List[dict], displays: List[Observer], messengers: List[Messenger]
    ) -> None:
        """
        Initialize a CoingeckoTracker instance.

        Args:
            symbols: List of dictionaries representing token id.
                     Example: [{'id': 'token1', 'gte': 100, 'lt': 80}, {'id': 'token2', 'gt': 1.2, 'lte': 0.9}]
            displays: List of display observers to visualize data.
            messengers: List of messengers to alert the user when the price reaches the set conditions.
        """
        ids = []
        handlers: List[Observer] = []
        handlers.extend(displays)
        for symbol in symbols:
            id = symbol[TOKEN_SYMBOL_ID]
            ids.append(id)
            processors = self.get_processors(symbol)
            handlers.extend(self.get_price_checker(id, processors, messengers))

        super().__init__(Coingecko(*ids), handlers)
