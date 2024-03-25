from typing import Dict, Tuple

from cuckoo.base import DataSource, Token
from cuckoo.utils import LOGGER


class Coingecko(DataSource):
    # Datasource name
    name = "coingecko"
    # Query parameter which is multiple address
    parameters: Tuple[str, ...]
    # The return currency of token
    currency: str = "usd"

    def __init__(self, *args: str) -> None:
        super().__init__(Coingecko.name, 30)
        self.parameters = args

    def query(self) -> Dict[str, Token]:
        tokens = {}
        token_ids = ",".join(self.parameters)
        response = self.request_helper.request(
            f"https://api.coingecko.com/api/v3/simple/price?ids={token_ids}&vs_currencies={self.currency}"
        )

        if response is None or len(response) == 0:
            LOGGER.warn(f"No {token_ids} data")
            return tokens

        for token_id in self.parameters:
            if token_id in response:
                token = Token(token_id, response[token_id][self.currency])
                tokens[token_id] = token
        return tokens
