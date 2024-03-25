import os
import smtplib
from email.message import EmailMessage

from cuckoo.base import Messenger
from cuckoo.utils import SMTP_EMAIL, SMTP_PASSWORD, SMTP_PORT, SMTP_SERVER, SMTP_USER


class EmailSender(Messenger):
    def __init__(self, to_email: str) -> None:
        self.to_email = to_email
        self.from_email = os.environ[SMTP_EMAIL]
        self.user = os.environ[SMTP_USER]
        self.password = os.environ[SMTP_PASSWORD]
        self.smtp_server = os.environ[SMTP_SERVER]
        self.smtp_port = int(os.environ[SMTP_PORT])

    def send(self, text: str) -> None:
        self.send_email(text, text)

    def send_email(self, subject, body):
        # Create the MIME object
        message = EmailMessage()
        message.set_content(body)
        message["Subject"] = subject
        message["From"] = self.from_email
        message["To"] = self.to_email

        # Create an SMTP session
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.user, self.password)
            server.sendmail(self.from_email, self.to_email, message.as_string())
