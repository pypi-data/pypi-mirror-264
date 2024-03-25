import argparse
import os
import time
from typing import List, Tuple

from cuckoo.base import Messenger
from cuckoo.datasource.coingecko import Coingecko
from cuckoo.handler.checker_handler import CheckerHandler
from cuckoo.handler.handler_manager import HandlerManager
from cuckoo.handler.watcher_handler import WatcherHandler
from cuckoo.messenger.console_sender import ConsoleSender
from cuckoo.messenger.email_sender import EmailSender
from cuckoo.messenger.messenger_manager import MessengerManager
from cuckoo.processor.simple_processor import SimpleProcessor
from cuckoo.tracker.coingecko_tracker import CoingeckoTracker
from cuckoo.tracker.geckoterminal_tracker import GeckoterminalTracker
from cuckoo.tracker.token_tracker import TokenTracker
from cuckoo.utils import (DISPLAYS, INTERVAL_MINUTES, LOGGER, MESSENGERS,
                          TOKEN_POOL, TOKEN_SYMBOL, TOKENS, yaml_load)

HIGHER_PROCESSOR = "higher"
LOWER_PROCESSOR = "lower"


def get_watch_tokens(watch_tokens: str) -> Tuple[str, ...]:
    if isinstance(watch_tokens, str):
        tokens = [t for t in watch_tokens.split(",")]
    else:
        tokens = ["bitcoin"]
    return tuple(set(tokens))


def active_command_mode(args: dict):
    watch_tokens = args.pop("watch_tokens")
    check_token = args.pop("check_token")
    checker = args.pop("checker")
    target_price = args.pop("target_price")
    send_mail = args.pop("send_mail")
    LOGGER.info(f"Watch tokens: {watch_tokens}")
    LOGGER.info(f"Check token: {check_token}")
    LOGGER.info(f"Checker: {checker}")
    LOGGER.info(f"Target price: {target_price}")
    LOGGER.info(f"Send mail to: {send_mail}")

    # Setting up data source and tracker
    datasource = Coingecko(*watch_tokens.split(","))
    tracker = TokenTracker(datasource)
    LOGGER.info(f"Datasource: {tracker.get_datasource_name()}")

    # Register watcher handler
    watcher_handler = WatcherHandler()
    tracker.attach(watcher_handler)

    # Registering checker handler if check_token is provided
    if not check_token is None:
        if checker is None:
            raise ValueError("Missing checker value")
        if target_price is None:
            raise ValueError("Missing target value")

        # Creating processor based on checker type
        if HIGHER_PROCESSOR in checker:
            processor = SimpleProcessor(
                target_price, SimpleProcessor.Condition.GREATER_OR_EQUAL
            )
        elif LOWER_PROCESSOR in checker:
            processor = SimpleProcessor(
                target_price, SimpleProcessor.Condition.LESS_OR_EQUAL
            )
        else:
            raise ValueError(
                f"The checker value should be in {HIGHER_PROCESSOR},{LOWER_PROCESSOR}"
            )

        # Setting up messengers for notification
        messengers: List[Messenger] = [ConsoleSender()]
        if not send_mail is None:
            messengers.append(EmailSender(send_mail))

        # Registering checker handler
        checker_handler = CheckerHandler(check_token, processor, messengers)
        LOGGER.info(
            f"Setting {len(checker_handler.get_messengers())} Messenger: {checker_handler.get_messengers()}"
        )
        tracker.attach(checker_handler)

    LOGGER.info(
        f"Register {len(tracker.get_observers())} handlers: {tracker.get_observers()}"
    )

    while True:
        # Starting tracker
        tracker.fetch()
        time.sleep(INTERVAL_MINUTES * 60)


def active_config_mode(watchlist_config: str):
    if not os.path.exists(watchlist_config):
        raise FileNotFoundError(
            f"Watchlist config file not found {os.path.abspath(watchlist_config)}"
        )

    LOGGER.info(f"Watchlist config: {watchlist_config}")
    watchlist_data = yaml_load(watchlist_config)

    displays = HandlerManager.get_displays(
        [displays for displays in watchlist_data[DISPLAYS]]
    )

    messengers = MessengerManager.get_messengers(
        [messengers for messengers in watchlist_data[MESSENGERS]]
    )

    symbols = [
        token[TOKEN_SYMBOL] for token in watchlist_data[TOKENS] if TOKEN_SYMBOL in token
    ]

    pools = [pool[TOKEN_POOL] for pool in watchlist_data[TOKENS] if TOKEN_POOL in pool]

    # Initialize trackers based on available data
    trackers = []
    if len(symbols) > 0:
        trackers.append(CoingeckoTracker(symbols, displays, messengers))
    if len(pools) > 0:
        trackers.append(GeckoterminalTracker(pools, displays, messengers))

    while True:
        # Start fetching data from all trackers
        for tracker in trackers:
            tracker.fetch()

        time.sleep(INTERVAL_MINUTES * 60)


def cli():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--watchlist",
        type=str,
        default=None,
        help="optional to load watchlist configuration file",
    )
    parser.add_argument(
        "--watch_tokens",
        type=str,
        default="bitcoin",
        help="comma-separated list of token symbol",
    )
    parser.add_argument(
        "--check_token",
        type=str,
        default=None,
        help="optional to alert token price if the market price reaches your target price",
    )
    parser.add_argument(
        "--checker",
        type=str,
        default=None,
        choices=[HIGHER_PROCESSOR, LOWER_PROCESSOR],
        help="optional to set check type",
    )
    parser.add_argument(
        "--target_price", type=float, default=None, help="optional to set target price"
    )
    parser.add_argument(
        "--send_mail",
        type=str,
        default=None,
        help="optional to send message to user's mail",
    )
    args = parser.parse_args().__dict__

    watchlist_config = args.pop("watchlist")
    if watchlist_config:
        # Config Mode: Load watchlist configuration file
        active_config_mode(watchlist_config)
    else:
        # Command Line Mode: Execute based on command line arguments
        active_command_mode(args)


if __name__ == "__main__":
    cli()
