import os

from cuckoo.messenger.gmail_sender import GmailSender

MAIL_RECEIVER = os.environ["MAIL_RECEIVER"]


def test_send():
    gm = GmailSender(MAIL_RECEIVER)
    gm.send("Hello, this is a test email from Cuckoo.")
