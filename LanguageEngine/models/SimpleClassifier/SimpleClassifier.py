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


def loadTFModel(lengthInput, lengthOutput):
    """Loads and returns trained TFModel

    Parameters
    ----------
    lengthInput : str
        The size of the input vector
    lengthOutput: str
        The size of the output vector (number of classes)

    Returns
    -------
    model : tflearn.DNN
        The model with appropriate size

    """

    net = tflearn.input_data(shape=[None, lengthInput])
    net = tflearn.fully_connected(net, 16)
    net = tflearn.fully_connected(net, 16)
    net = tflearn.fully_connected(net, lengthOutput, activation='softmax')
    net = tflearn.regression(net)
    model = tflearn.DNN(net, tensorboard_dir='LanguageEngine/models/SimpleClassifier/data/tflearn_logs')
    model.load('LanguageEngine/models/SimpleClassifier/data/TrainedModel/model.tflearn')
    return model

def loadAllData():
    """Loads all data required for prediction
    
    Returns
    -------
    st : StanfordNERTagger
        The 7 class version of the StanfordNERT
    words : list
        The list of all words in the corpus (training data)
    classes : list
        The list of all classes in the corpus (training data)
    trainX : list
        The set of all input vectors (sentences)
    trainY : list
        The set of all output vectors corresponding to the position in trainX
    stemmer : LancasterStemmer
        An object of LancasterStemmer is returned by default
    model : tflearn.DNN
        The trained neural network model
    """

    st = StanfordNERTagger("LanguageEngine/models/Dependencies/stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz", "LanguageEngine/models/Dependencies/stanford-ner/stanford-ner.jar", encoding="utf-8")
    data = pickle.load(open("LanguageEngine/models/SimpleClassifier/data/trainingData", "rb"))
    words = data['words']
    classes = data['classes']
    trainX = data['trainX']
    trainY = data['trainY']
    stemmer = LancasterStemmer()
    print(len(trainX[0]), len(trainY[0]))
    model = loadTFModel(len(trainX[0]), len(trainY[0]))
    return (st, words, classes, trainX, trainY, stemmer, model)

# Initializing all the variables required by the predict function
st, words, classes, trainX, trainY, stemmer, model = loadAllData()


def tokenizeAndStem(sentence):
    """Tokenizes and Stems the given sentence

    Parameters
    ----------
    sentence : str
        The sentence that needs to be tokenized and stemmed
    
    Returns
    -------
    sentenceWords : list
        The list of stemmed words from the sentence

    """

    sentenceWords = word_tokenize(sentence)
    sentenceWords = [stemmer.stem(word.lower()) for word in sentenceWords]
    return sentenceWords


def makeInputArray(sentence, words):
    """Makes the input array for model

    Parameters
    ----------
    sentence : str
        The sentence that needs to be classified
    words : list
        The list of all words in the corpus (training data)
    
    Returns
    -------
    bag : np.array
        The one hot encoded vector of the sentence
    """

    sentenceWords = tokenizeAndStem(sentence)
    bag = [0]*len(words)
    for s in sentenceWords:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return(np.array(bag))


def predict(sentence, MIN_ACC=0.1):
    """predicts the class of sentence

    Predicts the class and the slots (entities) of the given sentene

    Parameters
    ----------
    sentence : str
        The sentence that needs to be classified
    MIN_ACC : float
        The threshold probability

    Returns
    -------
    returnJson : dict
        The dict containing the class, original sentence and the predicted entities of the sentence
    """

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

def predictSlots(sentence, predictedClass):
    """Predicts the slots

    StanfordNERTagger is used to predict get the entities in a given sentence

    Parameters
    ---------
    sentence : str
        The sentence that needs to be classified
    predictedClass : str
        The predicted class of the input sentence
    
    Returns
    -------
    entities : dict
        The dict containing all the entities recognized by the StanfordNERTagger

    """
    # TODO: Add code for class wise entity recognition (some classes may not need certain entities)

    tokenizedWords = word_tokenize(sentence.title())
    classifiedWords = st.tag(tokenizedWords)
    entities = []
    for classifiedWord in classifiedWords:
        if classifiedWord[1] is not "O":
            entity = {"entity": classifiedWord[1], 'value': classifiedWord[0]}
            entities.append(entity)
    return entities
