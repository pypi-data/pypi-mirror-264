import os
from typing import List

from cuckoo.base import Messenger
from cuckoo.messenger.console_sender import ConsoleSender
from cuckoo.messenger.email_sender import EmailSender
from cuckoo.messenger.gmail_sender import GmailSender
from cuckoo.utils import (
    GMAIL_FROM,
    LOGGER,
    MESSENGER_CONSOLE,
    MESSENGER_MAIL,
    SMTP_SERVER,
)


class MessengerManager:
    @staticmethod
    def get_messengers(messenger_items: List[dict]) -> List[Messenger]:
        """
        [{'console': None}, {'mail': ['abc@abc.com']}, {'telegram': []}]
        """
        def get_mail_sender(receiver: str) -> Messenger:
            smtp_server = os.getenv(SMTP_SERVER)
            gmail_from = os.getenv(GMAIL_FROM)
            if smtp_server:
                LOGGER.info(f"Using {smtp_server} to send mail")
                return EmailSender(receiver)
            elif gmail_from:
                LOGGER.info(f"Using the gmail {gmail_from} to send mail")
                return GmailSender(receiver)
            else:
                raise ValueError("Missing mail sender")

        messengers: List[Messenger] = []
        for item in messenger_items:
            if MESSENGER_CONSOLE in item:
                messengers.append(ConsoleSender())
            elif MESSENGER_MAIL in item:
                for value in item[MESSENGER_MAIL]:
                    messengers.append(get_mail_sender(value))
        return messengers
