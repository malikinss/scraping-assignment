# src/config/proxy.py

import json
from pathlib import Path
from dataclasses import dataclass
from src.config.settings import settings


@dataclass
class ProxyCredentials:
    username: str
    password: str
    hostname: str
    http_port: int
    https_port: int
    socks5_port: int


class ProxyManager:
    def __init__(self):
        self.credentials = self._load()

    def _load(self) -> ProxyCredentials:
        path = Path(settings.proxy_file)

        if not path.exists():
            raise FileNotFoundError(f"Proxy file not found: {path}")

        with open(path, "r") as f:
            data = json.load(f)

        if "proxy" not in data:
            raise ValueError("Invalid proxy format")

        proxy = data["proxy"]

        return ProxyCredentials(
            username=proxy["username"],
            password=proxy["password"],
            hostname=proxy["hostname"].split(":")[0],
            http_port=proxy["port"]["http"],
            https_port=proxy["port"]["https"],
            socks5_port=proxy["port"]["socks5"],
        )

    def get_httpx_proxy(self) -> dict:
        creds = self.credentials
        url = f"http://{creds.username}:{creds.password}@{creds.hostname}"
        return {
            "http://": f"{url}:{creds.http_port}",
            "https://": f"{url}:{creds.https_port}",
        }

    def get_playwright_proxy(self) -> dict:
        creds = self.credentials
        return {
            "server": f"http://{creds.hostname}:{creds.http_port}",
            "username": creds.username,
            "password": creds.password,
        }


proxy_manager = ProxyManager()
