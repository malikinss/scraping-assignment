# main.py

from src.config.proxy import ProxyLoader
from src.scrapers.http_scraper import HttpScraper
from src.scrapers.browser_scraper import BrowserScraper

WEB_SITE_URL = "https://www.google.com"


def main():
    proxy = ProxyLoader.load("data/proxy.json")

    httpx_scraper = HttpScraper(proxy)
    httpx_scraper_result = httpx_scraper.fetch(WEB_SITE_URL)
    print(httpx_scraper_result)

    browser_scraper = BrowserScraper()
    browser_scraper_result = browser_scraper.fetch(WEB_SITE_URL)
    print(browser_scraper_result)


if __name__ == "__main__":
    main()
