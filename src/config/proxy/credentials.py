# ./src/config/proxy/credentials.py
from .deps import dataclass


@dataclass
class ProxyCredentials:
    username: str
    password: str
    hostname: str
    http_port: int
    https_port: int
    socks5_port: int
