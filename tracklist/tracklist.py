from urllib.parse import urlparse
from lxml import etree
import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
# from utils import errors
try:
    from .utils.exceptions import WebsiteNotSupportedError, InvalidUrlError, NoTracklistError
except ImportError:
    from utils.exceptions import WebsiteNotSupportedError, InvalidUrlError, NoTracklistError


class Tracklist:
    XPATH_TABLE = {
        'nts': {
            'xpath_track': '//li[@class="track"]',
            'xpath_artist': '//span[@class="track__artist"]',
            'xpath_title': '//span[@class="track__title"]',
            'method': 'requests',
            'name': 'NTS Radio',
        },
        'bbc': {
            'xpath_track': '//li[contains(@class, "segments-list__item--music")]',
            'xpath_artist': '//*[@class="gamma no-margin"]/span[@class="artist"]',
            'xpath_title': '//p[@class="no-margin"]/span',
            'method': 'requests',
            'name': 'BBC iPlayer Radio',
        },
        'mixesdb': {
            'xpath_track': '//li[contains(@class,"aff-api-done")]',
            'xpath_artist': '//span//@data-keywordsartist',
            'xpath_title': '//span//@data-keywordstitle',
            'method': 'selenium',
            'name': 'MixesDB',
        }
    }

    def __init__(self, url):
        self.url = url
        self.website = urlparse(url).hostname.split('.')[1]
        self.xpath = self._xpath_lookup()

        if not self.xpath:
            u = self.url
            raise WebsiteNotSupportedError(u)

        self.raw_html = self._get_data_from_web()

        if not self.raw_html:
            u = self.url
            raise InvalidUrlError(u)

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
        el = root.xpath(self.XPATH_TABLE[self.website]['xpath_' + elem_type])
        if len(el) == 0:
            return None
        return el

    def construct_tracklist(self):
        tracks = self.get_element_by_type(self.tree, 'track')

        if not tracks:
            u = self.url
            raise NoTracklistError(u)

        for track in tracks:
            track_dict = {}
            t = etree.HTML(etree.tostring(track))
            artist = self.get_element_by_type(t, 'artist')
            title = self.get_element_by_type(t, 'title')

            if not artist or not title:
                continue

            track_dict['artist'] = self.remove_duplicates_from_list(self.extract_element_text(artist))
            print(track_dict['artist'])
            track_dict['title'] = self.remove_duplicates_from_list(self.extract_element_text(title))
            self.tracklist.append(track_dict)

        return self.tracklist


    @staticmethod
    def remove_duplicates_from_list(l):
        return list(dict.fromkeys(l))

    @staticmethod
    def extract_element_text(elem):
        try:
            return [l.text for l in elem]
        except:
            return elem

    def _requests_get(self, u):
        self.session = requests.Session()
        try:
            return self.session.get(u).text
        except Exception as e:
            print(e)
            return None

    def _selenium_get(self, u):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)
        try:
            self.driver.get(u)
            page_source = self.driver.page_source
        except Exception as e:
            print(e)
            page_source = None
        self.driver.quit()
        return page_source


if __name__ == '__main__':

    tl = Tracklist('https://www.bbc.couoiuiouiuiouuiouiuiuiuiuiuio.uk/programmes/m0007b6z')
    t = tl.construct_tracklist()

    ender = True
