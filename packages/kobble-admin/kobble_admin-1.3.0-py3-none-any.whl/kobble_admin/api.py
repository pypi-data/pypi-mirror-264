import urllib.parse
import requests
from typing import Any, Dict

SDK_SECRET_HEADER_NAME = "Kobble-Sdk-Secret"
SDK_USER_AGENT = "Kobble Python SDK/1.0"


class HttpClient:
    def __init__(self, secret: str, base_url: str):
        self.secret = secret
        self.base_url = base_url

    def _make_url(self, path: str) -> str:
        return urllib.parse.urljoin(self.base_url, path)

    def _make_base_headers(self) -> Dict[str, str]:
        headers = {}
        headers[SDK_SECRET_HEADER_NAME] = self.secret
        headers["User-Agent"] = SDK_USER_AGENT

        return headers

    def get_json(self, path: str, params={}) -> Any:
        url = self._make_url(path)
        headers = self._make_base_headers()
        res = requests.get(url, params, headers=headers)
        res.raise_for_status()

        return res.json()

    def post_json(self, path: str, data: Any) -> Any:
        url = self._make_url(path)
        headers = self._make_base_headers()
        res = requests.post(
            url=url, json=data, headers=headers)
        res.raise_for_status()

        return res.json()
