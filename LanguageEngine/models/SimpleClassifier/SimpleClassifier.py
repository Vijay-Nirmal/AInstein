import pickle
import json
import tflearn
import tensorflow as tf
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import random

context = {}

stemmer = LancasterStemmer()
data = pickle.load(open("models/SimpleClassifier/data/trainingData", "rb"))
words = data['words']
classes = data['classes']
trainX = data['trainX']
trainY = data['trainY']

net = tflearn.input_data(shape=[None, len(trainX[0])])
net = tflearn.fully_connected(net, 16)
net = tflearn.fully_connected(net, 16)
net = tflearn.fully_connected(net, len(trainY[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net, tensorboard_dir='models/SimpleClassifier/data/tflearn_logs')
model.load('models/SimpleClassifier/data/TrainedModel/model.tflearn')
MIN_ACC = 0.10


def tokenizeAndStem(sentence):
    sentenceWords = nltk.word_tokenize(sentence)
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
    # print(results)
    results = results[0]
    # print(results)
    results = [[i, r] for i, r in enumerate(results) if r > MIN_ACC]
    results.sort(key=lambda x: x[1], reverse=True)
    returnList = []
    returnJson = {}
    returnJson['predictions'] = []
    for r in results:
        returnList.append((classes[r[0]], r[1]))
        interm = {"intent": classes[r[0]], "originalSentence": sentence, "confidence": r[1]}
        returnJson['predictions'].append(interm)
    return returnJson

