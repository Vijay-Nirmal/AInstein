import ChatBase as cb
from SpeechEngine import SpeechToText as st
from SpeechEngine import TextToSpeech as ts

def Chat():
    """Main function
    """
    while True:
        request = input("User: ")
        isSuccess = True
        if isExitRequest(request):
            giveResponce("Goodbye")
            break
        if request.lower() == "listen":
            request, isSuccess = st.SpeechToText()
        if isSuccess == False:
            giveResponce(request)
            continue
        
        responce = cb.responceFor(request)
        giveResponce(responce)

def isExitRequest(request):
    """Is the given input is a exit command

    Parameters
    ----------
    request : str
        The input sentence
    Returns
    -------
    return : bool
        `true` if it is exit command else `false`
    """
    return request.lower() in ["exit", "goodbye"]

def giveResponce(responce):
    """Give responce to the user in text and speech

    Parameters
    ----------
    responce : str
        Responce sentence
    """
    print("AInstein: " + responce)
    ts.TextToSpeech(responce)

if __name__ == '__main__':
    giveResponce("Hello, I am AInstein")
    Chat()
