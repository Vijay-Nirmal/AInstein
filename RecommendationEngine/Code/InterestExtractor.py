import json

def loadData(location="KnowledgeEngine\\Data\\FacultyDetails.json"):
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
    
    with open(location, encoding="utf8") as jsonFile:
        data = json.load(jsonFile)
        return data

def makeInterestJson():
    """Makes the TeacherInterestJSONFile

    """

    data = loadData()
    teacherInterests = {}
    teacherInterests["Interests"] = []
    for i in range(1, len(data) + 1):
        teacher = data["{}".format(i)]
        if len(teacher["Interest"]) > 0:
            temp = {"id": i, "name":teacher["name"], "interest": teacher["Interest"]}
            teacherInterests["Interests"].append(temp)

    with open("Knowledge/Data/FacultyInterests.json", "w") as jsonFile:
        json.dump(teacherInterests, jsonFile)
 
if __name__ == "__main__":
    makeInterestJson()