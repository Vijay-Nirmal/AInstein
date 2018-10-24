from bs4 import BeautifulSoup
from urllib.request import urlopen
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import re

def removeRefNo(inputString):
    """Removes reference numbers from the string
    
    Parameters
    ----------
    inputString : `String`
        Input string

    Returns
    -------
    inputString : `String`
        Reference number removed string
    
    """

    return re.sub(r"[\[].*?[\]]", "", inputString)

def rank(ranking, n):
    """ Return the first n sentences with highest ranking

    """

    return nlargest(n, ranking, key=ranking.get)

def computeFrequencies(wordSent, minCut, maxCut):
    """ Compute the frequency of each of word
    
    Parameters
    ----------
    wordSent : list
        a list of sentences already tokenized
    minCut : float
        [description]
    maxCut : float
        [description]
    
    Returns
    -------
    freq : dictionary
        Dictionary where freq[w] is the frequency of w

    """

    stopwordsSet = set(stopwords.words('english') + list(punctuation))
    freq = defaultdict(int)
    for s in wordSent:
        for word in s:
            if word not in stopwordsSet:
                freq[word] += 1
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
        Number of sentence to make
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

def getOnlyText(url, noOfPar = 0):
    """ Get all the contents from a URI as a `string`
    
    Parameters
    ----------
    url : String
        Input URI
    noOfPar : int, optional
        Number of paragraph to get from the website (the default is 0, which takes all the paragraph)

    Returns
    -------
    text : String
        Contents from the URI
    
    """
    page = urlopen(url)
    soup = BeautifulSoup(page, "lxml")

    text = ""
    if noOfPar == 0:
        text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    else:
        for i, para in enumerate(soup.find_all('p')):
            if i >= noOfPar:
                break
            text += " " + para
    
    return text.strip()

def GetSummaryFromURI(url, sentencesCount = 5, noOfPar = 0):
    """Get summary of the data in the given URI
    
    Parameters
    ----------
    url : String
        Input URI
    sentencesCount : int, optional
        Number of output sentence (the default is 5, which gives summary in three sentence)
    noOfPar : int, optional
        Number of paragraph that should be taken from the URI (the default is 0, which takes all the paragraph)

    Returns
    -------
    inputString : String
        Summarized output
    
    """
    return summarize(getOnlyText(url, noOfPar), sentencesCount)

def GetSummary(inputString, sentencesCount = 5):
    """Get summary of the given paragraph
    
    Parameters
    ----------
    inputString : String
        Given paragraph
    sentencesCount : int, optional
        Number of output sentence (the default is 3, which gives summary in three sentence)
    
    Returns
    -------
    inputString : String
        Summarized output
        
    """
    return summarize(inputString, sentencesCount)
    