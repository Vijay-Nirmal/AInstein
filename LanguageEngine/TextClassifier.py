SIMPLE_CLASSIFIER = 1

class Classifier():
    
    def __init__(self, type=SIMPLE_CLASSIFIER):
        if type is SIMPLE_CLASSIFIER:
            from LanguageEngine.models.SimpleClassifier import SimpleClassifier as sc
            self.classifier = sc
    
    def predict(self, sentence):
        return self.classifier.predict(sentence)