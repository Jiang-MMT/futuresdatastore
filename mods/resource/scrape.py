from selenium import webdriver
from bs4 import BeautifulSoup
import lxml
import csv


class Scraper():
    def __init__(self, url, selenium_query, bs_query):
        self.url = url
        self.browser = webdriver.Firefox()
        self.selenium_query = selenium_query
        self.bs_query = bs_query

    def render_js(self):
        self.browser.get(self.url)
        clicks = self.browser.find_elements_by_class_name(self.selenium_query)
        for item in clicks:
            item.click()
        html = self.browser.page_source
        return html

    def parse_data(self):
        html = self.render_js()
        soup = BeautifulSoup(html, 'lxml')
        results = soup.select(self.bs_query)
        with open('symbol.csv', 'wt') as f:
            cw = csv.writer(f)
            cw.writerow(('symbol', 'description', 'exchange', 'category'))

            for r in results:
                name = r.get_text()
                keys = r['href'].split('/')
                symbol = keys[-1][-2:]
                if keys[-2].startswith('ice'):
                    sub_keys = keys[-2][:-1].split('-')
                    exchange = (' '.join(sub_keys[0:2])).upper()
                    del sub_keys[0:2]
                    category = (' '.join(sub_keys)).upper()
                else:
                    sub_keys = keys[-2][:-1].split('-')
                    exchange = sub_keys[0].upper()
                    category = (' '.join(sub_keys[1:])).upper()
                cw.writerow((symbol, name, exchange, category))
        self.browser.quit()
