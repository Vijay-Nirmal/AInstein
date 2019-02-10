from flask import Flask, jsonify, request, Markup, render_template
import markdown
import ChatBase as cb
from urllib import request as rs
from config import *
from SpeechEngine import SpeechToText as stt

app = Flask(__name__)
app.config['DEBUG'] = True
FILE_GET_ENDPOINT = "https://api.telegram.org/file/bot{}/".format(BOT_TOKEN)
VOICE_SAVE_PATH = "API/ReceivedData/{}"

@app.route("/api", methods=["GET"])
def apiHome():
    with open('API/templates/endpoints.md') as file:
        homeContent = file.read()
    homeContent = Markup(markdown.markdown(homeContent))
    return render_template("generic.html", content=homeContent)

@app.route("/api/textback/", methods=["GET"])
def textBack():
    if "mode" in request.args:
        mode = request.args['mode']
    else:
        return "Format Incorrect. Please see documentation"
    
    if mode == "text":
        if "query" in request.args:
            query = request.args['query']
            print(query)
        else:
            return "Query not specified. Please see documentation"
        response = {}
        response['response'] = cb.responceFor(query)
        return jsonify(response)
    
    if mode == "voice":
        if "location" in request.args:
            location = request.args['location']
        else:
            return "Location not specified. Please see documentation"
        
        saveLocation = VOICE_SAVE_PATH.format(location)
        rs.urlretrieve(FILE_GET_ENDPOINT+location, saveLocation)
        textData = stt.fromAudioFile(saveLocation)
        response = {}
        response['response'] = cb.responceFor(textData)
        return jsonify(response)

app.run()
