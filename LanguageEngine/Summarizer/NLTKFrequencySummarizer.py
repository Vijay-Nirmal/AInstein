from FrequencySummarizer import FrequencySummarizer
from bs4 import BeautifulSoup
from urllib.request import urlopen
 
 
def getOnlyText(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return text

def GetWikiSummary(url, wordCount = 50):
    fs = FrequencySummarizer()
    return fs.summarize(str(getOnlyText(url)), word_count = wordCount)

def GetSummary(inputString, wordCount = 50):
    fs = FrequencySummarizer()
    return fs.summarize(inputString, word_count = wordCount)

if __name__ == '__main__':
    GetWikiSummary(GetWikiSummary("https://en.wikipedia.org/wiki/Deep_learning"))