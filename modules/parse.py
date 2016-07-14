__author__ = 'koslib'
from bs4 import BeautifulSoup
import re
import hashlib
import logging
import robotparser

from modules.frontier import Frontier


class Parser:

    def __init__(self, current_url, content):
        self.current_url = current_url
        self.content = content

    def parse(self):    # main parsing method to be called from Fetcher
        hashed = self.fingerprint()
        frontier_obj = Frontier()
        indexed_list = frontier_obj.load_indexed()
        if hashed not in indexed_list:
            frontier_obj.add_to_indexed(hashed)
            links = self.extract_links()
            self.update_frontier(links)
        else:
            links = self.extract_links()
            self.update_frontier(links)

    def extract_links(self):
        links_temp = []     # temporary links list
        links = []          # normalized links list
        soup = BeautifulSoup(self.content)
        for link in soup.findAll('a'):
            # for links_temp starting with "http://",
            # we should use soup.findAll('a', attrs={'href': re.compile("^http://")})
            link = link.get('href')
            links_temp.append(link)

        # normalize urls and make relative paths absolute
        links_temp = self.normalize_links(links_temp)
        for link in links_temp:
            try:
                if link not in links:   # do not insert duplicate
                    links.append(link)
            except Exception, e:
                logging.warning(e)
                pass

        return links

    def normalize_links(self, links):
        normalized_links = []
        try:
            for link in links:
                if link == "/" or link == "#":
                    continue
                if "http://" not in link and "https://" not in link:
                    link = "%s%s" % (self.current_url, link)
                    normalized_links.append(link)
                elif link is "http:///" or link is "https:///" \
                        or link is "http://#" or link is "https://#":
                    continue
                else:
                    normalized_links.append(link)
        except Exception, e:
            logging.warning(e)

        return normalized_links

    def update_frontier(self, links):
        frontier_obj = Frontier()
        frontier = frontier_obj.load_frontier()
        del frontier[0]     # remove item just indexed from frontier list

        # parse and respect robots
        rp = robotparser.RobotFileParser()
        rp.set_url("%s/robots.txt" % self.current_url)
        rp.read()

        for link in links:
            if link not in frontier:
                # be polite & respect robots
                if rp.can_fetch("*", link):
                    frontier.append(link)

        # finally update the frontier of this thread
        frontier_obj.update_frontier(frontier)

    def fingerprint(self):
        m = hashlib.md5()
        m.update(self.striped_html_content())
        print "Checksum: %s" % m.hexdigest()
        return m.hexdigest()

    def striped_html_content(self):
        p = re.compile(r'<.*?>')
        return str(p.sub('', self.content))

