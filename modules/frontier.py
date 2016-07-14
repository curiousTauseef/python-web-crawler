__author__ = 'koslib'

import logging

class Frontier:

    FRONTIER = []
    INDEXED = []

    def __init__(self):
        link = "http://stanford.edu"
        self.FRONTIER.append(link)  # initialize frontier list

    def load_frontier(self):
        return self.FRONTIER

    def update_frontier(self, new_list):
        try:
            del new_list[0]
            self.FRONTIER = new_list
            self.remove_duplicates()
            return True
        except Exception, e:
            logging.error(e)
            return False

    def next_frontier_url(self):
        try:
            return self.FRONTIER[0]
        except Exception, e:
            logging.error(e)
            return None

    def remove_duplicates(self):
        seen = set()
        seen_add = seen.add
        return [x for x in self.FRONTIER if not (x in seen or seen_add(x))]

    def remove_url(self, url_to_be_removed):
        self.FRONTIER.remove(url_to_be_removed)

    def add_to_indexed(self, checksum):
        try:
            self.INDEXED.append(checksum)
        except Exception, e:
            logging.error(e)

    def load_indexed(self):
        return self.INDEXED

