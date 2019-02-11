import json
import random


DataLocation = "LanguageEngine\models\TrainingData\context.json"

with open(DataLocation) as jsonData:
    replies = json.load(jsonData)

def defaultAnswer(className):
    if className:
        while className:
            for i in replies["contexts"]:
                if i["tag"] == className:
                    # if 'contextSet' in i:
                    #     context[chatID] = i['contextSet']

                    # if not 'contextFilter' in i or (chatID in context and 'contextFilter' in i and i['contextFilter'] == context[chatID]) or "contextCheck" in i:

                        return random.choice(i["responses"])
                    # return ""
    else:
        return ""