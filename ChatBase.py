from LanguageEngine import TextClassifier as tc
from ActionBase import FacultyActions as fa
from ActionBase import WebActions as wa

classifier = tc.Classifier()

def responceFor(input):
    predictResult = classifier.predict(input)
    questionClass = predictResult["predictions"][0]["intent"].split('.')[0]
    if(questionClass == "who"):
        return fa.action(input)
    elif(questionClass == "what"):
        return wa.scrapeDescription(fa.extractName(input))

    return "Oops, I can't understand"
