from typing import Set
from urllib.parse import urljoin, urlparse

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
                'id': input_field.attrs.get('id', ''),
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
        page_source = BeautifulSoup(self.driver.page_source, 'html.parser')
        for a_tag in page_source.findAll('a'):
            href = a_tag.attrs.get('href')
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
        urljoin(self.target_url, form_info['action'])
        input_css_selector = ''
        for input in form_info['inputs']:
            input_id, input_name = input['id'], input['name']
            input_css_selector = f'input[name="{input_name}"], input[id="{input_id}"]'
            if input['type'] in ('text', 'search') and (input['id'] or input['name']):
                self.driver.find_element(By.CSS_SELECTOR, input_css_selector).send_keys(script)
        form_selector = f'form:has({input_css_selector})'
        self.driver.find_element(By.CSS_SELECTOR, form_selector).submit()

    def scan_reflected_xss(self):
        vulnerable_urls = []
        self.create_sitemap(self.target_url)
        scripts = ['<script>alert("XSS")</script>']
        for url in self.internal_urls:
            forms = self.get_page_forms(url)
            for form in forms:
                form_info = self.get_form_info(form)
                for script in scripts:
                    self.submit_form(form, form_info, script)
                    if script in self.driver.page_source:
                        vulnerable_urls.append(url)
                        break
        return vulnerable_urls


if __name__ == '__main__':
    scan = ScanProcess('http://testphp.vulnweb.com/')
    print(scan.scan_reflected_xss())
    print(1)
