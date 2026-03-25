# main.py

from src.config.proxy import ProxyLoader


def main():
    proxy = ProxyLoader.load("data/proxy.json")

    print("HTTPX:", proxy.to_httpx())
    print("Playwright:", proxy.to_playwright())
    print("SOCKS5:", proxy.to_socks5())


if __name__ == "__main__":
    main()
