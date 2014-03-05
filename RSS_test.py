import unittest
from RSSFeed import RSSobject

class RSSTester(unittest.TestCase):
    def setUp(self):
        self.RSS = RSSobject('http://feeds.bbci.co.uk/news/rss.xml')
    def rss_raw_page_test(self):
        assert '<?xml' in self.RSS.raw
