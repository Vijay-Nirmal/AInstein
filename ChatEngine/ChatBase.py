from LanguageEngine import TextClassifier as tc

classifier = tc.Classifier()

def responceFor(input):
    print(input)
    # predictResult = classifier.predict(input)
    # questionClass = predictResult["predictions"][0]["intent"].split('.')[0]
    # if(questionClass == "who"):
    #     print("Hello")

if __name__ == '__main__':
    responceFor("input")