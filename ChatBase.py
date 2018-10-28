from LanguageEngine import TextClassifier as tc
from ActionBase import FacultyActions as fa
from ActionBase import WebActions as wa
import re

classifier = tc.Classifier()

def responceFor(input):
    predictResult = classifier.predict(input)
    questionClass = predictResult["predictions"][0]["intent"].split('.')[0]
    if(questionClass == "who"):
        return fa.action(input)
    elif(questionClass == "what"):
        noOfWordsRegex = re.compile(r'in \d+ words')
        noOfWordsRegexSearch = noOfWordsRegex.search(input)
        if noOfWordsRegexSearch is None:
            return wa.scrapeDescription(fa.extractName(input))
        else:
            return wa.scrapeDescription(fa.extractName(input), int(noOfWordsRegexSearch.group().split(' ')[1]))

    return "Oops, I can't understand"
