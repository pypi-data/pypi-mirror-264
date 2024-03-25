import os

from cuckoo.datasource.coingecko import Coingecko
from cuckoo.datasource.geckoterminal import Geckoterminal
from cuckoo.handler.checker_handler import CheckerHandler
from cuckoo.handler.watcher_handler import WatcherHandler
from cuckoo.messenger.console_sender import ConsoleSender
from cuckoo.messenger.email_sender import EmailSender
from cuckoo.processor.simple_processor import SimpleProcessor
from cuckoo.tracker.token_tracker import TokenTracker

watcher = WatcherHandler()


def get_messengers():
    messengers = []
    console_sender = ConsoleSender()
    messengers.append(console_sender)
    return messengers


def get_coingecko(_messengers):
    token1 = "bonk"
    crossing_up_price = 0.000030
    crossing_down_price = 0.000028
    token2 = "solana"

    datasource = Coingecko(token1, token2)
    tracker = TokenTracker(datasource)
    tracker.attach(watcher)

    high_processor = SimpleProcessor(
        crossing_up_price, SimpleProcessor.Condition.GREATER_OR_EQUAL
    )
    high_checker = CheckerHandler(token1, high_processor, _messengers)
    tracker.attach(high_checker)

    low_processor = SimpleProcessor(
        crossing_down_price, SimpleProcessor.Condition.LESS_OR_EQUAL
    )
    low_checker = CheckerHandler(token1, low_processor, _messengers)
    tracker.attach(low_checker)
    tracker.fetch()
    return tracker.tokens[token1].price, tracker.tokens[token2].price


def test_coingecko_with_mail():
    MAIL_RECEIVER = os.environ["MAIL_RECEIVER"]
    email_sender = EmailSender(MAIL_RECEIVER)

    messengers = get_messengers()
    messengers.append(email_sender)

    price1, price2 = get_coingecko(messengers)
    assert price1 and price2


def test_coingecko():
    messengers = get_messengers()

    price1, price2 = get_coingecko(messengers)
    assert price1 and price2


def get_pool_info(network: str, address: str, query_name: str):
    return Geckoterminal.PoolInfo(network, address, query_name)


def get_geckoterminal():
    pools = []

    pool_address1_name = "CRV / cvxCRV"
    crossing_up_price = 0.94
    crossing_down_price = 0.89
    pools.append(
        get_pool_info(
            "eth",
            "0x971add32ea87f10bd192671630be3be8a11b8623",
            "quote_token_price_base_token",
        )
    )

    pool_address2_name = "BONK / SOL"
    pools.append(
        get_pool_info(
            "solana",
            "3ne4mWqdYuNiYrYZC9TrA3FcfuFdErghH97vNPbjicr1",
            "base_token_price_usd",
        )
    )

    datasource = Geckoterminal(pools)
    tracker = TokenTracker(datasource)
    tracker.attach(watcher)

    messengers = get_messengers()

    high_processor = SimpleProcessor(
        crossing_up_price, SimpleProcessor.Condition.GREATER_OR_EQUAL
    )
    high_checker = CheckerHandler(pool_address1_name, high_processor, messengers)
    tracker.attach(high_checker)

    low_processor = SimpleProcessor(
        crossing_down_price, SimpleProcessor.Condition.LESS_OR_EQUAL
    )
    low_checker = CheckerHandler(pool_address1_name, low_processor, messengers)
    tracker.attach(low_checker)
    tracker.fetch()

    return (
        tracker.tokens[pool_address1_name].price,
        tracker.tokens[pool_address2_name].price,
    )


def test_geckoterminal():
    price1, price2 = get_geckoterminal()
    assert price1 and price2
