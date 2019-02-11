import nltk
import random
import json
import difflib
from nltk.corpus import stopwords
from LanguageEngine.Summarizer import Gensim as gen
from LanguageEngine.Summarizer import NLTKFrequencySummarizer as nfs
from ActionBase import WebActions

facultyName = None
exclusionList = ["Me", "Email", "Id", "Address", "Her", "His", "Their", "He", "She", "Do", "Interests", "Are",
                 "Someone", "Who", "Teacher", "Person", "Faculty", "Knows", "Does", "Explain", "Words"]
stopWords = set(stopwords.words("english"))
with open("KnowledgeEngine/Data/FacultyDetails.json", encoding="utf8") as jsonData:
    facultyDetails = json.load(jsonData)

inclusionList = []
for key in facultyDetails.keys():
    for interest in facultyDetails[key]["Interest"]:
        for word in nltk.word_tokenize(interest):
            if word not in inclusionList and word not in stopWords:
                inclusionList.append(word)

def action(data):
    """
    The logic part of FacultyActions, this part chooses  whether to find
    interest, description or to get the email of the person.

    Parameters
    ----------
    data : model inference
        the output of the trained model, including question class,
        slots, name, etc

    Returns
    -------
    response : str
        The reply to be sent to the user
    """
    questionClass = data["predictions"][0]["intent"]
    
    if questionClass == "who":
        return getDescription(data['predictions'][0]['originalSentence'].title())
    elif questionClass.split(".")[1] == "email":
        email = getEmail(data['predictions'][0]['originalSentence'].title())
        if email:
            return "There you go, the email address is " + email
        else:
            return defaultReply()
    elif questionClass.split(".")[1] == "interest":
        interests = getInterest(data['predictions'][0]['originalSentence'].title())
        if interests:
            return "Their interests include " + ", ".join(interests)
        else:
            return defaultReply()
    else:
        return defaultReply()

def defaultReply():
    return random.choice(["I'm sorry, I couldn't find that information for you.",
                                 "Well, I don't seem to be able to find that information for you now"])

def extractName(originalSentence):
    """
    Uses NLP to extract the name of the person

    Parameters
    ----------
    originalSentence : str
        the raw sentence to be processed

    Returns
    -------
    name : str
        The name of the person in the sentence
    """
    words = nltk.word_tokenize(originalSentence)
    posTags = nltk.pos_tag(words)
    # print(posTags)
    name = ""
    for tag in posTags:
        if "NN" in tag[1]:
            if tag[0] not in exclusionList:
                name += tag[0] + " "
        elif tag[0] in inclusionList:
            name += tag[0] + " "
    # print(name)
    return name.strip()


def getInterest(originalSentence):
    """
    The ID of the person is found using their name, and their
    interest is returned after fetching from KnowledgeBase

    Parameters
    ----------
    originalSentence : str
        the raw sentence to be processed


    Returns
    -------
    interest : str
        The summarized interest of the person
    """
    name = extractName(originalSentence)
    if name == '' and facultyName:
        name = facultyName
    ID = findFacultyID(name)

    if ID == -1:
        return None
    else:
        return facultyDetails[str(ID)]["Interest"]


def getEmail(originalSentence):
    """
    Using the ID of the person in the sentence, their Email
    is retrieved from KnowledgeBase

    Parameters
    ----------
    originalSentence : str
        the raw sentence to be processed


    Returns
    -------
    email : str
        The email of the person
    """
    name = extractName(originalSentence)
    if name == '' and facultyName:
        name = facultyName
    ID = findFacultyID(name)

    if ID == -1:
        return None
    else:
        return facultyDetails[str(ID)]["Email"]

def getDescription(originalSentence):
    """
    The ID of the person is found using their name, and their
    description is returned after fetching from KnowledgeBase

    Parameters
    ----------
    originalSentence : str
        the raw sentence to be processed


    Returns
    -------
    description : str
        The summarized description of the person
    """
    global facultyName
    name = extractName(originalSentence)
    facultyName = name
    ID = findFacultyID(name)

    if ID == -1:
        return scrapeDescription(name)
    
    summary = gen.getSummary(facultyDetails[str(ID)]['description'])
    if len(summary) == 0:
        return facultyDetails[str(ID)]['description']
    else:
        return summary

def findFacultyID(name):
    """
    The ID of the person is returned using their name

    Parameters
    ----------
    name : str
        the name of the person


    Returns
    -------
    ID : int
        The ID of the faculty, returns -1 if the person is not found in
        the database
    """
    with open("KnowledgeEngine/Data/FacultyNames.json", encoding="utf8") as jsonData:
        teacherNamesAndID = json.load(jsonData)
    teacherNames = teacherNamesAndID.values()
    
    try:
        teacherID = list(teacherNames).index(difflib.get_close_matches(name, teacherNames, cutoff=0.5)[0]) + 1
        return teacherID
    except Exception:
        return -1

def scrapeDescription(name):
    """
    The description of the person is scraped from the web.
    The method is only used if the person is not present
    in the database

    Parameters
    ----------
    name : str
        the name of the person


    Returns
    -------
    description : str
        The summarized description of the person
    """
    return WebActions.scrapeDescription(name)