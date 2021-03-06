import re
from urllib.request import urlopen

from bs4 import BeautifulSoup

from .ParserBase import Parser

def removeShares(element):
    shareRow = element.find(class_='with-extracted-share-icons')
    if (shareRow):
        shareRow.extract()
    shareTools = element.find(class_='share-tools--no-event-tag')
    if (shareTools):
        shareTools.extract()
    return element

class BBCRSS(Parser):   # BBC class tailored for feeds.bbci.co.uk/news/rss.xml?edition=uk, returns 60-70 latest.

    def article_split(self):
        links = self.soup.find_all('link')
        badPattern = re.compile(r'(/news/\d|ws/in-pictures)')
        goodPattern = re.compile(r'ws/\S')
        hrefs = []
        while links:
            link = links.pop()
            link = link.string
            try:
                link = link.partition('#')[0]
            except AttributeError:
                break
            if badPattern.search(link):
                continue
            elif goodPattern.search(link):
                hrefs.append(link)
        self.articles = []
        for index, href in enumerate(hrefs):
            rawpage = urlopen(href)
            page = rawpage.read()
            self.articles.append(self.pageParse(page))
            self.articles[index]['href'] = href

    def pageParse(self, page):  # Extracts the meat from BBC article pages
        pageSoup = BeautifulSoup(page)
        pageSoup = removeShares(pageSoup)
        article = dict()
        article['title'] = pageSoup.h1.get_text()
        if pageSoup.find(class_="date"):
            article['date'] = pageSoup.find(class_="date").get_text().strip()[0:11]
        else:
            article['date'] = " "
        mapBody = pageSoup.find(class_='map-body')  # deal with various possible page structures.
        storyInner = pageSoup.find(class_='story-inner')
        storyBody = pageSoup.find(class_='story-body')
        pictureGallery = pageSoup.find(class_='picture-gallery')
        textElements = dict()
        if storyBody:
            textElements = storyBody.find_all('p') + storyBody.find_all('ul')
        elif mapBody:
            textElements = mapBody.find_all('p') + storyInner.find_all('ul')
        elif storyInner:
            textElements = storyInner.find_all('p') + storyInner.find_all('ul')
        elif pictureGallery:
            textElements = pictureGallery.find_all('p')
        article['text'] = ""
        for textElement in textElements:
            try:
                if 'off-screen' in textElement['class']:
                    continue
                if 'date' in textElement['class']:
                    continue
                if 'twite__channel-text' in textElement['class']:
                    continue
                if 'twite__title' in textElement['class']:
                    continue
                if 'twite__copy-text' in textElement['class']:
                    continue
                if 'share__title' in textElement['class']:
                    continue
                if 'twite__new-window' in textElement['class']:
                    continue
            except KeyError:
                pass
            article['text'] += " " + textElement.get_text()
        return article
