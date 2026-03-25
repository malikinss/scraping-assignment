# src/config/proxy.py

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProxyConfig:
    username: str
    password: str
    hostname: str
    http_port: int
    https_port: int
    socks5_port: int

    def to_httpx(self) -> dict:
        url = f"http://{self.username}:{self.password}@{self.hostname}"
        http_url = f"{url}:{self.http_port}"
        https_url = f"{url}:{self.https_port}"

        return {
            "http://": http_url,
            "https://": https_url,
        }

    def to_playwright(self) -> dict:
        return {
            "server": f"http://{self.hostname}:{self.http_port}",
            "username": self.username,
            "password": self.password,
        }

    def to_socks5(self) -> dict:
        return {
            "server": f"socks5://{self.hostname}:{self.socks5_port}",
            "username": self.username,
            "password": self.password,
        }


class ProxyLoader:
    @staticmethod
    def load(path: str = "data/proxy.json") -> ProxyConfig:
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Proxy file not found: {path}")

        with open(path, "r") as f:
            data = json.load(f)

        if "proxy" not in data:
            raise ValueError("Invalid proxy format")

        proxy = data["proxy"]

        config = None

        if proxy:
            config = ProxyConfig(
                username=proxy["username"],
                password=proxy["password"],
                hostname=proxy["hostname"].split(":")[0],
                http_port=proxy["port"]["http"],
                https_port=proxy["port"]["https"],
                socks5_port=proxy["port"]["socks5"],
            )

        return config
