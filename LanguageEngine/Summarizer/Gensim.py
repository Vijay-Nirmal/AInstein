import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

def removeReferenceNumbers(inputString):
    """Removes reference numbers from the strings obtained from wikipedia
    
    Parameters
    ----------
    inputString : String
        Input string

    Returns
    -------
    inputString : String
        Reference number removed string obtained from wikipedia
    
    """

    return re.sub(r"[\[].*?[\]]", "", inputString)
 
def getOnlyText(url, noOfParagraphs = 0):
    """ Get all the contents from a URI as a `string`
    
    Parameters
    ----------
    url : String
        Input URI
    noOfParagraphs : int, optional
        Number of paragraph to get from the website (the default is 0, which takes all the paragraph)

    Returns
    -------
    text : String
        Contents from the URI
    
    """
    page = urlopen(url)
    soup = BeautifulSoup(page, "lxml")

    text = ""
    if noOfParagraphs == 0:
        text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    else:
        for i, para in enumerate(soup.find_all('p')):
            if i >= noOfParagraphs:
                break
            text += " " + para.text
    
    return text.strip()

def getSummaryFromURI(url, wordCount = 50, noOfParagraphs = 0):
    """Get summary of the data in the given URI
    
    Parameters
    ----------
    url : String
        Input URI
    wordCount : int, optional
        Number of words in the summarized paragraph (the default is 50, which gives summary in 50 words)
    noOfParagraphs : int, optional
        Number of paragraph that should be taken from the URI (the default is 0, which takes all the paragraph)

    Returns
    -------
    inputString : String
        Summarized output
    
    """
    return removeReferenceNumbers(summarize(str(getOnlyText(url, noOfParagraphs)), word_count = wordCount))

def getSummary(inputString, wordCount = 50):
    """Get summary of the given paragraph
    
    Parameters
    ----------
    inputString : String
        Given paragraph
    wordCount : int, optional
        Number of words in the summarized paragraph (the default is 50, which gives summary in 50 words)
    
    Returns
    -------
    inputString : String
        Summarized output
        
    """
    return removeReferenceNumbers(summarize(inputString, word_count = wordCount))

if __name__ == '__main__':
    print(getSummaryFromURI("https://en.wikipedia.org/wiki/Artificial_neural_network", 50, 5))
