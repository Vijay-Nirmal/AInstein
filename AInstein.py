import ChatBase as cb
from SpeechEngine import SpeechToText as st
from SpeechEngine import TextToSpeech as ts

def Chat():
    while True:
        request = input("User: ")
        if isExitRequest(request):
            giveResponce("Goodbye")
            break
        if request.lower() == "listen":
            request = st.SpeechToText()
        if request == 0:
            continue
        
        responce = cb.responceFor(request)
        giveResponce(responce)

def isExitRequest(request):
    request.lower() in ["exit", "goodbye"]

def giveResponce(responce):
    print("AInstein: " + responce)
    ts.TextToSpeech(responce)

if __name__ == '__main__':
    giveResponce("Hello, I am AInstein")
    Chat()
