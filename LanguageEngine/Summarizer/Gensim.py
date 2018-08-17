import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

def removeRefNo(inputString):
    return re.sub(r"[\(\[].*?[\)\]]", "", inputString)
 
def getOnlyText(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return text

def GetWikiSummary(url, wordCount = 50):
    return removeRefNo(summarize(str(getOnlyText(url)), word_count = wordCount))

def GetSummary(inputString, wordCount = 50):
    return removeRefNo(summarize(inputString, word_count = wordCount))

if __name__ == '__main__':
    print(GetWikiSummary("https://en.wikipedia.org/wiki/Machine_learning"))