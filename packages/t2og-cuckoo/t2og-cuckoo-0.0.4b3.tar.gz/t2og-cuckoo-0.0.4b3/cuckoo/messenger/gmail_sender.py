import base64
import os
from email.message import EmailMessage

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from cuckoo.base import Messenger
from cuckoo.utils import GMAIL_FROM, GMAIL_TOKEN, LOGGER

SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]


class GmailSender(Messenger):
    def __init__(self, to_email: str) -> None:
        self.to_email = to_email
        self.from_email = os.environ[GMAIL_FROM]
        self.api_token = os.environ[GMAIL_TOKEN]
        if os.path.exists(self.api_token):
            self.creds = Credentials.from_authorized_user_file(self.api_token, SCOPES)
        else:
            raise FileNotFoundError(
                f"Gmail authorized token file not found {os.path.abspath(self.api_token)}"
            )

    def send(self, text: str) -> None:
        self.send_email(text, text)

    def send_email(self, subject, body):
        try:
            # Create gmail api client
            service = build("gmail", "v1", credentials=self.creds)
            message = EmailMessage()
            message.set_content(body)
            message["To"] = self.to_email
            message["From"] = self.from_email
            message["Subject"] = subject

            # Encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {"raw": encoded_message}
            # pylint: disable=E1101
            send_message = (
                service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
            LOGGER.info(f'Message Id: {send_message["id"]}')
        except HttpError as error:
            LOGGER.error(f"An error occurred: {error}")
