__author__ = 'koslib'

#TODO: complete the crawling process description
"""
 The crawling process: to be completed
"""

from modules.fetch import Fetcher
from modules.frontier import Frontier

class Crawler:

    def __init__(self):
        pass

    def crawl(self):
        frontier = Frontier()
        loop = 0
        while len(frontier.load_frontier()) >= 1:
            loop += 1
            url = frontier.next_frontier_url()
            fetch = Fetcher(url)
            print "Loop: %s \nFRONTIER length: %s\nURL to occupy: %s\n============" % (loop, len(frontier.FRONTIER), url)


if __name__ == '__main__':
    crawler = Crawler()
    crawler.crawl()
