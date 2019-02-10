import ChatBase as cb
from SpeechEngine import SpeechToText as st
from SpeechEngine import TextToSpeech as ts

def Chat():
    while True:
        request = input("User: ")
        isSuccess = True
        if isExitRequest(request):
            giveResponce("Goodbye")
            break
        if request.lower() == "listen":
            request, isSuccess = st.fromMicrophone()
        if isSuccess == False:
            giveResponce(request)
            continue
        
        responce = cb.responceFor(request)
        giveResponce(responce)

def isExitRequest(request):
    return request.lower() in ["exit", "goodbye"]

def giveResponce(responce):
    print("AInstein: " + responce)
    # ts.TextToSpeech(responce)

if __name__ == '__main__':
    giveResponce("Hello, I am AInstein")
    Chat()
