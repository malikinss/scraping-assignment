# main.py

from src.config.proxy import ProxyLoader
from src.scrapers.http_scraper import HttpScraper


def main():
    proxy = ProxyLoader.load("data/proxy.json")
    scraper = HttpScraper(proxy)
    result = scraper.fetch("https://www.google.com")

    print(result)


if __name__ == "__main__":
    main()
