from bs4 import BeautifulSoup
from urllib.request import urlopen
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import re

def removeRefNo(inputString):
    return re.sub(r"[\[].*?[\]]", "", inputString)

def rank(ranking, n):
    """ return the first n sentences with highest ranking

    """

    return nlargest(n, ranking, key=ranking.get)

def computeFrequencies(wordSent, minCut, maxCut):
    """ 
      Compute the frequency of each of word.
      Input: 
       word_sent, a list of sentences already tokenized.
      Output: 
       freq, a dictionary where freq[w] is the frequency of w.
    """

    stopwordsSet = set(stopwords.words('english') + list(punctuation))
    freq = defaultdict(int)
    for s in wordSent:
        for word in s:
            if word not in stopwordsSet:
                freq[word] += 1
    # frequencies normalization and fitering
    m = float(max(freq.values()))
    keyIterator = list(freq.keys())
    for w in keyIterator:
        freq[w] = freq[w]/m
        if freq[w] >= maxCut or freq[w] <= minCut:
            del freq[w]
    return freq

def summarize(text, sentencesCount, minCut = 0.1, maxCut = 0.9):
    """ Get summarization with `sentencesCount` sentences
    
    Parameters
    ----------
    text : str
        Input passage
    sentencesCount : int
        Number of stentence to make
    minCut : float, optional
        [description] (the default is 0.1, which [default_description])
    maxCut : float, optional
        [description] (the default is 0.9, which [default_description])
    
    """

    sents = sent_tokenize(text)
    assert sentencesCount <= len(sents)
    wordSent = [word_tokenize(s.lower()) for s in sents]
    frequencies = computeFrequencies(wordSent, minCut, maxCut)
    ranking = defaultdict(int)
    for i,sent in enumerate(wordSent):
        for w in sent:
            if w in frequencies:
                ranking[i] += frequencies[w]
    sentsIdx = rank(ranking, sentencesCount)

    summarization = ""
    for sentence in [sents[j] for j in sentsIdx]:
        summarization += removeRefNo(sentence).strip()

    return summarization

def getOnlyText(url):
    soup = BeautifulSoup(urlopen(url), "lxml")
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return text

def GetWikiSummary(url = "", sentencesCount = 5):
    return summarize(getOnlyText(url), sentencesCount)

def GetSummary(inputString, sentencesCount = 5):
    return summarize(inputString, sentencesCount)

if __name__ == '__main__':
    print(GetWikiSummary("https://en.wikipedia.org/wiki/Machine_learning"))