from typing import Set
from urllib.parse import urljoin, urlparse

import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


class ScanProcess:
    def __init__(self, target_url: str):
        self.driver = uc.Chrome()
        self.urls_count = 0
        self.internal_urls = set()
        self.external_urls = set()
        self.target_url = target_url

    @staticmethod
    def is_valid_url(url: str) -> bool:
        parsed_url = urlparse(url)
        return bool(parsed_url.netloc) and bool(parsed_url.scheme)

    @staticmethod
    def get_form_info(form):
        inputs = []
        for input_field in form.find_all('input'):
            inputs.append({
                'name': input_field.attrs.get('name', ''),
                'type': input_field.attrs.get('type', 'text'),
            })
        return {
            'inputs': inputs,
            'action': form.attrs.get('action', '').lower(),
            'method': form.attrs.get('method', 'get').lower(),
        }

    def get_links(self, url: str) -> Set[str]:
        urls = set()
        domain_name = urlparse(url).netloc
        self.driver.get(url)
        a_tags = self.driver.find_elements(By.CSS_SELECTOR, 'a')
        for a_tag in a_tags:
            href = a_tag.get_attribute('href')
            if not href:
                continue
            parsed_href = urlparse(urljoin(url, href))
            href = f'{parsed_href.scheme}://{parsed_href.netloc}{parsed_href.path}'
            if domain_name not in href:
                if href not in self.external_urls:
                    self.external_urls.add(href)
                continue
            elif self.is_valid_url(href) and href not in self.internal_urls:
                urls.add(href)
                self.internal_urls.add(href)
        return urls

    def create_sitemap(self, url: str, max_urls: int = 20) -> None:
        self.urls_count += 1
        if self.urls_count > max_urls:
            return
        links = self.get_links(url)
        for link in links:
            self.create_sitemap(link, max_urls=max_urls)

    def get_page_forms(self, url):
        self.driver.get(url)
        page_content = BeautifulSoup(self.driver.page_source, 'html.parser')
        return page_content.find_all('form')

    def submit_form(self, form, form_info, script):
        scan_url = urljoin(self.target_url, form_info['action'])
        data = {}
        for form_input in form_info['inputs']:
            if form_input['type'] in ('text', 'search') and form_input['name']:
                data[form_input['name']] = script
        if form_info['method'] == 'post':
            return requests.post(scan_url, data=data)
        return requests.get(scan_url, params=data)

    def scan_reflected_xss(self):
        vulnerable_urls = set()
        self.create_sitemap(self.target_url)
        scripts = [
            '<script>alert("XSS")</script>',
            '"><script>alert("xss")</script>',
            '"%3cscript%3ealert(document.cookie)%3c/script%3e',
        ]
        for url in self.internal_urls:
            page_forms = self.get_page_forms(url)
            for form in page_forms:
                form_info = self.get_form_info(form)
                for script in scripts:
                    submit_response = self.submit_form(form, form_info, script).content.decode()
                    if script in submit_response:
                        vulnerable_urls.add(url)
                        break
        return vulnerable_urls


if __name__ == '__main__':
    scan = ScanProcess('http://testphp.vulnweb.com/')
    print(scan.scan_reflected_xss())
