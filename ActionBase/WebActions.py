from bs4 import BeautifulSoup
from urllib.request import urlopen
from LanguageEngine.Summarizer import Gensim as gen

def scrapeDescription(item, wordCount = 30):
    url = "https://www.bing.com/search?q=" + item.replace(" ", "+") + "+wikipedia"
    wikiLink = BeautifulSoup(urlopen(url), "lxml").find("ol", {"id": "b_results"}).find("li", {"class": "b_algo"}).find("a", href=True)['href']
    return gen.getSummaryFromURI(wikiLink, wordCount, 5)
