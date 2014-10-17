from urllib.request import urlopen
import re

from bs4 import BeautifulSoup

from ParserBase import Parser


class BBCRSSUK(Parser):   # BBC class tailored for feeds.bbci.co.uk/news/rss.xml?edition=uk, returns 60-70 latest.

    def article_split(self):
        hinks = self.soup.find_all('link')
        bad = re.compile(r'(/news/\d|ws/in-pictures)')
        good = re.compile(r'ws/\S')
        links = []
        while hinks:
            a = hinks.pop()
            a = a.string
            try:
                a = a.partition('#')[0]
            except AttributeError:
                break
            a = a.replace('//www.', '//m.')  # Specify mobile version to minimise bandwidth
            if bad.search(a):
                continue
            elif good.search(a):
                links.append(a)
        self.articles = []
        for n, href in enumerate(links):
            rawpage = urlopen(href)
            page = rawpage.read()
            self.articles.append(self.page_parse(page))
            self.articles[n]['href'] = href

    def page_parse(self, page):  # Extracts the meat from BBC article pages
        p = BeautifulSoup(page)
        article = {'title': p.h1.get_text()}
        if p.find(class_="date"):
            article['date'] = p.find(class_="date").get_text().strip()[0:11]
        else:
            article['date'] = " "
        d = p.find(class_='map-body')  # deal with various possible page structures.
        e = p.find(class_='story-inner')
        f = p.find(class_='story-body')
        g = p.find(class_='picture-gallery')
        if f:
            tex = f.find_all('p') + f.find_all('ul')
        elif d:
            tex = d.find_all('p') + e.find_all('ul')
        elif e:
            tex = e.find_all('p') + e.find_all('ul')
        elif g:
            tex = g.find_all('p')
        article['text'] = ""
        for h in tex:
            try:
                if 'date' in h['class']:
                    continue
            except KeyError:
                pass
            article['text'] += " " + h.get_text()
        return article