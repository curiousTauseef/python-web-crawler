__author__ = 'koslib'
import requests
import logging

from modules.parse import Parser
from modules.frontier import Frontier

class Fetcher:

    def __init__(self, url):
        self.url = url
        self.get_content()

    def dns_check(self):
        try:
            r = requests.get(self.url)
            if r.status_code == requests.codes.ok:
                return True
            else:
                frontier = Frontier()
                logging.error("Could not fetch url %s" % self.url)
                frontier.remove_url(self.url)
                pass
        except Exception, e:
            logging.error("Exception occurred: %s" % e)
            pass
        return False

    def fetch(self):
        try:
            r = requests.get(self.url)
            r.links.viewitems()
            content = r.text
        except Exception, e:
            logging.error(e)
            content = None

        return content

    def fetch_html(self):
        try:
            r = requests.get(self.url)
            html = r.content
        except Exception, e:
            logging.error(e)
            html = None
        return html

    def get_content(self):
        try:
            if self.dns_check():
                content = self.fetch()
                html = self.fetch_html()

                # fire up the parser after exiting fetching module
                parser = Parser(self.url, html)
                parser.parse()

                # return content, html
            else:
                # return None, None
                logging.warning("DNS Check failed in get_content() method on url %s" % self.url)
                pass
        except Exception, e:
            logging.warning(e)
