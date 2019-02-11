from bs4 import BeautifulSoup
from urllib.request import urlopen
from LanguageEngine.Summarizer import Gensim as gen

def scrapeDescription(item, wordCount = 30):
    """
    The description of the given item is scraped from wikipedia. Multiple
    paragraphs are run through a summarizer and the summary is returned

    Parameters
    ----------
    item : str
        the subject which has to be scraped
    wordCount : int
        The maximum number of words the summary should be

    Returns
    -------
    description : str
        The summarized description of the item
    """
    url = "https://www.bing.com/search?q=" + item.replace(" ", "+") + "+wikipedia"
    wikiLink = BeautifulSoup(urlopen(url), "lxml").find("ol", {"id": "b_results"}).find("li", {"class": "b_algo"}).find("a", href=True)['href']
    return gen.getSummaryFromURI(wikiLink, wordCount, 5)
