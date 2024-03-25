import logging.config
import os
import re
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()
LOGGING_NAME = "cuckoo"
DEFAULT_REFRESH_MINUTES = 6
# ENV config
REFRESH_MINUTES = "REFRESH_MINUTES"
SMTP_SERVER = "SMTP_SERVER"
SMTP_PORT = "SMTP_PORT"
SMTP_USER = "SMTP_USER"
SMTP_PASSWORD = "SMTP_PASSWORD"
SMTP_EMAIL = "SMTP_EMAIL"
LOG_VERBOSE = "LOG_VERBOSE"
GMAIL_TOKEN = "GMAIL_TOKEN"
GMAIL_FROM = "GMAIL_FROM"
# Watchlist config
TOKENS = "tokens"
TOKEN_SYMBOL = "symbol"
TOKEN_SYMBOL_ID = "id"
TOKEN_POOL = "pool"
TOKEN_POOL_NETWORK = "network"
TOKEN_POOL_ADDRESS = "address"
TOKEN_POOL_NAME = "name"
TOKEN_POOL_ATTRIBUTE = "attribute"
DISPLAYS = "displays"
DISPLAY_CONSOLE = "console"
MESSENGERS = "messengers"
MESSENGER_CONSOLE = "console"
MESSENGER_MAIL = "mail"
MESSENGER_TELEGRAM = "telegram"


VERBOSE = str(os.getenv(LOG_VERBOSE, True)).lower() == "true"

INTERVAL_MINUTES = float(os.getenv(REFRESH_MINUTES, DEFAULT_REFRESH_MINUTES))

SUBSCRIPT_DIGITS = {
    0: "\u2080",
    1: "\u2081",
    2: "\u2082",
    3: "\u2083",
    4: "\u2084",
    5: "\u2085",
    6: "\u2086",
    7: "\u2087",
    8: "\u2088",
    9: "\u2089",
}


def set_logging(name=LOGGING_NAME, verbose=True):
    level = logging.INFO if verbose else logging.ERROR
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                name: {
                    "format": "%(asctime)s %(levelname)s:%(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                name: {
                    "class": "logging.StreamHandler",
                    "formatter": name,
                    "level": level,
                }
            },
            "loggers": {name: {"level": level, "handlers": [name], "propagate": False}},
        }
    )


# Set logger
set_logging(LOGGING_NAME, verbose=VERBOSE)
LOGGER = logging.getLogger(LOGGING_NAME)


def yaml_load(file="watchlist.yaml"):
    """
    Load YAML data from a file.

    Args:
        file (str, optional): File name. Default is 'watchlist.yaml'.

    Returns:
        (dict): YAML data and file name.
    """
    assert Path(file).suffix in (
        ".yaml",
        ".yml",
    ), f"Attempting to load non-YAML file {file} with yaml_load()"
    with open(file, errors="ignore", encoding="utf-8") as f:
        s = f.read()  # string

        # Remove special characters
        if not s.isprintable():
            s = re.sub(
                r"[^\x09\x0A\x0D\x20-\x7E\x85\xA0-\uD7FF\uE000-\uFFFD\U00010000-\U0010ffff]+",
                "",
                s,
            )

        # Add YAML filename to dict and return
        data = yaml.safe_load(s) or {}

        return data


def get_pretty_number(number: float) -> str:
    number_str = str(number)
    num = re.compile("([-+]?[\d]+)\.?([\d]*)[Ee]((?:[-+]?[\d]+)?)")
    match = re.match(num, number_str)
    if match:
        integer_part = match.group(1)
        decimal_part = match.group(2)
        power_value = int(match.group(3))
        if power_value > -6:
            precision = len(decimal_part) - int(power_value)
            return f"{number:.{precision}f}"

        return (
            f"0.0{SUBSCRIPT_DIGITS[abs(power_value + 1)]}{integer_part}{decimal_part}"
        )

    return number_str
