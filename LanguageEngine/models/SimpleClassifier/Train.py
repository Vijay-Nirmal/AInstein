import nltk
from nltk.stem.lancaster import LancasterStemmer
import tensorflow as tf
import tflearn
import random
import json
import pickle
import numpy as np

stemmer = LancasterStemmer()


def makeModel(lengthInput, lengthOutput):
    """Makes a tflearn model with two hidden layers with 16 nodes each.

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

    tf.reset_default_graph()
    net = tflearn.input_data(shape=[None, lengthInput])
    net = tflearn.fully_connected(net, 16)
    net = tflearn.fully_connected(net, 16)
    net = tflearn.fully_connected(
        net, lengthOutput, activation='softmax')
    net = tflearn.regression(net)
    model = tflearn.DNN(net, tensorboard_dir='data/tflearn_logs')
    return model


def train():
    """Preprocesses and trains model

        Preprocesses the data by creating bag of words for each sentence with its class, and trains 
        the neural netowrk model for classification. The trained model along with the serialized 
        training data is saved in the data/ directory.
    """

    with open("../TrainingData/context.json") as jsonData:
        intents = json.load(jsonData)

    words = []
    tags = []
    documents = []
    stopWords = ["?"]

    for intent in intents['contexts']:
        for pattern in intent['patterns']:
            w = nltk.word_tokenize(pattern)
            words.extend(w)
            w = [stemmer.stem(i.lower()) for i in w if i not in stopWords]
            documents.append((w, intent['tag']))
            if intent['tag'] not in tags:
                tags.append(intent['tag'])

    words = [stemmer.stem(w.lower()) for w in words if w not in stopWords]
    words = sorted(list(set(words)))
    trainingData = []

    for doc in documents:
        bag = []
        patternWords = doc[0]

        for w in words:
            bag.append(1) if w in patternWords else bag.append(0)

        outputRow = list([0] * len(tags))
        outputRow[tags.index(doc[1])] = 1
        trainingData.append([bag, outputRow])

    random.shuffle(trainingData)
    trainingData = np.array(trainingData)

    trainingDataX = list(trainingData[:, 0])
    trainingDataY = list(trainingData[:, 1])
    model = makeModel(len(trainingDataX[0]), len(trainingDataY[0]))

    model.fit(trainingDataX, trainingDataY, n_epoch=700,
              batch_size=16, show_metric=True)

    model.save('data/TrainedModel/model.tflearn')

    pickle.dump({'words': words, 'classes': tags, 'trainX': trainingDataX,
                 'trainY': trainingDataY}, open("data/trainingData", "wb"))


if __name__ == '__main__':
    train()
