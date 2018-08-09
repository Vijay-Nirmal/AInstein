import pickle
import json
import tflearn
import tensorflow as tf
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import StanfordNERTagger
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import random

context = {}

stemmer = LancasterStemmer()
st = StanfordNERTagger("LanguageEngine/models/Data/stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz", "LanguageEngine/models/Data/stanford-ner/stanford-ner.jar", encoding="utf-8")
data = pickle.load(open("LanguageEngine/models/SimpleClassifier/data/trainingData", "rb"))
words = data['words']
classes = data['classes']
trainX = data['trainX']
trainY = data['trainY']

net = tflearn.input_data(shape=[None, len(trainX[0])])
net = tflearn.fully_connected(net, 16)
net = tflearn.fully_connected(net, 16)
net = tflearn.fully_connected(net, len(trainY[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net, tensorboard_dir='LanguageEngine/models/SimpleClassifier/data/tflearn_logs')
model.load('LanguageEngine/models/SimpleClassifier/data/TrainedModel/model.tflearn')
MIN_ACC = 0.10


def tokenizeAndStem(sentence):
    sentenceWords = word_tokenize(sentence)
    sentenceWords = [stemmer.stem(word.lower()) for word in sentenceWords]
    return sentenceWords


def makeInputArray(sentence, words, showDetails=False):
    sentenceWords = tokenizeAndStem(sentence)
    bag = [0]*len(words)
    for s in sentenceWords:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if showDetails:
                    print("found in bag: %s" % w)
    return(np.array(bag))


def predict(sentence):
    results = model.predict([makeInputArray(sentence, words)])
    results = results[0]
    results = [[i, r] for i, r in enumerate(results) if r > MIN_ACC]
    results.sort(key=lambda x: x[1], reverse=True)
    returnJson = {}
    returnJson['predictions'] = []
    for r in results:
        entities = predictSlots(sentence, classes[r[0]])
        interm = {"intent": classes[r[0]], "originalSentence": sentence, "confidence": r[1], 'entities': entities}
        returnJson['predictions'].append(interm)
    return returnJson

def predictSlots(sentence, c):
    tokenizedWords = word_tokenize(sentence.title())
    classifiedWords = st.tag(tokenizedWords)
    entities = []
    for classifiedWord in classifiedWords:
        if classifiedWord[1] is not "O":
            entity = {"entity": classifiedWord[1], 'value': classifiedWord[0]}
            entities.append(entity)
    return entities