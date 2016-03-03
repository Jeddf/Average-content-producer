from bs4 import BeautifulSoup

from ParserBase import Parser


class ViceRSS(Parser):    # Vice Class tailored for vice.com/rss, typically returns 50 latest.

    def article_split(self):
        items = self.soup.find_all('item')
        self.articles = []
        for n, i in enumerate(items):
            i = str(i)
            soop = BeautifulSoup(i, "xml")
            self.articles.append({})
            self.articles[n]['title'] = soop.title.string
            self.articles[n]['href'] = soop.link.string
            try:
                self.articles[n]['date'] = soop.pubdate.string
            except AttributeError:
                self.articles[n]['date'] = soop.pubDate.string
            t = soop.encoded.string
            s = BeautifulSoup(t, "html")
            self.articles[n]['text'] = s.get_text(" ", strip=True)
