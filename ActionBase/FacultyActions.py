import nltk
import random
import json
import difflib
from LanguageEngine.Summarizer import Gensim as gen
from LanguageEngine.Summarizer import NLTKFrequencySummarizer as nfs

facultyName = None


def action(data):
    questionClass = data["predictions"][0]["intent"]
    
    
    if questionClass == "who":
        return fetchDescription(data['predictions'][0]['originalSentence'].title())
    else:
        return random.choice(["I'm sorry, I couldn't find that information for you.",
                                 "Are you sure that's spelled correctly? I don't seem to know anyone of that name."])

def fetchDescription(originalSentence):
    global facultyName
    posTags = nltk.pos_tag(nltk.word_tokenize(originalSentence))
    print(posTags)
    name = ""
    for tag in posTags:
        if "NN" in tag[1]:
            if tag[0] != "Me":
                name += tag[0] + " "
    print(name)
    ID = findFacultyID(name.strip())
    with open("KnowledgeEngine/Data/FacultyDetails.json", encoding="utf8") as jsonData:
        teacherDetails = json.load(jsonData)
    
    summary = gen.getSummary(teacherDetails[str(ID)]['description'])
    if len(summary) == 0:
        return teacherDetails[str(ID)]['description']
    else:
        return summary

def findFacultyID(name):
    with open("KnowledgeEngine/Data/FacultyNames.json", encoding="utf8") as jsonData:
        teacherNamesAndID = json.load(jsonData)
    teacherNames = teacherNamesAndID.values()
    # print(teacherNames)
    print(list(teacherNames).index(difflib.get_close_matches(name, teacherNames, cutoff=0.3)[0]) + 1)
    return list(teacherNames).index(difflib.get_close_matches(name, teacherNames, cutoff=0.3)[0]) + 1
