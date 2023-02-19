from typing import Set, Tuple

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


class ScanProcess:
    def __init__(self, target_url: str):
        self.driver = uc.Chrome()
        self.urls_count = 0
        self.internal_urls = set()
        self.external_urls = set()
        self.target_url = target_url

    def create_sitemap(self, url: str, max_urls: int = 100) -> None:
        self.urls_count += 1
        if self.urls_count > max_urls:
            return
        links = self.get_links(url)
        for link in links:
            self.create_sitemap(link, max_urls=max_urls)

    def get_links(self, url: str) -> Set[str]:
        urls = set()
        domain_name = urlparse(url).netloc
        soup = BeautifulSoup(self.driver.get(url).page_source, 'html.parser')
        for a_tag in soup.findAll('a'):
            href = a_tag.attrs.get('href')
            if not href:
                continue
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            href = f'{parsed_href.scheme}://{parsed_href.netloc}{parsed_href.path}'
            if self.is_valid_url(href) and href not in self.internal_urls:
                urls.add(href)
                self.internal_urls.add(href)
            elif domain_name not in href and href not in self.external_urls:
                self.external_urls.add(href)
        return urls

    @staticmethod
    def is_valid_url(url: str) -> bool:
        parsed_url = urlparse(url)
        return bool(parsed_url.netloc) and bool(parsed_url.scheme)