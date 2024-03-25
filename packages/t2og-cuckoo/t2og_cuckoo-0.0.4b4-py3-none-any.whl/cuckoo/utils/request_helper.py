import json
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from cuckoo.utils import LOGGER


class RequestHelper:
    def __init__(self, retries=3):
        self.request_timeout = 60
        self.session = requests.Session()
        retries = Retry(
            total=retries, backoff_factor=1, status_forcelist=[502, 503, 504]
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def request(self, url) -> Any:
        try:
            response = self.session.get(url, timeout=self.request_timeout)
        except requests.exceptions.RequestException as e:
            LOGGER.error(f"Request {url} error {e}")
            return

        try:
            response.raise_for_status()
            content = json.loads(response.content.decode("utf-8"))
            return content
        except Exception as e:
            LOGGER.error(f"Json load error {e}")
            return
