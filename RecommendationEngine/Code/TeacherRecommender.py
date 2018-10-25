import nltk
import json
import pickle
from scipy import spatial
from autocorrect import spell
import sys

interestWords = []
facultyWordList = []
facultyFeatureVectors = []


def loadData(location="RecommendationEngine/Data/FacultyInterests.json"):
    """Loads the specified JSON file and returns the data object

    Parameters
    ----------
    location : str
        The string location of the JSON file
    

    Returns
    -------
    data : dict
        The python dictionary form of the JSON file

    """

    with open(location) as jsonFile:
        faculties = json.load(jsonFile)
    return faculties

def prepareData():
    """Creates the feature vectors for all teachers

    """

    global interestWords

    faculties = loadData()
    stopWords = ["?", "/", "&", "(", ")", "-"]
    for faculty in faculties["Interests"]:
        w = []
        for interest in faculty["interest"]:
            temp = [word.lower() for word in nltk.word_tokenize(interest) if word not in stopWords]
            w.extend(temp)
        interestWords.extend(w)
        facultyWordList.append((w, faculty["id"], faculty["name"]))

    interestWords = sorted(list(set(interestWords)))

    for wordList in facultyWordList:
        vector = []
        for word in interestWords:
            vector.append(1) if word in wordList[0] else vector.append(0)
        facultyFeatureVectors.append([wordList[2], vector])
        

def recommendTeacher(sent, top=1):
    """Gives the top n teacher recommendations. 

    Parameters
    ----------
    sent : str
        The sentence used for the recommendation
    top : int
        The n in 'top n recommendations'

    Returns
    -------
    topTeachers : list
        The list containing the names of the top n recommendations

    """
    words = nltk.word_tokenize(sent)
    inputVector = []
    for word in interestWords:
        inputVector.append(1) if word in words else inputVector.append(0)
    allScores = {}
    for faculty in facultyFeatureVectors:
        similarity = 1 - spatial.distance.cosine(inputVector, faculty[1])
        allScores[faculty[0]] = similarity
    
    allScores = sorted(allScores.items(), key=lambda kv: kv[1], reverse=True)
    topTeachers = []
    for item in allScores[:top]:
        topTeachers.append(item[0])
    
    return topTeachers

prepareData()