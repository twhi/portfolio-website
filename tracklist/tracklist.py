from urllib.parse import urlparse
from lxml import etree
import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

class Tracklist:
    XPATH_TABLE = {
        'nts': {
            'xpath_track': '//li[@class="track"]',
            'xpath_artist': '//span[@class="track__artist"]',
            'xpath_title': '//span[@class="track__title"]',
            'method': 'requests'
        },
        'bbc': {
            'xpath_track': '//li[contains(@class, "segments-list__item")]',
            'xpath_artist': '//h3[@class="gamma no-margin"]/span[@class="artist"]',
            'xpath_title': '//p[@class="no-margin"]/span',
            'method': 'selenium'
        }
    }

    def __init__(self, url):
        self.url = url
        self.website = urlparse(url).hostname.split('.')[1]
        self.xpath = self._xpath_lookup()
        self.raw_html = self._get_data_from_web()
        self.tree = etree.HTML(self.raw_html)
        self.tracklist = []

    def _xpath_lookup(self):
        if self.website in self.XPATH_TABLE:
            return self.XPATH_TABLE[self.website]
        return None

    def _get_data_from_web(self):
        if self.xpath['method'] == 'requests':
            return self._requests_get(self.url)
        elif self.xpath['method'] == 'selenium':
            return self._selenium_get(self.url)

    def get_element_by_type(self, root, elem_type):
        return root.xpath(self.XPATH_TABLE[self.website]['xpath_' + elem_type])

    def construct_tracklist(self):
        tracks = self.get_element_by_type(self.tree, 'track')

        for track in tracks:
            track_dict = {}
            t = etree.HTML(etree.tostring(track))
            artist = self.get_element_by_type(t, 'artist')
            title = self.get_element_by_type(t, 'title')
            track_dict['artist'] = self.extract_element_text(artist)
            track_dict['title'] = self.extract_element_text(title)
            self.tracklist.append(track_dict)

        return self.tracklist

    @staticmethod
    def extract_element_text(elem):
        return [l.text for l in elem]

    @staticmethod
    def _requests_get(u):
        session = requests.Session()
        try:
            return session.get(u).text
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def _selenium_get(u):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get(u)
            page_source = driver.page_source
        except Exception as e:
            print(e)
            page_source = None
        driver.quit()
        return page_source
