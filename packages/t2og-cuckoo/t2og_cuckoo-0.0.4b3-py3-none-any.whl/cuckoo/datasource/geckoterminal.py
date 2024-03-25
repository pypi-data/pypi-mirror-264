from typing import Dict, List

from cuckoo.base import DataSource, Token


class Geckoterminal(DataSource):
    class PoolInfo:
        def __init__(self, network: str, address: str, attribute: str) -> None:
            self.network = network
            self.address = address
            self.attribute = attribute

    # Datasource name
    name = "geckoterminal"
    # Query parameter
    pools: List[PoolInfo]

    def __init__(self, pools: List[PoolInfo]) -> None:
        super().__init__(Geckoterminal.name, 30)
        self.pools = pools

    def query(self) -> Dict[str, Token]:
        tokens = {}

        for pool in self.pools:
            response = self.request_helper.request(
                f"https://api.geckoterminal.com/api/v2/networks/{pool.network}/pools/{pool.address}"
            )
            attributes = response["data"]["attributes"]
            symbol = attributes["name"]
            value = float(attributes[pool.attribute])
            tokens[symbol] = Token(symbol, value)

        return tokens
